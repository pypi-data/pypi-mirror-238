#!/usr/bin/env python
import logging
import inspect
import urllib3
import click
import sys

from cobra.mit.request import ClassQuery, DnQuery, DeploymentQuery, ConfigRequest
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_dn_string(objects: list) -> list:
    return [str(obj.dn) for obj in objects]


class ACIClean(object):
    def __init__(
        self, apic_url="", apic_user="", apic_password="", debug=False
    ) -> None:
        if debug:
            logging.basicConfig(
                level=logging.INFO, format="[%(levelname)10s]: %(message)s"
            )
        self.log = logging.getLogger(__name__)
        self.report_data: list = []
        self.md = self.login(apic_url, apic_user, apic_password)

    def login(self, apic_url, apic_user, apic_password):
        session = LoginSession(apic_url, apic_user, apic_password)
        md = MoDirectory(session)
        try:
            md.login()
        except Exception as e:
            self.log.error(
                f"Failed to login to APIC at {apic_url} with user {apic_user}:{e}"
            )
            sys.exit(1)
        self.md = md

        return md

    def mock(self):
        self.g.init_sim()
        self.g.infraAttEntityP("AEP_EMPTY")
        self.g.infraAccPortP("LIP_EMPTY")
        self.g.physDomP("DOM_PHY_EMPTY")
        self.g.fvnsVlanInstP("VLP_EMPTY")
        AEP_PYTEST = self.g.infraAttEntityP("AEP_PYTEST")
        self.g.create_access(
            AEP_PYTEST, nodes=["3101"], ports=["10"], remote_name=["remote_name1"]
        )
        self.g.create_access(
            AEP_PYTEST,
            nodes=["3101", "3102"],
            ports=["20"],
            remote_name=["remote_name1", "remote_name2"],
        )

    def execute(self, methods):
        for method in methods:
            getattr(self, method)()

    def get_tests(self):
        methods = []
        for method in dir(self):
            if method.startswith(("warning_", "error_", "critical_")):
                methods.append(method)

        return methods

    def find_relations(self, cls: str, target_paths: list):
        calling_method = inspect.stack()[1][3]
        self.log.info(f"{'*' * 20} {calling_method}")

        query = ClassQuery(cls)
        dns = self.md.query(query)

        for policy in dns:
            self.log.info(f"{'*' * 10} Processing DN: {policy.dn}")
            used = []

            # Policies using the policy
            query = DnQuery(policy.dn)
            query.queryTarget = "children"
            query.classFilter = "relnFrom"
            relnFroms = self.md.query(query)

            if relnFroms:
                self.log.info(
                    f"Policies using the policy {policy.dn}: {get_dn_string(relnFroms)}"
                )
                used.extend(relnFroms)
            else:
                self.log.info(f"No policies using the policy {policy.dn}")

            # Target_paths using the policy
            for target_path in target_paths:
                query = DeploymentQuery(policy.dn)
                query.subtreeInclude = "full-deployment"
                query.targetPath = target_path
                deployed_on = [x for x in self.md.query(query) if x.dn != policy.dn]

                if deployed_on:
                    self.log.info(
                        f"{target_path} using the policy {policy.dn}: {get_dn_string(used)}"
                    )
                    used.extend(deployed_on)
                else:
                    self.log.info(f"No {target_path} using the policy: {policy.dn}")

            if used:
                self.log.info(
                    f"Summary: Policy {policy.dn} used by {get_dn_string(used)}"
                )
            else:
                self.log.warning(f"No policies using the policy {policy.dn}")
                self.report_data.append(
                    {
                        "message": f"No policies using the policy {policy.dn}",
                        "policy": policy,
                    }
                )

    def remove_all(self):
        if (
            input(
                "\n!!! Removing all policies without relationships from the APIC !!! Are you really sure? (Y/n): "
            )
            != "Y"
        ):
            print("Aborting...")
            return

        for line in self.report_data:
            policy = line.get("policy")
            self.log.warning(f"Removing {policy.dn}")

            policy.delete()
            configReq = ConfigRequest()
            configReq.addMo(policy)
            self.md.commit(configReq)

    def export_report(self):
        with open("aciclean_report.txt", "w", newline="") as report:
            report.write("# Unused DNs:\n")
            for data in self.report_data:
                report.write(f"- {data.get('policy').dn}\n")

    def warning_infraAccPortP(self):
        self.find_relations("infraAccPortP", ["AccPortPToEthIf"])

    def warning_infraAccPortGrp(self):
        self.find_relations("infraAccPortGrp", ["AccBaseGrpToEthIf"])

    def warning_infraAccBndlGrp(self):
        self.find_relations(
            "infraAccBndlGrp", ["AccBaseGrpToEthIf", "AccBndlGrpToAggrIf"]
        )

    def warning_infraAttEntityP(self):
        self.find_relations(
            "infraAttEntityP",
            [
                "AttEntityPToPortGroups",
                "AttEntityPToPthIf",
                "AttEntityPToVirtualMachines",
            ],
        )

    def warning_physDomP(self):
        self.find_relations("physDomP", ["ADomPToEthIf"])

    def warning_fvnsVlanInstP(self):
        self.find_relations(
            "fvnsVlanInstP",
            ["VlanNsToInterface", "VlanNsToVmmPortGroups", "VlanNsToVirtualMachines"],
        )

    def warning_vzBrCP(self):
        self.find_relations(
            "vzBrCP",
            [
                "VzBrCPToFvRsCons",
                "VzBrCPToFvRsProv",
                "CtrctIfToEPgCons",
                "CtrctIfToEPgConsNwIf",
                "ABrCPToAnyCons",
                "ABrCPToAnyProv",
                "ABrCPToEPgProv",
                "ABrCPToEPgCons",
                "GraphInstancesinacontract",
            ],
        )

    def warning_vzFilter(self):
        self.find_relations(
            "vzFilter",
            [],
        )


@click.command()
@click.option("--url", help="APIC URL including protocol.", envvar="ACI_APIC_URL")
@click.option("--user", show_default="admin", help="APIC user.", envvar="ACI_APIC_USER")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    help="APIC password.",
    envvar="ACI_APIC_PASSWORD",
)
@click.option(
    "-w",
    "--write",
    is_flag=True,
    show_default=False,
    help="Write report to aciclean_report.txt",
)
@click.option(
    "-r",
    "--remove",
    is_flag=True,
    show_default=False,
    help="WARNING: !!! This will remove all policies without relationships from the APIC !!!",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=False,
    help="Write report to aciclean_report.txt",
)
def run(url, user, password, write, remove, verbose):
    aciclean = ACIClean(url, user, password, verbose)

    print("Starting search. Please be patient. This can take a while.")

    aciclean.execute(aciclean.get_tests())

    if write:
        aciclean.export_report()

    if aciclean.report_data:
        print("\nList of policies with no relationships:")
        for data in aciclean.report_data:
            print(f"- {data.get('policy').dn}")

        if remove:
            aciclean.remove_all()
    else:
        print("\nNo policies without relationships found.")


if __name__ == "__main__":
    run()

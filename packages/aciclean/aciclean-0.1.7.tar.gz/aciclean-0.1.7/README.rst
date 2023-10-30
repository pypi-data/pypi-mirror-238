Cisco ACI Unused Policy Cleaner
===============================

ACIClean is a tool that helps you clean up your Cisco ACI infrastructure
by detecting and reporting on unused objects. It uses the `ACI COBRA
Python SDK <https://cobra.readthedocs.io/en/latest/install.html>`__
provided by Cisco.

ACIClean currently detects and reports on the following objects:

- VLAN Pools 
- AAEPs 
- Physical Domains 
- Leafswitch Profiles 
- Accessports 
- PCs and VPCs

Installation
------------

To install ACIClean, follow these steps:

1. Install the ACI COBRA Python SDK by following the instructions `here <https://cobra.readthedocs.io/en/latest/install.html>`__. 

If you dont’t have the SDK modules handy, run the following commands to install an ACI v5.2.7 SDK module:

- ``pip install https://github.com/cubinet-code/aci_cobra_sdk/raw/main/acicobra-5.2.7.0.7-py2.py3-none-any.whl``
- ``pip install https://github.com/cubinet-code/aci_cobra_sdk/raw/main/acimodel-5.2.7.0.7-py2.py3-none-any.whl``

2. Run ``pip install aciclean`` to install this module and command line script.

Usage
-----

To use ACIClean, run the aciclean.py script. The script will detect and
report on any unused objects in your Cisco ACI infrastructure.

The following APIC credentials will be read from the environment, if they exist:

-  ACI_APIC_URL
-  ACI_APIC_USER
-  ACI_APIC_PASSWORD

::

   aciclean --help

   Usage: aciclean.py [OPTIONS]

   Options:
     --url TEXT       APIC URL including protocol.
     --user TEXT      APIC user.  [default: (admin)]
     --password TEXT  APIC password.
     -w, --write      Write report to aciclean_report.txt
     -r, --remove     WARNING: !!! This will remove all policies without
                      relationships from the APIC !!!
     --help           Show this message and exit.
     

Contributing
------------

Contributions to ACIClean are welcome! If you find a bug or have a
feature request, please open an issue on the GitHub repository. If you
would like to contribute code, please fork the repository and submit a
pull request.

License
-------

ACIClean is licensed under the MIT License.

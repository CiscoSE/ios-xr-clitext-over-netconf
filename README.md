# Test Cisco IOS-XR CLItext capability in NETCONF
Cisco has recently added a featureset in IOS-XR 7.X code to allow you to send plain cli text leveraging the NETCONF/YANG infrastructure
This feature simplifies the configuration of the devices by not requiring a deep understanding of the YANG data models.
## More Information on the Features
For Official Cisco Documentation you can refer to examples at the NCS 1004 Programmability Guide Available at:
[CLI Over NETCONF](https://www.cisco.com/c/en/us/td/docs/optical/ncs1004/datamodels/guide/b_Datamodels_cg_ncs1004/b_Datamodels_cg_ncs1004_chapter_011.html#Cisco_Concept.dita_48fdc3a6-6a01-49b1-aae0-4cc11768dbac)
## Requirements
ncclient
xml.etree
lxml.builder
All tests performed using Python 2.7.15
## Script Usage
```
python cisco_cli_testing.py
```
## Configurable Changes
At the top of the script file you'll note some constant fields to update.
* RETRIEVEDCONFIG - this is an optional field to provide a filename to save the retrieved configuration
* ROUTERIP - The IP address or hostname of the device under test
* USERNAME - Configured username for access
* PASSWORD - Obviously the password
* INPUTFILE - If you want to test pushing an entire configuration file you can specify it's location here

In the main body of the script you can obviously tweak for specific tests to your requirements

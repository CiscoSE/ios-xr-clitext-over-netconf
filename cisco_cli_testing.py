import logging
from ncclient import manager
import xml.etree.ElementTree as ET
from lxml.builder import E


# Obviously hard coding credentials in a Python script is only a good choice for testing purposes
# Use at your own risk and sanitize before passing on or alternately add in some additional functionality
# file to write the router config leave blank to not output to file but rather to console
RETRIEVEDCONFIG = ''
# Router IP Address to query
ROUTERIP = ''
# Username
USERNAME = ''
# Password
PASSWORD = ''
# Optional filename for input to write to the router, leave blank and we'll add a MOTD to the retrieved config
INPUTFILE = ''


# Make a NETCONF connection to an IOS-XR Device
def netconf_connect(host, user, password):
    params = dict(host=host, username=user,
        password=password, device_params={'name': 'iosxr'}, hostkey_verify=False, port=22)
    return manager.connect(**params)


# Get the Configuration in Cisco CLI Text Configuration Format
def get_config(connection):

    # Create Filter
    configfilter = ET.Element("filter", type="subtree")
    cli = ET.SubElement(configfilter, 'cli', {'xmlns': 'http://cisco.com/ns/yang/Cisco-IOS-XR-cli-cfg'})

    # Get the config using our opened connection
    config = connection.get_config('running', filter=ET.tostring(configfilter))
    # Filter the XML to get just the CLI text
    root = ET.fromstring(config.xml)
    return root[0][0].text


def commit_config(connection):
    connection.commit()


# Write a configuration using CLI Text
def put_config(connection, configuration):


    req = E('edit-config', E('target', E('candidate')))
    req.append(E('config', E('cli', configuration, xmlns='http://cisco.com/ns/yang/Cisco-IOS-XR-cli-cfg')))

    with connection.locked(target='running'):
        connection.dispatch(req)
        # always provide diff information
        diff = diff_config(connection)
        print('Proposed Configuration Changes')
        print(diff)
        commit_it = raw_input("If changes look good type 'commmit' to commit: ")
        if commit_it.lower() == 'commit':
            commit_config(connection)
            logger.info('Configuration written and committed to the router')
    return diff


# Get the configuration DIFF
def diff_config(connection):
    diffxml = E('get-cli-config-diff', xmlns='http://cisco.com/ns/yang/Cisco-IOS-XR-cli-diff-act')
    diff = connection.dispatch(diffxml)
    return diff


if __name__ == '__main__':
    # Turn on logging change level=logging.DEBUG for full blown rundown
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('netconf')
    # Of course replace with your router: IP, Username, Password
    conn = netconf_connect(ROUTERIP, USERNAME, PASSWORD)
    logger.info('Connected to Router via NETCONF')
    deviceconfig = get_config(conn)
    logger.info('Retrieved Device Running Configuration')
    # Optional file writing commands here to save the output
    if RETRIEVEDCONFIG:
        f = open(RETRIEVEDCONFIG, 'w')
        f.write(deviceconfig)
        logger.info('Device configuration written to: %s', RETRIEVEDCONFIG)
        f.close()
    else:
        # assume they want us to print the config
        print('********************* RETRIEVED CONFIGURATIION ****************')
        print(deviceconfig)

    # Use the same connection and do a write
    diff_text = put_config(conn, 'hostname xrv9000-rtr-a')

    # If you've specified an INPUTFILE let's try and write it see above to specify the 'INPUTFILE' constant
    if INPUTFILE:
        f = open(INPUTFILE, 'r')
        config_text = f.read()
        f.close()
        file_diff = put_config(conn, config_text)


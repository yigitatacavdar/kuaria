kuariaAscii = r"""
               ______
              /     /       .                     .                         .               .
 .           /     /                        . 
            /     /   __________      ______________  ___________  ___________________________  ______
        .  /     /   /         /     /    /         \/     /     \/          /      /         \/     /   .
          /     /  /   / /    /     /    /    ______      /      ___________/______/    ______      /
   .     /     / /   /  /    /     /    /    /     /     /      /          /      /    /     /     /
        /      /   /   /    /     /    /    /     /     /      /  .       /      /    /     /     /  .
       /         /    /    /     /    /    /     /     /      /          /      /    /     /     /
      /        /     /    /     /    /    /     /     /      /      .   /      /    /     /     /       .
.    /    /\    \   /    /_____/    /    /_____/     /      /          /      /    /_____/     /
    /    /  \    \ /               /                 \     /  .       /      /                 \  .       .
___/____/    \____________________/___________________\___/          /______/___________________\___
"""

import nmap
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko import NetmikoAuthenticationException

optional_args_base = {
    "allow_agent": False,
    "look_for_keys": False,
    "global_delay_factor": 2,
    "fast_cli": False,
    "key_exchange": [
        "diffie-hellman-group14-sha1",
        "diffie-hellman-group1-sha1",
        "diffie-hellman-group-exchange-sha256",
        "ecdh-sha2-nistp256",
    ],
}

def loadCommonCreds(path="commonCreds.txt"):
    creds = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",", 2)]
            while len(parts) < 3:
                parts.append("")
            username, password, secret = parts
            creds.append((username, password, secret))
    return creds

def networkScannerFunc(subnetIpInput):

    nm = nmap.PortScanner()
    nm.scan(hosts=subnetIpInput, arguments='-T4 -F -O -sV')

    for host in nm.all_hosts():

        print('\n----------------------------------------------------')
        print('Host : %s (%s)' % ((host), nm[host].hostname()))
        print('State : %s' % nm[host].state())
            

        for proto in nm[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)
            lport = nm[host][proto].keys()
            for port in lport:
                print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))

        for proto in nm[host].all_protocols():
            print('----------')
            print(f"Host: {host}")

            if 'mac' in nm[host]['addresses']:
                mac = nm[host]['addresses']['mac']
                vendor = nm[host]['vendor'].get(mac, 'Unknown')
                print(f"MAC: {mac}  Vendor: {vendor}")
            else:
                print("MAC: Unknown  Vendor: Unknown")

            if 'osmatch' in nm[host]:
                for match in nm[host]['osmatch']:
                    print(f"OS Guess: {match['name']}  ({match['accuracy']}% sure)")
                    break;
            else:
                print("OS Guess: None")

def getDeviceFacts(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput):

    driver = get_network_driver("ios")

    optional_args = {
    "secret": deviceSecretInput,
    "allow_agent": False,
    "look_for_keys": False,
    "global_delay_factor": 2,
    "fast_cli": False,
    "ssh_config_file": None,
    "key_exchange": ["diffie-hellman-group14-sha1", "diffie-hellman-group1-sha1", "diffie-hellman-group-exchange-sha256", "ecdh-sha2-nistp256"]}

    device = driver(hostname=deviceIpInput, username=deviceUserInput, password=devicePasswordInput, optional_args=optional_args)
    try:
        device.open()
        print("retrieving device info...")
        facts = device.get_facts()
        device.close()
        return facts
    except (ConnectionException, NetmikoAuthenticationException) as e:
        print("connection failed!")
        autoConnect()

def connectDevice(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput):
    if __name__ == "__main__":
        deviceInfo = getDeviceFacts(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput)
        print(f"Device: {deviceInfo['vendor']} {deviceInfo['model']}")

def scan(subnetIpInput):
    print("scanning...")
    networkScannerFunc(subnetIpInput)

    print('----------------------------------------------------')

def autoConnect(deviceIpInput):
    print("trying to connect with common credentials...")

    for usernameCommon, passwordCommon, secretCommon in loadCommonCreds("commonCreds.txt"):
        optional_args = dict(optional_args_base)
        if secretCommon:
            optional_args["secret"] = secretCommon 

        driver = get_network_driver("ios")

        try:
            device = driver(hostname=deviceIpInput, username=usernameCommon, password=passwordCommon, optional_args=optional_args)
            device.open()
        except (ConnectionException, NetmikoAuthenticationException):
            continue
        else:
            print("connected")
            print("username and password found as: %s, %s" % (usernameCommon, passwordCommon))
            connectDevice(deviceIpInput, usernameCommon, passwordCommon, secretCommon)
            device.close()
            return

    print("connection failed with common credentials")
    manualConnect(deviceIpInput)


def manualConnect(deviceIpInput):
    deviceUserInput = input("enter the username of the device you want to work with: ")
    devicePasswordInput = input("enter the password of the device you want to work with: ")
    deviceSecretInput = input("enter the enable password of the device you want to work with: ")

    print("connecting...")

    connectDevice(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput)


def wizard():
    print("welcome to kuaria wizard")
    subnetIpInput = input("\nenter the subnet you want to work with: ")
    scan(subnetIpInput)
    deviceIpInput = input("enter the ip address of the device you want to work with: ")
    autoConnect(deviceIpInput)

def main():
    print(kuariaAscii)
    print("kuaria - simple command line tool for network automation")
    print("\ncreated by yigit ata cavdar")
    print('\n----------------------------------------------------')
    wizard()

main()

# commands: 
# -help 
# -scan     
# -connect
#
#
#
#
#



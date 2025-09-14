import nmap
from napalm import get_network_driver

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

    device.open()
    facts = device.get_facts()
    device.close()

    return facts


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

print(kuariaAscii)
print("created by yigit ata cavdar")
print('\n----------------------------------------------------')
subnetIpInput = input("\nEnter the subnet you want to work with: ")
print("scanning...")
networkScannerFunc(subnetIpInput)

print('----------------------------------------------------')

deviceIpInput = input("enter the ip address of the device you want to work with: ")
deviceUserInput = input("enter the username of the device you want to work with: ")
devicePasswordInput = input("enter the password of the device you want to work with: ")
deviceSecretInput = input("enter the enable password of the device you want to work with: ")

print("connecting...")

if __name__ == "__main__":
    deviceInfo = getDeviceFacts(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput)
    print("connected")
    print(f"Device: {deviceInfo['vendor']} {deviceInfo['model']}")  #the program should try common credentials first, if they fail, it should ask the user for the credentials
                                                                    #some way to save the connected device? maybe just save the device info for the ip, or save the credentials?







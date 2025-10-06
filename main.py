#!/usr/bin/env python3

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

import argparse
from backend import scanner
from backend import connector
from backend import configurer

def wizard():
    print(kuariaAscii)
    print("kuaria - simple command line tool for network automation")
    print("\ncreated by yigit ata cavdar")
    print('\n----------------------------------------------------')
    print("Options:")
    print("ssh and scp server must be enabled on devices (ip scp server enable)")
    print("user privilege should be 15 (username admin privilege 15 secret <password>) or (username admin privilege 15 password <password>)")
    print("-scan <IP_ADDRESS> to scan for devices or subnets")
    print("-connect <IP_ADDRESS> to test connection to devices")
    print('\n----------------------------------------------------')
    print("welcome to kuaria wizard")
    subnetIpInput = input("\nenter the subnet you want to work with: ")
    scanner.scan(subnetIpInput)
    deviceIpInput = input("enter the ip address of the device you want to work with: ")
    connector.autoConnect(deviceIpInput)

def main():
    parser = argparse.ArgumentParser(prog=kuariaAscii, description="kuaria - simple command line tool for network automation")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-scan", metavar="<IP_ADDRESS>", help="scan for devices or subnets")

    group.add_argument("-connect", metavar="<IP_ADDRESS>", help="test connection to devices")
    parser.add_argument("-info", action="store_true", help="-connect <IP_ADDRESS> -info to get detailed device information")
    parser.add_argument("-config", action="store_true", help="-connect <IP_ADDRESS> -config to get running configuration")
    parser.add_argument("-interface", action="store_true", help="-connect <IP_ADDRESS> -interface to get interfaces")
    parser.add_argument("-vlans", action="store_true", help="-connect <IP_ADDRESS> -vlan to get vlans")
    parser.add_argument("-mac", action="store_true", help="-connect <IP_ADDRESS> -mac to get mac table")
    parser.add_argument("-arp", action="store_true", help="-connect <IP_ADDRESS> -arp to get arp table")

    group.add_argument("-configure", metavar="<IP_ADDRESS>", help="change configuration of devices")
    parser.add_argument("-hostname", metavar="<hostname>", help="-configure <IP_ADDRESS> -hostname <hostname> to change the hostname of the device")
    parser.add_argument("-vlan", metavar="<vlan>", help="-configure <IP_ADDRESS -vlan <vlan> to create a vlan")
    parser.add_argument("-name", metavar="<name>", help="-name to add a name to vlans and other configurations")
    parser.add_argument("-delete", action="store_true", help="-configure 'configuration' -delete to delete the configuration")
    parser.add_argument("-int", metavar="<interface>", help="-int <interface> to configure interface")
    parser.add_argument("-open", action="store_true", help="-open to open interface (no shutdown)")
    parser.add_argument("-close", action="store_true", help="-close to close interface (shutdown)")


    
    args, unknown = parser.parse_known_args()

    if not any(vars(args).values()):
        wizard()
    else:
        if args.scan:
            scanner.scan(args.scan)
        if args.connect:
            if args.info:
                connector.getDeviceFacts(args.connect)
            if args.config:
                connector.getConfig(args.connect)
            if args.interface:
                connector.getInterfaces(args.connect)
            if args.vlans:
                connector.getVlans(args.connect)
            if args.mac:
                connector.getMacTable(args.connect)
            if args.arp:
                connector.getArpTable(args.connect)

        if args.configure:
            if args.hostname:
                configurer.changeHostname(args.configure, args.hostname)
            if args.vlan:
                name = args.name if args.name else ""
                delete = args.delete if args.delete else False
                configurer.changeVlan(args.configure, args.vlan, name, delete)
            if args.int:
                if args.open:
                    configurer.shutdown(args.configure, args.int, False)
                if args.close:
                    configurer.shutdown(args.configure, args.int, True)
    
if __name__ == "__main__":
    main()
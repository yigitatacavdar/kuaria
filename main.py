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
    parser.add_argument("-scan", metavar="<IP_ADDRESS>", help="scan for devices or subnets")
    parser.add_argument("-connect", metavar="<IP_ADDRESS>", help="test connection to devices")
    args, unknown = parser.parse_known_args()

    if not any(vars(args).values()):
        wizard()
    else:
        if args.scan:
            scanner.scan(args.scan)
        if args.connect:
            connector.autoConnect(args.connect)

    
if __name__ == "__main__":
    main()
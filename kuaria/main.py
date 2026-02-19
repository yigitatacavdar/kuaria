"""
kuaria - simple command line tool for network automation

Copyright (C) 2026 Yigit Ata Cavdar

This program is licensed under the GNU General Public License v3.0.
See the LICENSE file for details.
"""

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
from kuaria.core import scanner
from kuaria.core import connector
from kuaria.core import configurer
from kuaria.utils import commonCreds

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
    parser = argparse.ArgumentParser(prog=kuariaAscii, description="kuaria v1.0.0 - simple command line tool for network automation\n""Copyright (C) 2026 Yigit Ata Cavdar", epilog="""
Warnings:
  ssh and scp server must be enabled on devices (ip scp server enable)
  user privilege should be 15 (username admin privilege 15 secret <password>) or (username admin privilege 15 password <password>)
  do not modify the management session interface
  for information commands each general command must have a [MAIN COMMAND]
  for configuration commands each general command must have a [MAIN COMMAND] and [SUB COMMAND]
  nmap must be installed to use -scan feature
  adding more credentials slow the shh connection
""",
    formatter_class=argparse.RawDescriptionHelpFormatter)
 
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--scan", metavar="<IP_ADDRESS>", help="scan for devices or subnets [MAIN COMMAND]")

    group.add_argument("--creds", action="store_true", help="wizard for access to credentials of devices, credentials are encrypted and stored to automatically connect to devices [MAIN COMMAND]")

    group.add_argument("--connect", metavar="<IP_ADDRESS>", help="get information about devices, first must --connect <IP_ADDRESS> to use other commands [MAIN COMMAND]")

    parser.add_argument("--info", action="store_true", help="detailed device information")
    parser.add_argument("--env", action="store_true", help="device environment information")
    parser.add_argument("--config", action="store_true", help="running configuration")
    parser.add_argument("--interface", action="store_true", help="interfaces")
    parser.add_argument("--vlans", action="store_true", help="vlans")
    parser.add_argument("--mac", action="store_true", help="mac table")
    parser.add_argument("--arp", action="store_true", help="arp table")
    parser.add_argument("--switchports", action="store_true", help="switchports")
    parser.add_argument("--route", action="store_true", help="routing table")
    parser.add_argument("--lldp", action="store_true", help="lldp neighbors")


    group.add_argument("--configure", metavar="<IP_ADDRESS>", help="change configuration of devices, first must --configure <IP_ADDRESS> to use other commands [MAIN COMMAND]")

    parser.add_argument("--hostname", metavar="<hostname>", help="change the hostname of the device [SUB COMMAND]")
    parser.add_argument("--delete", metavar="<config>", help="delete a configuration [SUB COMMAND]")

    parser.add_argument("--vlan", metavar="<vlan>", help="create a vlan [SUB COMMAND]")
    parser.add_argument("--name", metavar="<name>", help="add a name to vlans and other configurations")

    parser.add_argument("--int", metavar="<interface>", help="configure interfaces [SUB COMMAND]")
    parser.add_argument("--open", action="store_true", help="open interface (no shutdown)")
    parser.add_argument("--close", action="store_true", help="close interface (shutdown)")
    parser.add_argument("--ip", metavar="<ip> <subnet>", help="add ip address to interfaces '<ip> <subnet>' or 'dhcp'")
    parser.add_argument("--nat", metavar="<direction>", help="add nat to interfaces 'inside' or 'outside'")
    parser.add_argument("--switchport", metavar="<mode>", help="add switchport mode to interface 'access' or 'trunk'")
    parser.add_argument("--access", metavar="<vlan>", help="add vlan to access interface 'vlan 10'")
    parser.add_argument("--trunk", metavar="<vlans>", help="add vlans to trunk interface'vlan 10,20'")
    parser.add_argument("--accgr", metavar="<acl> <in/out>", help="add an acl to the interface")
    parser.add_argument("--speed", metavar="<speed>", help="add speed to interfaces '<speed>' or 'auto'")
    parser.add_argument("--duplex", metavar="<duplex>", help="add duplex to interfaces 'full' or 'half' or 'auto'")

    parser.add_argument("--dhcp", action="store_true", help="add dhcp pool 'must have -name -network -defrouter -dns' [SUB COMMAND]")
    parser.add_argument("--static", action="store_true", help="use with -dhcp to assign a static dhcp pool to a device 'must have -name -host -clientid -defrouter -dns'")
    parser.add_argument("--exclude", metavar="<ip_range>", help="use with -dhcp to add excluded address to dhcp")
    parser.add_argument("--network", metavar="<ip> <subnet>", help="add network ip")
    parser.add_argument("--defrouter", metavar="<ip>", help="add default router")
    parser.add_argument("--dns", metavar="<dns>", help="add dns server")
    parser.add_argument("--clientid", metavar="<mac>", help="add client identifier")
    parser.add_argument("--host", metavar="<ip> <subnet>", help="add host ip")

    parser.add_argument("--routing", action="store_true", help="enable ip routing [SUB COMMAND]")
    parser.add_argument("--sroute", metavar="<ip> <subnet> <next-hop>", help="enable static routing [SUB COMMAND]")

    parser.add_argument("--subint", metavar="<sub-interface>", help="add sub interface [SUB COMMAND]")
    parser.add_argument("--encap", metavar="<vlan number>", help="use with -subint to add encapsulation")

    parser.add_argument("--pat", action="store_true", help="add port address translation 'must have --nat --list --int --pat' [SUB COMMAND]")
    parser.add_argument("--pfw", action="store_true", help="add port forwarding 'must have --nat --proto --ip --inport --int --outport' [SUB COMMAND]")
    parser.add_argument("--list", metavar="<acl-list>", help="add acl list")
    parser.add_argument("--proto", metavar="<protocol>", help="add protocol")
    parser.add_argument("--inport", metavar="<inside port>", help="add inside port")
    parser.add_argument("--outport", metavar="<outside port>", help="add outside port")

    parser.add_argument("--aclstd", action="store_true", help="add a standart access-list 'must have --name --permit --deny'")
    parser.add_argument("--aclext", action="store_true", help="add an extended access-list 'must have --name --permit --deny'")
    parser.add_argument("--permit", metavar="<rule>", help="add a permit rule")
    parser.add_argument("--deny", metavar="<rule>", help="add a deny rule")

    
    args, unknown = parser.parse_known_args()

    if not any(vars(args).values()):
        wizard()
    else:
        if args.scan:
            scanner.scan(args.scan)
        if args.creds:
            commonCreds.saveCommonCreds()
        if args.connect:
            if args.info:
                connector.getDeviceFacts(args.connect)
            if args.env:
                connector.getEnvironment(args.connect)
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
            if args.switchports:
                connector.getSwitchports(args.connect)
            if args.route:
                connector.getRoutingTable(args.connect)
            if args.lldp:
                connector.getLldp(args.connect)

        if args.configure:
            if args.hostname:
                configurer.changeHostname(args.configure, args.hostname)

            if args.delete:
                configurer.delete(args.configure, args.delete)

            if args.vlan:
                configurer.addVlan(args.configure, args.vlan)
                if args.name:
                    configurer.nameVlan(args.configure, args.vlan, args.name)

            if args.int:
                if args.open:
                    configurer.intShutdown(args.configure, args.int, False)
                if args.close:
                    configurer.intShutdown(args.configure, args.int, True)
                if args.ip:
                    configurer.intIp(args.configure, args.int, args.ip)
                if args.delete:
                    configurer.deleteInt(args.configure, args.int, args.delete)
                if args.switchport:
                    configurer.switchport(args.configure, args.int, args.switchport)
                if args.access:
                    configurer.switchportAccess(args.configure, args.int, args.access)
                if args.trunk:
                    configurer.switchportTrunk(args.configure, args.int, args.trunk)
                if args.nat:
                    configurer.intNat(args.configure, args.int, args.nat)
                if args.accgr:
                    configurer.intAccGr(args.configure, args.int, args.accgr)
                if args.speed:
                    configurer.intSpeed(args.configure, args.int, args.speed)
                if args.duplex:
                    configurer.intDuplex(args.configure, args.int, args.duplex)


            if args.dhcp:
                missing = []

                if not args.name:
                    missing.append("name")
                if not args.network:
                    missing.append("network")
                if not args.defrouter:
                    missing.append("defrouter")
                if not args.dns:
                    missing.append("dns")

                if missing:
                    print(f"Missing arguments: {', '.join(missing)}")
                else:
                    configurer.dhcpPool(
                        deviceIpInput=args.configure,
                        nameInput=args.name,
                        networkInput=args.network,
                        defaultRouterInput=args.defrouter,
                        dnsServerInput=args.dns)
                    
            if args.dhcp and args.static:
                missing = []

                if not args.name:
                    missing.append("name")
                if not args.host:
                    missing.append("host")
                if not args.clientid:
                    missing.append("clientid")
                if not args.defrouter:
                    missing.append("defrouter")
                if not args.dns:
                    missing.append("dns")

                if missing:
                    print(f"Missing arguments: {', '.join(missing)}")
                else:
                    configurer.dhcpPool(
                        deviceIpInput=args.configure,
                        nameInput=args.name,
                        hostInput=args.host,
                        clientIdentifierInput=args.clientid,
                        defaultRouterInput=args.defrouter,
                        dnsServerInput=args.dns
                    )

            if args.dhcp:
                if args.exclude:
                    configurer.dhcpExcluded(args.configure, args.exclude)

            if args.routing:
                configurer.routing(args.configure)

            if args.sroute:
                configurer.sroute(args.configure, args.sroute)

            if args.subint:
                configurer.subint(args.configure, args.subint)
                if args.encap:
                    configurer.encapsulation(args.configure, args.subint, args.encap)
                if args.ip:
                    configurer.intIp(args.configure, args.subint, args.ip)
                if args.open:
                    configurer.intShutdown(args.configure, args.subint, False)
                if args.close:
                    configurer.intShutdown(args.configure, args.subint, True)

            
            if args.pat:
                missing = []

                if not args.nat:
                    missing.append("nat")
                if not args.list:
                    missing.append("list")
                if not args.int:
                    missing.append("int")
                if not args.pat:
                    missing.append("pat")

                if missing:
                    print(f"Missing arguments: {', '.join(missing)}")
                else:
                    configurer.pat(
                        deviceIpInput=args.configure,
                        natInput=args.nat,
                        listInput=args.list,
                        intInput=args.int,
                        patInput=args.pat)
                    
            if args.pfw:
                missing = []

                if not args.nat:
                    missing.append("nat")
                if not args.proto:
                    missing.append("protocol")
                if not args.ip:
                    missing.append("ip")
                if not args.inport:
                    missing.append("inport")
                if not args.int:
                    missing.append("int")
                if not args.outport:
                    missing.append("outport")

                if missing:
                    print(f"Missing arguments: {', '.join(missing)}")
                else:
                    configurer.portForward(
                        deviceIpInput=args.configure,
                        natInput=args.nat,
                        protocolInput=args.proto,
                        ipInput=args.ip,
                        inPort=args.inport,
                        intInput=args.int,
                        outPort=args.outport)

            if args.aclstd:
                missing = []

                if not args.name:
                    missing.append("name")
                if not args.permit:
                    missing.append("permit")
                if not args.deny:
                    missing.append("deny")

                if missing:
                    print(f"Missing arguments: {', '.join(missing)}")
                else:
                    configurer.aclStandard(
                        deviceIpInput=args.configure,
                        nameInput=args.name,
                        permitRuleInput=args.permit,
                        denyRuleInput=args.deny)

            if args.aclext:
                missing = []

                if not args.name:
                    missing.append("name")
                if not args.permit:
                    missing.append("permit")
                if not args.deny:
                    missing.append("deny")

                if missing:
                    print(f"Missing arguments: {', '.join(missing)}")
                else:
                    configurer.aclExtended(
                        deviceIpInput=args.configure,
                        nameInput=args.name,
                        permitRuleInput=args.permit,
                        denyRuleInput=args.deny)
    
if __name__ == "__main__":
    main()
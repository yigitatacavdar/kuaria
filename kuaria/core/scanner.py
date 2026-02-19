import nmap

def scan(subnetIpInput):
    print("scanning...")
    networkScanner(subnetIpInput)

    print('----------------------------------------------------')

def networkScanner(subnetIpInput):

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
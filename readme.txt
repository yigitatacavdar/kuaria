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


Created By Yigit Ata Cavdar

kuaria - simple command line tool for network automation

see current feature document for work flow

see kuaria demo for working feature set

---------------------------------------------------------------------

Dev Guide:

napalm, python-nmap packages need to be installed

> create myproject-venv directory

> create a virtual environment
python3 -m venv ~/myproject-venv

> activate
source ~/myproject-venv/bin/activate

> upgrade pip
pip install --upgrade pip

> install packages
pip install python-nmap napalm

> to get it working with vscode go to command pallate and select python: select interpreter

> write down the path
myproject-venv/bin/python 

> to see the packages installed
python -m pip list

---------------------------------------------------------------------

Docs:

kuaria - simple command line tool for network automation

current feature document 15/09/2025

3 main parts are required for the program to exist

the scanner:

- auto scans common subnets, if no hosts found, asks user to input the desired subnet.
- retrieves active ips, port 22 states, device info, these are used when connecting with the configurer

- usage: -scan <IP_ADDRESS>

the connector:

- uses info gathered by the scanner to try an auto login on discovered devices
- retrieves detailed device info(make, model) 
- the user can login to devices that failed the auto login, the credentials entered this way are safely stored and will be used to auto login into devices

- usage: -connect <IP_ADDRESS>
         -connect <IP_ADDRESS> -info
         -connect <IP_ADDRESS> -config


the configurer:

- the basic configuration options of the program are: setting hostname, setting ip address, vlan configuration, port forwarding, static ip leasing
- the basic configuration options for switches and routers are different
- switches: vlan configuration, setting ports for inter-vlan routing
- routers: outside/inside interface configuration, port forwarding, static ip leasing

- usage: -configure <IP_ADDRESS> -hostname "newhostname"
         -configure <IP_ADDRESS> -changeip "<IP_ADDRESS>"   <- works for switches   ---| some way to
         -configure <IP_ADDRESS> -changeip "<IP_ADDRESS>" -interface "GE0/1"   <- works for routers---| differentiate?



to do:

- common credentials are to be entered by the user, saved, and used for connection with commoncreds, user can enter like 3 commoncreds to not tire ssh(for laterrrr)
- add other info to connector
- add hostname, ip and etc to configurer


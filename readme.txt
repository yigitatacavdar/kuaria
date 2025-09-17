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

2 main parts are required for the program to exist

the scanner:

- auto scans common subnets, if no hosts found, asks user to input the desired subnet.
- retrieves active ips, port 22 states, device info, these are used when connecting with the configurer

the connector:

- uses info gathered by the scanner to try an auto login on discovered devices
- retrieves detailed device info(make, model) 
- the user can login to devices that failed the auto login, the credentials entered this way are safely stored and will be used to auto login into devices

the configurer:

- the basic configuration options of the program are: setting hostname, setting ip address, vlan configuration, port forwarding, static ip leasing
- the basic configuration options for switches and routers are different
- switches: vlan configuration, setting ports for inter-vlan routing
- routers: outside/inside interface configuration, port forwarding, static ip leasing

to do:

- add argparse to the program to take commands
- package it all into a distributable format



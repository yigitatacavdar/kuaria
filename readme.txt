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

Copyright (C) 2026 Yigit Ata Cavdar

kuaria - simple command line tool for network automation

see current feature document for work flow

to become a collaborator, just email me at yigitatacavdar@gmail.com

---------------------------------------------------------------------

Dev Guide:

napalm, netmiko, python-nmap ntc-templates, tabulate packages need to be installed

> create kuaria-venv directory

> create a virtual environment
python3 -m venv ~/kuaria-venv

> activate
source ~/myproject-venv/bin/activate

> upgrade pip
pip install --upgrade pip

> install packages
pip install python-nmap napalm tabulate ntc-templates netmiko

> to get it working with vscode go to command pallate and select python: select interpreter

> write down the path
myproject-venv/bin/python 

> to see the packages installed
python -m pip list

> run
python -m kuaria.main -h

---------------------------------------------------------------------

Docs:

kuaria - simple command line tool for network automation
version: v1.0.1
Copyright (C) 2026 Yigit Ata Cavdar

current feature document 19/02/2026

currently only works for cisco devices

3 main parts are required for the program to exist

the scanner:

- scans entered subnets.
- retrieves active ips, port 22 states, device info, these are used when connecting with the configurer

- usage: --scan <IP_ADDRESS>

the connector:

- uses saved credentials to auto-connect to devices with given ip
- used with info commands to retrieve detailed device info(make, model, config) 
- the user can login to devices that failed the auto login

- usage: --connect <IP_ADDRESS> --info
         --connect <IP_ADDRESS> --config


the configurer:

- the basic configuration options of the program are: setting hostname, setting ip address, vlan configuration, port forwarding, static ip leasing
- switches: vlan configuration, setting ports for inter-vlan routing
- routers: outside/inside interface configuration, port forwarding, static ip leasing

- usage: --configure <IP_ADDRESS> --hostname "newhostname"
         --configure <IP_ADDRESS> --ip "<IP_ADDRESS>"

-----------------------------------------------------------------------------

to do:

- a wizard that finds your topology and sets a general config automatically (long shot)






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


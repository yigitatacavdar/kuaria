
from utils.commonCreds import loadCommonCreds
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko import NetmikoAuthenticationException
from tabulate import tabulate
import pprint

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

def getDeviceFacts(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving device info...")
    facts = device.get_facts()
    print(deviceIpInput)
    print("----------------------------------------------------")
    print(f"device: {facts['vendor']} {facts['model']}")
    print(f"hostname: {facts['hostname']}")
    device.close()

def getConfig(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving running configuration...")
    config = device.get_config()
    running_config = config.get("running", "")
    for line in running_config.splitlines():
        print(line)
    device.close()

def getInterfaces(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving interfaces...")
    interfaces = device.get_interfaces()

    table = []
    for intf, details in interfaces.items():
        table.append([
            intf,
            details["is_up"],
            details["is_enabled"],
            details["speed"],
            details["mac_address"]
        ])
    print(tabulate(table, headers=["interface", "up", "enabled", "speed", "MAC"]))

    device.close()

def getVlans(deviceInput):
    device = autoConnect(deviceInput)
    print("retrieving vlans..")
    vlans = device.get_vlans()

    table = []
    for vlan, details in vlans.items():
        if details["interfaces"]:
            interfaces_str = "\n".join(details["interfaces"])
        else:
            interfaces_str = "[]"

        table.append([
            vlan,
            details["name"],
            interfaces_str
            ])
    print(tabulate(table, headers=["vlan", "name", "interfaces"]))

    device.close()

def getMacTable(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving mac table...")
    macTable = device.get_mac_address_table()
    
    table = []
    for entry in macTable:
        interface = entry.get("interface")
        mac = entry.get("mac")
        vlan = entry.get("vlan")

        if interface:
            table.append([
                mac,
                interface,
                vlan
                ])
    print(tabulate(table, headers=["MAC", "interface", "vlan"]))

    device.close()

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
            print("connected to %s" %deviceIpInput)
            print("username and password found as: %s, %s" % (usernameCommon, passwordCommon))
            return device
    print("connection failed with common credentials")
    device = manualConnect(deviceIpInput)
    return device


def manualConnect(deviceIpInput):
    deviceUserInput = input("enter the username of the device you want to work with: ")
    devicePasswordInput = input("enter the password of the device you want to work with: ")
    deviceSecretInput = input("enter the enable password of the device you want to work with: ")

    print("connecting...")

    optional_args = dict(optional_args_base)
    if deviceSecretInput:
            optional_args["secret"] = deviceSecretInput 

    driver = get_network_driver("ios")
    device = driver(hostname=deviceIpInput, username=deviceUserInput, password=devicePasswordInput, optional_args=optional_args)

    try:
        device.open()
        print("connected to %s" %deviceIpInput)
        return device
    except (ConnectionException, NetmikoAuthenticationException):
        print("connection failed with entered credentials")
        return manualConnect(deviceIpInput)

    
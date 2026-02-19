
from kuaria.utils.commonCreds import loadCommonCreds
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko import NetmikoAuthenticationException
from tabulate import tabulate
from ntc_templates.parse import parse_output
import pprint
import re

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

    table = []

    for key, value in facts.items():
        if key == "interface_list":
            continue

        table.append([key, value])

    print(tabulate(
        table,
        headers=["Fact", "Value"]
    ))

    device.close()

def getConfig(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving running configuration...")
    config = device.get_config()
    running_config = config.get("running", "")
    for line in running_config.splitlines():
        print(line)
    device.close()

def getEnvironment(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving environment information...")

    env = device.get_environment()

    table = []

    cpu = env.get("cpu", {})
    for cpu_id, cpu_data in cpu.items():
        table.append([
            "CPU",
            cpu_id,
            cpu_data.get("usage"),
            "%"
        ])

    memory = env.get("memory", {})
    table.append([
        "Memory",
        "system",
        memory.get("used_ram"),
        "bytes"
    ])

    temperature = env.get("temperature", {})
    for sensor, temp_data in temperature.items():
        table.append([
            "Temperature",
            sensor,
            temp_data.get("temperature"),
            "C"
        ])

    fans = env.get("fans", {})
    for fan, fan_data in fans.items():
        table.append([
            "Fan",
            fan,
            "OK" if fan_data.get("status") else "FAIL",
            ""
        ])

    power = env.get("power", {})
    for psu, psu_data in power.items():
        table.append([
            "Power",
            psu,
            "OK" if psu_data.get("status") else "FAIL",
            ""
        ])

    print(tabulate(
        table,
        headers=["Component", "Name", "Value", "Unit"]
    ))

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
    print("retrieving vlans...")
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

def getSwitchports(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving switchport modes...")

    cmd = "show interfaces switchport"
    raw_output = device.cli([cmd])[cmd]

    parsed = parse_output(
        platform="cisco_ios",
        command="show interfaces switchport",
        data=raw_output
    )

    table = []

    for entry in parsed:
        interface = entry.get("interface")
        admin_mode = entry.get("admin_mode")
        oper_mode = entry.get("oper_mode")
        access_vlan = entry.get("access_vlan")
        native_vlan = entry.get("native_vlan")

        table.append([
            interface,
            admin_mode,
            oper_mode,
            access_vlan,
            native_vlan
        ])

    print(tabulate(
        table,
        headers=[
            "Interface",
            "Admin Mode",
            "Oper Mode",
            "Access VLAN",
            "Native VLAN"
        ]
    ))

    device.close()

def getArpTable(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving arp table...")
    arpTable = device.get_arp_table()
    
    table = []
    for entry in arpTable:
        interface = entry.get("interface")
        mac = entry.get("mac")
        ip = entry.get("ip")

        if interface:
            table.append([
                mac,
                interface,
                ip
                ])
    print(tabulate(table, headers=["MAC", "interface", "ip"]))

    device.close()

def getLldp(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving lldp neighbors...")

    lldp = device.get_lldp_neighbors()

    table = []

    for local_interface, neighbors in lldp.items():
        for neighbor in neighbors:
            table.append([
                local_interface,
                neighbor.get("hostname"),
                neighbor.get("port")
            ])

    print(tabulate(
        table,
        headers=["Local Interface", "Neighbor Hostname", "Neighbor Interface"]
    ))

    device.close()

def getRoutingTable(deviceIpInput):
    device = autoConnect(deviceIpInput)
    print("retrieving routing table...")

    output = device.cli(["show ip route"])
    lines = output["show ip route"].splitlines()

    table = []

    for line in lines:
        line = line.strip()

        if line.startswith("S*"):
            match = re.search(r"(0\.0\.0\.0/0).*via (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                table.append([
                    match.group(1),
                    "static",
                    match.group(2),
                    "",
                    "1"
                ])

        elif line.startswith("C "):
            match = re.search(r"(\d+\.\d+\.\d+\.\d+/\d+).*connected, (\S+)", line)
            if match:
                table.append([
                    match.group(1),
                    "connected",
                    "",
                    match.group(2),
                    "0"
                ])

    print(tabulate(
        table,
        headers=["Destination", "Protocol", "Next Hop", "Interface", "AD"]
    ))

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
            print("username and password found")
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

    
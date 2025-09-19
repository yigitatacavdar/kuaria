
from utils.commonCreds import loadCommonCreds
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko import NetmikoAuthenticationException

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
    
    try:
        device = autoConnect(deviceIpInput)
        print("retrieving device info...")
        facts = device.get_facts()
        print(f"Device: {facts['vendor']} {facts['model']}")
        device.close()
        return facts
    except (ConnectionException, NetmikoAuthenticationException) as e:
        print("connection failed!")
        autoConnect()

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
    manualConnect(deviceIpInput)


def manualConnect(deviceIpInput):
    deviceUserInput = input("enter the username of the device you want to work with: ")
    devicePasswordInput = input("enter the password of the device you want to work with: ")
    deviceSecretInput = input("enter the enable password of the device you want to work with: ")

    print("connecting...")
    driver = get_network_driver("ios")

    try:
        device = driver(hostname=deviceIpInput, username=deviceUserInput, password=devicePasswordInput, optional_args=deviceSecretInput)
        device.open()
    except (ConnectionException, NetmikoAuthenticationException):
        print("connection failed with entered credentials")
    else:
        print("connected to %s" %deviceIpInput)
        return device
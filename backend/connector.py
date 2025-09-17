
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

def getDeviceFacts(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput):

    driver = get_network_driver("ios")

    optional_args = {
    "secret": deviceSecretInput,
    "allow_agent": False,
    "look_for_keys": False,
    "global_delay_factor": 2,
    "fast_cli": False,
    "ssh_config_file": None,
    "key_exchange": ["diffie-hellman-group14-sha1", "diffie-hellman-group1-sha1", "diffie-hellman-group-exchange-sha256", "ecdh-sha2-nistp256"]}

    device = driver(hostname=deviceIpInput, username=deviceUserInput, password=devicePasswordInput, optional_args=optional_args)
    try:
        device.open()
        print("retrieving device info...")
        facts = device.get_facts()
        device.close()
        return facts
    except (ConnectionException, NetmikoAuthenticationException) as e:
        print("connection failed!")
        autoConnect()

def connectDevice(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput):
    deviceInfo = getDeviceFacts(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput)
    print(f"Device: {deviceInfo['vendor']} {deviceInfo['model']}")

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
            print("connected")
            print("username and password found as: %s, %s" % (usernameCommon, passwordCommon))
            connectDevice(deviceIpInput, usernameCommon, passwordCommon, secretCommon)
            device.close()
            return

    print("connection failed with common credentials")
    manualConnect(deviceIpInput)


def manualConnect(deviceIpInput):
    deviceUserInput = input("enter the username of the device you want to work with: ")
    devicePasswordInput = input("enter the password of the device you want to work with: ")
    deviceSecretInput = input("enter the enable password of the device you want to work with: ")

    print("connecting...")

    connectDevice(deviceIpInput, deviceUserInput, devicePasswordInput, deviceSecretInput)
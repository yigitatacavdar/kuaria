from core.connector import autoConnect

def areYouSureInput():
    sureInput = input("are you sure you want to change this configuration? (Y/n) ").strip().lower()
    if sureInput in ("y", "yes"):
        return True
    elif sureInput in ("n", "no"):
        return False
    else:
        print("please enter yes or no (Y/n)")
        return areYouSureInput()
    
def delete(deviceIpInput, confInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        print(f"deleting configuration {confInput}")
        conf = f"no {confInput}"
        print("Configuration deleted successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### HOSTNAME CONFIGURATION ###
    
def changeHostname(deviceIpInput, hostnameInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        device.load_merge_candidate(config=f"hostname {hostnameInput}")
        device.commit_config()
        print("configuration saved successfully")
    except Exception as e:
        print("error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### VLAN CONFIGURATION ###

def addVlan(deviceIpInput, vlanInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()

    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        print(f"adding vlan {vlanInput}")
        conf = f"vlan {vlanInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def nameVlan(deviceIpInput, vlanInput, nameInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()

    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        print(f"changing vlan name to {nameInput}")
        conf = f"vlan {vlanInput}\n name {nameInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### INTERFACE CONFIGURATION ###

def intShutdown(deviceIpInput, intInput, shutdownInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()

    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        if shutdownInput:
            print(f"closing interface {intInput}")
            conf = f"int {intInput}\n shutdown"
        else:
            print(f"opening interface {intInput}")
            conf = f"int {intInput}\n no shutdown"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def intIp(deviceIpInput, intInput, ipInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()

    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {intInput}\n ip address {ipInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def deleteInt(deviceIpInput, intInput, deleteInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()

    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {intInput}\n no {deleteInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()


### DHCP CONFIGURATION ###

def dhcpPool(deviceIpInput, nameInput, networkInput, defaultRouterInput, dnsServerInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"ip dhcp pool {nameInput}\n network {networkInput}\n default-router {defaultRouterInput}\n dns-server {dnsServerInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def dhcpPoolStatic(deviceIpInput, nameInput, hostInput, clientIdentifierInput, defaultRouterInput, dnsServerInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"ip dhcp pool {nameInput}\n host {hostInput}\n client-identifier {clientIdentifierInput}\n default-router {defaultRouterInput}\n dns-server {dnsServerInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def dhcpExcluded(deviceIpInput, excludedIp):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"ip dhcp excluded-address {excludedIp}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### ROUTING ###

def routing(deviceIpInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"ip routing"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### SUB INTERFACE ###

def subint(deviceIpInput, subIntInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {subIntInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def encapsulation(deviceIpInput, subIntInput, encapInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {subIntInput}\n encapsulation dot1Q {encapInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### SWITCHPORT CONFIGURATION ###

def switchport(deviceIpInput, intInput, modeInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {intInput}\n switchport mode {modeInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def switchportAccess(deviceIpInput, intInput, vlanInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {intInput}\n switchport access {vlanInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def switchportTrunk(deviceIpInput, intInput, vlanInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        conf = f"int {intInput}\n switchport trunk allowed {vlanInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

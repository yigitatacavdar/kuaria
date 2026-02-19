from kuaria.core.connector import autoConnect

def areYouSureInput():
    sureInput = input("are you sure you want to change this configuration? (Y/n) ").strip().lower()
    if sureInput in ("y", "yes"):
        return True
    elif sureInput in ("n", "no"):
        return False
    else:
        print("please enter yes or no (Y/n)")
        return areYouSureInput()
    
### DELETE FUNCTION ###
    
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
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration deleted successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### CONFIGURATION FUNCTION ###

def config(deviceIpInput, conf):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    
    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

### HOSTNAME CONFIGURATION ###
    
def changeHostname(deviceIpInput, hostnameInput):
    conf = f"hostname {hostnameInput}"
    config(deviceIpInput, conf)

### VLAN CONFIGURATION ###

def addVlan(deviceIpInput, vlanInput):
    conf = f"vlan {vlanInput}"
    config(deviceIpInput, conf)

def nameVlan(deviceIpInput, vlanInput, nameInput):
    conf = f"vlan {vlanInput}\n name {nameInput}"
    config(deviceIpInput, conf)

### INTERFACE CONFIGURATION ###

def intShutdown(deviceIpInput, intInput, shutdownInput):
    if shutdownInput:
        print(f"closing interface {intInput}")
        conf = f"int {intInput}\n shutdown"
    else:
        print(f"opening interface {intInput}")
        conf = f"int {intInput}\n no shutdown"
    config(deviceIpInput, conf)

def intIp(deviceIpInput, intInput, ipInput):
    conf = f"int {intInput}\n ip address {ipInput}"
    config(deviceIpInput, conf)

def intNat(deviceIpInput, intInput, natInput):
    conf = f"int {intInput}\n ip nat {natInput}"
    config(deviceIpInput, conf)

def intAccGr(deviceIpInput, intInput, aclInput):
    conf = f"int {intInput}\n ip access-group {aclInput}"
    config(deviceIpInput, conf)

def intSpeed(deviceIpInput, intInput, speedInput):
    conf = f"int {intInput}\n speed {speedInput}"
    config(deviceIpInput, conf)

def intDuplex(deviceIpInput, intInput, duplexInput):
    conf = f"int {intInput}\n duplex {duplexInput}"
    config(deviceIpInput, conf)

def deleteInt(deviceIpInput, intInput, deleteInput):
    conf = f"int {intInput}\n no {deleteInput}"
    config(deviceIpInput, conf)

## access-group

### DHCP CONFIGURATION ###

def dhcpPool(deviceIpInput, nameInput, networkInput, defaultRouterInput, dnsServerInput):
    conf = f"ip dhcp pool {nameInput}\n network {networkInput}\n default-router {defaultRouterInput}\n dns-server {dnsServerInput}"
    config(deviceIpInput, conf)

def dhcpPoolStatic(deviceIpInput, nameInput, hostInput, clientIdentifierInput, defaultRouterInput, dnsServerInput):
    conf = f"ip dhcp pool {nameInput}\n host {hostInput}\n client-identifier {clientIdentifierInput}\n default-router {defaultRouterInput}\n dns-server {dnsServerInput}"
    config(deviceIpInput, conf)

def dhcpExcluded(deviceIpInput, excludedIp):
    conf = f"ip dhcp excluded-address {excludedIp}"
    config(deviceIpInput, conf)

### ROUTING ###

def routing(deviceIpInput):
    conf = f"ip routing"
    config(deviceIpInput, conf)

def sroute(deviceIpInput, srouteInput):
    conf = f"ip route {srouteInput}"
    config(deviceIpInput, conf)

### SUB INTERFACE ###

def subint(deviceIpInput, subIntInput):
    conf = f"int {subIntInput}"
    config(deviceIpInput, conf)

def encapsulation(deviceIpInput, subIntInput, encapInput):
    conf = f"int {subIntInput}\n encapsulation dot1Q {encapInput}"
    config(deviceIpInput, conf)

### SWITCHPORT CONFIGURATION ###

def switchport(deviceIpInput, intInput, modeInput):
    conf = f"int {intInput}\n switchport mode {modeInput}"
    config(deviceIpInput, conf)

def switchportAccess(deviceIpInput, intInput, vlanInput):
    conf = f"int {intInput}\n switchport access {vlanInput}"
    config(deviceIpInput, conf)

def switchportTrunk(deviceIpInput, intInput, vlanInput):
    conf = f"int {intInput}\n switchport trunk allowed {vlanInput}"
    config(deviceIpInput, conf)

### PORT FORWARDING/ADDRESS TRANSLATION ###

def pat(deviceIpInput, natInput, listInput, intInput, patInput):
    conf = f"ip nat {natInput} source list {listInput} interface {intInput} {patInput}"
    config(deviceIpInput, conf)

def portForward(deviceIpInput, natInput, protocolInput, ipInput, inPort, intInput, outPort):
    conf = f"ip nat {natInput} source static {protocolInput} {ipInput} {inPort} interface {intInput} {outPort}"
    config(deviceIpInput, conf)    

### ACL CONFIGURATION ###

def aclStandard(deviceIpInput, nameInput, permitRuleInput, denyRuleInput):
    conf = f"ip access-list standard {nameInput}\n permit {permitRuleInput}\n deny {denyRuleInput}"
    config(deviceIpInput, conf)

def aclExtended(deviceIpInput, nameInput, permitRuleInput, denyRuleInput):
    conf = f"ip access-list extended {nameInput}\n permit {permitRuleInput}\n deny {denyRuleInput}"
    config(deviceIpInput, conf)




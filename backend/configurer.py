from backend.connector import autoConnect

def areYouSureInput():
    sureInput = input("are you sure you want to change this configuration? (Y/n) ").strip().lower()
    if sureInput in ("y", "yes"):
        return True
    elif sureInput in ("n", "no"):
        return False
    else:
        print("please enter yes or no (Y/n)")
        return areYouSureInput()
    
def changeHostname(deviceIpInput, hostnameInput):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()
    if sureInput:
        try:
            device.load_merge_candidate(config=f"hostname {hostnameInput}")
            device.commit_config()
            print("configuration saved successfully")
        except Exception as e:
            print("error, rolling back:", e)
            device.rollback()
        finally:
            device.close()
    else:
        print("canceled configuration")

def changeVlan(deviceIpInput, vlanInput, nameInput, deleteInput=False):
    device = autoConnect(deviceIpInput)
    sureInput = areYouSureInput()

    if not sureInput:
        print("Canceled configuration.")
        device.close()
        return
    try:
        if deleteInput:
            print(f"removing vlan {vlanInput}")
            conf = f"no vlan {vlanInput}"
        else:
            print(f"adding vlan {vlanInput}")
            conf = f"vlan {vlanInput}\n name {nameInput}"
        device.load_merge_candidate(config=conf)
        device.commit_config()
        print("Configuration saved successfully")
    except Exception as e:
        print("Error, rolling back:", e)
        device.rollback()
    finally:
        device.close()

def shutdown(deviceIpInput,intInput, shutdownInput):
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
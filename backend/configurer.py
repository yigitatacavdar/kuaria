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



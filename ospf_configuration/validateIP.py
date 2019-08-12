def validIPdevices(devices):
    i = 0
    for device in devices:
        if isValid(device['ip']) == "no":
            del devices[i]
            print("Deleting the device as its ip address is invalid: \n    "+str(device))
            i -= 1
        i += 1
    return devices

def isValid(ipv4_addr):
    ip_oct_list = ipv4_addr.split(".")
    if len(ip_oct_list) == 4:
        for oct in ip_oct_list:
            if int(oct) not in range(0,256):
                return "no"
        return "yes" 
    return "no"

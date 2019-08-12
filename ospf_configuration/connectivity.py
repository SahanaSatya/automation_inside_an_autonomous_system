import subprocess

def connected_devices(devices):
    i = 0
    for device in devices:
        if is_connected(device['ip']) == "no":
            del devices[i]
            print("Deleting the device as its ip address is not connected: \n    "+str(device))
            i -= 1
        i += 1
    return devices 

def is_connected(ipv4_addr):
    	try:
    		cmd = "ping -c 4 "+str(ipv4_addr)+"| grep '100% packet loss'"
    		p = subprocess.check_output([cmd],shell=True)
    	except:
                return "yes"
    	return "no"
    

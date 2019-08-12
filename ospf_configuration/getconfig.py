from napalm import get_network_driver
import datetime
def getConfig(driver_name, ip_addr, user, passw,secr):
	driver = get_network_driver(driver_name)
	dev = driver(hostname = ip_addr, username = user, password = passw,optional_args={'secret':secr},)
	dev.open()
	obj  = dev.get_facts()
	hostname = obj['hostname']
	filename = obj['hostname']+str("_")+datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")+".txt"
	output = dev.get_config(retrieve="running")["running"]
	with open(filename,'w') as fh:
		fh.write(output)
	return hostname,filename

def getHostname(driver_name, ip_addr, user, passw,secr):
        driver = get_network_driver(driver_name)
        dev = driver(hostname = ip_addr, username = user, password = passw,optional_args={'secret':secr},)
        dev.open()
        obj  = dev.get_facts()
        hostname = obj['hostname']
        return hostname

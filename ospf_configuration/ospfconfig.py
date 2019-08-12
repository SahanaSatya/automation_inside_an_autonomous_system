from napalm import get_network_driver
from netmiko import ConnectHandler
import time
def OspfConfig(driver_name, ip_addr, user, passw, secr, pid, network_list):
	driver = get_network_driver(driver_name)
	dev = driver(hostname = ip_addr, username = user, password = passw,optional_args={'secret':secr},)
	dev.open()
	cfg = 'router ospf '+pid+'\n'
	print(network_list)
	for network in network_list:
		cfg+='\tnetwork '+network['ip']+' '+network['wc']+' area '+network['aid']+'\n'
	cfg+='end'
	print(cfg)
	dev.load_merge_candidate(config=str(cfg))
	diffs = dev.compare_config()
	print(diffs)
	if len(diffs)>0:
		dev.commit_config()
		time.sleep(3)
	else:
		dev.discard_config()
	dev.close()

def lbconf(driver_name, ip_addr, user, passw, secr, lbint):
        #abstracted using Netmiko...could not accomplish using NAPALM
	dev = driver1(driver_name,ip_addr, user, passw,secr)
	open1(dev)
	commit_changes(dev,"interface "+lbint+"\nip load-sharing per-packet\nend")
def driver1(driver_name,ip_addr, user, passw,secr):
	dev_dict = {'device_type':'cisco_'+driver_name,'username':user,'password':passw,'secret':secr,'ip':ip_addr}
	return ConnectHandler(**dev_dict)
def open1(device):
	device.enable()
def commit_changes(device,cmd):
	print(cmd)
	device.send_config_set(cmd)

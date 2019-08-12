from netmiko import ConnectHandler
import threading
def config(*router_file):
	r = ConnectHandler(**router_file[0]) 
	r.enable()
	r.send_config_from_file(config_file=router_file[1])
R1 = {'device_type': 'cisco_ios','ip':'198.51.100.3','username': 'lab','password':'lab123','secret':'lab123'}
R2 = {'device_type': 'cisco_ios','ip':'198.51.100.4','username': 'lab','password':'lab123','secret':'lab123'}
R3 = {'device_type': 'cisco_ios','ip':'198.51.100.5','username': 'lab','password':'lab123','secret':'lab123'}
devices=[R1,R2,R3]
files=["R1.txt","R2.txt","R3.txt"]
t = [None] * len(devices)
for i in range(len(devices)):
		t[i] = threading.Thread(target=config, args = (devices[i],files[i]))
		t[i].start()

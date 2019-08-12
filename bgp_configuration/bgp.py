from netmiko import ConnectHandler
import threading
import os
import time

def get_commands(conf_file,ip_addr):
	config_set = []
	if os.path.isfile(conf_file):
		found = 0
		localasnum = ""
		nip = ""
		nremoteas = ""
		networklist = ""  
		with open(conf_file,'r') as file1:
			for row in file1:
				if found == 4:
					li = row.split(':')[1].split('\n')[0]
					networklist = li.split(';')
					break
				if found == 3:
                                        nremoteas = row.split(':')[1].split('\n')[0]
					found = 4
				if found == 2:
                                        nip = row.split(':')[1].split('\n')[0]
					found = 3
				if found == 1:
					localasnum = row.split(':')[1].split('\n')[0]
					found = 2
				if "For "+ip_addr in row:
                                        found = 1
		config_set.append("router bgp "+localasnum)
		config_set.append("neighbor "+nip+" remote-as "+nremoteas)
		for li in networklist:
			n = li.split(',')
			config_set.append("network "+n[0]+" mask "+n[1])
		return config_set
	else:
		return "No file exits for command"

def config(*device):
	dev_con = ConnectHandler(**device[0])
	dev_con.enable()
	cmd = get_commands("bgp.conf",device[0]['ip'])
	if cmd != "No file exits for command" :
		try:
			output = dev_con.send_config_set(cmd)
			if len(output.split('\n')) > 4+len(cmd):
				raise Exception(cmd)
		except Exception as e:
                        print("For the device with IP:"+device[0]['ip']+", BGP deployment is not properly done")
                        print("Reason: Error in the following commands")
                        print(e.args)
			output = dev_con.send_command("sh run")
	                file_save = "conf_"+device[0]['ip']+"_backup.txt"
        	        with open(file_save,'w') as fh:
                	        fh.write(output)
                	print("Backed-up the running config for device with IP:"+device[0]['ip']+" locally in file: "+file_save)
			return
		time.sleep(2)
		output = dev_con.send_command("sh ip bgp neighbor")
		tab = output.split('\n')[0:3]
		li = tab[0].split(',')
		neighIP = li[0].split()[-1]
		remoteAS = li[1].split()[-1]
		state = tab[2].split(",")[0].split()[-1]
		print("For device with IP:"+device[0]['ip'])
		print("BGP Neighbor IP".ljust(20)+"BGP Neighbor AS".ljust(20)+"BGP Neighbor State".ljust(20))
		print(str(neighIP.encode("utf-8")).ljust(20)+str(remoteAS.encode("utf-8")).ljust(20)+str(state.encode("utf-8")).ljust(20))
		output = dev_con.send_command("sh run")
		file_save = "conf_"+device[0]['ip']+"_backup.txt"
		with open(file_save,'w') as fh:
			fh.write(output)
		print("Backed-up the running config for device with IP:"+device[0]['ip']+" locally in file: "+file_save) 
		dev_con.disconnect()
	else:
		print("could not deploy as "+ str(cmd))
	


def config_devices(devices):
	t = [None] * len(devices)
	for i in range(len(devices)):
		t[i] = threading.Thread(target=config, args = (devices[i],))
		t[i].start()

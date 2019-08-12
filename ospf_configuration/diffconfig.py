from napalm import get_network_driver
import time
def diff(driver_name, ip_addr, user, passw, secr, filenm):
	driver = get_network_driver(driver_name)
	dev = driver(hostname = ip_addr, username = user, password = passw,optional_args={'secret':secr},)
	dev.open()
	dev.load_merge_candidate(filename=filenm)
	diffs = dev.compare_config()
	if len(diffs)>0:
		return diffs
	else:
		return "No difference"


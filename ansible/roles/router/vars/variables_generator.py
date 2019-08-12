import csv
devices = {}
with open ("router_info.csv") as csvfile1:
        reader = csv.reader(csvfile1)
        for row in reader:
                if row != None:
                        if row[0] not in devices:
                                devices[row[0]] = [[row[1]+row[2],row[3],row[4],row[6]]]
                        else:      
                                devices[row[0]].append([row[1]+row[2],row[3],row[4],row[6]])
with open ("main.yml",'w') as fh:
	fh.write("---\n")
	fh.write("routers:")
	for key in devices:
		fh.write("\n   - hostname: "+key)
		count = 1
		for i in devices[key]:
			if "Loopback"in i[0]:
				fh.write("\n     LoopbackInterface: "+i[0])
				fh.write("\n     LoopbackIPAddress: "+i[1]+" "+i[2])
				fh.write("\n     net1: "+i[1]+" "+i[2])
			elif "198.51.100." in i[1]:
				fh.write("\n     net2: "+i[1]+" "+i[2])
				fh.write("\n     pID: "+i[3])
			else:
				fh.write("\n     Interface"+str(count)+": "+i[0])
				fh.write("\n     address"+str(count)+": "+i[1]+" "+i[2])
				fh.write("\n     net"+str(count+2)+": "+i[1]+" "+i[2])
				count += 1

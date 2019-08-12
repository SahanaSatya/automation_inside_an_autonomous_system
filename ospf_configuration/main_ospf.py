from flask import Flask,render_template, Markup,request
import sqlite3
import subprocess
from prettytable import PrettyTable
from sshInfo import *
from getconfig import *
from validateIP import *
from connectivity import *
from ospfconfig import *
from diffconfig import *
app=Flask(__name__)
@app.route('/')
def index():
	return render_template('home.html')

@app.route('/Getconfig')
def Get_conf():
	devices = parse_file("sshInfo.csv") 
	bodyTxt_str = ""
	for device in devices:
		host,filename = getConfig(device['driver_name'],device['ip'],device['username'],device['password'],device['secret'])
		bodyTxt_str  += "Device "+host+"'s configuration is saved in the configuration file:"+filename+"<br>"
	bodyText = Markup(bodyTxt_str)
	return render_template('getconfig.html',bodyText=bodyText)

@app.route('/OSPFconfig')
def OSPF_Config():
	db = sqlite3.connect('Configuration.sql')
	devices = parse_file("sshInfo.csv")
	bodyTxt_str = ""
	for device in devices:
                host = getHostname(device['driver_name'],device['ip'],device['username'],device['password'],device['secret'])
                bodyTxt_str  += "<p><a href='/ospf_cred/"+host+"'>Configure "+host+"</a></p>"
	bodyText = Markup(bodyTxt_str)
	return render_template('ospf_conf.html',bodyText=bodyText)


@app.route('/ospf_cred/<string:hostname>',methods=['GET','POST'])
def ospf_cred(hostname):
	db = sqlite3.connect('Configuration.sql')
	db.row_factory = sqlite3.Row
	query="drop table "+hostname
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	query="create table "+hostname+" (Serial_number int, ProcessID varchar(3), AreaID varchar(3), IP_Addr varchar(255), Wildcard_mask varchar(255));"
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	bodyText_str = "<form method=post action =/ospfConfigure/"+hostname+">"
	bodyText_str += "<h1>Login Credentials for "+hostname+":</h1>Username:<br><input type=text name = Username></input>"
	bodyText_str += "<br>Password:<br><input type=text name = Password></input>"
	bodyText_str += "<br>Secret:<br><input type=text name = Secret></input>"
	bodyText_str += "<br>Management_IP:<br><input type=text name = IP_address></input>"
	bodyText_str += "<h2>OSPF Information for "+hostname+":</h2>"
	cnt = 0
	if  "R1" in hostname or "R3" in hostname:
		cnt = 2
	else:
		cnt = 3	
	for i in range(cnt):
		bodyText_str += "<h3>Network "+str(i+1)+":</h3>"
		bodyText_str += "<br>OSPF Process ID:<br><input type=text name = ospf_pid"+str(i)+"></input>"
		bodyText_str += "<br>OSPF Area ID:<br><input type=text name = ospf_aid"+str(i)+"></input>"
		bodyText_str += "<br>IP address to advertise:<br><input type=text name = ospf_ip"+str(i)+"></input>"
		bodyText_str += "<br>Wildcard mask for the IP Address:<br><input type=text name = ospf_wm"+str(i)+"></input>"
	if cnt == 3:
		bodyText_str += "<br><h4>Interface for Load-Balancing:</h4><br><input type=text name = Loadbalancing_int></input>"
	bodyText_str += "<br><input type=submit name=submit value=submit></input></form>"
	bodyText = Markup(bodyText_str)
	return render_template('ospf_cred.html',bodyText=bodyText)


@app.route('/ospfConfigure/<string:hostname>',methods=['GET','POST'])
def ospf_configure(hostname):
	db = sqlite3.connect('Configuration.sql')
	db.row_factory = sqlite3.Row
	cnt = 0
	device = getDevicebyIP("sshInfo.csv",request.form['IP_address'])
	if device == None or device['username']!=request.form['Username'] or device['password'] != request.form['Password'] or device['secret'] != request.form['Secret']:
		bodyText = Markup("Invalid Login Credentials")
		return render_template('ospf_cred.html',bodyText = bodyText)
	if  "R1" in hostname or "R3" in hostname:
                cnt = 2
	else:
                cnt = 3
	for i in range(cnt):
		query ="INSERT INTO "+hostname+" (Serial_number, ProcessID, AreaID, IP_Addr, Wildcard_mask) VALUES ("+str(i)+","+request.form['ospf_pid'+str(i)]+","+request.form['ospf_aid'+str(i)]+",'"+request.form['ospf_ip'+str(i)]+"','"+request.form['ospf_wm'+str(i)]+"');"
		cursor = db.cursor()
		cursor.execute(query)
		db.commit()
	query = "Select * from "+hostname
	cursor = db.cursor()
	cursor.execute(query)
	table = PrettyTable(["Serial_number","Process ID","Area ID","IP Address", "Wildcard mask"])
	rows = cursor.fetchall()
	bodyTxt_str = "<table><caption>Login Verified!!!!Valid IP address and Wildcard mask configuration Info:</caption><tr><th>Serial Number</th><th>Process ID</th><th>Area ID</th><th>IP Address</th><th>Wildcard Mask</th></tr>"
	network_dict = {}
	for row in rows:
		if row:
			if isValid(row[3])=="yes" and isValid(row[4])=="yes":
					print(row[3])
					if row[1] not in network_dict:
						network_dict[row[1]] = []
					network_dict[row[1]].append({'aid':row[2],'ip':row[3],'wc':row[4]})
					table.add_row([row[0],row[1],row[2],row[3],row[4]])
					bodyTxt_str+="<tr><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td></tr>"
	for key in network_dict:
		try:
			OspfConfig(device['driver_name'],device['ip'],device['username'],device['password'],device['secret'],key,network_dict[key])
		except:
			pass
	bodyTxt_str += "</table>"
	print(table)
	if cnt == 3:
		try:
			lbconf(device['driver_name'],device['ip'],device['username'],device['password'],device['secret'],request.form['Loadbalancing_int'])
			bodyTxt_str+="Configured Load Balancing on interface"+request.form['Loadbalancing_int']
		except:
			pass
	bodyTxt_str += "<h3><a href=/verifyConn>Verify Connectivity</a>"
	bodyText = Markup(bodyTxt_str)
	return render_template('ospf_cred.html',bodyText=bodyText)

@app.route('/verifyConn',methods=['GET','POST'])
def verifyConn():
	bodyText_str = "<form method=post action =/results>"
	for i in range(4):
		bodyText_str += "<br>IP Address<br><input type=text name = ip_addr"+str(i)+"></input>"
	bodyText_str += "<br><input type=submit name=VerifyConnectivity value=submit></input></form>"
	bodyText = Markup(bodyText_str)
	return render_template('ospf_cred.html',bodyText=bodyText)

@app.route('/results',methods=['GET','POST'])
def results():
	bodyText_str = ""
	for i in range(4):
		bodyText_str += "<br>IP Address "
		ipv4 = request.form["ip_addr"+str(i)]
		if isValid(ipv4) == "yes":
			if is_connected(ipv4) == "yes":
				bodyText_str += ipv4+" is reachable"
			else:
				bodyText_str += ipv4+" is not reachable"
		else:
			bodyText_str += ipv4+" is invalid"
	bodyText = Markup(bodyText_str)
	return render_template('ospf_cred.html',bodyText=bodyText)

@app.route('/Diffconfig')
def Diffconfig():
	devices = parse_file("sshInfo.csv")
	body_Txt_str = ""
	for device in devices:
		hostname = getHostname(device['driver_name'],device['ip'],device['username'],device['password'],device['secret'])
		p = subprocess.check_output(["ls -la|grep "+hostname],shell=True)
		body_Txt_str +="<br>Comparing for"+hostname+" with file:"
		filenm = str(p).split('\\n')[-2].split()[-1]
		body_Txt_str +=filenm+"<br>"
		body_Txt_str +=diff(device['driver_name'],device['ip'],device['username'],device['password'],device['secret'], filenm)	
		print(body_Txt_str)
	bodyText = Markup(body_Txt_str)
	return render_template('diff_conf.html',bodyText=bodyText)
@app.route('/Migration')
def Migration():
	while True:
		if is_connected('172.16.1.1')!="yes":
			return render_template('diff_conf.html',bodyText=Markup("Migration Error: Traffic Loss"))
	#couldn't complete
	return render_template('diff_conf.html',bodyText=Markup("Migration completed Successfully"))
if __name__=='__main__':
    	app.debug = True
    	app.run(host='0.0.0.0',port=80)


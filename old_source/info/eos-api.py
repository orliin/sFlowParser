#!/usr/bin/env python

from jsonrpclib import Server
from devices import get_devices

devices = get_devices()
#devices = {
##        '10.10.0.99':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc'},
#        '10.10.0.41':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc'},
##        '10.10.0.42':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc'},
#        '10.10.0.43':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc'},
#        '10.10.0.11':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc'},
#        '10.10.0.12':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc'},
#}

backbone_ports = [
	'10.10.0.11-po2',
	'10.10.0.11-po3',
	'10.10.0.11-po4',
	'10.10.0.11-po5',

	'10.10.0.12-po2',

	'10.10.0.41-po4',
	'10.10.0.41-po6',
	'10.10.0.41-po8',

	'10.10.0.42-po8',

	'10.10.0.43-po6',
]

def getUnicastMacs(ip, user, password, macs):
	connectionString = "http://%s:%s@%s/command-api" % (user, password, ip)
	response = Server(connectionString).runCmds(version=1, cmds=["show mac address-table"])
	
#	macs = {}
	for item in response[0]["unicastTable"]["tableEntries"] :
		mac = item["macAddress"]
		vlan = item["vlanId"]
		port = "%s-%s" % (ip, item["interface"].replace('Port-Channel', 'po').replace('Ethernet', 'e'))
		
		## TODO: implement exclude parameter, that cpecifies ports, vlans, mac-addresses that should be excluded from the result
		if(port in backbone_ports): continue
		
		if(mac in macs.keys()):
			if(port in macs[mac].keys()):
				macs[mac][port] += [vlan]
			else:
				macs[mac][port] = [vlan]
		else:
			macs[mac] = {port:[vlan]}
#	return macs

###################################################################

macs = {}

for device in devices.keys() :
	ip = device
	user = devices[device]['user']
	password = devices[device]['password']
#	print ip, user, password
	print "Processing %s ..." % ip 
	getUnicastMacs(ip, user, password, macs)

for mac in macs:
    print mac, macs[mac]

print len(macs)

#!/usr/bin/env python

from jsonrpclib import Server

##
## Data structures
##

devices = {
	'10.10.0.11':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-telep-1',
		'ports': {
			'po2': {'type' : 'backbone'},
			'po3': {'type' : 'backbone'},
			'po4': {'type' : 'backbone'},
			'po5': {'type' : 'backbone'}
		}
	},
	'10.10.0.12':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-telep-2'},
	'10.10.0.13':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-telep-3'},
#	'10.10.0.21':{'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-kiev'},
	'10.10.0.31':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-ams'},
	'10.10.0.41':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'omnix-telep'},
	'10.10.0.42':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'omnix-datic'},
	'10.10.0.43':{
		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'omnix-3dc'},	
#	'10.10.0.51':{
#		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-bchrst'},
#	'10.10.0.61':{
#		'user':'httpapi', 'password':'dwZWTdPE3pfar7vc', 'name':'sc-lon'},	
}

##
## Methods
##
def get_devices():
	return devices

def get_ports():
	for ip in devices.keys():
		if(ip == '10.10.0.11'): continue #this is because the response format is text
		print '--------------- %s ------------------' % ip
		if('ports' not in devices[ip].keys()): devices[ip]['ports'] = {}
		user = devices[ip]['user']
		password = devices[ip]['password']
		response = Server("http://%s:%s@%s/command-api" % (user, password, ip)).runCmds(version=1, cmds=["show interfaces description"])
		response = response[0]['interfaceDescriptions']
		for interface in response.keys():
			if(interface[0] == 'E' or interface[0] == 'P'): 
#				print interface.replace('Port-Channel', 'po').replace('Ethernet', 'e'), response[interface]['description']
				iname = interface.replace('Port-Channel', 'po').replace('Ethernet', 'e')
				if(iname not in devices[ip]['ports'].keys()): devices[ip]['ports'][iname] = {}
				devices[ip]['ports'][iname]['description'] = response[interface]['description']

def get_vlans():
	for ip in devices.keys():
		#if(ip == '10.10.0.11'): continue #this is because the response format is text
		print '--------------- %s ------------------' % ip
		if('vlans' not in devices[ip].keys()): devices[ip]['vlans'] = {}
		user = devices[ip]['user']
		password = devices[ip]['password']
		response = Server("http://%s:%s@%s/command-api" % (user, password, ip)).runCmds(version=1, cmds=["show vlan"])
		print response[0]['vlans']
#		response = response[0]['interfaceDescriptions']

##
## Test code
##
get_ports()
get_vlans()
print get_devices()

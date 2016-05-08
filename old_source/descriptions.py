#!/usr/bin/python

#from quagga import get_quagga_data #gate, net, asn
import re
#from routes_list import routes

##
## Global constants
##
unknown = 'unknown'

agent_description_map = {
	'10.10.0.11':
	{
		'description':'sc-telep-1',
	},
	'10.0.7.7': 
	{
		'description':'sc-telep-1',
	},
	'212.5.50.7': 
	{
		'description':'sc-telep-1',
	},

	'10.10.0.12':
	{
		'description':'sc-telep-2',
	},
	'10.0.7.8': 
	{
		'description':'sc-telep-2',
	},

	'10.10.0.21':
	{
		'description':'sc-kiev-1',
	},
	'10.10.0.31':
	{
		'description':'omn-ams-1',
	},
	'10.10.0.41':
	{
		'description':'omn-telep-1',
	},
	'10.10.0.42':
	{
		'description':'omn-datic-1',
	},
	'10.10.0.43':
	{
		'description':'omn-3dc-1',
	}
}

vlan_description_map = {
'1' : 'default',
'3' : 'IP_Backbone_VLAN_B-IX',
'4' : 'b-ix',
'5' : 'IP_Servers_VLAN_B-IX',
'6' : 'Inband_MGMT_VLAN_B-IX',
'7' : 'om-nix-mgmt',
'10' : 'test-router-port-2',
'12' : 'DTEL-mgmt-UA',
'14' : 'b-ix-infra',
'15' : 'b-ix-infra-peer',
'33' : 'novatel-gcn',
'34' : 'he.com',
'44' : 'OM-NIX',
'101' : 'he-via-gcn',
'190' : 'Ucom-via-caucasus',
'280' : 'vivacom-internet',
'300' : 'cogent-internet',
'302' : 'mts',
'303' : 'google',
'305' : 'bulgartel-internet',
'350' : '3tcom',
'400' : 'ROSTELECOM',
'401' : 'GREEK-IX',
'402' : 'INTEROUTE',
'493' : 'novatel-int',
'600' : 'SC-int-to-omnix',
'602' : 'APOSTOLIS-GREEK',
'603' : 'banda',
'604' : 'CUST-001',
'605' : 'sirius',
'606' : 'Yannis',
'607' : 'dream-connect',
'609' : 'Intelsoft',
'610' : 'HristosGR',
'611' : 'Toli',
'612' : 'Giorgi-gConnect',
'613' : 'GTT-Watershed-marketing',
'614' : 'inteliquent-via-bulgartel',
'615' : 'ams-ix-all-to-bulgartel',
'617' : 'dream-connect-bg',
'618' : 'arena-grader',
'670' : 'gcn-int',
'671' : 'gcn-bg',
'677' : 'gcn-cust',
'701' : 'balkanix-AMS-IX',
'702' : 'delta-AMS-IX',
'709' : 'telehouse-AMS-IX',
'712' : 'novatel-AMS-IX',
'713' : 'mtel-AMS-IX',
'715' : 'ams-ix-sofia-connect',
'716' : 'gcn-AMS-IX',
'717' : 'ams-ix-sofia-connect-2',
'720' : '3DC',
'761' : 'DecisionMarketing',
'762' : 'NTT-Netguard',
'763' : 'NTT-internet',
'777' : 'DTEL-Kiev-UA',
'778' : 'DATAIX-Moscow-RU',
'800' : 'euroloop',
'901' : 'CO.ge',
'923' : 'sofcon-kukush',
'950' : 'bulgartel-caucasus-armenia',
'951' : 'Level3-internet',
'1000' : 'VLAN1000',
'1011' : 'ITSystems-via-DTEL-IX',
'1035' : 'sofcon-datic',
'1038' : 'onlinedirect-AMS-IX',
'1111' : 'sof-con',
'1214' : 'sestrimo',
'1231' : 'teleh-int',
'1344' : 'delta-AMS-IX',
'1397' : 'fiord',
'1416' : 'misho-balchik',
'1417' : 'misho-balchik-bg',
'1489' : 'gcn-multicast',
'1499' : 'telehouse-internet',
'1531' : 'teleh-',
'2001' : 'omnix-gcn-Skopie',
'2008' : 'petrich-gcn-Yannis',
'2518' : 'ams-ix-2-monitoring',
'2550' : 'opticcom-bulgartel',
'2910' : 'opticom-gcn',
'3115' : 'vestitel-gcn',
'3116' : 'interoute-via-gcn',
'3117' : 'kandreevo-via-gcn',
'3180' : 'networx-tv-stream',
'3181' : 'gcn-tv-stream',
'3572' : 'vivacom-caucasus-Kapan',
'3739' : 'setservice.bg',
}

ip_description_map = {
'195.69.144.255':'ams-ix-route-server',
'195.69.144.80':'datagroup-ua',
'195.69.145.20':'mikrosoft',
'195.69.145.21':'mikrosoft',
'195.69.146.140':'forthnet-gr',
'195.69.146.198':'ams-ix-booking.com',
'195.69.145.150':'ams-ix-all',
'195.69.147.45':'ams-ix-liquidtelecom.com',
'195.69.144.189':'ams-ix-openpeering.nl',
'195.69.147.155':'ams-ix-colocationix',
'195.69.145.1':'ams-ix',
'195.69.147.12':'ams-ix-wnet.ua',
'195.69.145.197':'ams-ix-openpeering.nl',
'195.69.146.31':'hgc',
'195.69.145.208':'ams-ix-akamai.com',
'195.69.147.84':'ams-ix-rascom.ru',
'80.249.209.0':'ams-ix',
'80.249.208.255':'ams-ix',
'80.249.208.1':'ams-ix',
'80.249.208.80':'datagroup-ua',
'80.249.209.20':'microsoft',
'80.249.209.21':'microsoft',
'80.249.210.140':'forthnet-gr',
'80.249.210.198':'booking.com',
'80.249.209.150':'he',
'80.249.211.45':'liquidtelecom',
'80.249.208.189':'openpeering.nl',
'80.249.211.155':'collocation-ix',
'80.249.209.1':'ams-ix',
'80.249.211.12':'wnet.ua',
'80.249.209.197':'openpeering.nl',
'80.249.210.31':'hgc',
'80.249.209.208':'akamai.com',
'80.249.211.84':'rascom',
'80.249.210.150':'wargaming',
'80.249.210.152':'wargaming',
'80.249.210.135':'ip-max',
'149.6.68.153':'cogent',
'216.66.83.117':'he.com',
'77.85.193.233':'vivacom',
'213.133.172.33':'itsys-ua',
'95.169.219.57':'bulgartel-inteliquenst',
'109.160.1.25':'gcn-int',
'213.24.114.29':'rostelecom',
'212.162.46.193':'level3-int',
'83.217.227.41':'ntt',
'212.5.48.62':'daticum',
'185.44.116.50':'dream-trichkov',
'185.44.116.170':'naicom3dc',
'185.44.116.42':'lafi-balchik',
'185.44.116.174':'asnicom-3dc',
'91.212.235.1':'balkanix',
'185.44.116.18':'caucasus-ix',
'185.1.30.254':'balkanix2-new',
'185.1.30.1':'balkanix-new',
'185.44.116.226':'euroloop',
'91.212.235.9':'balkan-ix-he.com',
'109.160.0.233':'gcn-bg',
'185.44.116.38':'dream-trichkov-bg',
'193.25.180.255':'dtel-ix',
'193.25.181.0':'dtel-ix',
'178.18.230.200':'data-ix',
'178.18.230.100':'data-ix',
'194.183.113.233':'interoute-euro-ix',
'185.44.116.162':'ucom',
'185.44.116.163':'ucom'#,
}

own_net_map = {
'10.9.23.1/24':'SC-siemens-telepoint',
'77.85.193.234/30':'vivacom-int',
'80.249.211.76/21':'ams-ix-715',
'83.217.227.42/30':'NTT',
'91.212.235.11/24':'balkanix',
'95.169.219.58/30':'inteliquent-via-bulgartel',
'109.160.0.234/30':'gcn-bg',
'109.160.1.26/30':'gcn-int',
'149.6.68.154/30':'Cogent',
'178.18.230.103/24':'DATA-IX-RU',
'185.1.30.11/24':'balkanix',
'185.44.116.1/28':'SC-siemens-telepoint',
'185.44.116.17/30':'caucasus-ix',
'185.44.116.33/30':'BePro-Sestrimo-via-vivacom',
'185.44.116.37/30':'dream-trichkov-bg',
'185.44.116.41/30':'lafi-balchik',
'185.44.116.49/30':'dream-trichkov-int',
'185.44.116.53/30':'bulgartel-amsix',
'185.44.116.57/29':'gtt-client',
'185.44.116.64/26':'g-connect',
'185.44.116.128/27':'gtt-client',
'185.44.116.161/29':'Ucom-via-co.ge-cust',
'185.44.116.169/30':'naicom-via-gcn',
'185.44.116.173/30':'naicom-via-gcn',
'185.44.116.227/27':'SC-siemens-telepoint',
'185.44.117.64/26':'g-connect',
'185.44.119.78/29':'CUST-001',
'185.44.119.81/30':'apostolis',
'193.25.181.6/23':'dtel-ix-ua',
'194.183.113.234/30':'interoute',
'195.69.147.76/22':'ams-ix-715',
'195.69.147.197/22':'ams-ix-717',
'212.5.48.17/28':'SC-siemens-telepoint',
'212.5.48.33/29':'sirius',
'212.5.48.49/29':'cpay',
'212.5.48.57/30':'g-connect',
'212.5.48.61/30':'daticum',
'212.5.48.65/30':'bandacom',
'212.5.48.97/27':'hristos-gr',
'212.5.48.225/29':'yannis-jonni',
'212.5.49.1/24':'sysmasters',
'212.5.50.1/27':'yalamov',
'212.5.50.128/27':'bandacom',
'212.162.46.194/30':'level3-int',
'213.24.114.30/30':'rostelecom',
'213.133.172.34/30':'its-ua-int',
'216.66.83.118/30':'he.com'#,
}

# TODO : da se opravi tazi boza :)
def describe(key, value) :
	if(key == 'agent') :
		return agent_description_map[value]['description']
	return value


def describe_agent(agent) :
	if(agent in agent_description_map) : 
		if('description' in agent_description_map[agent]) :
			return agent_description_map[agent]['description']
	return agent

def describe_port(agent, port) :
	if(agent in agent_description_map) : 
		if('ports' in agent_description_map[agent]) :
			if(port in agent_description_map[agent]['ports']) :
#				if('description' in  agent_description_map[agent][port]) :
				return agent_description_map[agent]['ports'][port]#['description']
	return port

def describe_vlan(vlan) :
	if(vlan in vlan_description_map) : 
#		if('description' in vlan_description_map[vlan]) :
		return vlan+'-'+vlan_description_map[vlan]#['description']
	return vlan

def describe_mac(mac) :
	return mac

def ip_to_bin(ip) :
	list = ip.split('.')
#	if(len(list)!=4) : return 0
	ip_bin = ''# '.'.join(net_ip) + ":\t";
	for num in list :
		ip_bin += format(int(num), "08b")
	return ip_bin

def describe_ip(ip) :
	if ip_description_map.has_key(ip) :
		return ip_description_map[ip]
	
# if not found in ip_description_map
	ip_bin = ip_to_bin(ip)

	for key in own_net_map :
		split1 = key.split("/")
		net_bin = ip_to_bin(split1[0])
		net_mask = int(split1[1])
		if net_bin[:net_mask]==ip_bin[:net_mask] :
			return own_net_map[key]

# change this to binary search method
	gate = 'undefined'#get_gate(ip_bin)

	pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
	if not pat.match(gate) : return gate
# if not found in own_net_map
#	gate, net, asn = get_quagga_data(ip)
	if ip_description_map.has_key(gate) :
		return 'gate-'+ip_description_map[gate]	

# if gate not found, check if gate net is on known nets
	gate_bin = ip_to_bin(gate)
	for key in own_net_map :
		split1 = key.split("/")
		net_bin = ip_to_bin(split1[0])
		net_mask = int(split1[1])
		if net_bin[:net_mask]==gate_bin[:net_mask] :
			return 'gate-'+own_net_map[key]

	
	if gate != "" : return 'gate-'+gate	

	return ip

#def get_gate(ip_bin) :
#	for index in range(0,len(routes)) :
#		net_mask = int(routes[index][1])
##		print routes[index][0], ip_bin
#		if routes[index][0][:net_mask]==ip_bin[:net_mask] :
#			return  routes[index][3]
#	
#	return ''


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_gate(ip_bin) :
	left = 0
	right = len(routes)-1
	index = 0

	while right != left :
		index = (right+left)/2
		net_mask = int(routes[index][1])
		
#		print left, index, right, routes[index], routes[index][0][:net_mask], ip_bin[:net_mask], int(routes[index][0][0:8],2), int(routes[index][0][8:16],2), int(routes[index][0][16:24],2), int(routes[index][0][24:32],2)
		
		
		if routes[index][0][:net_mask]>=ip_bin[:net_mask] :
			right = index
		else :
			left = index+1
	
#	print left, index, right, routes[index], routes[index][0][:net_mask], ip_bin[:net_mask], int(routes[index][0][0:8],2), int(routes[index][0][8:16],2), int(routes[index][0][16:24],2), int(routes[index][0][24:32],2)
	return routes[left][3]



print describe_ip('185.44.116.4') #SC-siemens-telepoint
print describe_ip('195.69.145.20') #microsoft
print describe_ip('1.2.3.4') #unknown

print describe_ip('192.95.15.192')
print describe_ip('5.79.73.114')
print describe_ip('37.48.81.205')
print describe_ip('79.124.14.37')
print describe_ip('94.190.230.209')
print describe_ip('109.108.65.100')

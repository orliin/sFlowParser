#!/usr/bin/python

from descriptions import describe_agent
from descriptions import describe_port
from descriptions import describe_vlan
from descriptions import describe_mac
from descriptions import describe_ip
from rrd_manipulator import update_rrd

##
## Global constants
##
#sflow_datagram_fields = 'agent', 'startDatagram', 'endDatagram', 'unixSecondsUTC', 'meanSkipCount',
sflow_sample_fields = 'sampleType', 'inputPort', 'outputPort', 'in_vlan', 'out_vlan', 'srcMAC', 'dstMAC', 'srcIP', 'dstIP'#, 'startSample', 'endSample', 'sampledPacketSize',
mac_addresses = {}
datasource_names = {'input', 'output', 'traffic'}
debug = 0
info = 0
RRDpath = '/var/lib/sflow' #'/home/orliin/sflow'

##
## Global variables
##
datagram = {'unixSecondsUTC':0}
sample = {}
counters = {}
newSecond = 1

##
## Functions
##
def updateCounters() :
	if debug : 
		print "Update counters"
		print "sample:", sample

	dataSize = sample['sampledPacketSize'] * datagram['meanSkipCount'];	

	if debug: print "sample:", sample

	agent = describe_agent(datagram['agent']);
	if(not agent in counters) : counters[agent] = {};

	inputPort = describe_port(datagram['agent'], sample['inputPort'])
	outputPort = describe_port(datagram['agent'], sample['outputPort'])
	if(not 'ports' in counters[agent]) : counters[agent]['ports'] = {}
	if(not inputPort in counters[agent]['ports']) : counters[agent]['ports'][inputPort] = {'input':0, 'output':0}
	if(not outputPort in counters[agent]['ports']) : counters[agent]['ports'][outputPort] = {'input':0, 'output':0}
	
	in_vlan = describe_vlan(sample['in_vlan'])
	out_vlan = describe_vlan(sample['out_vlan'])
	if(not 'vlans' in counters[agent]['ports'][inputPort]) : counters[agent]['ports'][inputPort]['vlans'] = {}
	if(not in_vlan in counters[agent]['ports'][inputPort]['vlans']) : counters[agent]['ports'][inputPort]['vlans'][in_vlan] = {'input':0, 'output':0}
	if(not 'vlans' in counters[agent]['ports'][outputPort]) : counters[agent]['ports'][outputPort]['vlans'] = {}
	if(not out_vlan in counters[agent]['ports'][outputPort]['vlans']) : counters[agent]['ports'][outputPort]['vlans'][out_vlan] = {'input':0, 'output':0}

	srcMAC = describe_mac(sample['srcMAC'])
	dstMAC = describe_mac(sample['dstMAC'])

	if('srcIP' in sample) :
		srcIP = describe_ip(sample['srcIP'])
	else :
#		print sample
		srcIP = 'noIP'
	if('dstIP' in sample) :
		dstIP = describe_ip(sample['dstIP'])
	else :
#		if('srcIP' in sample) : print sample
		dstIP = 'noIP'

	flow = srcIP+':'+dstIP
#	if(not 'vlans' in counters[agent]) : counters[agent]['vlans'] = {}
#	if(not in_vlan in counters[agent]['vlans']) : counters[agent]['vlans'][in_vlan] = {}
#	if(not 'flows' in counters[agent]['vlans'][in_vlan]) : counters[agent]['vlans'][in_vlan]['flows'] = {}
#	if(not flow in counters[agent]['vlans'][in_vlan]['flows']) : counters[agent]['vlans'][in_vlan]['flows'][flow] = {'traffic' : 0}
	
	
	#inputPort / outputPort - all ports graphs - sflow/{agent}/ports/{all port graphs}
	counters[agent]['ports'][inputPort]['input'] += dataSize
	counters[agent]['ports'][outputPort]['output'] += dataSize

	#in_vlan / out_vlan - all vlan to all ports? - sflow/{agent}/vlans/{vlan}/{all port graphs for this vlan}
	counters[agent]['ports'][inputPort]['vlans'][in_vlan]['input'] += dataSize
	counters[agent]['ports'][outputPort]['vlans'][out_vlan]['output'] += dataSize
	
	#srcMAC / dstMAC - list of MAC addresses to all ports? - sflow/{agent}/macs/{mac}/{all port graphs for this mac}
	if(mac_addresses.has_key(srcMAC)) : 
		if(not 'macs' in counters[agent]['ports'][inputPort]) : counters[agent]['ports'][inputPort]['macs'] = {}
		if(not srcMAC in counters[agent]['ports'][inputPort]['macs']) : counters[agent]['ports'][inputPort]['macs'][srcMAC] = {'input':0, 'output':0}
		counters[agent]['ports'][inputPort]['macs'][srcMAC]['input'] += dataSize

	if(mac_addresses.has_key(dstMAC)) : 
		if(not 'macs' in counters[agent]['ports'][outputPort]) : counters[agent]['ports'][outputPort]['macs'] = {}
		if(not dstMAC in counters[agent]['ports'][outputPort]['macs']) : counters[agent]['ports'][outputPort]['macs'][dstMAC] = {'input':0, 'output':0}
		counters[agent]['ports'][outputPort]['macs'][dstMAC]['output'] += dataSize
	
	#srcIP / dstIP - all ip, translated into neighbour/client networks - sflow/{agent}/ips/{neighbour}/{all single flows}
#	counters[agent]['vlans'][in_vlan]['flows'][flow]['traffic'] += dataSize
	
	return

def exportMap(map, path) :
	data = {}
	if debug : print "Clear counters map:", map

	if info :
		for ds_name in datasource_names :
			if map.has_key(ds_name) : print path, ds_name, map[ds_name]
	for key in map :
		if(key in datasource_names) :
			data[key] = map[key]
			map[key] = 0
		else :
			exportMap(map[key], path+'/'+key)
	if (data != {}) : 
		keys = path[len(RRDpath)+1:].split('/')
		filename = keys[0]+'.rrd'
		
		for index in range(0,(len(keys)-1)/2) :
			filename = keys[(index*2)+1]+'.'+keys[(index*2)+2]+'#'+filename
	
		if 'traffic' in data : 
			filename = 'tr#'+filename
		else :
			filename = 'io#'+filename
		update_rrd(path+'/', filename, data, datagram['unixSecondsUTC'])
	return


##
## Main script:
##

print "/home/orliin/programming/sflow.py: Let the show begin!";

## Reading of flow data
while(1) :
	line = raw_input()
	key = line.split()[0]
	value = line.split()[1]

	if debug : print key, value
## Reading datagram fields
	if(key == 'startDatagram') :
		# new datagram - clear all info except unixSecondsUTC
		datagram = {'unixSecondsUTC' : datagram['unixSecondsUTC']}

	elif(key == 'unixSecondsUTC' and datagram['unixSecondsUTC'] != long(value) and (long(value)%10 == 0)) :
		# time of datagram - mark that a second has passed
		newSecond = 1
		datagram[key] = long(value)

	elif(key == 'meanSkipCount') :
		# statistical data (packet size and count) should be multiplied by this number
		datagram['meanSkipCount'] = long(value)

	elif(key == 'agent') :
		# get agent trasmitting the datagram
		datagram[key] = value

	elif(key == 'endDatagram' and newSecond) :
		if(datagram['unixSecondsUTC']!=0) :
			exportMap(counters,RRDpath)
			newSecond = 0

## Reading sample fields
	elif(key == 'startSample') :
		# new sample - clear previous info
		sample.clear()

	elif(key == 'endSample') :
		# at the end of a sample we should check filters this sample matches and update corresponding counters
		if(sample['sampleType'] == 'FLOWSAMPLE') : updateCounters() 

	elif(key == 'sampledPacketSize') :
		# get the size of the packet to add it to counters. Multiply by 8 to get in bits
		sample[key] = (long(value) * 8)

	elif(key in sflow_sample_fields) :
		# fill in sample fields
		sample[key] = value



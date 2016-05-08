#!/usr/bin/python

import os
#import re
#import sys
import time
import rrdtool
#import subprocess

def update_rrd(path, filename, data, timestamp) :
#	print 'path:\t', path
#	print 'filename:\t', filename
#	print 'data:\t', data

	file = path + filename
#	print 'file:\t', file
	if(not os.path.exists(file)) : create_rrd(path, filename, data, timestamp)

	if(filename[:2] == 'tr') :
		rrdtool.update(file, '%s:%s' % (timestamp, data['traffic']))
	elif(filename[:2] == 'io'):
		rrdtool.update(file, '%s:%s:%s' % (timestamp, data['input'], data['output']))

	return

def create_rrd(path, filename, data, timestamp) :
	file = path + filename
	if(not os.path.exists(path)) :
		os.makedirs(path)

	params = [file, '--start', '0', '--step', '1']
#str(int(time.time())-3)
	if(filename[:2] == 'tr') :
		params += ['DS:traffic:ABSOLUTE:600:U:U']
	elif(filename[:2] == 'io'):
		params += ['DS:input:ABSOLUTE:600:U:U', 'DS:output:ABSOLUTE:600:U:U']
	params += [
#Minute (1 Second "Average")	every second(1s) for a minute(1m = 60s = 1s * 60times)
				'RRA:AVERAGE:0.5:1:60',
				'RRA:MAX:0.5:1:60',
				'RRA:MIN:0.5:1:60',
#Hourly (1 Minute Average)	every minute(60s) for an hour(1h = 3600s = 60s * 60times)
				'RRA:AVERAGE:0.5:60:60',
				'RRA:MAX:0.5:60:60',
				'RRA:MIN:0.5:60:60',
#Daily (5 Minute Average)	every 5 minutes(300s) for a day(1d = 86400s = 300s * 288times)
				'RRA:AVERAGE:0.5:300:288',
				'RRA:MAX:0.5:300:288',
				'RRA:MIN:0.5:300:288',
#Weekly (30 Minute Average)	every 30 minutes(1800s) for a week(1w = 604800s = 1800s * 336times)
				'RRA:AVERAGE:0.5:1800:336',
				'RRA:MAX:0.5:1800:336',
				'RRA:MIN:0.5:1800:336',
#Monthly (10 Minute Average)	every 10 minutes(600s) for a month(1m = 2678400s = 600s * 4464times)
				'RRA:AVERAGE:0.5:600:4464',
				'RRA:MAX:0.5:600:4464',
				'RRA:MIN:0.5:600:4464',
#Yearly (1 Day Average)		every day(86400s) for a year(1y = 31536000s = 86400s * 365times)
				'RRA:AVERAGE:0.5:86400:365',
				'RRA:MAX:0.5:86400:365',
				'RRA:MIN:0.5:86400:365']
#	print params
	rrdtool.create(params)
# file,
#				'--start', str(int(time.time())-2),
#				'--step', '1',                  #one second granularity
# TODO: change data source name to include description (change conf file first)
#				'DS:%s%s:ABSOLUTE:600:U:U' % (line[1][0], line[1][1]),
#				'DS:%s%s:ABSOLUTE:600:U:U' % (line[2][0], line[2][1]),
#				'DS:input:ABSOLUTE:600:U:U',
#				'DS:output:ABSOLUTE:600:U:U',

	return

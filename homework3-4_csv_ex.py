#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

import csv
import re 

csvfile = open('beijing_jt.csv','r')

reader = csv.reader(csvfile)
next(reader)

result={}

while True:
	try:
		jt_info = next(reader)
	except:
		break

	print jt_info[1].decode('utf-8')

	# convert stations info format
	station_pattern = (r'(?P<number>[0-9]+)\s(?P<name>\D+)')
	station_list = []

	stations = re.findall(station_pattern,jt_info[-1].decode('utf-8')) 
	for tmp in stations:
	    #print tmp[0],tmp[1].strip()
	    station_list.append(tmp[1].strip())
	    
	
	result[jt_info[1]]=station_list


csvfile.close()


while True:
	print u"请输入你想要查询的站名："
	find_station=raw_input()
	try:
		s_in = unicode(find_station,'utf-8')
	except:
		s_in = unicode(find_station, 'gbk')

	for k,v in result.iteritems():
		for station_name in v:
			if s_in in station_name:
				print unicode(k,'utf-8'),station_name

print result    
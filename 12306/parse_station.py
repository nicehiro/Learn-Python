# coding: utf-8

import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'

url2 = "http://nicehiro.org"
text = requests.get(url, verify=False)
stations = re.findall(b'([A-Z]+)\|([a-z]+)', text.content)
stations = dict(stations)
stations = dict(zip(stations.values(), stations.keys()))
pprint(stations, indent=4)

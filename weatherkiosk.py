#!/usr/bin/python

import requests
import json
from pprint import pprint

url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
response = requests.get(url, headers=headers)

rdata = response.text
jdata = json.loads(rdata)

# print(type(jdata))
# print(jdata)

print(jdata['properties']['meta'])

print(jdata['properties']['timeseries'][1])

print(jdata['properties']['timeseries'][1]['time'])
print(jdata['properties']['timeseries'][1]['data']['instant']['details']['air_temperature'])



# print(response.text)
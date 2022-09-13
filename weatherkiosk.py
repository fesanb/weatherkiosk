#!/usr/bin/python

import requests
import json

import tkinter


url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
response = requests.get(url, headers=headers)

rdata = response.text
jdata = json.loads(rdata)

# print(type(jdata))
# print(jdata)

# print(jdata['properties']['meta'])

# print(jdata['properties']['timeseries'][1])




# print(jdata['properties']['timeseries'][1]['time'])
# print(jdata['properties']['timeseries'][1]['data']['instant']['details']['air_temperature'])
# print(jdata['properties']['timeseries'][1]['data']['instant']['details']['wind_speed'])
# print(jdata['properties']['timeseries'][1]['data']['next_1_hours']['summary']['symbol_code'])
# print(jdata['properties']['timeseries'][1]['data']['next_1_hours']['details']['precipitation_amount'])

times = 24
ts = 0

while ts < times:
    path_time = jdata['properties']['timeseries'][ts]['time']
    path_temp = jdata['properties']['timeseries'][ts]['data']['instant']['details']['air_temperature']
    path_wind = jdata['properties']['timeseries'][ts]['data']['instant']['details']['wind_speed']
    path_rain = jdata['properties']['timeseries'][ts]['data']['next_1_hours']['details']['precipitation_amount']
    path_symbol = jdata['properties']['timeseries'][ts]['data']['next_1_hours']['summary']['symbol_code']

    print(path_time, path_temp, path_temp, path_wind, path_rain, path_symbol)
    ts += 1

win=tkinter.Tk() #creating the main window and storing the window object in 'win'
win.geometry('500x200') #setting the size of the window
win.title('WeatherKiosk') #setting title of the window
win.mainloop() #running the loop that works as a trigger

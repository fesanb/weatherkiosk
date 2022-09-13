#!/usr/bin/python

import requests
import json

from tkinter import *


url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
response = requests.get(url, headers=headers)

rdata = response.text
jdata = json.loads(rdata)


def fetch_weather(wid):

    time = str(jdata['properties']['timeseries'][wid]['time'])
    temp = str(jdata['properties']['timeseries'][wid]['data']['instant']['details']['air_temperature'])
    wind = str(jdata['properties']['timeseries'][wid]['data']['instant']['details']['wind_speed'])
    rain = str(jdata['properties']['timeseries'][wid]['data']['next_1_hours']['details']['precipitation_amount'])
    symbol = str(jdata['properties']['timeseries'][wid]['data']['next_1_hours']['summary']['symbol_code'])

    cleantime = time[11:16]

    return cleantime, temp, wind, rain, symbol



print(fetch_weather(1)[0])

win = Tk() #creating the main window and storing the window object in 'win'
win.geometry('500x200') #setting the size of the window
win.title('WeatherKiosk') #setting title of the window

wl0 = Label(win, text=fetch_weather(1)[0])
wl1 = Label(win, text=fetch_weather(1)[1])
wl2 = Label(win, text=fetch_weather(1)[2])
wl3 = Label(win, text=fetch_weather(1)[3])
wl4 = Label(win, text=fetch_weather(1)[4])

wl0.grid(row=0, column=0)
wl1.grid(row=0, column=1)
wl2.grid(row=0, column=2)
wl3.grid(row=0, column=3)
wl4.grid(row=0, column=4)



win.mainloop() #running the loop that works as a trigger

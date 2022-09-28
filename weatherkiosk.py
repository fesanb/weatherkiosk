#!/usr/bin/python

import requests
import json
import time

from tkinter import *
from PIL import ImageTk, Image
import os

weather_list = 20


weather_url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
weather_header = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
weather_response = requests.get(weather_url, headers=weather_header)

weather_rdata = weather_response.text
weather_jdata = json.loads(weather_rdata)


# list of variants
variants_url = "https://api.met.no/weatherapi/weathericon/2.0/legends"
variants_headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
variants_response = requests.get(variants_url, headers=variants_headers)

variants_rdata = variants_response.text
variants_jdata = json.loads(variants_rdata)

print(variants_jdata)
print(variants_jdata["clearsky"])

def fetch_weather(wid):

    time = str(weather_jdata['properties']['timeseries'][wid]['time'])
    temp = str(weather_jdata['properties']['timeseries'][wid]['data']['instant']['details']['air_temperature'])
    wind = str(weather_jdata['properties']['timeseries'][wid]['data']['instant']['details']['wind_speed'])
    rain = str(weather_jdata['properties']['timeseries'][wid]['data']['next_1_hours']['details']['precipitation_amount'])
    symbol = str(weather_jdata['properties']['timeseries'][wid]['data']['next_1_hours']['summary']['symbol_code'])

    cleantime = time[11:16]

    return cleantime, temp, wind, rain, symbol


def fetch_symbols():
    isymb = 0
    weather_code = []

    while isymb < weather_list:
        weather_code.append(str(weather_jdata['properties']['timeseries'][isymb]['data']['next_1_hours']['summary']['symbol_code']))
        isymb += 1

    weather_code_red1 = [*set(weather_code)]
    print(weather_code_red1)

    isymb = 0
    weather_code_red2 = []

    for x in weather_code_red1:
        #print(weather_code_red1[isymb])
        if "_" in weather_code_red1[isymb]:
            a = weather_code_red1[isymb].split("_")
            weather_code_red2.append(a[0])
        else:
            a = weather_code_red1[isymb]
            weather_code_red2.append(a)

        isymb += 1
    weather_code_red2 = [*set(weather_code_red2)]
    print(weather_code_red2)

    isymb = 0
    weather_dict = {}
    for x in weather_code_red2:
        weather_dict[weather_code_red2[isymb]] = variants_jdata[weather_code_red2[isymb]]
        isymb += 1


    isymb = 0
    images = {}
    for x in weather_code_red2:
        if len(weather_dict[weather_code_red2[isymb]]['old_id']) == 1:
            name = "0" +  weather_dict[weather_code_red2[isymb]]['old_id']
        else:
            name =  weather_dict[weather_code_red2[isymb]]['old_id']



        print(weather_code_red2[isymb], " ", name)
        #images[weather_code_red2[isymb]] = weather_dict[weather_code_red2[isymb]]['old_id']

        isymb += 1

fetch_symbols()


win = Tk() #creating the main window and storing the window object in 'win'
win.geometry('500x200') #setting the size of the window
win.title('WeatherKiosk') #setting title of the window
win.geometry("720x480")

h0 = Label(win, text="TID")
h1 = Label(win, text="Temperatur")
h2 = Label(win, text="Vind")
h3 = Label(win, text="Regn")
h4 = Label(win, text="Info")
h5 = Label(win, text="ICON")

h0.grid(row=0, column=0)
h1.grid(row=0, column=1)
h2.grid(row=0, column=2)
h3.grid(row=0, column=3)
h4.grid(row=0, column=4)
h5.grid(row=0, column=5)

win.columnconfigure(0, minsize=100)
win.columnconfigure(1, minsize=100)
win.columnconfigure(2, minsize=100)
win.columnconfigure(3, minsize=100)
win.columnconfigure(4, minsize=100)
win.columnconfigure(5, minsize=100)


def pick_img(code):
    if code == 18:
        img = "w-img/03n.png"
    elif code == 19:
        img = "w-img/03d.png"
    else:
        img = "w-img/03d.png"

    return img

row = 1
timeseri = 0
i = 1

while i < weather_list:
    wl0 = Label(win, text="kl " + fetch_weather(timeseri)[0])
    wl1 = Label(win, text=fetch_weather(timeseri)[1] + " °C")
    wl2 = Label(win, text=fetch_weather(timeseri)[2] + " m/s")
    wl3 = Label(win, text=fetch_weather(timeseri)[3] + " mm")
    wl4 = Label(win, text=fetch_weather(timeseri)[4])

    img = ImageTk.PhotoImage(Image.open(pick_img(i)))
    wl5 = Label(win, image=img)

    wl0.grid(row=row, column=0)
    wl1.grid(row=row, column=1)
    wl2.grid(row=row, column=2)
    wl3.grid(row=row, column=3)
    wl4.grid(row=row, column=4)
    wl5.grid(row=row, column=5)

    row += 1
    timeseri += 1
    i += 1


win.mainloop() #running the loop that works as a trigger

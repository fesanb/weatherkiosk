#!/usr/bin/python

import requests
import json
import time

from tkinter import *

from PIL import ImageTk, Image
import os

weather_list = 20


url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
response = requests.get(url, headers=headers)

rdata = response.text
jdata = json.loads(rdata)

partlycloudy_night = "03n.png"

symbols = [
["clearsky", "01"],
["cloudy", "04"],
["fair", "02"],
["fog", "15"],
["heavyrain", "10"],
["heavyrainandthunder", "11"],
["heavyrainshowers", "41"],
["heavyrainshowersandthunder", "25"],
["heavysleet", "48"],
["heavysleetandthunder", "32"],
["heavysleetshowers", "43"],
["heavysleetshowersandthunder", "27"],
["heavysnow", "50"],
["heavysnowandthunder", "34"],
["heavysnowshowers", "45"],
["heavysnowshowersandthunder", "29"],
["lightrain", "46"],
["lightrainandthunder", "30"],
["lightrainshowers", "40"],
["lightrainshowersandthunder", "24"],
["lightsleet", "47"],
["lightsleetandthunder", "31"],
["lightsleetshowers", "42"],
["lightsnow", "49"],
["lightsnowandthunder", "33"],
["lightsnowshowers", "44"],
["lightssleetshowersandthunder", "26"],
["lightssnowshowersandthunder", "28"],
["partlycloudy", "03"],
["rain", "09"],
["rainandthunder", "22"],
["rainshowers", "05"],
["rainshowersandthunder", "06"],
["sleet", "12"],
["sleetandthunder", "23"],
["sleetshowers", "07"],
["sleetshowersandthunder", "20"],
["snow", "13"],
["snowandthunder", "14"],
["snowshowers", "08"],
["snowshowersandthunder", "21"]
]


def fetch_weather(wid):

    time = str(jdata['properties']['timeseries'][wid]['time'])
    temp = str(jdata['properties']['timeseries'][wid]['data']['instant']['details']['air_temperature'])
    wind = str(jdata['properties']['timeseries'][wid]['data']['instant']['details']['wind_speed'])
    rain = str(jdata['properties']['timeseries'][wid]['data']['next_1_hours']['details']['precipitation_amount'])
    symbol = str(jdata['properties']['timeseries'][wid]['data']['next_1_hours']['summary']['symbol_code'])

    cleantime = time[11:16]

    return cleantime, temp, wind, rain, symbol





def fetch_symbols():
    isymb = 0
    weather_code = []


    while isymb < weather_list:
        weather_code.append(str(jdata['properties']['timeseries'][isymb]['data']['next_1_hours']['summary']['symbol_code']))
        isymb += 1

    weather_code_red = [*set(weather_code)]
    print(weather_code_red)

    for list in symbols:
        if weather_code_red[0] in list:
            weather_symbol.append(weather_code_red[0], )


        lists = [[1, 2, 3], [4, 5, 6]]

        element = 4

        element_in_lists = False

        for list in lists:
            if
        element in list:

        element_in_lists = True

        print(element_in_lists)




fetch_symbols()



win = Tk() #creating the main window and storing the window object in 'win'
win.geometry('500x200') #setting the size of the window
win.title('WeatherKiosk') #setting title of the window
win.geometry("720x480")

h0 = Label(win, text="TID")
h1 = Label(win, text="Temperatur")
h2 = Label(win, text="Vind")
h3 = Label(win, text="Regn")
h4 = Label(win, text="ICON")

h0.grid(row=0, column=0)
h1.grid(row=0, column=1)
h2.grid(row=0, column=2)
h3.grid(row=0, column=3)
h4.grid(row=0, column=4)

win.columnconfigure(0, minsize=100)
win.columnconfigure(1, minsize=100)
win.columnconfigure(2, minsize=100)
win.columnconfigure(3, minsize=100)
win.columnconfigure(4, minsize=100)


def pick_img(code):
    if code == 18:
        img = "w-img/03n.png"
    elif code == 19:
        img = "w-img/03d.png"

    return img

row = 1
timeseri = 0
i = 18

while i < weather_list:
    wl0 = Label(win, text="kl " + fetch_weather(timeseri)[0])
    wl1 = Label(win, text=fetch_weather(timeseri)[1] + " °C")
    wl2 = Label(win, text=fetch_weather(timeseri)[2] + " m/s")
    wl3 = Label(win, text=fetch_weather(timeseri)[3] + " mm")

    img = ImageTk.PhotoImage(Image.open(pick_img(i)))
    wl4 = Label(win, image=img)

    wl0.grid(row=row, column=0)
    wl1.grid(row=row, column=1)
    wl2.grid(row=row, column=2)
    wl3.grid(row=row, column=3)
    wl4.grid(row=row, column=4)

    row += 1
    timeseri += 1
    i += 1


win.mainloop() #running the loop that works as a trigger

#!/usr/bin/python

import requests
import json
import time

from tkinter import *

from PIL import ImageTk, Image
import os



url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
response = requests.get(url, headers=headers)

rdata = response.text
jdata = json.loads(rdata)

partlycloudy_night = "03n.png"


def fetch_weather(wid):

    time = str(jdata['properties']['timeseries'][wid]['time'])
    temp = str(jdata['properties']['timeseries'][wid]['data']['instant']['details']['air_temperature'])
    wind = str(jdata['properties']['timeseries'][wid]['data']['instant']['details']['wind_speed'])
    rain = str(jdata['properties']['timeseries'][wid]['data']['next_1_hours']['details']['precipitation_amount'])
    symbol = str(jdata['properties']['timeseries'][wid]['data']['next_1_hours']['summary']['symbol_code'])

    cleantime = time[11:16]

    return cleantime, temp, wind, rain, symbol


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

while i < 20:
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

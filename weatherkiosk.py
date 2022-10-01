#!/usr/bin/python

import requests
import json

from datetime import datetime, timedelta

from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path

# definitions
weather_list = 6

# Get weather
weather_url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.961662&lon=10.741941'
weather_header = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
weather_response = requests.get(weather_url, headers=weather_header)

weather_rdata = weather_response.text
weather_jdata = json.loads(weather_rdata)


# Get of variants / Legend
variants_url = "https://api.met.no/weatherapi/weathericon/2.0/legends"
variants_headers = {'user-agent': 'weatherkiosk/0.1 stefan@bahrawy.net'}
variants_response = requests.get(variants_url, headers=variants_headers)

variants_rdata = variants_response.text
variants_jdata = json.loads(variants_rdata)


def fetch_weather(wid):

    time = str(weather_jdata['properties']['timeseries'][wid]['time'])
    temp = str(weather_jdata['properties']['timeseries'][wid]['data']['instant']['details']['air_temperature'])
    wind = str(weather_jdata['properties']['timeseries'][wid]['data']['instant']['details']['wind_speed'])
    rain = str(weather_jdata['properties']['timeseries'][wid]['data']['next_1_hours']['details']['precipitation_amount'])
    code = str(weather_jdata['properties']['timeseries'][wid]['data']['next_1_hours']['summary']['symbol_code'])
    cleantime = time[11:16]

    format = '%H:%M'

    time = datetime.strptime(cleantime, format)
    tmp_cleantime = time + timedelta(minutes=120)
    tmp_cleantime = tmp_cleantime.strftime(format)
    cleantime = str(tmp_cleantime)

    return cleantime, temp, wind, rain, code


win = Tk() # creating the main window and storing the window object in 'win'
win.title('WeatherKiosk') # setting title of the window

win.geometry("720x480")
# win.attributes("-fullscreen", True)

path = str(Path(__file__).parent.absolute())

tmp_img = Image.open(path + "/img/clock.png")
img = tmp_img.resize((50, 50))
img_clock = ImageTk.PhotoImage(img)

tmp_img = Image.open(path + "/img/temp.png")
img = tmp_img.resize((50, 50))
img_temp = ImageTk.PhotoImage(img)

tmp_img = Image.open(path + "/img/wind.png")
img = tmp_img.resize((50, 50))
img_wind = ImageTk.PhotoImage(img)

tmp_img = Image.open(path + "/img/rain.png")
img = tmp_img.resize((50, 50))
img_rain = ImageTk.PhotoImage(img)

# h0 = Label(win, text="TID")
# h1 = Label(win, text="TEMPERATUR")
# h2 = Label(win, text="VIND")
# h3 = Label(win, text="REGN")

h0 = Label(win, image=img_clock)
h1 = Label(win, image=img_temp)
h2 = Label(win, image=img_wind)
h3 = Label(win, image=img_rain)

h4 = Label(win, text="")
h5 = Label(win, text="")

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

row = 1
timeseri = 1
i = 0
img = {}

while i < weather_list:
    # Get data for wl4
    tmp_code = fetch_weather(timeseri)[4]
    if "_" in tmp_code:
        red_code = tmp_code.split("_")
        code = red_code[0]
        tmp_variant = red_code[1]
    else:
        code = fetch_weather(timeseri)[4]
        tmp_variant = ""

    # get data for wl5
    tmp_num = variants_jdata[code]['old_id']
    if len(tmp_num) == 1:
        number = "0" + tmp_num
    else:
        number = tmp_num

    if tmp_variant == "day":
        variant = "d"
    elif tmp_variant == "night":
        variant = "n"
    else:
        variant = ""

    name = path + "/w-img/" + number + variant + ".png"

    tmp_img = Image.open(name)
    images = tmp_img.resize((50, 50))

    img[timeseri] = ImageTk.PhotoImage(images)

    x = 0
    while x is not weather_list:
        print("TEST")
        x += 1

    wl0 = Label(win, text="kl " + fetch_weather(timeseri)[0])
    wl1 = Label(win, text=fetch_weather(timeseri)[1] + " °C")
    wl2 = Label(win, text=fetch_weather(timeseri)[2] + " m/s")
    wl3 = Label(win, text=fetch_weather(timeseri)[3] + " mm")
    wl4 = Label(win, text=variants_jdata[code]['desc_nb'])
    wl5 = Label(win, image=img[timeseri])

    wl0.grid(row=row, column=0)
    wl1.grid(row=row, column=1)
    wl2.grid(row=row, column=2)
    wl3.grid(row=row, column=3)
    wl4.grid(row=row, column=4)
    wl5.grid(row=row, column=5)

    row += 1
    timeseri += 1
    i += 1


def update():
    wl1.configure(text="TEST")
    wl1.grid(row=1, column=0)
    win.after(1000, update)


# update()

win.mainloop()  # running the loop that works as a trigger

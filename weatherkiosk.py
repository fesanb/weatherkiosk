#!/usr/bin/python

import requests
import json

from tkinter import *
from PIL import ImageTk, Image

# definitions
weather_list = 20

# Get weather
weather_url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.96&lon=10.74'
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
    return cleantime, temp, wind, rain, code


def fetch_symbols():
    isymb = 0
    weather_code = []

    while isymb < weather_list:
        weather_code.append(str(weather_jdata['properties']['timeseries'][isymb]['data']['next_1_hours']['summary']['symbol_code']))
        isymb += 1

    weather_code_red1 = [*set(weather_code)]

    isymb = 0
    weather_code_red2 = []

    for x in weather_code_red1:
        if "_" in weather_code_red1[isymb]:
            a = weather_code_red1[isymb].split("_")
            weather_code_red2.append(a[0])
        else:
            a = weather_code_red1[isymb]
            weather_code_red2.append(a)

        isymb += 1
    weather_code_red2 = [*set(weather_code_red2)]

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

        if not (weather_dict[weather_code_red2[isymb]]['variants']):
            name = name + ".png"
        else:
            name = name + "d.png"

        path = "w-img/"

        tmp_img = Image.open(path+name)
        images[weather_code_red2[isymb]] = tmp_img.resize((50, 50))

        isymb += 1

    return images


def fetch_info(code, variant):
    print(variants_jdata[code]['old_id'])
    print(variants_jdata[code]['desc_nb'])


fetch_info('clearsky', 'night')


win = Tk() #creating the main window and storing the window object in 'win'
win.title('WeatherKiosk') #setting title of the window
win.geometry("720x480")
#win.attributes("-fullscreen", True)

h0 = Label(win, text="TID")
h1 = Label(win, text="Temperatur")
h2 = Label(win, text="Vind")
h3 = Label(win, text="Regn")
h4 = Label(win, text="Info")
h5 = Label(win, text="ICON")

h0.config(font=("Courier", 20))


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
timeseri = 2
i = 8
img = {}

while i < weather_list:
    wl0 = Label(win, text="kl " + fetch_weather(timeseri)[0])
    wl1 = Label(win, text=fetch_weather(timeseri)[1] + " °C")
    wl2 = Label(win, text=fetch_weather(timeseri)[2] + " m/s")
    wl3 = Label(win, text=fetch_weather(timeseri)[3] + " mm")

    tmp_code = fetch_weather(timeseri)[4]
    if "_" in tmp_code:
        red_code = tmp_code.split("_")
        code = red_code[0]
        tmp_variant = red_code[1]
    else:
        code = fetch_weather(timeseri)[4]
        tmp_variant = ""

    wl4 = Label(win, text=variants_jdata[code]['desc_nb'])
    tmp_num =variants_jdata[code]['old_id']
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


    name = "w-img/" + number + variant + ".png"

    tmp_img = Image.open(name)
    images = tmp_img.resize((50, 50))

    img[timeseri] = ImageTk.PhotoImage(images)
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


win.mainloop() #running the loop that works as a trigger

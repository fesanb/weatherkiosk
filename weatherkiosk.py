#!/usr/bin/python

import user_data # local file for coordinates and e-mail. See readme for creation.
import requests
import json

from datetime import datetime, timedelta
from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path

# definitions
weather_list = 8
api_offset = 0
bg_color = "#020410"
fg_color = "#DDDDDD"

# Get of variants / Legend
variants_url = "https://api.met.no/weatherapi/weathericon/2.0/legends"
variants_headers = {'user-agent': 'weatherkiosk/1.0' + user_data.mail}
variants_response = requests.get(variants_url, headers=variants_headers)

variants_rdata = variants_response.text
variants_jdata = json.loads(variants_rdata)

def api_weather():
    weather_url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=' + user_data.lat + "&lon=" + user_data.lon
    weather_header = {'user-agent': 'weatherkiosk/1.0' + user_data.mail}
    weather_response = requests.get(weather_url, headers=weather_header)

    weather_rdata = weather_response.text
    weather_jdata = json.loads(weather_rdata)

    return weather_jdata



def fetch_weather(wid):

    time = str(api_weather()['properties']['timeseries'][wid]['time'])
    temp = str(api_weather()['properties']['timeseries'][wid]['data']['instant']['details']['air_temperature'])
    wind = str(api_weather()['properties']['timeseries'][wid]['data']['instant']['details']['wind_speed'])
    rain = str(api_weather()['properties']['timeseries'][wid]['data']['next_1_hours']['details']['precipitation_amount'])
    code = str(api_weather()['properties']['timeseries'][wid]['data']['next_1_hours']['summary']['symbol_code'])
    cleantime = time[11:16]

    format = '%H:%M'

    time = datetime.strptime(cleantime, format)
    tmp_cleantime = time + timedelta(minutes=120)
    tmp_cleantime = tmp_cleantime.strftime(format)
    cleantime = str(tmp_cleantime)

    return cleantime, temp, wind, rain, code


win = Tk() # creating the main window and storing the window object in 'win'
win.title('WeatherKiosk') # setting title of the window

#win.geometry("720x480")
win.attributes("-fullscreen", True)
win.configure(background=bg_color)

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

h0 = Label(win, image=img_clock)
h1 = Label(win, image=img_temp)
h2 = Label(win, image=img_wind)
h3 = Label(win, image=img_rain)

h4 = Label(win, text="")
h5 = Label(win, text="")

h0.config(bg=bg_color)
h1.config(bg=bg_color)
h2.config(bg=bg_color)
h3.config(bg=bg_color)
h4.config(bg=bg_color)
h5.config(bg=bg_color)

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

img = {}
wl0 = {}
wl1 = {}
wl2 = {}
wl3 = {}
wl4 = {}
wl5 = {}

i_c = 0
row = 1
timeseri = api_offset

while i_c < weather_list: # Create Grid
    wl0[timeseri] = (Label(win, text="wl0"))
    wl1[timeseri] = (Label(win, text="wl1"))
    wl2[timeseri] = (Label(win, text="wl2"))
    wl3[timeseri] = (Label(win, text="wl3"))
    wl4[timeseri] = (Label(win, text="wl4"))
    wl5[timeseri] = (Label(win))

    wl0[timeseri].config(bg=bg_color, fg=fg_color)
    wl1[timeseri].config(bg=bg_color, fg=fg_color)
    wl2[timeseri].config(bg=bg_color, fg=fg_color)
    wl3[timeseri].config(bg=bg_color, fg=fg_color)
    wl4[timeseri].config(bg=bg_color, fg=fg_color)
    wl5[timeseri].config(bg=bg_color, fg=fg_color)

    wl0[timeseri].grid(row=row, column=0)
    wl1[timeseri].grid(row=row, column=1)
    wl2[timeseri].grid(row=row, column=2)
    wl3[timeseri].grid(row=row, column=3)
    wl4[timeseri].grid(row=row, column=4)
    wl5[timeseri].grid(row=row, column=5)

    row += 1
    timeseri += 1
    i_c += 1

last_update = (Label(win, text="Oppdatert", font=('Arial 10 italic')))
last_update.config(bg=bg_color, fg=fg_color)
last_update.place(relx=1.0,
                  rely=0.0,
                  anchor='ne')

def image(t): # t =timeseri
    # Get data for wl4
    tmp_code = fetch_weather(t)[4]
    if "_" in tmp_code:
        red_code = tmp_code.split("_")
        code = red_code[0]
        tmp_variant = red_code[1]
    else:
        code = fetch_weather(t)[4]
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

    img[t] = ImageTk.PhotoImage(images)

    return img[t], code


# while i < weather_list:
#     image
#
#     wl0[timeseri] = (Label(win, text="kl " + fetch_weather(timeseri)[0]))
#     wl1[timeseri] = (Label(win, text=fetch_weather(timeseri)[1] + " °C"))
#     wl2[timeseri] = (Label(win, text=fetch_weather(timeseri)[2] + " m/s"))
#     wl3[timeseri] = (Label(win, text=fetch_weather(timeseri)[3] + " mm"))
#     wl4[timeseri] = (Label(win, text=variants_jdata[code]['desc_nb']))
#     wl5[timeseri] = (Label(win, image=img[timeseri]))
#
#     wl0[timeseri].config(bg=bg_color, fg=fg_color)
#     wl1[timeseri].config(bg=bg_color, fg=fg_color)
#     wl2[timeseri].config(bg=bg_color, fg=fg_color)
#     wl3[timeseri].config(bg=bg_color, fg=fg_color)
#     wl4[timeseri].config(bg=bg_color, fg=fg_color)
#     wl5[timeseri].config(bg=bg_color, fg=fg_color)
#
#     wl0[timeseri].grid(row=row, column=0)
#     wl1[timeseri].grid(row=row, column=1)
#     wl2[timeseri].grid(row=row, column=2)
#     wl3[timeseri].grid(row=row, column=3)
#     wl4[timeseri].grid(row=row, column=4)
#     wl5[timeseri].grid(row=row, column=5)
#
#     row += 1
#     timeseri += 1
#     i += 1
#
#     last_update = (Label(win, text="Oppdatert", font=('Arial 10 italic')))
#     last_update.config(bg=bg_color, fg=fg_color)
#     last_update.place(relx = 1.0,
#                       rely = 0.0,
#                       anchor = 'ne')


def update():
    api_weather()

    now = datetime.now()
    current_time = now.strftime("%d.%m.%Y - %H:%M")
    last_update.configure(text="Oppdatert: " + current_time)

    timeseri = api_offset
    i = 0

    while i < weather_list:
        wl0[timeseri].configure(text="kl " + fetch_weather(timeseri)[0])
        wl1[timeseri].configure(text=fetch_weather(timeseri)[1] + " °C")
        wl2[timeseri].configure(text=fetch_weather(timeseri)[2] + " m/s")
        wl3[timeseri].configure(text=fetch_weather(timeseri)[3] + " mm")
        wl4[timeseri].configure(text=variants_jdata[image(timeseri)[1]]['desc_nb'])
        wl5[timeseri].configure(image=image(timeseri)[0])

        i += 1
        timeseri += 1

    win.after(900000, update) # 900000


update()

win.mainloop()  # running the loop that works as a trigger

#!/usr/bin/env python

#Data from OpenWeatherMap
#show_graph function adapted from cpu_temp.py


import blinkt
from time import sleep
try:
    import requests
except ImportError:
    print("This example requires \"requests\" package.")
    print("Please install it by running \"sudo pip install requests\"")


#Grab your API key here: http://openweathermap.org
#List of city ID city.list.json.gz can be downloaded here http://bulk.openweathermap.org/sample/
API_KEY='a217a2719b9b2640b50dc43ad5e0b468'
CITY_ID='2773913'

url = 'http://api.openweathermap.org/data/2.5/weather'

temp = 0

def update_weather():
    payload = {
        'id': CITY_ID,
        'units': 'metric',
        'appid': API_KEY
    }
    global temp
    try:
        r = requests.get(url=url, params=payload)
        temp = r.json().get('main').get('temp')
        print("Temperture = "+str(temp)+" C")
    except:
        print("Connection Error")

def show_graph(v, r, g, b):
    v *= 8
    for x in range(8):
        if v  < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v,1.0) * c) for c in [r,g,b]]
        blinkt.set_pixel(x, r, g, b)
        v -= 1
    blinkt.show()

def draw_thermo(temp):
    v = temp
    v /= 40
    v += (1/8)
    show_graph(v, 255, 0, 0)

blinkt.set_brightness(0.1)

while 1:
    update_weather()
    draw_thermo(temp)
    sleep(120)

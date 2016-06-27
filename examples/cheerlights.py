#!/usr/bin/env python

import time
import requests
from blinkt import set_pixel, show

while True:
    r = requests.get('http://api.thingspeak.com/channels/1417/field/2/last.json')
    col = r.json()['field2']
    r, g, b = tuple(ord(c) for c in col[1:].lower().decode('hex'))
    for i in range(8):
        set_pixel(i, r, g, b)
    show()
    time.sleep(1)

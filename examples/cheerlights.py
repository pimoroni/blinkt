#!/usr/bin/env python

import time
from sys import exit

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

from blinkt import set_clear_on_exit, set_pixel, show

set_clear_on_exit()

while True:
    r = requests.get('http://api.thingspeak.com/channels/1417/field/2/last.json', timeout=2)
    col = r.json()['field2']
    r, g, b = tuple(ord(c) for c in col[1:].lower().decode('hex'))
    for i in range(8):
        set_pixel(i, r, g, b)
    show()
    time.sleep(1)

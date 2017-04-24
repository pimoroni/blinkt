#!/usr/bin/env python

import time
from sys import exit

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

import blinkt

blinkt.set_clear_on_exit()

def hex_to_rgb(col_hex):
    """Convert a hex colour to an RGB tuple"""
    col_hex = col_hex.lstrip("#")
    return bytearray.fromhex(col_hex)

while True:
    r = requests.get("http://api.thingspeak.com/channels/1417/field/2/last.json", timeout=2)
    r, g, b = hex_to_rgb(r.json()["field2"])

    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i, r, g, b)

    blinkt.show()

    time.sleep(5) # Be friendly to the API

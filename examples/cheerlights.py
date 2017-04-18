#!/usr/bin/env python

import time
import struct
from sys import exit

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

import blinkt

blinkt.set_clear_on_exit()

def hex_to_rgb(col_hex):
    col_hex = col_hex.lstrip("#")
    try:
        return struct.unpack("BBB",bytes.fromhex(col_hex))
    except AttributeError:
        return struct.unpack("BBB",col_hex.decode("hex"))

while True:
    r = requests.get("http://api.thingspeak.com/channels/1417/field/2/last.json", timeout=2)
    r, g, b = hex_to_rgb(r.json()["field2"])

    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i, r, g, b)
        
    blinkt.show()

    time.sleep(5) # Be friendly to the API
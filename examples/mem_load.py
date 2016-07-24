#!/usr/bin/env python

import math
import time

try:
    import psutil
except ImportError:
    exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

from blinkt import set_brightness, set_pixel, show


def show_graph(v, r, g, b):
    v *= 8
    for x in range(8):
        if v  < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v,1.0) * c) for c in [r,g,b]]
        set_pixel(x, r, g, b)
        v -= 1

    show()

set_brightness(0.1)

while True:
    v = psutil.virtual_memory().percent / 100.0
    show_graph(v, 255, 0, 255)
    time.sleep(0.01)

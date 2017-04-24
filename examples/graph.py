#!/usr/bin/env python

import math
import time

import blinkt


blinkt.set_clear_on_exit()

def show_graph(v, r, g, b):
    v *= blinkt.NUM_PIXELS
    for x in range(blinkt.NUM_PIXELS):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v,1.0) * c) for c in [r, g, b]]
        blinkt.set_pixel(x, r, g, b)
        v -= 1

    blinkt.show()

blinkt.set_brightness(0.1)

try:
    while True:
        t = time.time()
        v = (math.sin(t) + 1) / 2 # Get a value between 0 and 1
        show_graph(v, 255, 0, 255)
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

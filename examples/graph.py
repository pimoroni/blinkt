#!/usr/bin/env python

import math
import time

from blinkt import set_clear_on_exit, set_brightness, set_pixel, show


set_clear_on_exit()

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

try:
    while True:
        t = time.time()
        v = (math.sin(t) + 1) / 2 # Get a value between 0 and 1
        show_graph(v,255,0,255)
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

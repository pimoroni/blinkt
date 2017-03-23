#!/usr/bin/env python

import math
import time
from subprocess import PIPE, Popen

import blinkt

blinkt.set_clear_on_exit()

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def show_graph(v, r, g, b):
    v *= blinkt.NUM_PIXELS
    for x in range(blinkt.NUM_PIXELS):
        if v  < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v,1.0) * c) for c in [r,g,b]]
        blinkt.set_pixel(x, r, g, b)
        v -= 1

    blinkt.show()

blinkt.set_brightness(0.1)

while True:
    v = get_cpu_temperature() / 100.0
    show_graph(v, 255, 255, 255)
    time.sleep(0.01)

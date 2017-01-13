#!/usr/bin/env python

import math
import time
from subprocess import PIPE, Popen

from blinkt import set_clear_on_exit, set_brightness, set_pixel, show

set_clear_on_exit()

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()

    pos_start = output.index('=') + 1
    pos_end = output.rindex("'")

    temp = float(output[pos_start:pos_end])

    return temp

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
    v = get_cpu_temperature() / 100.0
    show_graph(v, 255, 255, 255)
    time.sleep(0.01)

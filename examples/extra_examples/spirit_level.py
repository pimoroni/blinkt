#!/usr/bin/env python

import time
from sys import exit

try:
    from envirophat import motion
except ImportError:
    exit("This script requires the envirophat module\nInstall with: sudo pip install envirophat")

import blinkt


x_avg = []

while True:
    x, y, z = motion.accelerometer()

    x_avg.append(x)
    x_avg = x_avg[-5:]

    x = float(sum(x_avg)) / len(x_avg)
    x = max(-1, x)
    x = min(1, x)

    blinkt.clear()
    if abs(x) < 0.05:
        blinkt.set_pixel(3, 0, 255, 0)
        blinkt.set_pixel(4, 0, 255, 0)

    elif x > 0:
        val = abs(x) * 4.0
        for x in range(4):
            if val < 0: break
            blinkt.set_pixel(3-x, int(255.0 * min(val, 1.0)), 0, 0)
            val -= 1

    elif x < 0:
        val = abs(x) * 4.0
        for x in range(4):
            if val < 0: break
            blinkt.set_pixel(4+x, int(255.0 * min(val, 1.0)), 0, 0)
            val -= 1

    blinkt.show()

    time.sleep(0.01)

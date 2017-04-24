#!/usr/bin/env python

import math
import time
from colorsys import hsv_to_rgb
from sys import exit

try:
    from envirophat import motion
except ImportError:
    exit("This script requires the envirophat module\nInstall with: sudo pip install envirophat")

import blinkt

offset = 0
direction = 0
t = []
t_start = 0

total_time = 1000

def millis():
    return int(round(time.time() * 1000))

while True:
    x, y, z = motion.accelerometer()
    print(y)

    if y < -1.9 and not direction == -1:
        direction = -1
        t.append(millis() - t_start)
        t_start = millis()
        t = t[-5:]

    if y > 1.9 and not direction == 1:
        direction = 1
        t.append(millis() - t_start)
        t_start = millis()
        t = t[-5:] 

    if len(t) > 0:
        total_time = float(sum(t)) / len(t)

    offset = ((millis() - t_start) / total_time)

    #offset += direction * 10

    offset = min(1.0, offset)
    offset = max(0.0, offset)

    hue = offset

    if direction == -1:
        hue = 1.0 - offset

    r, g, b = [int(x * 255.0) for x in hsv_to_rgb(hue, 1.0, 1.0)]

    for x in range(8):
        blinkt.set_pixel(x, r, g, b)

    blinkt.show()

    time.sleep(0.0001)

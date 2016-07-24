#!/usr/bin/env python

import random
import time

from blinkt import set_pixel, show, set_brightness


set_brightness(0.1)

while True:
    for i in range(8):
        set_pixel(i, random.randint(0,255), random.randint(0,255), random.randint(0,255))
    show()
    time.sleep(0.05)

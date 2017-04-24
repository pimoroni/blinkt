#!/usr/bin/env python

import random
import time

import blinkt

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

while True:
    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    blinkt.show()
    time.sleep(0.05)

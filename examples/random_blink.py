#!/usr/bin/env python

import random
import time

import blinkt

blinkt.set_clear_on_exit()

while True:
    pixels = random.sample(range(blinkt.NUM_PIXELS), random.randint(1, 5))
    for i in range(blinkt.NUM_PIXELS):
        if i in pixels:
            blinkt.set_pixel(i, 255, 150, 0)
        else:
            blinkt.set_pixel(i, 0, 0, 0)
    blinkt.show()
    time.sleep(0.05)

#!/usr/bin/env python

import random
import time

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness, NUM_PIXELS


set_clear_on_exit()
set_brightness(0.1)

while True:
    for i in range(NUM_PIXELS):
        set_pixel(i, random.randint(0,255), random.randint(0,255), random.randint(0,255))
    show()
    time.sleep(0.05)

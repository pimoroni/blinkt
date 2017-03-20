#!/usr/bin/env python

import random
import time

from blinkt import set_clear_on_exit, set_pixel, show, NUM_PIXELS


set_clear_on_exit()

while True:
    pixels = random.sample(range(NUM_PIXELS), random.randint(1, 5))
    for i in range(NUM_PIXELS):
        if i in pixels:
            set_pixel(i, 255, 150, 0)
        else:
            set_pixel(i, 0, 0, 0)
    show()
    time.sleep(0.05)

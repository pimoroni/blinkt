#!/usr/bin/env python

import random
import time
from blinkt import set_pixel, show

while True:
    pixels = random.sample(range(8), random.randint(1, 5))
    for i in range(8):
        if i in pixels:
            set_pixel(i, 255, 150, 0)
        else:
            set_pixel(i, 0, 0, 0)
    show()
    time.sleep(0.05)

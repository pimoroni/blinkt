#!/usr/bin/env python

import colorsys
import random
import time
from sys import exit

try:
    import numpy as np
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

from blinkt import set_pixel, set_brightness, show, clear


clear()
start = 0
end = 60

while True:
    wait = np.random.choice(np.random.noncentral_chisquare(5, 1, 1000), 1)[0] / 50
    n = np.random.choice(np.random.noncentral_chisquare(5, 0.1, 1000), 1)
    limit = int(n[0])
    if limit > 8:
        limit = 8
    for pixel in range(limit):
        hue = start + (((end - start) / 8.0) * pixel) 
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue/360.0, 1.0, 1.0)]
        set_pixel(pixel, r, g, b)
        show()
        time.sleep(0.05 / (pixel + 1))
    time.sleep(wait)
    clear()

#!/usr/bin/env python

import time, colorsys
from blinkt import set_pixel, show, set_brightness

try:
    import numpy as np
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

def make_gaussian(fwhm):
    x = np.arange(0, 8, 1, float)
    y = x[:, np.newaxis]
    x0, y0 = 3.5, 3.5
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

while True:
    for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
        fwhm = 5.0/z
        gauss = make_gaussian(fwhm)
        start = time.time()
        y = 4
        for x in range(8):
            h = 0.5
            s = 1.0
            v = gauss[x, y]
            rgb = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = [int(255.0 * i) for i in rgb]
            set_pixel(x, r, g, b)
        show()
        end = time.time()
        t = end - start
        if t < 0.04:
            time.sleep(0.04 - t)

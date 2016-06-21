#!/usr/bin/env python

import time
from blinkt import set_pixel, show
import colorsys
from sys import argv

spacing = 360.0 / 16.0
hue = int(argv[1])

for x in range(8):
    offset = x * spacing
    h = ((hue + offset) % 360) / 360.0
    r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
    set_pixel(x,r,g,b)
    print(r,g,b)
show()

#!/usr/bin/env python

import math
import time
import colorsys

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness

FALLOFF = 1.9
SCAN_SPEED = 4

set_clear_on_exit()

start_time = time.time()


while True:
    delta = (time.time() - start_time)

    # Offset is a sine wave derived from the time delta
    # we use this to animate both the hue and larson scan
    # so they are kept in sync with each other
    offset = (math.sin(delta * SCAN_SPEED) + 1) / 2

    # Use offset to pick the right colour from the hue wheel
    hue = int(round(offset * 360))

    # Now we generate a value from 0 to 7
    offset = int(round(offset * 7))

    for x in range(8):
        sat = 1.0
 
        val = 7 - (abs(offset - x) * FALLOFF)
        val /= 7.0 # Convert to 0.0 to 1.0
        val = max(val,0.0) # Ditch negative values

        xhue = hue # Grab hue for this pixel
        xhue += (1-val) * 10 # Use the val offset to give a slight colour trail variation
        xhue %= 360 # Clamp to 0-359
        xhue /= 360.0 # Convert to 0.0 to 1.0

        r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]

        set_pixel(x, r, g, b, val / 4)

    show()

    time.sleep(0.001)

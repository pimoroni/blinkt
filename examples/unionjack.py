#!/usr/bin/env python

import colorsys
import time
import blinkt

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

blinkt.set_pixel(0,   0,   0, 255)
blinkt.set_pixel(0,   0,   0, 255)
blinkt.set_pixel(0, 255, 255, 255)
blinkt.set_pixel(0, 255,   0,   0)
blinkt.set_pixel(0, 255,   0,   0)
blinkt.set_pixel(0, 255, 255, 255)
blinkt.set_pixel(0,   0,   0, 255)
blinkt.set_pixel(0,   0,   0, 255)
blinkt.show()

while 1:
    time.sleep(1)

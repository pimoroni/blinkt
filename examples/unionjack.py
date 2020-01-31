#!/usr/bin/env python

import colorsys
import time
import blinkt

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

blinkt.set_pixel(0,   0,   0, 255)
blinkt.set_pixel(1,   0,   0, 255)
blinkt.set_pixel(2, 195, 195, 195)
blinkt.set_pixel(3, 255,   0,   0)
blinkt.set_pixel(4, 255,   0,   0)
blinkt.set_pixel(5, 195, 195, 195)
blinkt.set_pixel(6,   0,   0, 255)
blinkt.set_pixel(7,   0,   0, 255)
blinkt.show()

while 1:
    time.sleep(1)

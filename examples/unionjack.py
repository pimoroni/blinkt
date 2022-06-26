#!/usr/bin/env python3

import time
import blinkt

RED__ = (255, 0, 0)
WHITE = (127, 127, 127)
BLUE_ = (0, 0, 255)

pattern = [
    [RED__, BLUE_, WHITE, RED__, RED__, WHITE, BLUE_, RED__],
    [BLUE_, RED__, WHITE, RED__, RED__, WHITE, RED__, BLUE_],
    [WHITE, WHITE, WHITE, RED__, RED__, WHITE, WHITE, WHITE],
    [RED__, RED__, RED__, RED__, RED__, RED__, RED__, RED__],
    [RED__, RED__, RED__, RED__, RED__, RED__, RED__, RED__],
    [WHITE, WHITE, WHITE, RED__, RED__, WHITE, WHITE, WHITE],
    [BLUE_, RED__, WHITE, RED__, RED__, WHITE, RED__, BLUE_],
    [RED__, BLUE_, WHITE, RED__, RED__, WHITE, BLUE_, RED__],
]

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

while 1:
    for line in pattern:
        for i, pixel in enumerate(line):
            r, g, b = pixel
            blinkt.set_pixel(i, r, g, b)
        blinkt.show()
        time.sleep(0.25)

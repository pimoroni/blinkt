#!/usr/bin/env python

from time import localtime, sleep

import blinkt

blinkt.set_clear_on_exit()

MODE_HOUR = 0
MODE_MIN = 1
MODE_SEC = 2

time_to_stay_in_mode = 3
time_in_mode = 0
mode = 0

lh = 0
lm = 0

while True:
    t = localtime()
    h, m, s = t.tm_hour, t.tm_min, t.tm_sec
    print(h, m, s, mode, time_in_mode)

    if h != lh:
        mode = MODE_HOUR
        time_in_mode = 0

    elif m != lm:
        mode = MODE_MIN
        time_in_mode = 0

    lm = m
    lh = h

    blinkt.clear()

    if (s % 2) == 0:
        blinkt.set_pixel(1, 64, 64, 64)

    if mode == MODE_HOUR:
        blinkt.set_pixel(0, 255, 0, 0)
        for x in range(6):
            bit = (h & (1 << x)) > 0
            r, g, b = [128 * bit] * 3
            blinkt.set_pixel(7 - x, r, g, b)

    if mode == MODE_MIN:
        blinkt.set_pixel(0, 0, 255, 0)
        for x in range(6):
            bit = (m & (1 << x)) > 0
            r, g, b = [128 * bit] * 3
            blinkt.set_pixel(7 - x, r, g, b)

    if mode == MODE_SEC:
        blinkt.set_pixel(0, 0, 0, 255)
        for x in range(6):
            bit = (s & (1 << x)) > 0
            r, g, b = [128 * bit] * 3
            blinkt.set_pixel(7 - x, r, g, b)

    blinkt.show()

    time_in_mode += 1
    if time_in_mode == time_to_stay_in_mode:
        mode += 1
        mode %= 3
        time_in_mode = 0

    sleep(1)

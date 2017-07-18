#!/usr/bin/env python

import time
import math

import blinkt

blinkt.set_clear_on_exit()

REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]

start_time = time.time()

while True:
    # Sine wave, spends a little longer at min/max
    # delta = (time.time() - start_time) * 8
    # offset = int(round(((math.sin(delta) + 1) / 2) * (blinkt.NUM_PIXELS - 1)))

    # Triangle wave, a snappy ping-pong effect
    delta = (time.time() - start_time) * 16
    offset = int(abs((delta % len(REDS)) - blinkt.NUM_PIXELS))

    for i in range(blinkt.NUM_PIXELS):
        blinkt.set_pixel(i , REDS[offset + i], 0, 0)

    blinkt.show()

    time.sleep(0.1)

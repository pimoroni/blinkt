#!/usr/bin/env python

import time

import blinkt

blinkt.set_clear_on_exit()

REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0]

start_time = time.time()

while True:
    delta = (time.time() - start_time) * 16

    # Sine wave, spends a little longer at min/max
    # offset = int(round(((math.sin(delta) + 1) / 2) * 7))

    # Triangle wave, a snappy ping-pong effect
    offset = int(abs((delta % 16) - 8))

    for i in range(8):
        blinkt.set_pixel(i , REDS[offset + i], 0, 0)

    blinkt.show()

    time.sleep(0.1)

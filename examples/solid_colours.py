#!/usr/bin/env python

import time

import blinkt


blinkt.set_clear_on_exit()

step = 0

while True:
    if step == 0:
        blinkt.set_all(128, 0, 0)

    if step == 1:
        blinkt.set_all(0, 128, 0)

    if step == 2:
        blinkt.set_all(0, 0, 128)

    step += 1
    step %= 3
    blinkt.show()
    time.sleep(0.5)

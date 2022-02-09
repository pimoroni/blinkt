#!/usr/bin/env python

import time

import blinkt


blinkt.set_clear_on_exit()

step = 0

while True:
    if step == 0:
        blinkt.set_all(128, 0, 0)
    elif step == 1:
        blinkt.set_all(0, 128, 0)
    elif step == 2:
        blinkt.set_all(128, 128, 0)
    elif step == 3:
        blinkt.set_all(0, 0, 128)
    elif step == 4:
        blinkt.set_all(128, 0, 128)
    elif step == 5:
        blinkt.set_all(0, 128, 128)
    elif step == 6:
        blinkt.set_all(128, 128, 128)

    step += 1
    step %= 7
    blinkt.show()
    time.sleep(0.5)

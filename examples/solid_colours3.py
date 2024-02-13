#!/usr/bin/env python

import time

import blinkt

blinkt.set_clear_on_exit()

step = 0

while True:
    for i in range(0, 128):
        j = 128 - i
        if step == 0:
            blinkt.set_all(128, j, j)
        elif step == 1:
            blinkt.set_all(j, i, 0)
        elif step == 2:
            blinkt.set_all(i, 128, 0)
        elif step == 3:
            blinkt.set_all(j, j, i)
        elif step == 4:
            blinkt.set_all(i, 0, 128)
        elif step == 5:
            blinkt.set_all(j, i, 128)
        elif step == 6:
            blinkt.set_all(i, 128, 128)
        blinkt.show()
        time.sleep(0.01)

    step += 1
    step %= 7
    time.sleep(0.5)

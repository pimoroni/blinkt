#!/usr/bin/env python

import time
from blinkt import set_pixel, show

step = 0

def set_all(r,g,b):
    for x in range(8):
        set_pixel(x,r,g,b)

while True:
    if step == 0:
        set_all(128,0,0)
    if step == 1:
        set_all(0,128,0)
    if step == 2:
        set_all(0,0,128)

    step+=1
    step%=3
    show()
    time.sleep(0.5)

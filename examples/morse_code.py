#!/usr/bin/env python

import time

import blinkt

blinkt.set_clear_on_exit()

def show_all(state):
    for i in range(blinkt.NUM_PIXELS):
        val = state * 255
        blinkt.set_pixel(i, val, val, val)
    blinkt.show()

def dot():
    show_all(1)
    time.sleep(0.05)
    show_all(0)
    time.sleep(0.2)

def dash():
    show_all(1)
    time.sleep(0.2)
    show_all(0)
    time.sleep(0.2)

def space():
    time.sleep(0.2)

#0 is a space, 1 is a dot and 2 is a dash
MORSE = '211101101211022101020120210212000'

while True:
    for m in MORSE:
        if m == '0':
            space()
        elif m == '1':
            dot()
        elif m == '2':
            dash()

#!/usr/bin/env python

import time

import blinkt

blinkt.set_clear_on_exit()


def show_all(state):
    """Set all LEDs."""
    for i in range(blinkt.NUM_PIXELS):
        val = state * 255
        blinkt.set_pixel(i, val, val, val)
    blinkt.show()


def dot():
    """Blink LEDs for 0.05 seconds."""
    show_all(1)
    time.sleep(0.05)
    show_all(0)
    time.sleep(0.2)


def dash():
    """Blink LEDs for 0.2 seconds."""
    show_all(1)
    time.sleep(0.2)
    show_all(0)
    time.sleep(0.2)


def space():
    """Delay for 0.02 seconds."""
    time.sleep(0.2)


# 0 is a space, 1 is a dot and 2 is a dash
MORSE = " -... .. . -..  - -. .  - . -  -.  -. -   "

while True:
    for m in MORSE:
        if m == " ":
            space()
        elif m == ".":
            dot()
        elif m == "-":
            dash()

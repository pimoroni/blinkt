#!/usr/bin/env python

import time

import blinkt

blinkt.set_clear_on_exit()


def get_cpu_temperature():
    with open("/sys/devices/virtual/thermal/thermal_zone0/temp","r") as file:
        temp_raw=file.read()
    temp=int(temp_raw)/1000
    return temp

def show_graph(v, r, g, b):
    v *= blinkt.NUM_PIXELS
    for x in range(blinkt.NUM_PIXELS):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]

        blinkt.set_pixel(x, r, g, b)
        v -= 1

    blinkt.show()


blinkt.set_brightness(0.1)

while True:
    v = get_cpu_temperature() / 100.0
    show_graph(v, 255, 255, 255)
    time.sleep(0.01)

#!/usr/bin/env python

import time  # so we can wait between frames

import blinkt  # so we can talk to our blinkt lights!

BRIGHTNESS = 0.2     # range is 0.0 to 1.0
MAX_COLOUR = 255     # range is 0 to 255
DECAY_FACTOR = 1.5   # how quickly should MAX_COLOUR fade? (1.5 works well)
TIME_SLEEP = 0.04    # seconds (0.04 works well)

PIXELS = blinkt.NUM_PIXELS  # usually 8, can use fewer if you like!

blinkt.clear         # make all pixels blank / black
blinkt.set_brightness(BRIGHTNESS)

brightpixel = -1
direction = 1

print('Hello Michael.\nHow are you today?')

while True:
    # decay all pixels
    for x in range(PIXELS):
        pixel = blinkt.get_pixel(x)  # format is [ r, g, b, brightness? ]
        blinkt.set_pixel(x, pixel[0] / DECAY_FACTOR, 0, 0)

    # brightpixel should move back and forth all the pixels,
    # in a ping-pong, triangle wave. Not (co)sine.
    brightpixel += direction

    if brightpixel >= PIXELS - 1:
        brightpixel = PIXELS - 1
        direction = - abs(direction)
    if brightpixel <= 0:
        brightpixel = 0
        direction = abs(direction)

    blinkt.set_pixel(brightpixel, MAX_COLOUR, 0, 0)

    blinkt.show()           # draw the lights!
    time.sleep(TIME_SLEEP)  # wait a bit before working on next frame

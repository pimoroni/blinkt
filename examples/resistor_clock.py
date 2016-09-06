#!/usr/bin/env python

import time
from blinkt import set_clear_on_exit, set_pixel, show

colours = [
[  0,  0,  0],#0 black
[139, 69, 19],#1 brown
[255,  0,  0],#2 red
[255, 69,  0],#3 orange
[255,255,  0],#4 yellow
[  0,255,  0],#5 green
[  0,  0,255],#6 blue
[128,  0,128],#7 violet
[255,255,100],#8 grey
[255,255,255],#9 white
]

set_clear_on_exit()

while True:
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min

    hourten = hour / 10
    hourunit = hour % 10
    minuteten = minute / 10
    minuteunit = minute % 10

    r, g, b = colours[hourten]
    set_pixel(0,r,g,b)
    set_pixel(1,r,g,b)

    r, g, b = colours[hourunit]
    set_pixel(2,r,g,b)
    set_pixel(3,r,g,b)

    r, g, b = colours[minuteten]
    set_pixel(4,r,g,b)
    set_pixel(5,r,g,b)

    r, g, b = colours[minuteunit]
    set_pixel(6,r,g,b)
    set_pixel(7,r,g,b)

    show()

    time.sleep(0.5)

    set_pixel(7,0,0,0)

    show()

    time.sleep(0.5)


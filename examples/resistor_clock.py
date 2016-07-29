#!/usr/bin/env python

import time
from blinkt import set_brightness, set_pixel, show

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

while True:
	hour = time.localtime().tm_hour
	minute = time.localtime().tm_min

	hourten = hour / 10
	hourunit = hour % 10
	minuteten = minute / 10
	minuteunit = minute % 10

	set_pixel(0,str(colours[hourten][0]),str(colours[hourten][1]),str(colours[hourten][2]))
	set_pixel(1,str(colours[hourten][0]),str(colours[hourten][1]),str(colours[hourten][2]))
	set_pixel(2,str(colours[hourunit][0]),str(colours[hourunit][1]),str(colours[hourunit][2]))
	set_pixel(3,str(colours[hourunit][0]),str(colours[hourunit][1]),str(colours[hourunit][2]))
	set_pixel(4,str(colours[minuteten][0]),str(colours[minuteten][1]),str(colours[minuteten][2]))
	set_pixel(5,str(colours[minuteten][0]),str(colours[minuteten][1]),str(colours[minuteten][2]))
	set_pixel(6,str(colours[minuteunit][0]),str(colours[minuteunit][1]),str(colours[minuteunit][2]))
	set_pixel(7,str(colours[minuteunit][0]),str(colours[minuteunit][1]),str(colours[minuteunit][2]))
	show()
	time.sleep(0.5)
	set_pixel(7,0,0,0)
	show()
	time.sleep(0.5)


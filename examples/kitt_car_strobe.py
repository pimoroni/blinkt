#!/usr/bin/env python

from time import sleep
from blinkt import set_brightness, set_pixel, show

brightness = [0, 0, 0, 0, 0, 0.033, 0.2, 1, 0.2, 0.033, 0, 0, 0, 0, 0, 0] 

try:
	while True:
		for strobe in range(0, 8):
			for pixel in range(0, 8):
				set_pixel(pixel,255,0,0,brightness[strobe+pixel])
			show()
			sleep(0.1)

		for strobe in range(7, -1, -1):
			for pixel in range(0, 8):
				set_pixel(pixel,255,0,0,brightness[strobe+pixel])
			show()
			sleep(0.1)

except:
	set_brightness(0)
	show()

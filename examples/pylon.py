import time
import blinkt

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

x = 0
d = 1

while True:
	blinkt.clear()
	blinkt.set_pixel(x,128,0,0,0.5)
	y = x - d
	if y > 0 or y < 7:
		blinkt.set_pixel(y,255,0,0,0.1)
	if x > 6:
		d = -1
	if x < 1:
		d = 1
	x += d
	blinkt.show()
	time.sleep(0.1)
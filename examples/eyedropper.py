#!/usr/bin/env python3

from PIL import ImageGrab
import pyautogui
import blinkt
import time

print('Press Ctrl-C to quit.')

try:
    while True:
        x, y = pyautogui.position()
        im = ImageGrab.grab(bbox=(x - 1, y, x, y + 1))
        rawrgb = list(im.getdata())
        rgb = str(rawrgb)[2:-2]
        r, g, b = rgb.split(', ')
        blinkt.set_all(int(r), int(g), int(b))
        blinkt.set_brightness(1)
        blinkt.show()
        time.sleep(0.01)
except KeyboardInterrupt:
    print('\n')

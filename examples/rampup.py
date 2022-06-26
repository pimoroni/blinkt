#!/usr/bin/env python
import sys
from time import sleep
import blinkt

for i in range(256):
    blinkt.set_all(i, i, i, 1.0)
    sys.stdout.write("%3d" % i)
    blinkt.show()
    sleep(0.1)

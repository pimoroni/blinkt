#!/usr/bin/env python

import sys

import blinkt 


def usage():
    print("Usage: {} <r> <g> <b>".format(sys.argv[0]))
    sys.exit(1)

if len(sys.argv) != 4:
    usage()

# Exit if non integer value. int() will raise a ValueError
try:
    r, g, b = [int(x) for x in sys.argv[1:]]
except ValueError:
    usage()

# Exit if any of r, g, b are greater than 255
if max(r, g, b) > 255:
    usage()

print("Setting Blinkt to {r},{g},{b}".format(r=r, g=g, b=b))

blinkt.set_clear_on_exit(False)

blinkt.set_all(r, g, b)

blinkt.show()

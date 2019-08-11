#!/usr/bin/env python

import sys
from sys import argv
import blinkt

if len(argv)<2 or len(argv)>5:
    sys.stderr.write( "Syntax: {0} <red> <green> <blue> [brightness]]\n".format(argv[0]) )
    exit(1)

red    = int(argv[1])   if len(argv)>3 else 0
green  = int(argv[2])   if len(argv)>3 else 0
blue   = int(argv[3])   if len(argv)>3 else 0
bright = float(argv[4]) if len(argv)>4 else 0.0

blinkt.set_clear_on_exit(False)
blinkt.set_all(red, green, blue, bright)
blinkt.show()

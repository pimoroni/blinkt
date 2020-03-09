#!/usr/bin/env python

import time
import blinkt

RED   = (255,0,0)
WHITE = (127,127,127)
BLUE  = (0,0,255)

pattern = \
[
    [   RED,    BLUE,   WHITE,  RED,    RED,    WHITE,  BLUE,   RED,    ],
    [   BLUE,   RED,    WHITE,  RED,    RED,    WHITE,  RED,    BLUE,   ],
    [   WHITE,  WHITE,  WHITE,  RED,    RED,    WHITE,  WHITE,  WHITE,  ],
    [   RED,    RED,    RED,    RED,    RED,    RED,    RED,    RED,    ],
    [   RED,    RED,    RED,    RED,    RED,    RED,    RED,    RED,    ],
    [   WHITE,  WHITE,  WHITE,  RED,    RED,    WHITE,  WHITE,  WHITE,  ],
    [   BLUE,   RED,    WHITE,  RED,    RED,    WHITE,  RED,    BLUE,   ],
    [   RED,    BLUE,   WHITE,  RED,    RED,    WHITE,  BLUE,   RED,    ],
]

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

while 1:
    for line in pattern:
        for i,pixel in enumerate(line):
            r, g, b = pixel
            blinkt.set_pixel(i, r, g, b)
        blinkt.show()
        time.sleep(0.25)

#!/usr/bin/env python

import colorsys
import time
import blinkt

Red   = (255,0,0)
White = (127,127,127)
Blue  = (0,0,255)

Pattern = \
[
    [   Red,    Blue,   White,  Red,    Red,    White,  Blue,   Red,    ],
    [   Blue,   Red,    White,  Red,    Red,    White,  Red,    Blue,   ],
    [   White,  White,  White,  Red,    Red,    White,  White,  White,  ],
    [   Red,    Red,    Red,    Red,    Red,    Red,    Red,    Red,    ],
    [   Red,    Red,    Red,    Red,    Red,    Red,    Red,    Red,    ],
    [   White,  White,  White,  Red,    Red,    White,  White,  White,  ],
    [   Blue,   Red,    White,  Red,    Red,    White,  Red,    Blue,   ],
    [   Red,    Blue,   White,  Red,    Red,    White,  Blue,   Red,    ],
]

blinkt.set_clear_on_exit()
blinkt.set_brightness(0.1)

blinkt.set_pixel(0,   0,   0, 255)
blinkt.set_pixel(1,   0,   0, 255)
blinkt.set_pixel(2, 195, 195, 195)
blinkt.set_pixel(3, 255,   0,   0)
blinkt.set_pixel(4, 255,   0,   0)
blinkt.set_pixel(5, 195, 195, 195)
blinkt.set_pixel(6,   0,   0, 255)
blinkt.set_pixel(7,   0,   0, 255)
blinkt.show()

while 1:
    for line in Pattern:
        for i in range(len(line)):
            blinkt.set_pixel(i, line[i][0], line[i][1], line[i][2])
            blinkt.show()
        time.sleep(0.2)

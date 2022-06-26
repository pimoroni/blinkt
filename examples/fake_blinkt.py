"""fake_blink terminal simulation of blinkt, to use rename to blinkt.py and place in same directory as blinkt program"""
import sys
import pantilthat
import atexit
import signal

_clear_on_exit = True
_true_color    = True
NUM_PIXELS     = 8
pixels         = [(0,0,0,1)] * NUM_PIXELS

def _exit():
    if _clear_on_exit:
        clear()
        show()
    else:
        print("")


def set_brightness(brightness):
    pass

def clear():
    pixels[:] = [(0,0,0,1)] * NUM_PIXELS


def show():
    sys.stdout.write(" ")
    for (r,g,b,_) in pixels:
        if _true_color:
            sys.stdout.write("\033[48;2;%d;%d;%dm   " % (r,g,b))
        else:
            if r==g==b:
                col = 232 + r*24//256
            else:
                col = 16 + (b*6//256) + (g*6//256)*6 + (r*6//256)*36
            sys.stdout.write("\033[48;5;%dm   " % col)
    sys.stdout.write("\033[0m\r")
    sys.stdout.flush()


def set_all(r, g, b, brightness=None):
    global _brightness
    if brightness is not None:
        _brightness = brightness
    pixels[:] = [(r, g, b, 1)] * NUM_PIXELS


def set_pixel(x, r, g, b, brightness=None):
    global _brightness
    if brightness is not None:
        _brightness = brightness
    pixels[x] = (r, g, b, 1)


def get_pixel(x):
    return pixels[x]


def set_clear_on_exit(value=True):
    """Set whether Blinkt! should be cleared upon exit

    By default Blinkt! will turn off the pixels on exit, but calling::

        blinkt.set_clear_on_exit(False)

    Will ensure that it does not.

    :param value: True or False (default True)
    """
    global _clear_on_exit
    _clear_on_exit = value


# Module Initialisation
atexit.register(_exit)

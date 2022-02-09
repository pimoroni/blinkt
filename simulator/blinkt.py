import sys
import subprocess
import pickle
import os
import atexit
import signal


__version__ = '0.1.2'


NUM_PIXELS = 8
BRIGHTNESS = 7

pixels = [[0, 0, 0, BRIGHTNESS]] * NUM_PIXELS

_process = None
_clear_on_exit = True


def _exit():
    global _process, _clear_on_exit
    if not _clear_on_exit:
        sys.stdout.write("Ctrl+C to exit...\n")
        sys.stdout.flush()
        signal.pause()
    if _process is not None:
        _process.kill()


def set_brightness(brightness):
    """Set the brightness of all pixels.

    :param brightness: Brightness: 0.0 to 1.0

    """
    if brightness < 0 or brightness > 1:
        raise ValueError('Brightness should be between 0.0 and 1.0')

    for x in range(NUM_PIXELS):
        pixels[x][3] = int(31.0 * brightness) & 0b11111


def clear():
    """Clear the pixel buffer."""
    for x in range(NUM_PIXELS):
        pixels[x][0:3] = [0, 0, 0]


def show():
    """Output the buffer to Blinkt!."""
    global _process

    if _process is None:
        _process = subprocess.Popen(
            [sys.executable, os.path.dirname(os.path.abspath(
                __file__)) + '/blinkt_simulator.py'],
            stdin=subprocess.PIPE)
        atexit.register(_exit)

    try:
        pickle.dump(pixels, _process.stdin)
        _process.stdin.flush()
    except OSError:
        sys.stderr.write('Lost connection to Blinkt! simulator\n')
        sys.stderr.flush()
        sys.exit(-1)


def set_all(r, g, b, brightness=None):
    """Set the RGB value and optionally brightness of all pixels.

    If you don't supply a brightness value,
    the last value set for each pixel be kept.

    :param r: Amount of red: 0 to 255
    :param g: Amount of green: 0 to 255
    :param b: Amount of blue: 0 to 255
    :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)

    """
    for x in range(NUM_PIXELS):
        set_pixel(x, r, g, b, brightness)


def get_pixel(x):
    """Get the RGB and brightness value of a specific pixel.

    :param x: The horizontal position of the pixel: 0 to 7

    """
    r, g, b, brightness = pixels[x]
    brightness /= 31.0

    return r, g, b, round(brightness, 3)


def set_pixel(x, r, g, b, brightness=None):
    """Set the RGB value, and optionally brightness, of a single pixel.

    If you don't supply a brightness value, the last value will be kept.

    :param x: The horizontal position of the pixel: 0 to 7
    :param r: Amount of red: 0 to 255
    :param g: Amount of green: 0 to 255
    :param b: Amount of blue: 0 to 255
    :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)

    """
    if brightness is None:
        brightness = pixels[x][3]
    else:
        brightness = int(31.0 * brightness) & 0b11111

    pixels[x] = [int(r) & 0xff, int(g) & 0xff, int(b) & 0xff, brightness]


def set_clear_on_exit(value=True):
    """Set whether Blinkt! should be cleared upon exit.

    By default Blinkt! will turn off the pixels on exit, but calling::

        blinkt.set_clear_on_exit(False)

    Will ensure that it does not.

    :param value: True or False (default True)

    """
    global _clear_on_exit
    _clear_on_exit = value

"""Library for the Pimoroni Blinkt! - 8-pixel APA102 LED display."""
import atexit
import time

from gpio import GPIOPin


__version__ = '0.1.2'

DAT = GPIOPin(23)
CLK = GPIOPin(24)
NUM_PIXELS = 8
BRIGHTNESS = 7

atexit.register(DAT.cleanup)
atexit.register(CLK.cleanup)

pixels = [[0, 0, 0, BRIGHTNESS]] * NUM_PIXELS

sleep_time = 0

_clear_on_exit = True


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


def _write_byte(byte):
    for x in range(8):
        DAT.write(byte & 0b10000000)
        CLK.write(1)
        time.sleep(sleep_time)
        byte <<= 1
        CLK.write(0)
        time.sleep(sleep_time)


# Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
# for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
def _eof():
    DAT.write(0)
    for x in range(36):
        CLK.write(1)
        time.sleep(sleep_time)
        CLK.write(0)
        time.sleep(sleep_time)


def _sof():
    DAT.write(0)
    for x in range(32):
        CLK.write(1)
        time.sleep(sleep_time)
        CLK.write(0)
        time.sleep(sleep_time)


def show():
    """Output the buffer to Blinkt!."""

    t_start = time.time()
    _sof()

    for pixel in pixels:
        r, g, b, brightness = pixel
        _write_byte(0b11100000 | brightness)
        _write_byte(b)
        _write_byte(g)
        _write_byte(r)

    _eof()
    print(f"Update took: {time.time() - t_start}")


def set_all(r, g, b, brightness=None):
    """Set the RGB value and optionally brightness of all pixels.

    If you don't supply a brightness value, the last value set for each pixel be kept.

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

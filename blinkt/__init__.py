"""Library for the Pimoroni Blinkt! - 8-pixel APA102 LED display."""
import atexit
import time

import gpiod
import gpiodevice
from gpiod.line import Direction, Value

__version__ = '0.1.2'

OUTL = gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
PLATFORMS = {
        "Radxa ROCK 5B": {"dat": ("PIN_16", OUTL), "clk": ("PIN_18", OUTL)},
        "Raspberry Pi 5": {"dat": ("PIN16", OUTL), "clk": ("PIN18", OUTL)},
        "Raspberry Pi 4": {"dat": ("GPIO23", OUTL), "clk": ("GPIO24", OUTL)}
}
NUM_PIXELS = 8
BRIGHTNESS = 7

pixels = [[0, 0, 0, BRIGHTNESS]] * NUM_PIXELS

sleep_time = 0

clk_lines = None
clk_line = None
dat_lines = None
dat_line = None
_clear_on_exit = True

gpiodevice.friendly_errors = True


def _exit():
    if _clear_on_exit:
        clear()
        show()


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
        dat_lines.set_value(dat_line, Value.ACTIVE if (byte & 0b10000000) else Value.INACTIVE)
        clk_lines.set_value(clk_line, Value.ACTIVE)
        time.sleep(sleep_time)
        byte <<= 1
        clk_lines.set_value(clk_line, Value.INACTIVE)
        time.sleep(sleep_time)


# Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
# for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
def _eof():
    dat_lines.set_value(dat_line, Value.INACTIVE)
    for x in range(36):
        clk_lines.set_value(clk_line, Value.ACTIVE)
        time.sleep(sleep_time)
        clk_lines.set_value(clk_line, Value.INACTIVE)
        time.sleep(sleep_time)


def _sof():
    dat_lines.set_value(dat_line, Value.INACTIVE)
    for x in range(32):
        clk_lines.set_value(clk_line, Value.ACTIVE)
        time.sleep(sleep_time)
        clk_lines.set_value(clk_line, Value.INACTIVE)
        time.sleep(sleep_time)


def set_pins(pin_dat, pin_clk):
    global clk_lines, dat_lines, dat_line, clk_line

    try:
        chip = gpiodevice.find_chip_by_pins((pin_dat, pin_clk))
        dat_line = chip.line_offset_from_id(pin_dat)
        clk_line = chip.line_offset_from_id(pin_clk)
        dat_lines = clk_lines = chip.request_lines(consumer="blinkt", config={
            dat_line: OUTL,
            clk_line: OUTL
        })
        return
    except SystemExit:
        pass

    chip_dat = gpiodevice.find_chip_by_pins(pin_dat)
    dat_line = chip_dat.line_offset_from_id(pin_dat)
    dat_lines = chip_dat.request_lines(consumer="blinkt-dat", config={dat_line: OUTL})

    chip_clk = gpiodevice.find_chip_by_pins(pin_clk)
    clk_line = chip_clk.line_offset_from_id(pin_clk)
    clk_lines = chip_clk.request_lines(consumer="blinkt-clk", config={clk_line: OUTL})


def default_pins():
    global clk_lines, dat_lines, dat_line, clk_line

    dat, clk = gpiodevice.get_pins_for_platform(PLATFORMS)
    dat_lines, dat_line = dat
    clk_lines, clk_line = clk


def show():
    """Output the buffer to Blinkt!."""
    if not clk_line:
        default_pins()

    atexit.unregister(_exit)
    atexit.register(_exit)

    _sof()

    for pixel in pixels:
        r, g, b, brightness = pixel
        _write_byte(0b11100000 | brightness)
        _write_byte(b)
        _write_byte(g)
        _write_byte(r)

    _eof()


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

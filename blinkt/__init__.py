"""Library for the Pimoroni Blinkt! - 8-pixel APA102 LED display."""
import atexit
import glob
import time

import gpiod
from gpiod.line import Direction, Value

__version__ = '0.1.2'

DAT = 23
CLK = 24
NUM_PIXELS = 8
BRIGHTNESS = 7
RPI_GPIO_LABELS = [
    "pinctrl-rp1", # Pi 5 - Bookworm, /dev/gpiochip4 maybe
    "pinctrl-bcm2711" # Pi 4, Pi 400 - Bullseye and Ubuntu, /dev/gpiochip0 maybe
]

pixels = [[0, 0, 0, BRIGHTNESS]] * NUM_PIXELS

sleep_time = 0

gpio_lines = None
_clear_on_exit = True


def _exit():
    if _clear_on_exit:
        clear()
        show()
    gpio_lines.release()


def check_pins_available(chip, pins):
    """Check if a list of pins are in use on a given gpiochip device.

    Raise a RuntimeError with a friendly list of in-use pins and their consumer if
    any are in used.
    """
    err = []
    for (label, pin) in pins.items():
        pin_info = chip.get_line_info(pin)
        if pin_info.used:
            err.append(f" ⚠️  {label} (GPIO {pin}) is currently claimed by {pin_info.consumer}")
    if len(err):
        err.insert(0, "some pins we need are in use:")
        raise RuntimeError("\n".join(err))


def find_gpiochip(labels, pins=None):
    """Try to find a /dev/gpiochipN device matching one of a set of labels.

    Raise a RuntimeError with a friendly error digest if one is not found.
    """
    err = []
    for path in glob.glob("/dev/gpiochip*"):
        if gpiod.is_gpiochip_device(path):
            try:
                label = gpiod.Chip(path).get_info().label
            except PermissionError:
                err.append(f" ⚠️  {path}: Permission error!")
                continue
            if label in labels:
                chip = gpiod.Chip(path)
                if pins is not None:
                    check_pins_available(chip, pins)
                return chip
            else:
                err.append(f" ⚠️  {path}: This is not the GPIO we're looking for! ({label})") 
    err.insert(0, "Compatible /dev/gpiochipN device not found!")
    raise RuntimeError("\n".join(err))


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
        gpio_lines.set_value(DAT, Value.ACTIVE if (byte & 0b10000000) else Value.INACTIVE)
        gpio_lines.set_value(CLK, Value.ACTIVE)
        time.sleep(sleep_time)
        byte <<= 1
        gpio_lines.set_value(CLK, Value.INACTIVE)
        time.sleep(sleep_time)


# Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
# for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
def _eof():
    gpio_lines.set_value(DAT, Value.INACTIVE)
    for x in range(36):
        gpio_lines.set_value(CLK, Value.ACTIVE)
        time.sleep(sleep_time)
        gpio_lines.set_value(CLK, Value.INACTIVE)
        time.sleep(sleep_time)


def _sof():
    gpio_lines.set_value(DAT, Value.INACTIVE)
    for x in range(32):
        gpio_lines.set_value(CLK, Value.ACTIVE)
        time.sleep(sleep_time)
        gpio_lines.set_value(CLK, Value.INACTIVE)
        time.sleep(sleep_time)


def show():
    """Output the buffer to Blinkt!."""
    global gpio_lines

    if not gpio_lines:
        chip = find_gpiochip(RPI_GPIO_LABELS, {"Data": DAT, "Clock": CLK})
        gpio_lines = chip.request_lines(
            consumer="blinkt",
            config={
                DAT: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
                CLK: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
            }
        )
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

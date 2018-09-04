"""Test Blinkt! basis initialisation."""
import mock
import sys
from tools import GPIO


def test_setup():
    """Test init succeeds and GPIO pins are setup."""
    gpio = GPIO()
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi'].GPIO = gpio
    sys.modules['RPi.GPIO'] = gpio
    import blinkt
    blinkt.show()

    assert gpio.pin_modes[blinkt.DAT] == gpio.OUT
    assert gpio.pin_modes[blinkt.CLK] == gpio.OUT

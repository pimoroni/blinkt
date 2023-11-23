"""Test Blinkt! basic initialisation."""
import mock
import pytest


def test_setup(gpiod):
    """Test init succeeds and GPIO pins are set up."""
    import blinkt
    with pytest.raises((RuntimeError, SystemExit)):
        blinkt.show()


def test_set_pins(gpiod):
    import blinkt

    with pytest.raises((RuntimeError, SystemExit)):
        blinkt.set_pins("PIN1", "PIN2")


def test_set_pixel(gpiod):
    import blinkt
    blinkt.set_brightness(1.0)

    blinkt.set_pixel(0, 255, 0, 0)
    blinkt.set_pixel(1, 0, 255, 0)
    blinkt.set_pixel(2, 0, 0, 255)

    assert blinkt.get_pixel(0)[0:3] == (255, 0, 0)
    assert blinkt.get_pixel(1)[0:3] == (0, 255, 0)
    assert blinkt.get_pixel(2)[0:3] == (0, 0, 255)


def test_set_all_and_clear(gpiod):
    import blinkt
    blinkt.set_brightness(1.0)

    blinkt.set_all(1, 2, 3, 0)

    for x in range(blinkt.NUM_PIXELS):
        assert blinkt.get_pixel(0)[0:3] == (1, 2, 3)

    blinkt.clear()

    for x in range(blinkt.NUM_PIXELS):
        assert blinkt.get_pixel(0)[0:3] == (0, 0, 0)


def test_brightness(gpiod):
    import blinkt
    blinkt.set_brightness(1.0)

    assert blinkt.pixels[0][3] == 0b11111

    with pytest.raises(ValueError):
        blinkt.set_brightness(1.5)

    with pytest.raises(ValueError):
        blinkt.set_brightness(-1)


def test_show(gpiod, gpiod_request):
    import blinkt

    blinkt.clk_lines = gpiod_request
    blinkt.dat_lines = gpiod_request

    blinkt.dat_line = 0
    blinkt.clk_line = 1

    blinkt.show()

    gpiod_request.set_value.assert_has_calls((
        mock.call(0, blinkt.Value.INACTIVE),  # Dat line low
        mock.call(1, blinkt.Value.ACTIVE),    # Clock pin high
        mock.call(1, blinkt.Value.INACTIVE)   # Clock pin low
    ))
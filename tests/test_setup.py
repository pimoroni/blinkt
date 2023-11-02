"""Test Blinkt! basic initialisation."""
import pytest


def test_setup(gpiod):
    """Test init succeeds and GPIO pins are set up."""
    import blinkt
    with pytest.raises((RuntimeError, SystemExit)):
        blinkt.show()

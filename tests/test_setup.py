"""Test Blinkt! basic initialisation."""

def test_setup(gpiod):
    """Test init succeeds and GPIO pins are set up."""
    import blinkt
    blinkt.show()
    gpiod.request_lines.assert_called_once()

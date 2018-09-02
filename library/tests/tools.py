# noqa D100
class GPIO:
    """Mock RPi.GPIO class.

    Stubs out enough of RPi.GPIO to validate pin states are set correctly.

    """

    BCM = 1
    OUT = 1
    IN = 1

    def __init__(self):              # noqa D100
        self.pin_modes = {}
        self.pin_states = {}

    def output(self, pin, value):    # noqa D100
        self.pin_states[pin] = value

    def setmode(self, mode):         # noqa D100
        pass

    def setwarnings(self, mode):     # noqa D100
        pass

    def setup(self, pin, mode):      # noqa D100
        self.pin_modes[pin] = mode

    def cleanup(self):               # noqa D100
        pass

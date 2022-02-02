# Basic example for controlling the Blinkt LED colours via Anvil
# Learn more at: https://anvil.works/
#
# Dependencies:
#
# python3 -m pip install blinkt colour anvil-uplink
#
# Run this example with:
#
# python3 anvil-colour-control.py
#
# You'll be prompted for an email address to set up the web control
# portion of this example.
#
# Check your email, click the link and- when the app has loads -
# hit the "Run" button at the top to start remote-controlling
# your Blinkt!

import blinkt
from colour import Color

from anvil.app_creator import create_app
import anvil.server

# Create the Blinkt demo app in your Anvil account
app = create_app("blinkt")

# Define functions that can be called from your Anvil app on the web
anvil.server.connect(app.uplink_key)


@anvil.server.callable
def set_color(color_string):
    print("Setting LEDs to {}".format(color_string))
    c = Color(color_string)
    blinkt.set_all(c.red * 255, c.green * 255, c.blue * 255, 1.0)
    blinkt.show()


@anvil.server.callable
def clear():
    print("Clearing LEDs")
    blinkt.clear()
    blinkt.show()


# Display the URL where you can control the Blinkt LEDS
print("Control your Blinkt LEDs at {}".format(app.origin))
print("Press Ctrl-C to exit")

# Keep the script running until the user exits with Ctrl-C
anvil.server.wait_forever()

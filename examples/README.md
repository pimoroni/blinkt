## Examples

The examples in this directory should just work with Blinkt!, although you'll need to add Twitter developer access tokens and secrets in the `twitter_monitor.py` example. You can get these at [https://dev.twitter.com/](https://dev.twitter.com/), after setting up a new application. Where noted, the instructions for adding keys / installing modules are in the code itself.

The examples in the `extra_examples` folder are designed to work with other pHATs and HATs, so be aware of that before trying them.

## List of examples with basic instructions

- 1d_tetris - shows randomly coloured lights falling into place and clearing occasionally. No input needed. Offline.
- binary_clock - shows time in hours, minutes, and seconds using the local time from your Pi. No input needed. Offline.
- binary_clock_meld - shows time in hours (red), minutes (green) and seconds (blue) using local time from your Pi. No input needed. Offline.
- blinkt_thermo - draws a graph of the temperature based on the openweather data for whatever city you set it to. Needs keys and ID from openweathermap.org. Online.
- candle - flickers the pixels in a candle effect. May require a numpy install. Offline.
- cheerlights - reads twitter for any tweets with the hashtag "cheerlights" and a colour. Changes all the pixels to that colour. Online.
- cpu_load - shows a graph of cpu usage as a percentage. May require a psutil install. Offline.
- cpu_temp - shows a graph of the cpu temperature as a percentage. Offline.
- gradient_graph - pulses a rainbow across the blinkt and back again. Offline.
- graph - pulses a magenta graph across the blinkt and back again. Offline.
- larson - remember Knight Rider? Offline.
- larson_hue - same as larson, but in rainbow colours! Offline.
- mem_load - shows a graph of the memory load on the Pi as a percentage. Offline.
- morse_code - shows a message in [warning: flashing] morse code. Change line 40 if you want a different message. Offline.
- mqtt - send controls remotely to your Blinkt. May require a paho-mqtt install. Requires setup on another machine as per instructions in the code. Online.
- pulse - pulses cyan light from the centre pixels to outer edges. Offline.
- rainbow - shows a gently moving rainbow along the blinkt. Yay, rainbows! Offline.
- random_blink - blinks yellow lights at random, like paparazzi in a crowd. Change colour on line 14 if you like. Offline.
- random_blink_colours - imagine if the paparazzi were carrying pastel unicorns. Offline.
- resistor_clock - shows the time in pairs of pixels, using resistor codes. Brown light (representing a 1) is a bit hard to see. Offline.
- rgb - Run this one a bit differently. Type python rgb.py and then three values, eg python rgb.py 10 90 80 will make it turn on cyan, python rgb.py 100 0 0 will make it turn on red. Offline.
- setup.cfg is NOT an example.
- solid_colours - Flashes red, green, blue on repeat. You can change the colours on lines 14, 17 and 20. Offline.
- twitter_monitor - Will show a notification when the hashtag of your choice (line 48) is mentioned on Twitter. You need to add consumer key, consumer secret, access token and access secret (see instructions at top of this document). Online.

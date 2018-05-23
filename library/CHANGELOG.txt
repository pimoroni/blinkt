0.1.2
-----

* BugFix: Added sleep to data output, see: https://github.com/pimoroni/blinkt/issues/62

0.1.1
-----

* New: Added `get_pixel` to return colour and brightness of a single pixel

0.1.0
-----

* Removed try/except from RPi.GPIO import, output was misleading at best
* Reverted default behaviour of clear on exit

0.0.9
-----

* Added set_all method to set all pixels
* Changed default behaviour of clear on exit to reduce module side-effects
* Move GPIO initialisation to show() to reduce module side-effects

0.0.8
-----

* Tweaked some methods to show intent as implementation detail only
* Added docstrings detailing public methods

0.0.7
-----

* Fixed bug with APA102 pixels that have a small, black die (vs the larger, paler one)

0.0.6
-----

* set_clear_on_exit now method

0.0.5
-----

* Range clamping and coercion to integers

0.0.4
-----

* Various bug fixes

0.0.3
-----

* Switch to Python

0.0.2
-----

* Bug fixes for C Library

0.0.1
-----

* Original C Library


.. role:: python(code)
   :language: python

.. toctree::
   :titlesonly:
   :maxdepth: 0

Welcome
-------

This documentation will guide you through the methods available in the Blinkt! python library.

Blinkt! is a tiny Raspberry Pi add-on with 8, APA102, RGB LEDs which you can drive
independently for notifications, lighting effects, animation effects and more!

* More information - https://shop.pimoroni.com/products/blinkt
* Get the code - https://github.com/pimoroni/blinkt
* Get started - https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-blinkt
* Get help - http://forums.pimoroni.com/c/support

At A Glance
-----------

.. automoduleoutline:: blinkt
   :members:

Set A Single Pixel
------------------

The bread and butter of Blintk! is setting pixels. You can set any of the 8 pixels
on your Blinkt! to one of around 16 million colours!

The :python:`brightness` argument is completely optional. Omit it to keep the last
brightness value set for that particular pixel.

.. automodule:: blinkt
   :noindex:
   :members: set_pixel

Set All Pixels
--------------

Sometimes you need to set all the pixels to the same colour. This convinience method
does just that!

.. automodule:: blinkt
   :noindex:
   :members: set_all

Show
----

None of your pixels will appear on Blinkt! until you :python:`show()` them. This method writes
all the pixel data out to your device.

.. automodule:: blinkt
   :noindex:
   :members: show

Clear
-----

Exactly the same as calling :python:`set_all(0,0,0)`, clear sets all the pixels to black.

You must also call :python:`show()` if you want to turn Blinkt! off.

.. automodule:: blinkt
   :noindex:
   :members: clear

Enable/Disable Clear On Exit
----------------------------

Sometimes you want a script that runs and quits, leaving a pattern up on Blinkt!

.. automodule:: blinkt
   :noindex:
   :members: set_clear_on_exit

Get A Single Pixel
------------------

.. automodule:: blinkt
   :noindex:
   :members: get_pixel

Constants
---------

Blinkt! has 8 pixels. Simple. Use the constant :python:`blinkt.NUM_PIXELS` when you're iterating over pixels,
so you can avoid a *magic number* in your code.

:python:`blinkt.NUM_PIXELS = 8`

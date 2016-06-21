#Blinkt

Eight super-bright RGB LED indicators, ideal for adding visual notifications to your Raspberry Pi on their own or on a pHAT stacking header.

Available from Pimoroni: https://shop.pimoroni.com/products/blinkt

#Usage

The two Blinkt methods you'll most commonly use are `set_pixel` and `show`. Here's a simple example:

```
from blinkt import set_pixel, show

set_pixel(0,255,0,0)
show()
```

`set_pixel` takes an optional forth parameter; the brightness from 0.0 to 1.0.

You can also change the brightness with `set_brightness` from 0.0 to 1.0, for example:

```
from blinkt import set_brightness

set_brightness(0.5)
```

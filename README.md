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

#Examples

The examples in the `examples` folder should just work with Blinkt!, although you'll need to add Twitter developer access tokens and secrets in the `twitter_monitor.py` example. You can get these at [https://dev.twitter.com/](https://dev.twitter.com/), after setting up a new application.

The examples in the `extra_examples` folder are designed to work with other pHATs and HATs, so be aware of that before trying them.

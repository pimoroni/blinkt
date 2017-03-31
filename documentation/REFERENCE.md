# Blinkt Function Reference

The two Blinkt methods you'll most commonly use are `set_pixel` and `show`. Here's a simple example:

```
from blinkt import set_pixel, show

set_pixel(0,255,0,0)
show()
```

`set_pixel` takes an optional fifth parameter; the brightness from 0.0 to 1.0.

`set_pixel(pixel_no, red, green, blue, brightness)`

You can also change the brightness with `set_brightness` from 0.0 to 1.0, for example:

```
from blinkt import set_brightness

set_brightness(0.5)
show()
```

Additionally, there exists a helper function `set_all` which allows you to set all pixels to the same color and brightness. The `brightness` parameter is just like the one in `set_pixel`: it's optional and ranges from 0.0 to 1.0.

`set_all(red, green, blue, brightness)`

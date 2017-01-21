![Blinkt!](blinkt-logo.png)

Eight super-bright RGB LED indicators, ideal for adding visual notifications to your Raspberry Pi on their own or on a pHAT stacking header.

Available from Pimoroni: https://shop.pimoroni.com/products/blinkt

##Installation

**Full install ( recommended ):**

We've created a super-easy installation script that will install all pre-requisites and get your Blinkt! up and running in a jiffy. To run it fire up Terminal which you'll find in Menu -> Accessories -> Terminal on your Raspberry Pi desktop like so:

![Finding the terminal](terminal.jpg)

In the new terminal window type:

```bash
curl -sS https://get.pimoroni.com/blinkt | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/blinkt`.

**Library install for Python 3:**

on Raspbian:

```bash
sudo apt-get install python3-blinkt
```
other environments:

```bash
sudo pip3 install blinkt
```

**Library install for Python 2:**

on Raspbian:

```bash
sudo apt-get install python-blinkt
```
other environments:

```bash
sudo pip2 install blinkt
```

##Usage

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

##Documentation & Support

* Getting started - https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-blinkt
* Function reference - http://docs.pimoroni.com/blinkt/
* GPIO Pinout - https://pinout.xyz/pinout/blinkt
* Get help - http://forums.pimoroni.com/c/support

##Examples

The examples in the `examples` folder should just work with Blinkt!, although you'll need to add Twitter developer access tokens and secrets in the `twitter_monitor.py` example. You can get these at [https://dev.twitter.com/](https://dev.twitter.com/), after setting up a new application.

###HomeKit Example

Based on the Using Mote with Homekit and Siri tutorial (https://learn.pimoroni.com/tutorial/sandyj/using-mote-with-homekit-and-siri) and modified to support Blinkt by Phil Robinson (https://github.com/philprobinson84/blinkt).

Borrow the easy setup of Flask and Mote from the aforementioned guide:
```bash
curl -sS get.pimoroni.com/mote | bash
```
Next, run:
```bash
sudo python homekit.py
```
Then, open another terminal window or tab, and type the following to test that our API is working as expected.
```bash
curl -i http://127.0.0.1:5000/blinkt/api/v1.0/on
```
That should have just turned your blinkt on! You should also be able to do this remotely, on another machine, replacing the 127.0.0.1 part of the URL with the IP address of the machine on which your API is running. You should also be able to do this in your web browser rather than with curl in the terminal.

Try typing the following to change the colour of the blinkt LEDs to red.
```bash
curl -i http://127.0.0.1:5000/blinkt/api/v1.0/set/FF0000
```
Set brightness (doesn't change the colour):
```bash
curl -i http://127.0.0.1:5000/blinkt/api/v1.0/brightness/50
```
N.B. Homebridge, and therefore our API, uses a brightness value of 0 to 100, which is translated by homekit.py to the range 0 to 1 required by the blinkt Python library.

Now for Homebridge installation and setup.

Open a terminal, and type the following to upgrade to the latest and greatest version of Node.js:
```bash
sudo apt-get update
sudo apt-get upgrade
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
```
Before we install homebridge, we'll also need to install a couple of dependencies. Type the following to install them:
```bash
sudo apt-get install libavahi-compat-libdnssd-dev
```
Now, we can install homebridge itself, as well as the homebridge-better-http-rgb plugin:
```bash
sudo npm install -g --unsafe-perm homebridge
sudo npm install -g --unsafe-perm homebridge-better-http-rgb
```
Now that everything is installed, we have to do a couple more things to configure homebridge correctly. homebridge is configured through a .json file that must be put into the /home/pi/.homebridge/ directory. We'll create that directory now:
```bash
mkdir /home/pi/.homebridge
```
Now we'll copy the example JSON file over, change directory to wherever the blinkt examples reside, then:
```bash
cp homekit-sample-config.json /home/pi/.homebridge/config.json
```
To run everything, first we start the Python script:
```bash
sudo python homekit.py
```
Then in another teminal just type:
```bash
homebridge
```
If you're running iOS 10 or above, you can now open the Home app and the device will be shown, allowing you to change colour, brightness and other goodness. Enjoy!

###Extra Examples
The examples in the `examples/extra_examples` folder are designed to work with other pHATs and HATs, so be aware of that before trying them.

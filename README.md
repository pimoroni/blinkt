![Blinkt!](blinkt-logo.png)

[![Build Status](https://travis-ci.com/pimoroni/blinkt.svg?branch=master)](https://travis-ci.com/pimoroni/blinkt)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/blinkt/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/blinkt?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/blinkt.svg)](https://pypi.python.org/pypi/blinkt)
[![Python Versions](https://img.shields.io/pypi/pyversions/blinkt.svg)](https://pypi.python.org/pypi/blinkt)

https://shop.pimoroni.com/products/blinkt

Eight super-bright RGB LED indicators, ideal for adding visual notifications to your Raspberry Pi on their own or on a pHAT stacking header.

## Installing

### Full install (recommended):

We've created an easy installation script that will install all pre-requisites and get your Blinkt!
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
curl https://get.pimoroni.com/blinkt | bash
```

Alternatively, on Raspbian, you can download the `pimoroni-dashboard` and install your product by browsing to the relevant entry:

```bash
sudo apt-get install pimoroni
```
(you will find the Dashboard under 'Accessories' too, in the Pi menu - or just run `pimoroni-dashboard` at the command line)

If you choose to download examples you'll find them in `/home/pi/Pimoroni/blinkt/`.

### Manual install:

#### Library install for Python 3:

on Raspbian:

```bash
sudo apt-get install python3-blinkt
```

other environments: 

```bash
sudo pip3 install blinkt
```

#### Library install for Python 2:

on Raspbian:

```bash
sudo apt-get install python-blinkt
```

other environments: 

```bash
sudo pip2 install blinkt
```

### Development:

If you want to contribute, or like living on the edge of your seat by having the latest code, you should clone this repository, `cd` to the library directory, and run:

```bash
sudo python3 setup.py install
```
(or `sudo python setup.py install` whichever your primary Python environment may be)

## Documentation & Support

* Guides and tutorials - https://learn.pimoroni.com/blinkt
* Function reference - http://docs.pimoroni.com/blinkt/
* GPIO Pinout - https://pinout.xyz/pinout/blinkt
* Get help - http://forums.pimoroni.com/c/support

## Unofficial / Third-party libraries

* Golang library & examples by [Alex Ellis](https://www.alexellis.io) - https://github.com/alexellis/blinkt_go_examples
* Java library by Jim Darby - https://github.com/hackerjimbo/PiJava
* Java library by @HoldYourWaffle - https://github.com/HoldYourWaffle/blinkt4j

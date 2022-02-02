#!/usr/bin/env python

from sys import exit
import argparse
import time

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requires the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")

import blinkt


MQTT_SERVER = "iot.eclipse.org"
MQTT_PORT = 1883
MQTT_TOPIC = "pimoroni/blinkt"

# Set these to use authorisation
MQTT_USER = None
MQTT_PASS = None

description = """\
MQTT Blinkt! Control

This example uses public MQTT messages from {server} on port {port} to control Blinkt!

It will monitor the {topic} topic by default, and understands the following messages:

rgb,<pixel>,<r>,<g>,<b> - Set a single pixel to an RGB colour. Example: rgb,1,255,0,255
clr - Clear Blinkt!
bri,<val> - Set global brightness (for val in range 0.0-1.0)

You can use the online MQTT tester at http://www.hivemq.com/demos/websocket-client/ to send messages.

Use {server} as the host, and port 80 (Eclipse's websocket port). Set the topic to topic: {topic}
""".format(
    server=MQTT_SERVER,
    port=MQTT_PORT,
    topic=MQTT_TOPIC
)
parser = argparse.ArgumentParser(description = description, formatter_class = argparse.RawDescriptionHelpFormatter)
parser.add_argument( '-H', '--host', default = MQTT_SERVER,
                        help = 'MQTT broker to connect to' )
parser.add_argument( '-P', '--port', default = MQTT_PORT, type = int,
                        help = 'port on MQTT broker to connect to' )
parser.add_argument( '-T', '--topic', action = 'append',
                        help = 'MQTT topic to subscribe to; can be repeated for multiple topics' )
parser.add_argument( '-u', '--user',
                        help = 'MQTT broker user name' )
parser.add_argument( '-p', '--pass', dest = 'pw',
                        help = 'MQTT broker password' )
parser.add_argument( '-q', '--quiet', default = False, action = 'store_true',
                        help = 'Minimal output (eg for running as a daemon)' )
parser.add_argument( '-g', '--green-hack', default = False, action = 'store_true',
                        help = 'Apply hack to green channel to improve colour saturation' )
parser.add_argument( '--timeout', default = '0',
                        help = 'Pixel timeout(s).  Pixel will blank if last update older than X seconds.  May be a single number or comma-separated list.  Use 0 for no timeout' )
parser.add_argument( '-D', '--daemon', metavar='PIDFILE',
                        help = 'Run as a daemon (implies -q)' )
args = parser.parse_args()

# Get timeout list into expected form
args.timeout = args.timeout.split( ',' )
if len(args.timeout) == 1:
    args.timeout = args.timeout * blinkt.NUM_PIXELS
elif len(args.timeout) != blinkt.NUM_PIXELS:
    exit("--timeout list must be %s elements long" % (blinkt.NUM_PIXELS,))
try:
    args.timeout = [int(x) for x in args.timeout]
except ValueError as e:
    exit("Bad timeout value: %s" % (e,))
args.timeout = [x and x or None for x in args.timeout]
args.min_timeout = min(args.timeout)

if args.daemon:
    import signal
    try:
        import daemon
    except ImportError:
        exit("--daemon requires the daemon module.  Install with: sudo pip install python-daemon")
    try:
        import lockfile.pidlockfile
    except ImportError:
        exit("--daemon requires the lockfile module.  Install with: sudo pip install lockfile")
if not args.topic:
    args.topic = [MQTT_TOPIC]

class PixelClient( mqtt.Client ):
    def __init__( self, prog_args, *args, **kwargs ):
        super( PixelClient, self ).__init__( *args, **kwargs )
        self.args = prog_args
        self.update_time = [None] * blinkt.NUM_PIXELS
        self.on_connect = self.on_connect
        self.on_message = self.on_message

        blinkt.set_clear_on_exit()
        # Some stuff doesn't get set up until the first time show() is called
        blinkt.show()

        if self.args.user is not None and self.args.pw is not None:
            self.username_pw_set(username=self.args.user, password=self.args.pw)
        self.connect(self.args.host, self.args.port, 60)

    def cmd_clear( self ):
        blinkt.clear()
        blinkt.show()

    def cmd_brightness( self, bri ):
        try:
            bri = float(bri)
        except ValueError:
            print("Malformed command: ", str(msg.payload))
            return
        blinkt.set_brightness(bri)
        blinkt.show()

    def cmd_rgb( self, pixel, data ):
        try:
            if pixel == "*":
                pixel = None
            else:
                pixel = int(pixel)
                if pixel > 7:
                    print("Pixel out of range: " + str(pixel))
                    return

            r, g, b = [int(x) & 0xff for x in data]
            if self.args.green_hack:
                # Green is about twice the luminosity for a given value
                # than red or blue, so apply a hackish linear compensation
                # here taking care of corner cases at 0 and 255.  To do it
                # properly, it should really be a curve but this approximation
                # is quite a lot better than nothing.
                if r not in [0,255]:
                    r = r + 1
                if g not in [0]:
                    g = g/2 + 1
                if b not in [0,255]:
                    b = b + 1

            if not self.args.quiet:
                print('rgb', pixel, r, g, b)

        except ValueError:
            print("Malformed command: " + str(msg.payload))
            return

        if pixel is None:
            for x in range(blinkt.NUM_PIXELS):
                blinkt.set_pixel(x, r, g, b)
                self.update_time[x] = time.time()
        else:
            blinkt.set_pixel(pixel, r, g, b)
            self.update_time[pixel] = time.time()

        blinkt.show()

    def on_connect(self, client, userdata, flags, rc):
        if not self.args.quiet:
            print("Connected to {s}:{p} listening for topics {t} with result code {r}.\nSee {c} --help for options.".format(s = self.args.host, p = self.args.port, t = ', '.join(self.args.topic), r = rc, c = parser.prog))

        for topic in self.args.topic:
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):

        data = msg.payload.split(',')
        command = data.pop(0)

        if command == "clr" and len(data) == 0:
            self.cmd_clear()
            return

        if command == "bri" and len(data) == 1:
            self.cmd_brightness( data[0] )
            return

        if command == "rgb" and len(data) == 4:
            self.cmd_rgb( data[0], data[1:] )
            return

    def blank_timed_out_pixels( self ):
        now = time.time()
        to_upt_pairs = zip(self.args.timeout,self.update_time)
        for pixel, (to, uptime) in enumerate(to_upt_pairs):
            if to is not None and uptime is not None and uptime < now - to:
                blinkt.set_pixel( pixel, 0, 0, 0 )
                self.update_time[pixel] = None
        blinkt.show()

    def loop( self, timeout = 1.0, max_packets = 1 ):
        self.blank_timed_out_pixels()
        return super( PixelClient, self ).loop( timeout, max_packets )


def sigterm( signum, frame ):
    client._thread_terminate = True

if args.daemon:
    # Monkey-patch daemon so's the daemon starts reasonably quickly.  FDs don't
    # strictly speaking need closing anyway because we haven't opened any (yet).
    daemon.daemon.get_maximum_file_descriptors = lambda: 32
    args.quiet = True
    pidlf = lockfile.pidlockfile.PIDLockFile( args.daemon )
    with daemon.DaemonContext(
            pidfile = pidlf,
            signal_map = {signal.SIGTERM: sigterm} ):
        client = PixelClient( args )
        client.loop_forever()
else:
    client = PixelClient( args )
    client.loop_forever()

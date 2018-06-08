#!/usr/bin/env python

from sys import exit
import argparse

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
parser.add_argument( '-T', '--topic', default = MQTT_TOPIC,
                        help = 'MQTT topic to subscribe to' )
parser.add_argument( '-u', '--user',
                        help = 'MQTT broker user name' )
parser.add_argument( '-p', '--pass', dest = 'pw',
                        help = 'MQTT broker password' )
parser.add_argument( '-q', '--quiet', default = False, action = 'store_true',
                        help = 'Minimal output (eg for running as a daemon)' )
parser.add_argument( '-g', '--green-hack', default = False, action = 'store_true',
                        help = 'Apply hack to green channel to improve colour saturation' )
parser.add_argument( '-D', '--daemon', default = False, action = 'store_true',
                        help = 'Run as a daemon (implies -q)' )
args = parser.parse_args()

if args.daemon:
    try:
        import daemon
    except ImportError:
        exit("--daemon requires the daemon module.  Install with: sudo pip install python-daemon")

MQTT_SERVER = args.host
MQTT_PORT = args.port
MQTT_TOPIC = args.topic
MQTT_USER = args.user
MQTT_PASS = args.pw

def on_connect(client, userdata, flags, rc):
    if not args.quiet:
        print("Connected to {s}:{p}/{t} with result code {r}.\nSee {c} --help for options.".format(s = MQTT_SERVER, p = MQTT_PORT, t = MQTT_TOPIC, r = rc, c = parser.prog))

    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):

    data = msg.payload.split(',')
    command = data.pop(0)

    if command == "clr" and len(data) == 0:
        blinkt.clear()
        blinkt.show()
        return

    if command == "bri" and len(data) == 1:
        try:
            bri = float(data[0])
        except ValueError:
            print("Malformed command: ", str(msg.payload))
            return
        blinkt.set_brightness(bri)
        blinkt.show()
        return

    if command == "rgb" and len(data) == 4:
        try:
            pixel = data.pop(0)

            if pixel == "*":
                pixel = None
            else:
                pixel = int(pixel)
                if pixel > 7:
                    print("Pixel out of range: " + str(pixel))
                    return

            r, g, b = [int(x) & 0xff for x in data]
            if args.green_hack:
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

            print(command, pixel, r, g, b)

        except ValueError:
            print("Malformed command: " + str(msg.payload))
            return

        if pixel is None:
            for x in range(blinkt.NUM_PIXELS):
                blinkt.set_pixel(x, r, g, b)
        else:
            blinkt.set_pixel(pixel, r, g, b)

        blinkt.show()
        return


def mqtt_subscriber():
    blinkt.set_clear_on_exit()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    if MQTT_USER is not None and MQTT_PASS is not None:
        print("Using username: {un} and password: {pw}".format(un=MQTT_USER, pw="*" * len(MQTT_PASS)))
        client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    client.loop_forever()

if args.daemon:
    args.quiet = True
    with daemon.DaemonContext():
            mqtt_subscriber()
else:
    mqtt_subscriber()

#!/usr/bin/env python

try:
    import paho.mqtt.client as mqtt
except ImportError:
    raise ImportError("This example requires the paho-mqtt module\nInstall with: python3 -m pip install paho-mqtt")

import blinkt

MQTT_SERVER = "iot.eclipse.org"
MQTT_PORT = 1883
MQTT_TOPIC = "pimoroni/blinkt"

# Set these to use authorisation
MQTT_USER = None
MQTT_PASS = None

print(
    f"""
MQTT Blinkt! Control

This example uses public MQTT messages from {MQTT_SERVER} on port {MQTT_PORT} to control Blinkt!

It will monitor the {MQTT_TOPIC} topic by default, and understands the following messages:

rgb,<pixel>,<r>,<g>,<b> - Set a single pixel to an RGB colour. Example: rgb,1,255,0,255
clr - Clear Blinkt!

You can use the online MQTT tester at http://www.hivemq.com/demos/websocket-client/ to send messages.

Use {MQTT_SERVER} as the host, and port 80 (Eclipse's websocket port). Set the topic to topic: {MQTT_TOPIC}
"""
)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    data = msg.payload
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    data = data.split(",")
    command = data.pop(0)

    if command == "clr" and len(data) == 0:
        blinkt.clear()
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

            r, g, b = [int(x) & 0xFF for x in data]

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


blinkt.set_clear_on_exit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if MQTT_USER is not None and MQTT_PASS is not None:
    pw = "*" * len(MQTT_PASS)
    print(f"Using username: {MQTT_USER} and password: {pw}")
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()

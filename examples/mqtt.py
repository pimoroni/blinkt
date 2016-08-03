#!/usr/bin/env python

from blinkt import set_pixel, show

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requies the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")


MQTT_SERVER = "iot.eclipse.org"
MQTT_PORT = 1883
MQTT_TOPIC = "pimoroni/blinkt"

print("""
MQTT Blinkt! Control

This example uses public MQTT messages from {server} on port {port} to control Blinkt!

It will monitor the {topic} topic by default, and understands the following messages:

rgb,<pixel>,<r>,<g>,<b> - Set a single pixel to an RGB colour. Example: rgb,1,255,0,255
clr - Clear Blinkt!

You can use the online MQTT tester at http://www.hivemq.com/demos/websocket-client/ to send messages.
""".format(
    server=MQTT_SERVER,
    port=MQTT_PORT,
    topic=MQTT_TOPIC
))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):

    data = msg.payload.split(',')
    command = data.pop(0)

    if command == "clr" and len(data) == 0:
        clear()
        show()
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

            print(command, pixel, r, g, b)

        except ValueError:
            print("Malformed command: " + str(msg.payload))
            return

        if pixel is None:
            for x in range(8):
                set_pixel(x, r, g, b)
        else:
            set_pixel(pixel, r, g, b)

        show()
        return


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()

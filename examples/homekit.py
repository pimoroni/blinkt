from colorsys import hsv_to_rgb, rgb_to_hsv
import blinkt
from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Initialize blinkt device
blinkt.set_clear_on_exit()
blinkt.clear()
blinkt.show()

colour = 'FFFFFF'
status = 0
brightness = 0.2

# Unlike the mote library, the blinkt library doesn't have a get_pixel function so we'll need to keep track of things ourselves...
anyLEDon = 0

def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

def blinkt_on(c):
    global brightness
    r, g, b = hex_to_rgb(c)
    for pixel in range(8):
        blinkt.set_pixel(pixel, r, g, b, brightness)
    anyLEDon = 1
    blinkt.show()
    return True

def blinkt_off():
    blinkt.clear()
    blinkt.show()
    anyLEDon = 0
    return True

def blinkt_brightness_get():
    global brightness
    return brightness

def blinkt_brightness_set(newbrightness):
    global brightness, colour
    brightness = newbrightness
    blinkt_on(colour)
    return True

def get_status():
    global status
    if anyLEDon != 0:
        status = 1
    return status

@app.route('/blinkt/api/v1.0/<string:st>', methods=['GET'])
def set_status(st):
    global status, colour, brightness
    if st == 'on':
        status = 1
        blinkt_on(colour)
    elif st == 'off':
        status = 0
        blinkt_off()
    elif st == 'status':
        status = get_status()
    return jsonify({'status': status, 'colour': colour, 'brightness' : brightness})

@app.route('/blinkt/api/v1.0/set', methods=['GET'])
def get_colour():
    global colour, brightness
    return jsonify({'status': status, 'colour': colour, 'brightness' : brightness})

@app.route('/blinkt/api/v1.0/set/<string:c>', methods=['GET'])
def set_colour(c):
    global status, colour, brightness
    colour = c
    if status != 0:
        blinkt_on(colour)
        status = 1
    return jsonify({'status': status, 'colour': colour, 'brightness' : brightness})

@app.route('/blinkt/api/v1.0/brightness', methods=['GET'])
def get_brightness():
    global colour, brightness
    return jsonify({'status': status, 'colour': colour, 'brightness' : brightness})

@app.route('/blinkt/api/v1.0/brightness/<string:c>', methods=['GET'])
def set_brightness(x):
    global status, colour, brightness
    brightness = x
    if status != 0:
        blinkt_on(colour)
        status = 1
    return jsonify({'status': status, 'colour': colour, 'brightness' : brightness})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    blinkt_off()
    app.run(host='0.0.0.0', debug=True)

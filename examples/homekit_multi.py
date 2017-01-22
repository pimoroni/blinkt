from colorsys import hsv_to_rgb, rgb_to_hsv
import blinkt
from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Initialize blinkt device
blinkt.set_clear_on_exit(True)
blinkt.clear()
blinkt.show()

NUM_PIXELS = 8

# We're going to use a multi-dimensional (8x3) array / list to hold our status, colour and brightness for each of the 8 LEDs
status = []
for i in range(NUM_PIXELS):
    status.append(['FFFFFF', 0, 50])

def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

def blinkt_on(p,c):
    global status
    r, g, b = hex_to_rgb(c)
    blinkt.set_pixel(p, r, g, b, float(status[p][2])/100)
    status[p][1] = 1
    status[p][0] = c
    blinkt.show()
    return True

def blinkt_off(p):
    global status
    blinkt.set_pixel(p, 0, 0, 0, float(status[p][2])/100)
    blinkt.show()
    status[p][1] = 0
    return True

def blinkt_brightness_get(p):
    global status
    return status[p][2]

def blinkt_brightness_set(p,b):
    global status
    status[p][2] = b
    blinkt_on(p,status[p][0])
    return True

def get_status(p):
    global status
    return status[p][1]

@app.route('/blinkt/api/v1.0/<int:p>/<string:st>', methods=['GET'])
def set_status(p,st):
    global status
    if st == 'on':
        blinkt_on(p,status[p][0])
    elif st == 'off':
        blinkt_off(p)
    elif st == 'status':
        ret = get_status(p)
    return str(get_status(p))

@app.route('/blinkt/api/v1.0/<int:p>/set', methods=['GET'])
def get_colour(p):
    global status
    return str(status[p][0])

@app.route('/blinkt/api/v1.0/<int:p>/set/<string:c>', methods=['GET'])
def set_colour(p,c):
    global status
    if status[p][1] != 0:
        blinkt_on(p,c)
    return str(c)

@app.route('/blinkt/api/v1.0/<int:p>/brightness', methods=['GET'])
def get_brightness(p):
    global status
    return str(status[p][2])

@app.route('/blinkt/api/v1.0/<int:p>/brightness/<string:x>', methods=['GET'])
def set_brightness(p,x):
    global status
    status[p][2] = int(x)
    if status[p][1] != 0:
        blinkt_on(p,status[p][0])
    return str(x)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    blinkt_off()
    app.run(host='0.0.0.0', debug=True)

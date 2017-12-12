from colorsys import hsv_to_rgb, rgb_to_hsv
import blinkt
from flask import Flask, jsonify, make_response
import threading
import time
from concurrent.futures import TimeoutError
from pebble import ProcessPool, ProcessExpired

app = Flask(__name__)

# Initialize blinkt device
blinkt.set_clear_on_exit(True)
blinkt.clear()
blinkt.show()

NUM_PIXELS = 8


def runPattern(n):
    # As long as we weren't asked to stop, do our pattern
    spacing = 360.0 / 16.0
    hue = 0
    global thread_stopReq
    while not thread_stopReq:
        hue = int(time.time() * 2) % 360
        h = (hue % 360) / 360.0
        r, g, b = [int(c*255) for c in hsv_to_rgb(h, 1.0, 1.0)]
        blinkt.set_all(r,g,b,1)
        blinkt.show()
        time.sleep(0.001)
        global thread_stopReq
    return n

thread_running = False;
thread_stopReq = False;

with ProcessPool() as pool:
    future = pool.map(function, 0, None)
    if

def pattern_cycle_on():
    try:
        thread.start()
        thread_running = True
    except:
        thread = PatternThread()
        thread.start()
        thread_running = True
    return True

def pattern_cycle_off():
    try:
        thread.join()
        blinkt.clear()
        blinkt.show()
        thread_running = False
    except:
        blinkt.clear()
        blinkt.show()
        thread_running = False
    return True

def pattern_cycle_status():
    return thread_running

def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

def clamp(x):
  return max(0, min(x, 255))

def rgb_to_hex(r,g,b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

@app.route('/blinkt/api/v1.0/pattern/<string:pat>/<string:st>', methods=['GET'])
def set_pattern(pat,st):
    if st == 'on':
        if pat == 'cycle':
            pattern_cycle_on()
    elif st == 'off':
        if pat == 'cycle':
            pattern_cycle_off()
    elif st == 'status':
        return str(pattern_cycle_status())
    return str(pattern_cycle_status())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

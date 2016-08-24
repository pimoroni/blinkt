import atexit

try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")


DAT = 23
CLK = 24
NUM_PIXELS = 8
BRIGHTNESS = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([DAT,CLK],GPIO.OUT)

pixels = [[0,0,0,BRIGHTNESS]] * 8

_clear_on_exit = True

def _exit():
    if _clear_on_exit:
        clear()
        show()
    GPIO.cleanup()

def set_brightness(brightness):
    for x in range(NUM_PIXELS):
        pixels[x][3] = int(31.0 * brightness) & 0b11111

def clear():
    for x in range(NUM_PIXELS):
        pixels[x][0:3] = [0,0,0]

def write_byte(byte):
    for x in range(8):
        GPIO.output(DAT, byte & 0b10000000)
        GPIO.output(CLK, 1)
        byte <<= 1
        GPIO.output(CLK, 0)

# Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
def _latch():
    GPIO.output(DAT, 0)
    for x in range(36):
        GPIO.output(CLK, 1)
        GPIO.output(CLK, 0)

def show():
    for x in range(4):
        write_byte(0)

    for pixel in pixels:
        r, g, b, brightness = pixel
        write_byte(0b11100000 | brightness)
        write_byte(b)
        write_byte(g)
        write_byte(r)

    _latch()

def set_pixel(x, r, g, b, brightness=None):
    if brightness is None:
        brightness = pixels[x][3]
    else:
        brightness = int(31.0 * brightness) & 0b11111
    pixels[x] = [int(r) & 0xff,int(g) & 0xff,int(b) & 0xff,brightness]

def set_clear_on_exit(value):
    global _clear_on_exit
    _clear_on_exit = value

atexit.register(_exit)

import RPi.GPIO as GPIO

DAT = 23
CLK = 24
BRIGHTNESS = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup([DAT,CLK],GPIO.OUT)

pixels = [[0,0,0,BRIGHTNESS]] * 8

def set_brightness(brightness):
    for x in range(NUM_PIXELS):
        pixels[x][3] = int(31.0 * brightness) & 0b11111

def write_byte(byte):
    for x in range(8):
        bit = (byte & (1 << (7-x))) > 0
        GPIO.output(DAT, bit)
        GPIO.output(CLK, 1)
        GPIO.output(CLK, 0)

def show():
    for x in range(4):
        write_byte(0)

    for pixel in pixels:
        r, g, b, brightness = pixel
        write_byte(0b11100000 | (brightness & 0b11111))
        write_byte(r)
        write_byte(g)
        write_byte(b)

    write_byte(0xff)

def set_pixel(x, r, g, b, brightness=BRIGHTNESS/31.0):
    brightness = int(brightness * 31.0) & 0b11111
    pixels[x] = [r,g,b,brightness]

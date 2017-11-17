#include <bcm2835.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <linux/types.h>
#include <signal.h>
#include <unistd.h>
#include "blinkt.h"

#define APA_SOF 0b11100000

#define DEFAULT_BRIGHTNESS 7
#define NUM_LEDS 8

#define MOSI 23
#define SCLK 24

#ifdef TEST
volatile int running = 0;
#endif

int x;

uint32_t leds[NUM_LEDS] = {};

#ifdef TEST
void sigint_handler(int dummy){
	running = 0;
	return;
}
#endif

void clear(){
	for(x = 0; x < NUM_LEDS; x++){
		leds[x] = DEFAULT_BRIGHTNESS;
	}	
}

void set_pixel(uint8_t led, uint8_t r, uint8_t g, uint8_t b){
	if(led > NUM_LEDS) return;

	leds[led] = rgbb(r,g,b,leds[led] & 0b11111);
}

void set_pixel_brightness(uint8_t led, uint8_t brightness){
	leds[led] = (leds[led] & 0xFFFFFF00) | (brightness & 0b11111);
}

void set_pixel_uint32(uint8_t led, uint32_t color){
	if(led > NUM_LEDS) return;

	leds[led] = color;
}

uint32_t rgbb(uint8_t r, uint8_t g, uint8_t b, uint8_t brightness){
	uint32_t result = 0;
	result = (brightness & 0b11111);
	result |= ((uint32_t)r << 24);
	result |= ((uint32_t)g << 16);
	result |= ((uint16_t)b << 8);
	return result;
}

uint32_t rgb(uint8_t r, uint8_t g, uint8_t b){
	return rgbb(r, g, b, DEFAULT_BRIGHTNESS);
}

inline static void write_byte(uint8_t byte){
	int n;
	for(n = 0; n < 8; n++){
		bcm2835_gpio_write(MOSI, (byte & (1 << (7-n))) > 0);
		bcm2835_gpio_write(SCLK, HIGH);
		bcm2835_gpio_write(SCLK, LOW);
	}

}

void show(void){
	write_byte(0);
	write_byte(0);
	write_byte(0);
	write_byte(0);
	for(x = 0; x < NUM_LEDS; x++){
		write_byte(APA_SOF | (leds[x] & 0b11111));
		write_byte((leds[x] >> 8 ) & 0xFF);
		write_byte((leds[x] >> 16) & 0xFF);
		write_byte((leds[x] >> 24) & 0xFF);
	}
	write_byte(0xff);
	//write_byte(0xff);
	//write_byte(0xff);
	//write_byte(0xff);
}

void stop(void){
	bcm2835_spi_end();

	bcm2835_close();
}


int start(void){

	if(!bcm2835_init()) return 1;

#ifdef TEST
	printf("GPIO Initialized\n");
#endif

	bcm2835_gpio_fsel(MOSI, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_write(MOSI, LOW);
	bcm2835_gpio_fsel(SCLK, BCM2835_GPIO_FSEL_OUTP);
	bcm2835_gpio_write(SCLK, LOW);

	clear();

	return 0;

}

#ifdef TEST
int main(){

	int z;
	int y = 0;

	running = 1;

	signal(SIGINT, sigint_handler);

	if (start()){
		printf("Unable to start apa102\n");
		return 1;
	}

	printf("Running test cycle\n");

	int col = 0;

	while(running){

		for(z = 0; z < NUM_LEDS; z++){		
			switch(col){
				case 0: set_pixel_uint32(z, rgb(y,0,0)); break;
				case 1: set_pixel_uint32(z, rgb(0,y,0)); break;
				case 2: set_pixel_uint32(z, rgb(0,0,y)); break;
			}
		}

		show();

		usleep(1000);

		y+=1;
                if(y>254) col++;
                col%=3;
		y%=255;

	}


	clear();

	usleep(1000);

	stop();

	return 0;

}
#endif

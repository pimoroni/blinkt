void clear(void);
void set_pixel_uint32(uint8_t led, uint32_t color);
void set_pixel(uint8_t led, uint8_t r, uint8_t g, uint8_t b);
void set_pixel_brightness(uint8_t led, uint8_t brightness);
uint32_t rgbb(uint8_t r, uint8_t g, uint8_t b, uint8_t brightness);
uint32_t rgb(uint8_t r, uint8_t g, uint8_t b);
void stop(void);
int start(void);
void show(void);

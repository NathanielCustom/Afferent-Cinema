## Requirements ##
Sketch has been adapted and tested on the ATMega328.
Arduino Wire library needed for I2C communication.
ATMega328's TWI (I2C) pins are 27 (SDA, PC4) and 28 (SCL, PC5).
WS2812 Neopixels tested; connect Neopixel data line to ATMega Pin 14 (PB0)


## Limitations ##
The number of pixels has been set to 70. No concrete testing has been done to determine upper limits at this time.


## I2C Address##
User definable. Currently set to 0x28.


## Debug LED ##
An LED and resistor in series can can be attached to ATMega Pins 15 (PB1, Arduino 9) for debugging.

By default the LED will flash five times when power is applied.
There is a comment block within 'process_data' function with code that will cause the LED to flash when data is received on the I2C bus.

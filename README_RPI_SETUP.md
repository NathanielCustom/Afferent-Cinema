## Introduction

Afferent Cinema has been tested on a Raspberry Pi 3 running Raspbian.
There are two syncronization modes in Afferent Cinema:
- Manual - Time Offset
- Automatic - Audio Recognition

This guide will setup the RPi for the 'manual' mode.


KNOWN ISSUE: Main.py needs to be changed to allow for Afferent Cinema to run without the audio recognition software (Dejavu) being installed.


## I2C

Enable I2C on GPIOs --- as outlined in /boot/overlays/README section i2c-gpio
1. Terminal: sudo nano /boot/config.txt
2. Add: dtoverlay=i2c-gpio,i2c_gpio_sda=5,i2c_gpio_scl=6
2a. This will add a new bus /dev/i2c-3 to pins 5 & 6

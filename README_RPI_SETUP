I2C
Enable I2C on GPIOs --- as outlined in /boot/overlays/README section i2c-gpio
1. Terminal: sudo nano /boot/config.txt
2. Add: dtoverlay=i2c-gpio,i2c_gpio_sda=5,i2c_gpio_scl=6
2a. This will add a new bus /dev/i2c-3 to pins 5 & 6

Swap File
As of the release of Dejavu by bcollazo the swap file size of 100MB is not enough. Follow the steps below to edit the swap file. Be mindful that the stability of the SD card, though already volatile, becomes even more compromised when the swap file is increased. 
(Ref: https://www.bitpi.co/2015/02/11/how-to-change-raspberry-pis-swapfile-size-on-rasbian/)
1. Terminal: sudo nano /etc/dphys-swapfile
2. Change “CONF_SWAPSIZE=100” to desired size.
2a. Recommended twice that of RAM (ex. 2048)
3. Reboot to take effect.

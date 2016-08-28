# External Module Imports
import RPi.GPIO as GPIO
import time
import smbus

### I2C ###
bus = smbus.SMBus(1)

def initialize_device(address, msb, lsb): 								#PCA9685 Specific
	bus.write_byte_data(address, (msb-2), 0x00)							#On start time
	bus.write_byte_data(address, (lsb-2), 0x00)							#On start time
	bus.write_byte_data(address, msb, 0x10)								#LED Off

def initialize_controller(controller_addresses):						#PCA9685 Specific
	controller_total = len(controller_addresses)
	for address in xrange(controller_total):
		bus.write_byte_data(controller_addresses[address], 0x00, 0x10)	#MODE1 Sleep (Bit On)
		bus.write_byte_data(controller_addresses[address], 0x01, 0x04)	#MODE2 OUTDRV; Totem Pole Structure
		bus.write_byte_data(controller_addresses[address], 0x00, 0x00)	#MODE1 Sleep (Bit Off)

def range2percent(value):
	value = (value / 4095 ) * 100
	return (value)

def convertMSB(value):
	value = value << 8 #bit shift from bits 0-7 to 8-15
	return (value)

def extractMSB(value):
	scale = int((value * 4095) / 100) #convert % to 0-4095 scale
	msb = scale & 65280 #extract MSB from binary result (& 1111111100000000)
	msb = msb >> 8 #bit shift from bits 8-15 to 0-7
	return (msb)

def extractLSB(value):
	scale = int((value * 4095) / 100) #convert % to 0-4095 scale	
	lsb = scale & 255 #extract LSB from binary result (& 11111111)
	return (lsb)

def device_read(address, ch_msb, ch_lsb):
	
	value_msb = bus.read_byte_data(address, ch_msb)
	value_lsb = bus.read_byte_data(address, ch_lsb)
	
	value_msb = convertMSB(value_msb)									# Convert 8-bit register to 16-bit
	value_sum = value_msb + value_lsb									# Combine Registers
	value_current = range2percent(value_sum) 							# Convert 0-4095 range to 0-100 range.
	
	return (value_current)

def device_write(value, address, ch_msb, ch_lsb):
	value_msb = extractMSB(value)										# Convert value to 2 x 8-bit registers
	value_lsb = extractLSB(value)										# Convert value to 2 x 8-bit registers
	bus.write_byte_data(address, ch_msb, value_msb)
	bus.write_byte_data(address, ch_lsb, value_lsb)
	return()

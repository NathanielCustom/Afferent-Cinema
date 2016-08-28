# External Module Imports
import RPi.GPIO as GPIO
import time
import os
import json
import smbus
import i2c_control


### JSON Files ###
hw_file = json.load(open('LED_hwprofile.json'))
hw_file_open = open('LED_hwprofile.json', 'r+')

### I2C ###
bus = smbus.SMBus(1)

# Search JSON for addresses...
#PWM Controller
PCA9685_ADDRESS = 0x40
#Red LED
PCA9685_OUTPUT0_ON_H = 0x07
PCA9685_OUTPUT0_ON_L = 0x06
PCA9685_OUTPUT0_OFF_H = 0x09
PCA9685_OUTPUT0_OFF_L = 0x08
#Green LED
PCA9685_OUTPUT1_ON_H = 0x0b
PCA9685_OUTPUT1_ON_L = 0x0a
PCA9685_OUTPUT1_OFF_H = 0x0d
PCA9685_OUTPUT1_OFF_L = 0x0c
#Blue LED
PCA9685_OUTPUT2_ON_H = 0x0f
PCA9685_OUTPUT2_ON_L = 0x0e
PCA9685_OUTPUT2_OFF_H = 0x11
PCA9685_OUTPUT2_OFF_L = 0x10
#Fan
PCA9685_OUTPUT3_ON_H = 0x13
PCA9685_OUTPUT3_ON_L = 0x12
PCA9685_OUTPUT3_OFF_H = 0x15
PCA9685_OUTPUT3_OFF_L = 0x14

# INITIALIZE #
# PCA9685
bus.write_byte_data(PCA9685_ADDRESS, 0x00, 0x10)
bus.write_byte_data(PCA9685_ADDRESS, 0x01, 0x04)
bus.write_byte_data(PCA9685_ADDRESS, 0x00, 0x00)

#Red LED
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT0_ON_H, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT0_ON_L, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT0_OFF_H, 0x10) #LED Off
#Green LED
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT1_ON_H, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT1_ON_L, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT1_OFF_H, 0x10) #LED Off
#Blue LED
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT2_ON_H, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT2_ON_L, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT2_OFF_H, 0x10) #LED Off
#Fan
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_ON_H, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_ON_L, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x04) #Fan Off


# Output 4
bus.write_byte_data(PCA9685_ADDRESS, 0x17, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x16, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x19, 0x10) #LED Off
# Output 5
bus.write_byte_data(PCA9685_ADDRESS, 0x1B, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x1A, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x1D, 0x10) #LED Off	
# Output 6
bus.write_byte_data(PCA9685_ADDRESS, 0x1F, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x1E, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x21, 0x10) #LED Off	

# Output 7
bus.write_byte_data(PCA9685_ADDRESS, 0x23, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x22, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x25, 0x10) #LED Off
# Output 8
bus.write_byte_data(PCA9685_ADDRESS, 0x27, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x26, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x29, 0x10) #LED Off
# Output 9
bus.write_byte_data(PCA9685_ADDRESS, 0x2B, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x2A, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x2D, 0x10) #LED Off

# Output 10
bus.write_byte_data(PCA9685_ADDRESS, 0x2F, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x2E, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x31, 0x10) #LED Off
# Output 11
bus.write_byte_data(PCA9685_ADDRESS, 0x33, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x32, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x35, 0x10) #LED Off
# Output 12
bus.write_byte_data(PCA9685_ADDRESS, 0x37, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x36, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x39, 0x10) #LED Off
	
# Output 13
bus.write_byte_data(PCA9685_ADDRESS, 0x3B, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x3A, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x3D, 0x10) #LED Off
# Output 14
bus.write_byte_data(PCA9685_ADDRESS, 0x3F, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x3E, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x41, 0x10) #LED Off
# Output 15
bus.write_byte_data(PCA9685_ADDRESS, 0x43, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x42, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, 0x45, 0x10) #LED Off	


address_select = -1
msb_select = -1
lsb_select = -1

### Functions ###

def select_device():
	global address_select
	global msb_select
	global lsb_select
	os.system('clear')
	device_total = len(hw_file["hw"])
	address_select = -1
	print "Available Devices "
	
	for device in xrange(device_total):
		print ( "Device #" + str(device) + ":  " + str(hw_file["hw"][device]["color"]) + " @ Address " + str(hw_file["hw"][device]["address_i2c"]) + " --  MSB: " + str(hw_file["hw"][device]["channel_msb"]) + ",  LSB: " + str(hw_file["hw"][device]["channel_lsb"]) )
	
	while address_select == -1:
		print " "
		try:
			device_select = input("Input Device Address ")
			address_select = hw_file["hw"][device_select]["address_i2c"]
			msb_select =  hw_file["hw"][device_select]["channel_msb"]
			lsb_select = hw_file["hw"][device_select]["channel_lsb"]
		except:
			print " "
			print "Not a Valid Input... Select Another"
			address_select = -1
			msb_select = -1
			lsb_select = -1
	return ()

def devices_off():
	global address_select
	global msb_select
	global lsb_select
	os.system('clear')
	device_total = len(hw_file["hw"])
	
	print "Turning Off All Devices --- Output to 0"
	
	for device in xrange(device_total):
		value = 0
		address = hw_file["hw"][device]["address_i2c"]
		ch_msb = hw_file["hw"][device]["channel_msb"]
		ch_lsb = hw_file["hw"][device]["channel_lsb"]
		i2c_control.device_write(value, address, ch_msb, ch_lsb)
		print " "
		print ("Device " + str(device) + " is off.")
		
	print " "
	print "All devices are off"
	time.sleep (2)
	

def display_menu(address):
	global address_select
	global msb_select
	global lsb_select
	
	selection = "a"
	while selection != "1" or "2" or "3" or "4" or "5" or "6" or "7":
		os.system('clear')
		print ("Input a Command for Device " + str(address_select) + ", " + str(msb_select) + ", " + str(lsb_select))
		print (" ")
		print ("1 - Select Device")
		print ("2 - Test Output")
		print ("3 - Calibrate High")
		print ("4 - Calibrate Delay")
		print (" ")
		print ("5 - Read/Write Values")
		print ("8 - Diagnostic Readings")
		print ("0 - Exit")
		selection = raw_input()
		if (selection == "2"):
			test_output()
			selection = "a"
		if (selection == "2") or (selection == "3") or (selection == "4"):
			calibration(address, selection)
			selection = "a"
		if selection == "8":
			diagnostic()
			selection = "a"
		if selection == "1":
			select_device()
			selection = "a"
		if selection == "0":
			return (1)

def diagnostic():
		os.system('clear')
		print ("MODE1: " + str(bus.read_byte_data(address_select, 0)))
		print ("MODE2: " + str(bus.read_byte_data(address_select, 1)))
		print ("SUBADR1: " + str(bus.read_byte_data(address_select, 2)))
		print ("SUBADR2: " + str(bus.read_byte_data(address_select, 3)))
		print ("SUBADR3: " + str(bus.read_byte_data(address_select, 4)))
		print ("ALLCALLADR set to " + str(bus.read_byte_data(address_select, 5)))
		print " "
		for output in xrange(0, 16):
			print ("LED" + str(output) + "_ON_L: " + str(bus.read_byte_data(address_select, ((output*4) + 6))))
			print ("LED" + str(output) + "_ON_H: " + str(bus.read_byte_data(address_select, ((output*4) + 7))))
			print ("LED" + str(output) + "_OFF_L: " + str(bus.read_byte_data(address_select, ((output*4) + 8))))
			print ("LED" + str(output) + "_OFF_H: " + str(bus.read_byte_data(address_select, ((output*4) + 9))))
		print " "	
		print ("ALL_LED_ON_L: " + str(bus.read_byte_data(address_select, 250)))
		print ("ALL_LED_ON_H: " + str(bus.read_byte_data(address_select, 251)))
		print ("ALL_LED_OFF_L: " + str(bus.read_byte_data(address_select, 252)))
		print ("ALL_LED_OFF_H: " + str(bus.read_byte_data(address_select, 253)))
		print ("PRE_SCALE: " + str(bus.read_byte_data(address_select, 254)))
		print ("TestMode " + str(bus.read_byte_data(address_select, 255)))
		print " "
		print "Enter 0 to Exit"
		
		selection = 1
		while selection != 0:
			selection = input
			
		return()

def test_output():
	global address_select
	global msb_select
	global lsb_select
	os.system('clear')
	
	value = 0
	print "TEST OUTPUT"
	print " "
	print "Input a value between 0 and 100. -1 exits."
	while value != -1:
		value = input(" ")
		#try:
		i2c_control.device_write(value, address_select, msb_select, lsb_select)
		print ("Device set to " + str(bus.read_byte_data(address_select, 0)))
		print ("Device set to " + str(bus.read_byte_data(address_select, 1)))
		print ("ALLCALLADR set to " + str(bus.read_byte_data(address_select, 5)))
		print ("Device OFF_H set to " + str(bus.read_byte_data(address_select, msb_select)))
		print ("Device OFF_L set to " + str(bus.read_byte_data(address_select, lsb_select)))
		print ("Device ON_H set to " + str(bus.read_byte_data(address_select, (msb_select-2))))
		print ("Device ON_L set to " + str(bus.read_byte_data(address_select, (lsb_select-2))))
		print ("LED ON L set to " + str(bus.read_byte_data(address_select, 250)))
		print ("LED ON H set to " + str(bus.read_byte_data(address_select, 251)))
		print ("LED OFF L set to " + str(bus.read_byte_data(address_select, 252)))
		print ("LED OFF H set to " + str(bus.read_byte_data(address_select, 253)))
		print ("Prescaler set to " + str(bus.read_byte_data(address_select, 254)))
		print ("Testmode set to " + str(bus.read_byte_data(address_select, 255)))
		#except:
			#print "Not a Valid Input"

def read_values(address):
	os.system('clear')
	print("Low - " + str(hw_file["hw"][address]["low"]) + "%")
	print("Medium - " + str(hw_file["hw"][address]["medium"]) + "%") 
	print("High - " + str(hw_file["hw"][address]["high"]) + "%")
	print("Delay - " + str(hw_file["hw"][address]["delay"]) + " seconds")
	print(" ")
	selection = "a"
	while selection != "Y" or "n":
		selection = raw_input("Write new values? Y/n ")
		if selection == "Y":
			change_values(address)
			return ()
		if selection == "n":
			return ()

def change_values(address):
			os.system('clear')
			print ("1 - Low")
			print ("2 - Medium")
			print ("3 - High")
			print ("4 - Delay")
			print ("0 - Exit")
			selection = "a"
			while selection != "1" or "2" or "3" or "4" or "0":
				print (" ")
				selection = raw_input("Select a field to change... ")
				if selection == "1":
					print (" ")
					print ("The existing value is " + str(hw_file["hw"][address]["low"]) + ":")
					field_value = input("Input a new value ")
					hw_file["hw"][address]["low"] = field_value
					hw_file_open.seek(0) # rewind to beginning of file
					hw_file_open.write(json.dumps(hw_file))
					print ("The new value has been saved as " + str(hw_file["hw"][address]["low"]))
					time.sleep(2)
					selection = "a"
				if selection == "2":
					print (" ")
					print ("The existing value is " + str(hw_file["hw"][address]["medium"]) + ":")
					field_value = input("Input a new value ")
					hw_file["hw"][address]["medium"] = field_value
					hw_file_open.seek(0) # rewind to beginning of file
					hw_file_open.write(json.dumps(hw_file))
					print ("The new value has been saved as " + str(hw_file["hw"][address]["medium"]))
					time.sleep(2)
					selection = "a"
				if selection == "3":
					print (" ")
					print ("The existing value is " + str(hw_file["hw"][address]["high"]) + ":")
					field_value = input("Input a new value ")
					hw_file["hw"][address]["high"] = field_value
					hw_file_open.seek(0) # rewind to beginning of file
					hw_file_open.write(json.dumps(hw_file))
					print ("The new value has been saved as " + str(hw_file["hw"][address]["high"]))
					time.sleep(2)
					selection = "a"
				if selection == "4":
					print (" ")
					print ("The existing value is " + str(hw_file["hw"][address]["delay"]) + ":")
					field_value = input("Input a new value ")
					hw_file["hw"][address]["delay"] = field_value
					hw_file_open.seek(0) # rewind to beginning of file
					hw_file_open.write(json.dumps(hw_file))
					print ("The new value has been saved as " + str(hw_file["hw"][address]["delay"]))
					time.sleep(2)
					selection = "a"
				if selection == "0":
					return()

def process_description():
	print ("Description of how the process works")

def extractMSB(value):
	scale = int((value * 4095) / 100) #convert % to 0-4095 scale
	msb = scale & 65280 #extract MSB from binary result (& 1111111100000000)
	msb = msb >> 8 #bit shift from bits 8-15 to 0-7
	return (msb)

def extractLSB(value):
	scale = int((value * 4095) / 100) #convert % to 0-4095 scale	
	lsb = scale & 255 #extract LSB from binary result (& 11111111)
	return (lsb)


def calibration(address, selection):
	os.system('clear')
	if selection == "1":
		print ("Starting the calibration process for the Low mode")
		process_description()
		print ("Description of the sensation you should adjust for")
		print ("  ")
		count_down()
		#pwm.ChangeDutyCycle(hw_file["hw"][address]["low"])
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, extractMSB(hw_file["hw"][address]["low"]))
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, extractLSB(hw_file["hw"][address]["low"]))
		currentDutyCycle = hw_file["hw"][address]["low"]
		currentDutyCycle = adjust_device(currentDutyCycle)
		os.system('clear')
		print ("Would you like to save the new value " + str(currentDutyCycle) + " over the old value " + str(hw_file["hw"][address]["low"]) + "? (Y)es/(n)o")
		savevalue = "a"
		while savevalue != "Y" or "n":
			savevalue = raw_input()
			if savevalue == "Y":
				hw_file["hw"][address]["low"] = currentDutyCycle
				hw_file_open.seek(0) # rewind to beginning of file
				hw_file_open.write(json.dumps(hw_file))
				print ("The new value has been saved as " + str(hw_file["hw"][address]["low"]))
				time.sleep(2)
				return()
			if savevalue == "n":
				return()
	if selection == "2":
		print ("Starting the calibration process for the Medium mode")
		process_description()
		print ("Description of the sensation you should adjust for")
		print ("  ")
		count_down()
		#pwm.ChangeDutyCycle(hw_file["hw"][address]["medium"])
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, extractMSB(hw_file["hw"][address]["medium"]))
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, extractLSB(hw_file["hw"][address]["medium"]))
		currentDutyCycle = hw_file["hw"][address]["medium"]
		currentDutyCycle = adjust_device(currentDutyCycle)
		os.system('clear')
		print ("Would you like to save the new value " + str(currentDutyCycle) + " over the old value " + str(hw_file["hw"][address]["medium"]) + "? (Y)es/(n)o")
		savevalue = "a"
		while savevalue != "Y" or "n":
			savevalue = raw_input()
			if savevalue == "Y":
				hw_file["hw"][address]["medium"] = currentDutyCycle
				hw_file_open.seek(0) # rewind to beginning of file
				hw_file_open.write(json.dumps(hw_file))
				print ("The new value has been saved as " + str(hw_file["hw"][address]["medium"]))
				time.sleep(2)
				return()
			if savevalue == "n":
				return()
	if selection == "3":
		print ("Starting the calibration process for the High mode")
		process_description()
		print ("Description of the sensation you should adjust for")
		print ("  ")
		count_down()
		#pwm.ChangeDutyCycle(hw_file["hw"][address]["high"])
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, extractMSB(hw_file["hw"][address]["high"]))
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, extractLSB(hw_file["hw"][address]["high"]))
		currentDutyCycle = hw_file["hw"][address]["high"]
		currentDutyCycle = adjust_device(currentDutyCycle)
		os.system('clear')
		print ("Would you like to save the new value " + str(currentDutyCycle) + " over the old value " + str(hw_file["hw"][address]["high"]) + "? (Y)es/(n)o")
		savevalue = "a"
		while savevalue != "Y" or "n":
			savevalue = raw_input()
			if savevalue == "Y":
				hw_file["hw"][address]["high"] = currentDutyCycle
				hw_file_open.seek(0) # rewind to beginning of file
				hw_file_open.write(json.dumps(hw_file))
				print ("The new value has been saved as " + str(hw_file["hw"][address]["high"]))
				time.sleep(2)
				return()
			if savevalue == "n":
				return()
	if selection == "4":
		print ("Starting the calibration process for the Delay")
		print ("Delay process description")
		print ("Description of the sensation you should adjust for")
		print ("  ")
		raw_input ("Press any key to continue...")
		print ("  ")
		currentDelay = adjust_delay(address)
		os.system('clear')
		print ("Would you like to save the new value " + str(currentDelay) + " over the old value " + str(hw_file["hw"][address]["delay"]) + "? (Y)es/(n)o")
		savevalue = "a"
		while savevalue != "Y" or "n":
			savevalue = raw_input()
			if savevalue == "Y":
				hw_file["hw"][address]["delay"] = currentDelay
				hw_file_open.seek(0) # rewind to beginning of file
				hw_file_open.write(json.dumps(hw_file))
				print ("The new value has been saved as " + str(hw_file["hw"][address]["delay"]))
				time.sleep(2)
				return()
			if savevalue == "n":
				return()

def count_down():
	time.sleep (1)
	print ("Starting in 3...")
	time.sleep (1)
	print ("2")
	time.sleep (1)
	print ("1")
	time.sleep (1)
	print ("GO!")

def adjust_device(currentDutyCycle):
	while 1:
		selection = raw_input("Press (u)p/(d)own to adjust speed. Press (s) to stop... ")
		if selection == "u":
			currentDutyCycle = currentDutyCycle + 2
			print currentDutyCycle
			#pwm.ChangeDutyCycle(currentDutyCycle)
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, extractMSB(currentDutyCycle))
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, extractLSB(currentDutyCycle))
			selection = "a"
		if selection == "d":
			currentDutyCycle = currentDutyCycle - 2
			print currentDutyCycle
			#pwm.ChangeDutyCycle(currentDutyCycle)
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, extractMSB(currentDutyCycle))
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, extractLSB(currentDutyCycle))
			selection = "a"
		if selection == "s":
			#pwm.ChangeDutyCycle(0)
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x00) #Minimal Speed to invoke stop
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, 0x51) 
			time.sleep(0.10)
			bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x10) #Fan Off
			return (currentDutyCycle)
			
def adjust_delay(address):
	delay = hw_file["hw"][address]["delay"]
	changedelay = 0
	while changedelay != "n":
		print ("The current Delay is set to " + str(delay) + " seconds")
		print ("  ")
		print ("Fan Starting...")
		#pwm.ChangeDutyCycle(hw_file["hw"][address]["medium"]) # medium PWM is current baseline for delay
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, extractMSB(hw_file["hw"][address]["medium"]))
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, extractLSB(hw_file["hw"][address]["medium"]))
		time.sleep(delay)
		print (" ")
		print ("NOW!")
		time.sleep(2)
		#pwm.ChangeDutyCycle(0)
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x00) #Minimal Speed to invoke stop
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, 0x51) 
		time.sleep(0.10)
		bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x10) #Fan Off
		print ("  ")
		print ("Change the Delay to...? (n)o/(r)epeat")
		changedelay = raw_input()
		if changedelay == "r":
			os.system('clear')
		if changedelay == "n":
			return(delay)
		if changedelay != "n" and changedelay != "r":
			print("entered else statement")
			delay = float(changedelay)
			os.system('clear')
	
	

print("Here we go! Press CTRL+C to exit")
try:
	address = select_device()
	exit_program = 0
	while exit_program == 0:
		exit_program = display_menu(address)
	devices_off()
	print "Exiting Program"
	time.sleep (2)
	
except KeyboardInterrupt:
	devices_off()

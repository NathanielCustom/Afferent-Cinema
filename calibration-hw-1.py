# External Module Imports
import RPi.GPIO as GPIO
import time
import os
import json
import smbus


### JSON Files ###
hw_file = json.load(open('hw-1.json'))
hw_file_open = open('hw-1.json', 'r+')

### I2C ###
bus = smbus.SMBus(1)
#PWM Controller
PCA9685_ADDRESS = 0x40
#Fan
PCA9685_OUTPUT3_ON_H = 0x13
PCA9685_OUTPUT3_ON_L = 0x12
PCA9685_OUTPUT3_OFF_H = 0x15
PCA9685_OUTPUT3_OFF_L = 0x14

### Initialize States ###

# PCA9685
bus.write_byte_data(PCA9685_ADDRESS, 0x00, 0x01)

#Fan
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_ON_H, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_ON_L, 0x00) #On start time
bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x10) #Fan Off



### Functions ###

def select_device():
	os.system('clear')
	address = input("Input Device Address ")
	return (address)

def display_menu(address):
	selection = "a"
	while selection != "1" or "2" or "3" or "4" or "5" or "6" or "7":
		os.system('clear')
		print ("Input a Command for Device " + str(address) + ":")
		print (" ")
		print ("1 - Calibrate Low")
		print ("2 - Calibrate Medium")
		print ("3 - Calibrate High")
		print ("4 - Calibrate Delay")
		print (" ")
		print ("5 - Read/Write Values")
		print ("6 - Select Different Device")
		print ("7 - Exit")
		selection = raw_input()
		if (selection == "1") or (selection == "2") or (selection == "3") or (selection == "4"):
			calibration(address, selection)
			selection = "a"
		if selection == "5":
			read_values(address)
			selection = "a"
		if selection == "6":
			address = select_device()
		if selection == "7":
			return (1)

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
	bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x00) #Minimal Speed to invoke stop
	bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, 0x51) 
	time.sleep(0.10)
	bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x10) #Fan Off
	
except KeyboardInterrupt:
	bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x00) #Minimal Speed to invoke stop
	bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_L, 0x51) 
	time.sleep(0.10)
	bus.write_byte_data(PCA9685_ADDRESS, PCA9685_OUTPUT3_OFF_H, 0x10) #Fan Off

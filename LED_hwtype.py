# External Module Imports
import json
import threading

def cie1931_lightness(L): # Logarithmic scaling of LED brightness based on CIE 1931 lightness formula
    if L <= 8:
		return (L/902.3*100)
    else:
        return ((((L+16.0)/116.0)**3)*100)

def processtrigger(pattern_percent, hwprofile_name, device, event, value_previous): # New
	### LED Specific ###
	
	device_color = device["color"]						# Is the device Red, Green or Blue?
	event_color = event[0]["color"]									# Get Event Color
	
	# Lookup Device Color's Target Value for Event Color
	if 'value_target' not in device:
		lock = threading.Lock()
		lock.acquire()
		
		try:
			value_target = json.load(open(hwprofile_name))["colors"][0][event_color][0][device_color]	
		except:
			value_target = json.load(open(json.load(open('LED_loaded_files.json'))["files"][0]["custom_colors"]))["colors"][0][event_color][0][device_color]
		finally:
			lock.release()
			device['value_target'] = value_target
	
	# Calculate Values
	value_target = device['value_target']	
	value_deltatotal = value_target - value_previous					# Total Delta of Color Value
	value_deltastep = value_deltatotal * pattern_percent				# Percentage of Delta at current time
	value = value_previous + value_deltastep
	value = cie1931_lightness(value)									# Adjust for CIE1931
	values_event = [value, value_target]

			
	return(values_event)

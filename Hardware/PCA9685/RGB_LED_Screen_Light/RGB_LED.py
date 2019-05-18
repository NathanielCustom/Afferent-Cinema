# External Module Imports
import json

def cie1931_lightness(L):
	'''
	Logarithmic scaling of LED brightness based on CIE 1931 lightness formula
    '''
	
	L = L/255*100 #Convert 8-bit (0-255) to Percent
	
	if L <= 8:
		return (L/902.3*255) # Formula based on 0-100% range.
	else:
		return ((((L+16.0)/116.0)**3)*255)


def values_step(device, event, value_percent, folder_session): # May need to pass custom colors file in future.
	# Example: device = 
    	#   {"address":[1,2,3], "device":"PCA9685", "x_position":0, "values":[120, 46, 34], I2C_address":68}	
	
	if isinstance(event["color"], str) == False:
		values_color = event["color"]
	else:
		custom_color_dictionary = json.load(open(folder_session + 'LED_RGB_Custom_Colors.json')) 
		custom_color = custom_color_dictionary[ event["color"] ]
		
		values_color[0] = custom_color["Red"]
		values_color[1] = custom_color["Green"]
		values_color[2] = custom_color["Blue"]

		event["color"] = values_color

	values = []
	value_beginning = device["values"]
	index_range = len(values_color)
	for index in range(index_range):
			value_target = cie1931_lightness(values_color[index])
			value_delta = value_target - value_beginning[index]
			# value_delta = values_color[index] - value_beginning[index]
			value_delta_step = value_delta * value_percent
			value_current = value_beginning[index] + value_delta_step
			# value_current = cie1931_lightness(value_current)
			values.append(value_current)
	
	return(values)

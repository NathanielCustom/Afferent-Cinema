# External Module Imports
import json
import threading


def calibrated_scale( event_value, device ):
	if event_value > 50:
		event_value = ( ( (event_value - device["medium"]) * ( device["high"] - device["medium"] ) ) /49) + device["medium"]
	else:
		event_value = ( ( (event_value - device["low"]) * (device["medium"] - device["low"]) ) /49) + device["low"]
	return(event_value)

def processtrigger(pattern_percent, hwprofile_name, device, event, value_previous): # New	
	
	### Fan Specific ###
	value_target = event[0]["strength"]					
	value = calibrated_scale( (value_target * pattern_percent), device )
	values_event = [value, value_target]				
					
	return(values_event)

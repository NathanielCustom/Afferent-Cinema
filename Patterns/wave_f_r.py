position_extreme = 0
delay_extreme = 0
analysis_ran = 0

def pattern_name():
	return("wavefromfront")

def reset_analysis():
	global position_extreme
	position_extreme = 0
	global delay_extreme
	delay_extreme = 0
	return()

def position_analysis(hwprofile_file):
	global analysis_ran
	
	if analysis_ran != 0:
		return()
	
	else:
		global position_extreme
		global delay_extreme
		
		## Find Most Extreme Position ##
		device_total = len(hwprofile_file["hw"])
		for device in xrange(device_total):										# Get number of Devices in HW Profile
		
			
			if hwprofile_file["hw"][device]["ypos"] > position_extreme:				
				position_extreme = hwprofile_file["hw"][device]["ypos"]			# Record most extreme Y-Position
				
			if 'delay' in hwprofile_file["hw"][device]:
				if hwprofile_file["hw"][device]["delay"] > delay_extreme:		# Record most extreme Delay
					delay_extreme = hwprofile_file["hw"][device]["delay"]
		analysis_ran = 1
	return()
						

def leadup_calc(event_file, event):
	global position_extreme
	global delay_extreme
		
	# Calculate ts_lead # 
	timestamp = event_file["events"][event]["ts_center"]				# Seconds
	wavespeed = event_file["events"][event]["wavespeed"]				# Chairs/Second ~= Meters/Second
	leadtime = position_extreme / wavespeed
	event_file["events"][event]["ts_lead"] = timestamp - leadtime - delay_extreme

	return(position_extreme)
	
	
def ts_calc(device, event, delay):

	t_offset = ( device["ypos"] * event["wavespeed"] ) + delay
	ts_position = event["ts_center"] - t_offset
	
	return(ts_position)

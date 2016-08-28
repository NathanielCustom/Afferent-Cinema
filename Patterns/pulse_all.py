def pattern_name():
	return("pulseall")

def reset_analysis():
	global position_extreme
	position_extreme = 0
	global delay_extreme
	delay_extreme = 0
	return()

def position_analysis(hwprofile_file):
	#global analysis_ran
	
	#if analysis_ran != 0:
		#return()
	
	#else:
		#global position_extreme
		#global delay_extreme
		
		### Find Most Extreme Position ##
		#device_total = len(hwprofile_file["hw"])
		#for device in xrange(device_total):											# Get number of Devices in HW Profile
		
			#print ("Leadup Calc. - Position Analysis - Wave - Front to Rear - Device: #" + str(device))	# Print Progress Check
		
			#if hwprofile_file["hw"][device]["ypos"] > position_extreme:				
				#position_extreme = hwprofile_file["hw"][device]["ypos"]				# Record most extreme Y-Position
				#print ("Position: " + str(position_extreme))
				#print ("Leadup Calc. - Poition Analysis -  Wave - Front to Rear - Device: #" + str(device) + " - New Extreme Position: " + str(position_extreme))	# Print Progress Check
		
			#if 'delay' in hwprofile_file["hw"][device]:
				#if hwprofile_file["hw"][device]["delay"] > delay_extreme:		# Record most extreme Delay
					#delay_extreme = hwprofile_file["hw"][device]["delay"]
					#print ("Leadup Calc. - Position Analysis - Wave - Front to Rear - Device: #" + str(device) + " - New Extreme Delay: " + str(delay_extreme))	# Print Progress Check
		#analysis_ran = 1
	return()
			

def leadup_calc(event_file, event):
	#print ("Initialize Values - Pulse - ALL - Leadup Calc. - Event: #" + str(event) + " - #BEGIN#")	# Print Progress Check
	fake_value = 0
	
	#print ("Initialize Values - Pulse - ALL - Leadup Calc. -  #END#")	# Print Progress Check


def ts_calc(device, event, delay):
	#print ("Pattern Assessment - Pulse - ALL - Value Calc. - #BEGIN#")	# Print Progress Check
	
	t_offset = delay
	ts_position = event["ts_center"] - t_offset
	
	#print ("Pattern Assessment - Pulse - ALL - Value Calc. - #END#")	# Print Progress Check	
	
	return(ts_position)

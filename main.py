# External Module Imports
import RPi.GPIO as GPIO
import time
import smbus			# I2C Communication Ports
import json				# Event and HW File Read/Write
import os
import re				# Regex for File Searching
import sys
import i2c_control		# I2C Communication Python Program
import importlib		# Dynamic Module Importing
from dejavu import Dejavu
from dejavu.recognize import MicrophoneRecognizer
import threading
from operator import itemgetter

### Lists ###

## Loaded Files ##
root_foldercontents = ' '.join(os.listdir('./'))						# Write all files in ./ as string
pattern_regex = re.compile(r'\w+loaded\_files\.json')					
file_lists = pattern_regex.findall(root_foldercontents)					# Generate a list from the string with regex value


### Generate Directories ###

# Flagged Events queued for Execution #TODO removal?
flagged_events = {}	

# PWM Controllers
controller_addresses = []

# Event Row - marks the current event to be processed
eventMonitor = {}
list_n = 0
for file_dir in file_lists:
	eventMonitor[list_n] = 0
	list_n = list_n + 1

## File Name Directories are coorelated with the given File Lists ##

# Events File Names -
events_filename = {}
list_n = 0
for file_dir in file_lists:
	events_filename[list_n] = json.load(open(file_dir))["files"][0]["events"]
	list_n = list_n + 1 


# Hardware Type File Names-
hwtype_programname = {}
list_n = 0
for file_dir in file_lists:
	hwtype_programname[list_n] = json.load(open(file_dir))["files"][0]["hw_type"]
	list_n = list_n + 1 


# Hardware Profile File Names -
hwprofile_filename = {}
list_n = 0
for file_dir in file_lists:
	hwprofile_filename[list_n] = json.load(open(file_dir))["files"][0]["hwprofile"]
	list_n = list_n + 1 


# Pattern Profile File Names - 
print ("Initialize Values - Search for Patterns")	# Print Progress Check
sys.path.append('./Patterns')										# Import Pattern Folder Location to Python
pattern_foldercontents = ' '.join(os.listdir('./Patterns'))			# Write all files in ./Patterns as string
pattern_regex = re.compile(r'\w+\.pyc|(\w+)\.py')					# Filter all values to .pyc and .py extensions. Only .py file names are stored.
pattern_filelist = pattern_regex.findall(pattern_foldercontents)	# Generate a list from the string with regex value

# Remove "Empty" Values from Final Pattern List
pattern_listtotal = len(pattern_filelist)
for entry in xrange(pattern_listtotal, 0, -1):
	if pattern_filelist[entry-1] == '':
		del pattern_filelist[entry-1]


# Pattern Name to Pattern File Dictionary
pattern_dictionary = {}
pattern_listtotal = len(pattern_filelist)
for pattern_num in xrange(pattern_listtotal):
	value = importlib.import_module(pattern_filelist[pattern_num]).pattern_name()
	pattern_dictionary[value] = (pattern_filelist[pattern_num])			# Coorelates name of pattern found in Event to the name of the Pattern Module


#### Calibrate / Initialize Values ####
### Calibrate Event Files to Room Hardware Placement & Reset HW Profiles ###
def values_initial():	
	
	global controller_addresses
	
	### Calculate Initial Values ###
	eventMonitor = 0
	for file_dir in file_lists:
		
		# Load Files
		event_filename = json.load(open(file_dir))["files"][0]["events"]
		event_file = json.load(open(event_filename))
		hwprofile_filename = json.load(open(file_dir))["files"][0]["hwprofile"]	
		hwprofile_file = json.load(open(hwprofile_filename))
		
		
		
	## Calculate Most Extreme Device Position ##
		# For each Event and each Pattern File
		events_total = len(event_file["events"])								# Get number of Events in Event List
		for event in xrange(events_total):										# Calculate for each Event
			if event_file["events"][event]["pattern"] in pattern_dictionary:
				pattern_value = pattern_dictionary[(event_file["events"][event]["pattern"])]
				importlib.import_module(pattern_value).position_analysis(hwprofile_file)			# Analysis Positional Values
				importlib.import_module(pattern_value).leadup_calc(event_file, event)				# Execute Pattern Leadup Calculations
			
			# No Matching Pattern File Found - Default to Pulse All #
			else:
				importlib.import_module("pulse_all").leadup_calc(event_file, event)
				

		# Reset Positional Analysis
		pattern_total = len(pattern_filelist)
		for pattern_num in xrange(pattern_total):
				importlib.import_module((pattern_filelist[pattern_num])).reset_analysis()
				
		# Sort Event List by ts_lead
		sortedevents_list = sorted(event_file["events"], key=itemgetter('ts_lead'))
		json.dump({"events":sortedevents_list}, open(event_filename, 'w'), sort_keys = True, indent = 4, ensure_ascii = False)
		
		
	## Reset HW Previous Values ##		
		# For each Device		
		device_total = len(hwprofile_file["hw"])
		for device in xrange(device_total):
			#hwprofile_file["hw"][device]["value_previous"] = 0	# TODO, this isn't a global variable, how is this helpful? Plus, do we need the prev_val in the JSON file?
		## Initialize Device Values ##
			i2c_control.initialize_device(hwprofile_file["hw"][device]["address_i2c"], hwprofile_file["hw"][device]["channel_msb"], hwprofile_file["hw"][device]["channel_lsb"])
			if hwprofile_file["hw"][device]["address_i2c"] not in controller_addresses:
				controller_addresses.append( (hwprofile_file["hw"][device]["address_i2c"]) )
		# Write Previous Values to Loaded JSON File
		json.dump(hwprofile_file, open((json.load(open(file_dir))["files"][0]["hwprofile"]), 'w'), sort_keys = True, indent = 4, ensure_ascii = False)
	
	## Initialize Controllers #
	i2c_control.initialize_controller(controller_addresses)
	
	return()



### Buffers (define precision) ###
bufferTime = 0.1											# minimum time to pass before allowing subsequent processing
bufferTrigger = 0.1 										# min/max time frame that trigger can be fired, otherwise it is skipped


### Global Variables ###
markertimestamp_movie = 0			# Place in movie Dejavu calculates to be present; Do not call directly; go through thread locking function
cputimestamp_movie = time.time()	# CPU time for calculating current place; revalued when markertimestamp_movie is determined


### Main Operation Functions ###
def movietime(marker, action):
	lock = threading.Lock()		# Why must this be declared, why isn't threading.Lock().acquire() suitable?
	lock.acquire()
	
	try:
		global markertimestamp_movie
		global cputimestamp_movie
	
		if action == 'store':
			markertimestamp_movie = marker
			cputimestamp_movie = time.time()
			return ()
	
		if action == 'retrieve_marker':
			return (markertimestamp_movie)

		if action == 'retrieve_cpu':
			return (cputimestamp_movie)

	finally:
		lock.release()


def calc_currenttimestamp():
	timestamp = (time.time()- movietime(None, 'retrieve_cpu')) + movietime(None, 'retrieve_marker')
	return (timestamp)
	
def counter(event_file, list_n):
	while event_file["events"][eventMonitor[list_n]]["ts_lead"] + bufferTrigger < calc_currenttimestamp(): # Has the time for the Event to trigger passed?
		eventMonitor[list_n] = eventMonitor[list_n] + 1													# Move Counter to next line
	return()
							

def patternfunction(device_entry, event):

	global pattern_dictionary

	if 'p_assessed' not in event[device_entry]:						# Only needs to be run once since pattern values don't change.
	## Event Transition ##
		# Non-Transitioning Event #
		if event[0]["t_transition"] <= 0:								# Includes values less than 0 result in an automatic 100%
			t_transition = 0.01											# Can't divide later by a Zero
		# Transitioning Event #
		else:
			t_transition = event[0]["t_transition"]
		
	## Device Delay ##	
		if 'delay' in event[device_entry]:
			delay = event[device_entry]["delay"]
		else:
			delay = 0
		
	## Pattern Assessment ##	
		if event[0]["pattern"] in pattern_dictionary:
			ts_position = importlib.import_module((pattern_dictionary[ (event[0]["pattern"]) ])).ts_calc(event[device_entry], event[0], delay)
		else:
			ts_position = event[0]["ts_center"]
	
	## Store Values ##
		event[device_entry]['t_transition'] = t_transition
		event[device_entry]['delay'] = delay
		event[device_entry]['ts_position'] = ts_position
		event[device_entry]['p_assessed'] = True
	
## Calculate Value Percent ##
	value_percent = ( calc_currenttimestamp() - event[device_entry]['ts_position'] ) / event[device_entry]['t_transition']

	#if value_percent <= 0:
		#value_percent = 0
		#event[device_entry]["update_value"] = True					# 'Flag' device for Previous Value update
	if value_percent >= 1.00:											
		value_percent = 1.00
		event[device_entry]['complete'] = True						# 'Flag' device that it has completed its transition
		## Test Output ##
		#json.dump(flagged_events, open('flagged_devices_dump.json', 'w'), sort_keys = True, indent = 4, ensure_ascii = False) # dump check
	
	return(value_percent)
	

def scalingfunction(event):
	
	
	loaded_commands	= {}	# Clear Dictionary of Commands to Pass to I2C
	commands_entry = 0		# Reset where to start entering Commands
	total_complete = 0		# Counts the number of complete devices
			
	# Determine HW Type
	hwtype_name = event[0]["hwtype"]
	
	# Determine HW Profile
	hwprofile_name = event[0]["hwprofile"]
	hwprofile = json.load(open(hwprofile_name))
	
	## Assess each Device for Value ##
	devices_total = len(event) - 1		# Get total number of flagged devices currently in row (-1, first row is Event)

	for device_entry in xrange( 1, (devices_total + 1) ):				# Shift values for xrange
		if 'complete' not in event[device_entry]:
			
			# Calculate pattern_percent in Pattern Function
			pattern_percent = patternfunction( device_entry, event )	# Also sets flags for 'complete'
			
			# Get I2C and Channel addresses of device
			address = event[device_entry]["address_i2c"]
			ch_msb = event[device_entry]["channel_msb"]
			ch_lsb = event[device_entry]["channel_lsb"]
			value_previous = event[device_entry]["value_previous"]
			
			## Process Flags & Load Commands ##
			
			# 'Update Flag' Management
			if "update_value" in event[device_entry] and pattern_percent > 0:
				#value_previous = hwprofile["hw"][device]["value_previous"] 				# Write new value to variable, OLD (see below operations)
				# Get value_previous from I2C
				device_address = {}
				device_address[0] = {"address":address, "msb":ch_msb, "lsb":ch_lsb}
				value_previous = i2c_lock(device_address, 'receive')						# Not a separate thread because we need this before proceeding
				event[device_entry]["value_previous"] = value_previous						# Write new value to flagged device
				del event[device_entry]["update_value"]										# Delete Update 'Flag' Key
			
			## OLD, don't need? moved to pattern_function						
			#elif pattern_percent <= 0:															# Device not ready to execute
				#event[device_entry]["update_value"] = True									# 'Flag' device for Previous Value update
						
						
			# Get new values
			if pattern_percent > 0:					
				values_event = importlib.import_module( hwtype_name ).processtrigger(pattern_percent, hwprofile_name, event[device_entry], event, value_previous)	
				
				# Load Commands to be sent over I2C
				loaded_commands[commands_entry] = {"value":values_event[0], "address":address, "msb":ch_msb, "lsb":ch_lsb}
				commands_entry += 1	
						
		else: # 'complete' in event[device_entry]
			total_complete += 1
			if total_complete == devices_total:
				loaded_commands = False
				return(loaded_commands)
			else:
				continue
	return(loaded_commands)


def eventsyc():
	return()
	# In each event file run through from the beginning of the list up to the current time.
	# Write I2C values to a list overwriting "earlier" events with "later" events.
	# When done processing events, pass list off to send commands over I2C.
	
	# start at event 0
	# while event ts_lead < current time
	# calc hw and value
	# store in dictionary


### New Functions and Classes ###
	
def i2c_lock(loaded_commands, action):
	
	# Manages the I2C traffic by locking threads out until released by previous thread #
	
	lock = threading.Lock()
	lock.acquire()
	
	if action == 'send':
		try:
			for entry in xrange(len(loaded_commands)):
				i2c_control.device_write( loaded_commands[entry]["value"], loaded_commands[entry]["address"], loaded_commands[entry]["msb"], loaded_commands[entry]["lsb"]  )

		finally:
			lock.release()
			return (False)
			
	elif action == 'receive':
		try:
			for entry in xrange(len(loaded_commands)): # TODO, not multi entry ?
				value_current = i2c_control.device_read( loaded_commands[entry]["address"], loaded_commands[entry]["msb"], loaded_commands[entry]["lsb"]  )
				
		
		finally:
			lock.release()
			return (value_current)
	
class i2csender(threading.Thread):
	# This non-daemon thread sends the commands through to i2c_lock to manage I2C traffic via thread locking #
	def __init__(self, loaded_commands, action):
		threading.Thread.__init__(self)
		self.loaded_commands = loaded_commands
		self.action = action
	def run(self):
		value_current = i2c_lock(self.loaded_commands, self.action)		# Do we ever request a value with this thread? If not, remove value_current
		return (value_current)
	
class eventexecute(threading.Thread):	
	def __init__(self, event):
		threading.Thread.__init__(self)
		self.event = event
	def run(self):
		frequency = .02													# .02 seconds = 50Hz
		
		while True:
			startloop = time.time()
			
			loaded_commands = scalingfunction(self.event)				# Calculate value and return I2C commands
			
			if loaded_commands == False:								# All devices marked as 'complete'
				break

			else: 
				# Start a non-daemon I2C thread (so that I2C can't be interrupted)
				i2csender(loaded_commands, action = 'send').start()
		
			endloop = time.time()
			
			# Frequency
			if frequency > (endloop - startloop ):
				time.sleep( frequency - ( endloop - startloop ) )
			
		

class eventmonitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			# TODO, frequency locking
			
			#try:
			list_n = 0 # Start at the first entry (for eventMonitor)
			
			## Check Current Events for valid Trigger Time ##
			for file_dir in file_lists:																# Read through each File List
				event_file = json.load(open(events_filename[list_n]))								# Load Event File
				
				counter(event_file, list_n)															# Adjust Counter to soonest relevant Event
				
				if calc_currenttimestamp() >= event_file["events"][eventMonitor[list_n]]["ts_lead"] - bufferTrigger:
					
					## Store File Data ##
					event = {}
					event[0] = event_file["events"][eventMonitor[list_n]]
					event[0]["hwtype"] = hwtype_programname[list_n]									# Add HW_Type to event[]
					event[0]["hwprofile"] = hwprofile_filename[list_n]								# Add HW_Profile to event[]
		
					## Store Device Data ##		
					device_entry = 1
					for device in xrange(len(json.load(open(hwprofile_filename[list_n]))["hw"])):	# For each device in HW Profile													
						
						## Directional Limitations ##	---		#Future Usage for Directional Buffers
						if ( "direction" in event[0] ) and ( "direction" in json.load(open(hwprofile_filename[list_n]))["hw"][device] ):	# 'direction' must be found in both documents
							if json.load(open(hwprofile_filename[list_n]))["hw"][device]["direction"] == event[0]["direction"]:				# 'direction' is the same in both documents
								event[device_entry] = {}
								event[device_entry] = json.load(open(hwprofile_filename[list_n]))["hw"][device]								# Add Device to Dictionary
							else:
								continue								# Directional not compatable with event
						elif "direction" not in event[0]:				# Non-Directional event
							event[device_entry] = {}
							event[device_entry] = json.load(open(hwprofile_filename[list_n]))["hw"][device]									# Add Device to Dictionary
						else:	# TODO, is there a case where this is needed?
							continue
												
						event[device_entry]['update_value'] = True
						print "updated an entry"
						device_entry += 1
				
					## Test Output ##
					json.dump(event, open('event_dump.json', 'w'), sort_keys = True, indent = 4, ensure_ascii = False)		
					
					## Execute Event Thread
					eventexecute.daemon = True
					eventexecute(event).start()
					
					eventMonitor[list_n] = eventMonitor[list_n] + 1									# Move Counter to next line

						
				list_n = list_n + 1																	# Tick to check next File List
				## TODO, do we need a wait in here to set frequency?
			#except:
				#print "eventmonitor thread error"


def keyboardescape():
	#bus = smbus.SMBus(1)
	#bus.write_byte_data(0x40, 0x00, 0x10)
	global controller_addresses
	## Turn off all PWM boards ##
	loaded_commands = {}
	for entry in xrange(len(controller_addresses)): #TODO rename source
		loaded_commands[entry] = {}
		loaded_commands[entry]["value"] = 0x40
		loaded_commands[entry]["address"] = controller_addresses[entry]
		loaded_commands[entry]["msb"] = 0x00
		loaded_commands[entry]["lsb"] = 0x10

	i2csender(loaded_commands, 'send').start()



class synctime(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		with open("dejavu.cnf") as f:
			config = json.load(f)
			
		id_specific = None
		starteventmonitor = True
		djv = Dejavu(config)											#Bypassed DB cataloging in __init__ component
		secs = 5														# Initial sample length to identify media
		while True:
			try:	
				while True:
					calctime_start = time.time()						# Processing Time Compensation (1/2)
		
					# Reduce sample length once track ID'd
					if id_specific != None:
						secs = 3
						if starteventmonitor == True:
							eventmonitor.daemon = True
							eventmonitor().start()						# Starts eventmonitor now that track is identified
							starteventmonitor = False
							
					song = djv.recognize(MicrophoneRecognizer, id_specific, seconds=secs)
					
					if song is None:
						print "Nothing recognized -- did you play the song out loud so your mic could hear it? :)"
					else:
						print "From mic with %d seconds we recognized: %s\n" % (secs, song)
					
					calctime_end = time.time()							# Processing Time Compensation (2/2)
					
					## ID stored if confident enough and not already identified
					if ( song['confidence'] > 10 ) and id_specific == None:
						id_specific = song['song_id']
					
					print "check offset seconds" #print check
					print song["offset_seconds"] #print check
					print calctime_end-calctime_start #print check
					
					## Recalculate Current Marker Time
					if song['confidence'] > 15:
						movietime(( (calctime_end-calctime_start) + song["offset_seconds"] ), 'store')
						print "Marker Time adjusted to %s" % movietime( None, 'retrieve_marker' )
					else:
						print "Not enough Confidence" #print check
						print "Current time is %s" % calc_currenttimestamp()
	
			except:
				print "synctime thread error"			

### Main Body ###
# Initialize #
values_initial()


try:
	mode = True
	while mode:
		print "Input Mode: \n 1. Offset Time \n 2. Dejavu Time"
		selection = input("")
		
		if selection == 1:
			markertime_offset = input("Input movie start time marker (seconds) ")
			markertime_movie = time.time() - markertime_offset
			eventmonitor.daemon = True
			eventmonitor().start()
			mode = False
	
		elif selection == 2:
			synctime.daemon = True
			synctime().start()
			mode = False
	
		else:
			""
	
	# Keep main thread alive to monitor for exit (keyboardinterrupt)
	while True:
		time.sleep(20) # pass would cause Dejavu to fail with IOError Overflow, value is arbitrary
		
except KeyboardInterrupt:
	keyboardescape()

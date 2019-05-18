# Module Imports
import time                     # Matching Playback to CPU Time
import threading
import re                       # Regex for File Searching
import importlib                # Dynamic Module Importing
import json
from operator import itemgetter # For sorting events in event_file by 'timestamp_start' value
import os
import copy
try:
    from Audio_Recognition.dejavu import Dejavu
except:
    print ("WARNING: Failed to Import Dejavu --- Audio Recognition will not work.")
try:
    from Audio_Recognition.dejavu.recognize import MicrophoneRecognizer
except:
    print ("WARNING: Failed to Import Dejavu.Recognize --- Audio Recognition will not work.")

# Session
folder_session = './Sessions/How_to_Train_Your_Dragon/'
file_extension = '.py'

# Timestamps
time_movie_start = time.time()

# Frequency Locking
frequency_event_monitor = 0.02
frequency_event_process = 0.02

# Buffers
buffer_event_trigger = .02      # Creates a plus-or-minus window for when the event can trigger. If processing
                                # is fast and always triggering in the minus window than we may want to consider
                                # creating two separate variables for addressing the program's needs.

# Threading Events
start_monitoring = threading.Event()
audiosync_setup_complete = threading.Event()



###################################################################################################################################################
#################################################### CLASSES ######################################################################################
###################################################################################################################################################

class AudioSync(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        global time_movie_start

        ############ Initialize Audio Recognition ##############
        ## Access Dejavu Database ##
        config_path = os.path.abspath(os.path.join("config.json"))
        config = json.load(open(config_path))
        database_query = (
                            "mysql+mysqlconnector://"
                            + str(config["database_username"])
                            + ":"
                            + str(config["database_password"])
                            + "@"\
                        + str(config["database_address"])
                            + "/"\
                            + str(config["database_name"])
                        )    
        dburl = os.getenv('DATABASE_URL', database_query)
        djv = Dejavu(dburl=dburl)

        
        ## Run Through Audio Related Warnings and Clear Screen ##
        void = djv.recognize(MicrophoneRecognizer, 0.01)    
        #os.system('clear')


        ### Flag Intialization Complete and Wait for Main Program ###
        audiosync_setup_complete.set()
        start_monitoring.wait()


        ############ Audio Recognition##############  
        sample_length = 3                                               # Initial sample length to identify media
        reset_length = 5                                                # Amount of time (seconds) changed before resetting hardware.
        id_specific = None

        while True:
            try:    
                processing_time_start = time.time()                        # Processing Time Compensation (1/2)

                # Reduce sample length once track ID'd
                if id_specific != None:
                    sample_length = 5

                try:    
                    movie = djv.recognize(MicrophoneRecognizer, seconds=sample_length)
                except:
                    print ("Dejavu Failed... starting again")

                processing_time = time.time() - processing_time_start   # Processing Time Compensation (2/2)
    

                if movie is None:
                    print ("\nNothing recognized -- verify audio and microphone settings.\n")
                else:
                    print ("\n%s recognized from sample with confidence %s.\n" % (movie['song_name'], str(movie["confidence"])))


                ## ID stored if confident enough and not already identified ##
                if (movie['confidence'] > 3) and (id_specific == None):
                    id_specific = movie['song_id']
                    time_movie_start = time.time() - (processing_time + movie["offset_seconds"])    #offset_seconds is the timestamp for the beginning of the sample
                    h, m, s = time_format(timestamp_movie_playback())
                    print ("Movie ID'd. Current movie time adjusted to %d:%d:%d" % (h, m, s))

                ## Recalculate Current Marker Time; Greater Confidence expected to change time. ##
                elif movie['confidence'] > 10:
                    prev_time_movie_start = time_movie_start
                    time_movie_start = time.time() - (processing_time + movie["offset_seconds"])    #offset_seconds is the timestamp for the beginning of the sample
                    h, m, s = time_format(timestamp_movie_playback())
                    print ("Current movie time adjusted to %d:%d:%d" % (h, m, s))
                    
                    ''' Any change in time greater than provided amount causes hardware to reset to minimize adverse effects when skipping through movie'''
                    if abs(time_movie_start - prev_time_movie_start) >= reset_length:
                        reset_hardware(hardware_directory)
                        print ("Time Change Threshold Met: Resetting Hardware")
                    
                else:
                    print ("Not enough Confidence.")
                    h, m, s = time_format(timestamp_movie_playback())
                    print ("Current movie time is %d:%d:%d" % (h, m, s))
                        
            except:
                print ("\nWARNING: Audio Recognition Thread Error\n")    


class EventMonitor(threading.Thread):
    def __init__(self, event_list, hardware_device_list):
        threading.Thread.__init__(self)
        self.event_list = event_list
        self.hardware_device_list = hardware_device_list
        # Example: hardware_device_list = [ {"address":[1,2,3],...}, {"address":[4,5,6],...} ]
        # Example: event_list = 
        #    [ {"timestamp_start": 1.0,...}, {"timestamp_start": 23.3},... ]
        
    def run(self):
        '''
        Monitors the passed event_file for triggered events. The events should already have timestamp_start calculated and 
        be in ascending order. First we synchronize to the next potential event, bypassing completed/passed events.
        '''
        global buffer_event_trigger
        global frequency_event_monitor


        ### Wait for Main Program ###
        start_monitoring.wait()


        ### Find Next Valid Event ###
        '''
        FALSE statement implies that the event has not been passed and is available for processing.
        TRUE statement implies that the event has been passed so the next event should be examined. 
        '''
        try:
            event_index = 0 # Start at the first entry in event_file
            while timestamp_movie_playback() > self.event_list[event_index]['timestamp_start'] + buffer_event_trigger :  # Cycle through events until timestamp_start + buffer trigger is less than the current time stamp
                event_index = event_index + 1
            ismonitored = True
            
            # Display #
            print ("Event Queued: " + str(self.event_list[event_index]["description"]))   
        
        except:
            print ("EventMonitor: Thread " + str(threading.current_thread()) + " has no Events to monitor.")
            ismonitored = False

        ### Monitor Event ###        
        while ismonitored == True:
            startloop = time.time()
            ## Check Current Events for valid Trigger Time ##
            try:
                if timestamp_movie_playback() >= self.event_list[event_index]["timestamp_start"] - buffer_event_trigger:
                    event = self.event_list[event_index]
             
                    ## Execute Event Thread ##
                    EventProcess.daemon = True
                    EventProcess(event, self.hardware_device_list, threading.current_thread()).start()
                    event_index += 1
                    
                    # Display #
                    print ("Event Queued: " + str(self.event_list[event_index]["description"]))   

                else:
                    '''
                    Manages the amount of time spent on checking trigger conditions.
                    Minimum amount of time between 'if' statement checks.
                    Upon trigger in 'if' statement, no sleep is performed and next event_index is immediately checked.
                    '''
                    endloop = time.time()
                    if  frequency_event_monitor - ( endloop - startloop ) > 0:
                        time.sleep(frequency_event_monitor - (endloop - startloop))                                 
            except IndexError:                                 # If exception raised, end the thread.
                print ("EventMonitor: Thread " + str(threading.current_thread()) + " has reached end of file.")
                ismonitored = False


class EventProcess(threading.Thread):
    def __init__(self, event, hardware_device_list, eventmonitor_thread_id):
        threading.Thread.__init__(self)
        self.event = event
        self.hardware_device_list_monitor = hardware_device_list
        # Example: hardware_device_list = [ {"address":[1,2,3],...}, {"address":[4,5,6],...} ]
        self.monitor_id = eventmonitor_thread_id

    def run(self):
        global frequency_event_process
        
        
        ### Variables ###
        hardware_device_list_process = copy.deepcopy(self.hardware_device_list_monitor)
        pattern_folder = which_pattern_folder(self.event)


        ### Remove Devices not Triggered by Pattern ###
        hw_isincluded_list = []
        for device in hardware_device_list_process:
            isincluded = importlib.import_module(pattern_folder).device_inclusion(device)
            if isincluded == True:
                hw_isincluded_list.append(hardware_device_list_process[hardware_device_list_process.index(device)])                
        hardware_device_list_process = hw_isincluded_list             # Copy Over New List


        ## Execute Device Trigger Thread ##
        for device in hardware_device_list_process:
            # Example: hardware_device_list_process = [ {"address":[1,2,3],...}, {"address":[4,5,6],...} ]
            # Example: device = 
            #   {"address":[1,2,3], "controller":"PCA9685", "x_position":0, "values":[120, 46, 34], I2C_address":68}
               
            DeviceTrigger.daemon = True
            DeviceTrigger(device, self.event, self.monitor_id, pattern_folder).start()


        return()


class DeviceTrigger(threading.Thread):
    def __init__(self, device, event, monitor_id, pattern_folder):
        threading.Thread.__init__(self)
        self.device = device
        self.event = event
        self.monitor_id = monitor_id
        self.pattern_folder = pattern_folder

    def run(self):
        devicelist_lock = threading.Lock()
        isProcessing = True
        
        ### Process Device for Trigger Time & Send Commands ###
        while isProcessing:
            startloop = time.time()
            
            ## Build values List ##

            # Calculate value_percent based on current time and pattern
            timestamp_position = importlib.import_module(self.pattern_folder).timestamp_position(self.device, self.event)
            value_percent = ( timestamp_movie_playback() - timestamp_position ) / self.event["time_transition"]
            

            ## Legal value check ##
            if value_percent >= 1.00:                                            
                value_percent = 1.00                                                        # Transition Complete...
            if value_percent < 0:
                value_percent = 0
                

            ## Send values to controller ##
            if value_percent != 0:            # Otherwise, queued events where particular device is not triggered yet will interfere with 'Zero' commands
                # Apply value_percent to target value (defined in event) as a 'step'.
                values = importlib.import_module(self.device["device_driver"]).values_step(self.device, self.event, value_percent, folder_session)
                    # Example: values = [230, 45, 0]
                
                # Error Fixing #
                '''
                Error Fixing: It is beyond me why as soon as any equation is executed values loses
                its value and becomes and empty list. To correct, I have made a deep copy
                before any equation.
                '''
                values_copy = copy.deepcopy(values)
                
                importlib.import_module(self.device["controller_driver"]).main(self.device, values)
                
            ## Update 'Master' Hardware List ##
            '''
            Writes values to EventMonitor ("master") instance of hardware_device_list[_monitor]
            '''
            if value_percent == 1.00:
                # Start thread to update instance of device list
                UpdateDeviceList.daemon = True
                UpdateDeviceList(self.device, values_copy, self.monitor_id, devicelist_lock).start()
                isProcessing = False

            ## Manage the amount of time spent on calculating values ##
            endloop = time.time()
            if  frequency_event_process - ( endloop - startloop ) > 0:
                time.sleep( frequency_event_process - (endloop - startloop) )
        


class UpdateDeviceList(threading.Thread):
    def __init__(self, device, values, monitor_id, devicelist_lock):
        threading.Thread.__init__(self)
        self.device = device
        self.values = values
        self.monitor_id = monitor_id
        self.devicelist_lock = devicelist_lock

    def run(self):
        #process values
        self.devicelist_lock.acquire()

        ### Find Match ###
        '''
        Itterates through all devices in Event Monitor's hardware list looking for a match
        against the passed 'device' to be updated. The 'I2C_address' and 'address' keys qualify
        if a match is found. When a match is found the passed values are written to the hardware
        list as 'values'.
        Future implementation of multiplexors can add an additional 'if' statement before the
        'I2C_address' check.
        '''
        
        
        # Error Fixing #
        '''
        Error Fixing: It is beyond me why as soon as any equation is executed self.values loses
        its value and becomes and empty list. To correct, I have made a deep copy
        before any equation.
        '''
        values_copy = copy.deepcopy(self.values)
        
        #print ("UPDATE VALUES THREAD")
        thread_device_list = self.monitor_id.hardware_device_list     
        for device in self.monitor_id.hardware_device_list:
            if thread_device_list[thread_device_list.index(device)]["I2C_address"] == self.device["I2C_address"]:
                if thread_device_list[thread_device_list.index(device)]["address"] == self.device["address"]:
                    self.monitor_id.hardware_device_list[thread_device_list.index(device)]["values"] = values_copy
                    #print ("UPDATED VALUES to: " + str(values_copy) + " for " + str(self.device["I2C_address"]) + ": " + str(self.device["address"]))

        self.devicelist_lock.release()


###################################################################################################################################################
################################################### FUNCTIONS #####################################################################################
###################################################################################################################################################

def initialize_hardware(hardware_directory):
    '''
    Imports the controller drivers for each type listed in the hardware_directory.
    Then passes the controller dictionary to the associated driver for initializing the hardware itself.
    '''
    controller_list = []

    for controller in hardware_directory:
        # Example: controller = 40 -or- 68
        # Example: hardware_directory[controller] =
        #   {'address': 40, 'device_group': {'00':{'address':[1,2,3,4],...}, '01':{'address':[5,6,7,8],...},... }

        if hardware_directory[controller]["controller"] not in controller_list:
        # Import Controller Driver
            controller_list.append(hardware_directory[controller]["controller"])
            # is this necessary? does it help?
            try:
                importlib.import_module(hardware_directory[controller]["controller_driver"])
            except:
                print ("initialize_hardware: error")

    # Intialize/Reset Controllers
    reset_hardware(hardware_directory)

    return ()


def keyboardescape(hardware_directory):
    #TODO Kill all threads so they are not trying to execute commands while shutting down.

    for controller in hardware_directory:
        # Example: controller = 40 -or- 68
        if "null" not in hardware_directory[controller]:
            importlib.import_module(hardware_directory[controller]["controller_driver"]).shutdown(hardware_directory[controller])
                # Example: hardware_directory[controller] =
                #   {'address': 40, 'device_group': {'00':{'address':[1,2,3,4],...}, '01':{'address':[5,6,7,8],...},... }
    return()


def load_system():
    """
    After initializing the system, the main thread builds a hardware list for each event file,
    starts a thread per event file, and monitors triggering times.
    A new thread is created and passes on the event for the value to be calculated at regular 
    intervals. The calculated value is then passed onto the proper driver where it is constructed
    into a format that the receiving controller can understand.
    """

    ############ Build Events List ##############
    ''' 

    '''
    session_foldercontents = ' '.join( os.listdir(folder_session) )                # Write all files in ./Sessions/Despicable_Me as string session_foldercontents
    pattern_regex = re.compile(r'\w+\_events\.json')
    session_folder_events = pattern_regex.findall(session_foldercontents)       # Generate a list from the string with regex value


    ######## Import & Calibrate Files ########
    '''
    Each event file, in the selected session folder, will be monitored by a thread.
    Prior to starting the thread a "quick reference" list of applicable hardware is built.
    The list reduces the amount of scanning each thread will have to do later when applying event triggers.

    Future will provide means of selecting the folder or a permanent "active" directory
    '''
    hardware_directory = json.load(open('./Hardware/hardware_directory.json'))                  # Open hardware_directory.json
    initialize_hardware(hardware_directory)                                                     # Initialize Hardware
    

    for event_file_name in session_folder_events:                                               # For each event file name listed and ...                                                 
        event_file = json.load(open(folder_session + event_file_name))                          # open the event_file.
  
        hardware_device_list = []
        
        # Preprocess Files
        hardware_device_list = preprocess_hardware_device_list(hardware_directory, event_file)  # Append additional devices that match to list.
            # Example: hardware_device_list = [ {"address":[1,2,3],...}, {"address":[4,5,6],...} ] 

        event_file = preprocess_patterns(event_file, hardware_device_list)         # Which patterns and at what timestamp?
        event_list = preprocess_events(event_file)
            # Example: event_list = 
            #    [ {"timestamp_start": 1.0,...}, {"timestamp_start": 23.3},... ]
            
        # Start Event Monitoring Thread
        EventMonitor.daemon = True
        EventMonitor(event_list, hardware_device_list).start()
    
    return(hardware_directory)
   

def preprocess_events(event_file):
    '''
    Sort Event List by timestamp_start
    '''
    event_list = sorted(event_file["events"], key=itemgetter('timestamp_start'))
    return (event_list)


def preprocess_hardware_device_list(hardware_directory, event_file):
    '''
    Finds matching devices in hardware_directory as defined by passed event_file. Matches are
    put into hardware_device_list list which will be unique to each event monitoring thread.
    '''
    hardware_device_list = []

    for controller in hardware_directory:                                                          # For each key (I2C Address) in the top level of hardware_directory...
            # Example: controller = 40
            # Example: hardware_directory[controller] =  
            #   { 'address':40, 'controller':'PCA9685'...'device_group':{ "40":{...}},{"68":{...} } }   
        if hardware_directory[controller]["controller"] == event_file["controller"]:                                   # and the controller value matches the controller value in the event file...
        
            # Build Hardware List
            for device_group in hardware_directory[controller]["device_group"]:                                        # then check each device group...
                # Example: device_group = 00 -or- 01 -or- 02...
                # Example: hardware_directory[controller]["device_group"] =  
                #   "device_group":{ "40":{...}},{"68":{...} } }
                # Example: hardware_directory[controller]["device_group"][device_group] =  
                #   "40":{'address': [3,4,5], 'device':'LED_RGB,...}

                if hardware_directory[controller]["device_group"][device_group]["device"] == event_file["device"]:     # if the device value ("device type") is the same... 
                    device_group_list = hardware_directory[controller]["device_group"][device_group]                   # Create a temporary list with the dictionary
                        # Example: device_group_list = {"address":[1,2,3"], "x_position":0,...}
                    device_group_list["I2C_address"] = hardware_directory[controller]["address"]                       # Add the I2C_address to the dictionary,
                    device_group_list["controller_driver"] = hardware_directory[controller]["controller_driver"]       # add controller driver to the dictionary,
                    hardware_device_list.append(device_group_list)                                                     # and add it to the hardware_device_list
                        # Example: hardware_device_list = [ {"address":[1,2,3],...}, {"address":[4,5,6],...} ]    
    return (hardware_device_list)


def preprocess_patterns(event_file, hardware_device_list):
    '''
    Process after hardware_device_list has been built for the current event file.
    Import all required Patterns files, then determine timestamp based on installed hardware (most extreme positions).
    Add 'extreme' adjusted time stamp to event as timestamp_start for later usage.
    '''
    # Example: hardware_device_list = [ {"address":[1,2,3],...}, {"address":[4,5,6],...} ] 
    global folder_session
    pattern_list = []

    for event in event_file["events"]:        
        '''
        core_pattern_library = ('Patterns.' + event["pattern"])
        session_pattern_library = (folder_session + '.Patterns.' + event["pattern"])
        '''
        pattern_folder = which_pattern_folder(event)
        event_path = event_file["events"][event_file["events"].index(event)]

        ## Folder Check ##
        '''
        Prioritize like-named patterns in the session folder over the core (Patterns) folder.
        '''
        '''
        if os.session_pattern_library.isfile:
            pattern_folder = session_pattern_library 
        else:
            pattern_folder = core_pattern_library  
        '''

        ## Process pattern file once for extremes ##
        if event_path["pattern"] not in pattern_list:
            pattern_list.append(event_path["pattern"])
            position_extreme, delay_extreme = importlib.import_module(pattern_folder).positional_extremes(event_path, hardware_device_list)

        ## Timestamp Leadup Calc ##
        timestamp_calibrated = importlib.import_module(pattern_folder).timestamp_leadup(event_path, hardware_device_list, position_extreme, delay_extreme)
        event_file["events"][event_file["events"].index(event)]["timestamp_start"] = timestamp_calibrated

        ## OLD ##
        '''
        library = ('Patterns.' + event["pattern"])
        event_path = event_file["events"][event_file["events"].index(event)]

        # Process pattern file once for extremes.
        if event_path["pattern"] not in pattern_list:
            pattern_list.append(event_path["pattern"])
            position_extreme, delay_extreme = importlib.import_module(library).positional_extremes(event_path, hardware_device_list)
        timestamp_calibrated = importlib.import_module(library).timestamp_leadup(event_path, hardware_device_list, position_extreme, delay_extreme)
        event_file["events"][event_file["events"].index(event)]["timestamp_start"] = timestamp_calibrated
            #except:
            #    print ("ERROR - preprocess_patterns: Process pattern file once for extremes.")
        '''    
    return (event_file)


def reset_hardware(hardware_directory):
    '''
    Passes the controller dictionary to the associated driver for initializing/resetting the hardware.
    '''
    # Intialize/Reset Controller
    for controller in hardware_directory:
        importlib.import_module(hardware_directory[controller]["controller_driver"]).initialize(hardware_directory[controller])
    return ()


def select_mode():
    global time_movie_start
    
    ### Select Playback Mode ###
    print ("\n\n\n####### MODE SELECTION #######")
    while True:
        print ("\n\nInput Mode: \n 1. Offset Time \n 2. Audio Sync Time\n 3. Audio Sync + Offset\n")
        selection = int(input(""))
        
        # Offset #
        if selection == 1:
            time_playback_offset = int(input("\n\nInput current movie time then press 'Enter'. Afferent Cinema will begin upon hitting 'Enter'.\n"))
            time_movie_start = time.time() - time_playback_offset
            break

        # Audio Recognition #
        elif selection == 2:
            print ("\nAudio Recognition Starting...\n")
            time_movie_start = time.time()
            AudioSync.daemon = True
            AudioSync().start()

            ## Wait for AudioSync to intialize ##
            audiosync_setup_complete.wait()
            break
        
        # Audio Recognition + Offset #
        elif selection == 3:
            print ("\nAudio Recognition Starting...\n")
            AudioSync.daemon = True
            AudioSync().start()

            ## Wait for AudioSync to intialize ##
            audiosync_setup_complete.wait()
            time_playback_offset = int(input("\n\nInput current movie time then press 'Enter'. Afferent Cinema will begin upon hitting 'Enter'.\n"))
            time_movie_start = time.time() - time_playback_offset
            break
        
        else:
            print ("\nInvalid Input\n")
            continue
    
    return()        
    

def select_session():
    global folder_session
 
    ### Load Config File ###
    while True:
        try:
            config = json.load(open('./config.json'))
            current_session_folder = config["session_folder_current"]
            break
        except KeyError:
            config["session_folder_current"] = ""
            json.dump(config, open('./config.json', 'w'), indent=4, ensure_ascii=False)
            #current_session_folder = config["session_folder_current"]
        except FileNotFoundError:
            json.dump({}, open('./config.json', 'w'), indent=4, ensure_ascii=False)
    
    
    ### Select Session Folder ###
    print ("\n####### FOLDER SELECTION #######")
    while True:
        print ("\nCurrent Session Folder: " + str(current_session_folder))
        print ("(K)eep or (S)elect new folder?")
        selection = input("")
        if selection == 'K' or selection == 'k':
            if os.path.isdir(current_session_folder):                
                break
            else:
                print ("\nNot a valid folder. Please (S)elect a new folder.")    
        elif selection == 'S' or selection == 's': 
            contents = os.listdir("./Sessions/")
            while True:
                print ("\nInput new folder from options below:")
                for item in contents:
                    if os.path.isdir("./Sessions/" + str(item)):
                        print (item)
                print ("")
                folder = ("./Sessions/" + input(""))
                if os.path.isdir(folder):
                    current_session_folder = folder
                    config["session_folder_current"] = folder
                    json.dump(config, open('./config.json', 'w'), indent=4, ensure_ascii=False)
                    print ("\nFolder " + str(folder) + " loaded.\n")
                    break
                else:
                    print ("\nINVALID INPUT... Try Again.")              
        else:
            print ("\nInvalid Selection\n")
    
    return()


def time_format(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return (h, m, s)   


def timestamp_movie_playback():
    '''
    Calculates the current movie playback time based on the current CPU time.
    Returns CPU time of current playback timestamp based on CPU time of movie start.
    '''
    global time_movie_start
    timestamp = time.time() - time_movie_start
    return (timestamp)


def values_unchanged_check(values_stored, values): 
    '''
    Determine if the calculated value has changed since last assessed.
    '''
    # Example: values = [230, 45, 0]

    value_count = len(values)
    value_index = 0
    for value in values:
        try:
            if value == values_stored[value_index]:
                continue
            else:
                result = False      # One or more Values is different and needs to be updated.
                break
            result = True           # All matches, Values are the same as previously.
        except:
            #error log
            print ("values_unchanged_check(): 'values_stored' and 'values' not same length")
    return (result)


def which_pattern_folder(event):
    '''
    Determines which folder the called pattern from the event is located.
    Prioritize like-named patterns in the session folder over the core (Patterns) folder.
    '''
    global folder_session
    global file_extension    


    session_pattern_library = (folder_session + 'Patterns/' + event["pattern"] + file_extension)
 
    if os.path.isfile(session_pattern_library):
        pattern_folder = ((folder_session + 'Patterns.' + event["pattern"]).replace('/', '.'))[2:] # Converts to absolute path and removes 
    else:
        pattern_folder = ('Patterns.' + event["pattern"])
    
    return (pattern_folder)      



###################################################################################################################################################
################################################# MAIN PROGRAM ####################################################################################
###################################################################################################################################################

try:
    ### Load File and Calibrate ###
    select_session()
    hardware_directory = load_system()
    
    ### Select Mode and Begin Monitoring ###
    select_mode()
    start_monitoring.set()   

    ### Keep Main Thread Alive ###
    while True:
        time.sleep(1) # Pass would cause Dejavu to fail with IOError Overflow, value is arbitrary
        #print ("Thread Count: " + str(threading.active_count()))
       
except KeyboardInterrupt:
    keyboardescape(hardware_directory)

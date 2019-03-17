def pattern_name():
    return("frontlefttoright")


def device_inclusion(device):
    if device["y_position"] == 0:
        isincluded = True
    else:
        isincluded = False
    return(isincluded)


def positional_extremes(event, hardware_list):
    '''
    Custom programmed for the pattern.
    Determines the extreme position(s) in the playback environment for calculating when an event should trigger in anticipation.
    Can return as a list.
    Delays can also play into determining this anticipation.
    '''    
    positions_extreme = 100
    delay_extreme = 0

    ## Find Most Extreme Position & Delay ##
    for device in hardware_list:
        device_index = hardware_list.index(device)
  
        if hardware_list[device_index]["x_position"] < positions_extreme:                
            positions_extreme = hardware_list[device_index]["x_position"]       # Record most extreme negative X-Position
                
        if 'delay' in hardware_list[device_index]:
            if hardware_list[device_index]["delay"] > delay_extreme:            # Record most extreme Delay
                delay_extreme = hardware_list[device_index]["delay"]

    return(positions_extreme, delay_extreme)
                        


def timestamp_leadup(event, hardware_list, positions_extreme, delay_extreme):
    '''
    Determines the start of an event based on where the devices are located in the playback environment.
    This pattern defined timestamp is then put into the event for later triggering.
    '''
    # positions_extreme may be a list/tuple depending on pattern.

    # Calculate timestamp 
    timestamp_center = event["timestamp_center_start"]           # Seconds
    wavespeed = event["wavespeed"]                               # Chairs/Second ~= Meters/Second
    time_lead = positions_extreme / wavespeed                    # Seconds
    timestamp = timestamp_center + time_lead - delay_extreme
    
    return(timestamp)
    
    
def timestamp_position(device, event):
    if "delay" in device:
        delay = device["delay"]
    else:
        delay = 0
    
    time_offset = ( device["x_position"] / event["wavespeed"] ) + delay
    timestamp_position = event["timestamp_center_start"] + time_offset
    
    return(timestamp_position)

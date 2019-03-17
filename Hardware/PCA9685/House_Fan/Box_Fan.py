### External Module Imports ###
# None


###################################################################################################################################################
################################################### FUNCTIONS #####################################################################################
###################################################################################################################################################

def calibration_scaling(device, event):
    '''
    Converts the given output value derived from a standard ('n' CFM at High, Medium, & Low)
    to the particular device's output scale. Equations based on 8-bit (0-255) values.
    
    High   - n CFM @ x meters - Byte: 255
    Medium - n CFM @ x meters - Byte: 127
    Low    - n CFM @ x meters - Byte: 000
    '''
    
    # Bypass for now.
    '''
    # Variables #
    medium_calibrated_byte = 127
    range_high_low = device["high"] - device["medium"]
    range_med_low = device["medium"] - device["low"]
    
    if event["value"][0] > medium_calibrated_byte:
        value = ( ( (event["value"][0] - device["medium"]) * ( range_high_low  ) ) / medium_calibrated_byte) + device["medium"]
    else:
        value = ( ( (event["value"][0] - device["low"]) * ( range_med_low ) ) / medium_calibrated_byte) + device["low"]    
    '''
    
    # Temporary
    value = event["value"][0]
    return(value)


def values_step(device, event, value_percent, folder_session):
    # Example: device = 
        #   {"address":[15], "device":"PCA9685", "x_position":0, "value":0, I2C_address":68}    
    value = []
    value_current = calibration_scaling(device, event)
    value_delta = value_current - device["value"][0]
    value_delta_step = value_delta * value_percent
    value.append(device["value"][0] + value_delta_step)
    #print ("BOX_FAN Value: " + str(value))
    return(value)

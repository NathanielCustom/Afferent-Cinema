'''
Purpose : Receive raw items that have been calculated that need to be converted so that receiving hardware can understand.
Receives: I2C_address, recipient address(es)/register(s), 3ea percent of final values
Sends to I2C_Master: Hex Address, First Byte, [List of Bytes]
    Example bus.write_i2c_block_data(0x28, 1, [100, 100, 100, 2, 240, 0, 0])
'''

### External Module Imports ###
import Interfaces.I2C.I2C_Master as I2C
import time
import threading

### Globals ###
lock = threading.Lock()
send_delay = 0.001          # Puts a delay after sending command to prevent flooding ATMega


###################################################################################################################################################
################################################### FUNCTIONS #####################################################################################
###################################################################################################################################################

def initialize(controller):
    # Example: controller =
       #   {'address': 40, 'device_group': {'00':{'address':[1,2,3,4],...}, '01':{'address':[5,6,7,8],...},... }    

    ### Declare Variables ###    
    initial_values = [1,1,1]

    ### Initialize Each Device Group ###
    for device_group in controller["device_group"]:
        controller["device_group"][device_group]["I2C_address"] = controller["address"]    # Add I2C Address to Device Group
        main(controller["device_group"][device_group], initial_values)
    return()


def shutdown(controller):
    # Example: controller =
        #   {'address': 40, 'device_group': {'00':{'address':[1,2,3,4],...}, '01':{'address':[5,6,7,8],...},... }
    
    initialize(controller)
    return()


def main(device, values):
    # Example: device = 
    #   {"address":[1,2,3,4,5,6,7], "device":"WS281x", "x_position":0, "I2C_address":68}
    # Example: values = [230, 45, 0]

    '''
    SMBus has a 32-byte limit when sending I2C data with write_i2c_block_data.
    Each WS281x package require 4 bytes of data.
    The first byte (LED address) for the first LED is written in byte_0. The last three bytes (color) to byte_block.
    For every following LED all four bytes will be written to byte_block.
    # 1 LED  -  3 bytes total in byte_block
    # 2 LEDs -  7 bytes          "
    # 3 LEDs - 11 bytes          "
    # ...
    # 8 LEDs - 31 bytes          "
    '''

    ### Declare Variables ###
    global lock
    global send_delay
    
    I2C_address = device["I2C_address"]
    byte_0 = 'null'
    byte_block = []   
    
    data_list = []

    red = values[0]                                    
    green = values[1]                                  
    blue = values[2]                                     


    ### Process Data ###
    
    # Aggregate List of Data
    for LED_address in device["address"]:                                   # Cycle through all LED_addresses...
        data_list.extend([LED_address, red, green, blue])                       # ... and add color values after each address.
        # Example: data_list = [1, 240, 40, 0, 2, 240, 40, 0, 3, 240, 40, 0,...]
    #print ("data_list: " + str(data_list))
    
    # Build byte_block and Send
    lock.acquire()
    for data in data_list:
        if len(byte_block) < 31:                                                # If byte_block is not full, add data.
            if (byte_0 == 'null'):                                                  # Has byte_0 been filled?
                byte_0 = data                                                           # No, fill byte_0 with data value from data_list
            else:
                byte_block.append(data)                                                 # Yes, add data value from data_list to byte_block
        else:                                                                   # Else, byte_block has reach "full" capacity so...
            I2C.I2C_block_data(I2C_address, byte_0, byte_block)              # ... send data and...
            byte_0 = 'null'                                                         # ... clear byte_0 and...
            byte_block = []                                                         # ... clear byte_block.
            time.sleep(send_delay)													# Brief Pause in sending subsequent data.
    else:                                                                   # No more data in data_list...
        if byte_block != 'null':                                                # ... and data is queued...
            I2C.I2C_block_data(I2C_address, byte_0, byte_block)              # ...then, send it
            time.sleep(send_delay)
    lock.release()
    
    return()

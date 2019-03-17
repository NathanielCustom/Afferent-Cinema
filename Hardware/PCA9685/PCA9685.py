'''
Purpose : Receive raw items that have been calculated that need to be converted so that receiving hardware can understand.
Receives: I2C_address, recipient address(es)/register(s), percent of final value(s)
Sends to I2C_Master: Hex Address, First Byte, Second Byte
'''

### External Module Imports ###
import Interfaces.I2C.I2C_Master as I2C

### Register Table ###
'''
Listed below are ON/OFF registers for each output.
The value held is the time during the PWM cycle the output is turned ON/OFF. The scale is 0-4095 (12-bit)
ON is set during intialization to time zero (0). 

Format:
        Output_Name : [ ON_L, ON_H, OFF_L, OFF_H ],...
'''
register_table = \
    {
         '0':[ 6,  7,  8,  9],
         '1':[10, 11, 12, 13],
         '2':[14, 15, 16, 17],
         '3':[18, 19, 20, 21],
         '4':[22, 23, 24, 25],
         '5':[26, 27, 28, 29],
         '6':[30, 31, 32, 33],
         '7':[34, 35, 36, 37],
         '8':[38, 39, 40, 41],
         '9':[42, 43, 44, 45],
        '10':[46, 47, 48, 49],
        '11':[50, 51, 52, 53],
        '12':[54, 55, 56, 57],
        '13':[58, 59, 60, 61],
        '14':[62, 63, 64, 65],
        '15':[66, 67, 68, 69]
    }

def initialize(controller):
    # Example: controller =
       #   {'address': 40, 'device_group': {'00':{'address':[1,2,3,4],...}, '01':{'address':[5,6,7,8],...},... }

    ### Declare Variables ###
    I2C_address = controller['address']

    ### Set all Registers ###
    I2C.I2C_byte_data(I2C_address, 0x00, 0x10)        #MODE1 Sleep (Bit On) - Allows programming changes
    I2C.I2C_byte_data(I2C_address, 0x01, 0x04)        #MODE2 OUTDRV; Totem Pole Structure
    I2C.I2C_byte_data(I2C_address, 0x00, 0x00)        #MODE1 Sleep (Bit Off)

    I2C.I2C_byte_data(I2C_address, 0xFA, 0x00)        # ALL_LED_ON_L
    I2C.I2C_byte_data(I2C_address, 0xFB, 0x00)        # ALL_LED_ON_H
    I2C.I2C_byte_data(I2C_address, 0xFC, 0x00)        # ALL_LED_OFF_L: Bits Set All Outputs to Full Off
    I2C.I2C_byte_data(I2C_address, 0xFD, 0x10)        # ALL_LED_OFF_H: Bits Set All Outputs to Full Off

    return()


def shutdown(controller):
    '''
    Sets register 0xFD/253 (ALL_LED_OFF_H) to 0x10 to shutdown all PWM
    '''
    # Example: controller =
        #   {'address': 40, 'device_group': {'00':{'address':[1,2,3,4],...}, '01':{'address':[5,6,7,8],...},... }

    I2C_address = controller['address']
    I2C.I2C_byte_data(I2C_address, 0xFC, 0x00)
    I2C.I2C_byte_data(I2C_address, 0xFD, 0x10)
    return()


def main(device, values):
    # Example: device = 
    #   {"address":[1,2,3], "device":"LED_RGB", "x_position":0, "I2C_address":68}
    # Example: values = [230, 45, 0]

    ### Declare Variables ###
    I2C_address = device["I2C_address"]
 
    ### Process Data and Send ###
    for address in device["address"]:

        # Coorelate address with Low and High OFF registers
        register_low = (register_table[str(address)][2])        
        register_high = (register_table[str(address)][3])

        # Convert associated value from 0-255 to two, 8-bit values (12-bit total max)
        #try:
        value = values[0]
            
        scale = int((value * 4095) / 255)                                 # Convert 0-255 to 0-4095 scale
        value_msb = scale & 65280                                         # Extract MSB from binary result (& 1111111100000000)
        value_msb = value_msb >> 8                                         # Bit shift from bits 8-15 to 0-7

        scale = int((value * 4095) / 255)                                 # Convert 0-255 to 0-4095 scale    
        value_lsb = scale & 255                                         # Extract LSB from binary result (& 11111111)

        del values[0]

        #except:
        #    pass
            # log missing data

        I2C.I2C_byte_data(I2C_address, register_low, value_lsb)
        I2C.I2C_byte_data(I2C_address, register_high, value_msb)    

    return()

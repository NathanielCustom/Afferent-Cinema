'''
### I2C Specific Pinout ###
SDA1 P1-02
SCL1 P1-03
'''

### External Module Imports ###
import smbus        # In Terminal:
                    # sudo pip3 install smbus2
import threading
import time

### Initialize I2C ###
bus = smbus.SMBus(3)


### Globals ###
lock = threading.Lock()


###################################################################################################################################################
################################################### FUNCTIONS #####################################################################################
###################################################################################################################################################

## Thread Locking for I2C Communications ##

def thread_lock():
    global lock
    lock.acquire()
    return()

def thread_release():
    global lock
    lock.release()
    return()


## Data Transmission Functions ##

def I2C_block_data(address, byte_0, byte_block):
    thread_lock()
    
    # Convert all values in byte_block to integers
    byte_block = [int(byte) for byte in byte_block]
        
    while len(byte_block) > 0:    
        # SMBus has 32 byte limit on blocks.
        if len(byte_block) > 31:                                           # If byte_block is more than 31 bytes...
            byte_block_chunk = byte_block[0:31]                                  # Slice index 0-31.
            del byte_block[0:31]
            
        else:
            byte_block_chunk = byte_block
            byte_block = []
        
        # Send Data #
        try:
            bus.write_i2c_block_data(address, byte_0, byte_block_chunk)              # Write final (or only) 32 bytes of in byte_block
        except:
            print ("I2C Block Send Fail")
            print ("Address: %d, Byte_0: %d, Byte_Block_Chunk: %s" % (address, byte_0, byte_block_chunk))
                    
    thread_release()
    
    return()


def I2C_byte_data(address, byte_0, byte_1):
    '''
    # Data Check
    print ("I2C BYTE DATA")
    print ("I2C: " + str(address))
    print ("Register: " + str(byte_0))
    print ("Data Value: " + str(byte_1))
    print ()
    '''
    
    thread_lock()
    
    # Send Data #
    try:
        bus.write_byte_data(address, byte_0, byte_1)
    except:
        print ("I2C Byte Send Fail")
        print ("Address: %d, Byte_0: %d, Byte_1: %s" % (address, byte_0, byte_1))
    finally:
        thread_release()

    return()

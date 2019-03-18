# Afferent Cinema
af·fer·ent

/ˈaf(ə)rənt/
1. conducting or conducted inward or toward something 

### Bring the 4D cinematic experience into your own home theater using the inexpensive Raspberry Pi.

Afferent Cinema follows a schedule of timed events to trigger in coorelation with on screen action. Triggered events send applicable commands over I2C where the intended receiving device actuates as instructed.


## Getting Started

To Be Completed.


Raspberry Pi 3 with Raspbian

I2C over GPIO Enabled (see Interfaces/I2C.py)

## Working with Events
An event is the occurrence of a special effect. Technically, an event is a single change in output.

![Light Switch to On](Documentation/Readme/fadeup.png?raw=true "Event - Light On")

Events are stored in event lists in JSON format. Each device type gets its own list. The web has more resources on learning about JSON files and their formatting (dictionaries, keys, and values). The events files are located in the Sessions/*name_of_media*/ folder and is denoted by name with a trailing “_events.json”.

Each event has a key (JSON terminology) called ‘timestamp_center_start’. This is the time, from the beginning of the film, that the event will be perceived (seen, felt, heard, smelled, tasted) from the (0, 0) position of the room at the final output. Positioning will be explained in a bit. 

![Timer Above Chair](Documentation/Readme/chair_timer.png?raw=true "Event - Timestamp")

The ‘timestamp_center_start’ value is important because pattern files use this to calculate when each seating position in the room will trigger.

![Timers Above Chair](Documentation/Readme/cascade_timer.png?raw=true "Event - Timestamps")

The ‘time_transition’ key tells Afferent Cinema how much time to use to transition from the devices current output to the new output. Calculations are made so that the transition effect ends on ‘timestamp_center_start’ plus any offsets determined by the ‘pattern’ key.

![Timers Demonstrating Transition](Documentation/Readme/transition.png?raw=true "Event - Transition Event")

The ‘pattern’ key defines a python file that is used to calculate in what manner or order devices will be triggered in the playback environment. Will they all trigger at the same time? Will there be a wave effect that travels from the right side of the room to the left side?

![Arrow Over Chairs](Documentation/Readme/wave_simple.png?raw=true "Event - Wave Effect")

The ‘wavespeed’ key sets the speed in which the ‘pattern’ is executed. The speed is measured in meters per second. One meter per second is approximately one chair (seating position) per second. Not all patterns will utilize the ‘wavespeed’ key. This will be explained in more detail in later sections.



## Working with Drivers
### Supported Controllers (-> Specific Device)
PCA9685

ATMega328 -> WS2812B


## Future Changes/Additions
* Documentation on creating events files and drivers
* Incorporation of Dejavu for automatic syncronization of RPi to playback media.

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

# System Explanation
## Introduction
The heart of the Afferent Cinema solution is the mini-computer, Raspberry Pi (RPi). Its low price tag (~$35-$40 USD) and feature rich design makes it a suitable choice for running Afferent Cinema.

The RPi provides a number of GPIO (general-purpose input/output) pins that enable the user to interact in a variety of ways with connected devices. Afferent Cinema’s included I2C drivers is the backbone of communication between the RPi and other I2C slaves. Future revisions may include additional drivers to support other communication protocols like SPI and DMX512.

The RPi also serves as the main microprocessor responsible for monitoring and executing events. Before diving into configuring Afferent Cinema there are a number of concepts that should be understood:
- Events
- Positional Coordinates
- Hardware Profile


### Events
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

### Positional Coordinates

The degree of freedom to which devices can be installed in a playback environment is almost limitless. To translate from an infinite number of positions in our playback environment to a finite scale that a computer can understand we imagine a Battleship-style, two-dimensional grid overlaying the space with our screen device (TV, projected image, laptop) in cell/square (0, 0).

![Room with Grid Overlay](Documentation/Readme/gridroom.png?raw=true "Coordinates - Room Grid")

Each cell is approximately 1m x 1m or about the size of a single seating position.

![1-Meter Measurements on Grid](Documentation/Readme/gridsize.png?raw=true "Coordinates - Grid Size")

The cells are numbered on both the ‘X’ and ‘Y’ axis as pictured.

![Grid with X/Y Labeled](Documentation/Readme/gridroom_screen.png?raw=true "Coordinates - Grid X/Y")

In the following example setup the TV is at (0, 0), the single-recliner is at (0, -3), the lamp is at (-2, -4), and the subwoofer is at (2, 1).

![Example Devices in Grid](Documentation/Readme/gridroom_numbered.png?raw=true "Coordinates - Example Devices")


## Working with Drivers
### Supported Controllers (-> Specific Device)
PCA9685

ATMega328 -> WS2812B


## Future Changes/Additions
* Documentation on creating events files and drivers
* Incorporation of Dejavu for automatic syncronization of RPi to playback media.

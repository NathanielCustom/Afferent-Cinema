ReadMe in Progress...

# Afferent Cinema
af·fer·ent

/ˈaf(ə)rənt/
1. conducting or conducted inward or toward something 

### Bring the 4D cinematic experience into your own home theater using the inexpensive Raspberry Pi.

Afferent Cinema follows a schedule of timed events to trigger in coorelation with on screen action. Triggered events send applicable commands over I2C where the intended receiving device actuates as instructed.


# Getting Started

The lofty vision of Afferent Cinema is to design a solution where an end user, with basic technical knowledge, can connect all hardware and enjoy a 4D cinematic experience with minimal, manual configuration.

- Automatic synchronization to media (done)
- Modular hardware connectivity
- Device calibration standards
- Automatic and manual retrieval of compatible drivers and events

We are a long way from implementing all those features.


### Standard Afferent-Cinema Install

1. Raspberry Pi 3 with Raspbian
2. Enable I2C over GPIOs --- as outlined in /boot/overlays/README section i2c-gpio. Avoid using the hardware I2C pins (3 & 5) as the Broadcomm BCM2835 chipset has an [inherent bug with clock stretching](http://www.advamation.com/knowhow/raspberrypi/rpi-i2c-bug.html).
>- Terminal: sudo nano /boot/config.txt
>- Add: dtoverlay=i2c-gpio,i2c_gpio_sda=5,i2c_gpio_scl=6
>- This will add a new bus /dev/i2c-3 to Broadcom pins GPIO5 & GPIO6 (RPi / breakout-board pins 29 & 31 respectively)
3. Install 2.2k pullup resistor on the I2C SDA and SCL lines.
>- One resistor from 5V+ to GPIO5 and another from 5V+ to GPIO6
4. Download the repository.

### Audio Recognition Afferent-Cinema Install
Documentation Coming "Valve Time"

See https://github.com/worldveil/dejavu for more details on Dejavu, the implemented solution for Audio Recognition.

# System Explanation
## Introduction
The heart of the Afferent Cinema solution is the mini-computer, Raspberry Pi (RPi). Its low price tag (~$35-$40 USD) and feature rich design makes it a suitable choice for running Afferent Cinema.

The RPi provides a number of GPIO (general-purpose input/output) pins that can be used to interact with connected devices (a.k.a. sensory feedback devices or sensory devices). Afferent Cinema’s included I2C drivers is the backbone of communication between the RPi and I2C-slaves, sensory devices. Future revisions may include additional drivers to support other communication protocols like SPI and DMX512.

The RPi also serves as the main microprocessor responsible for monitoring and executing events. Before diving into configuring Afferent Cinema there are a number of concepts that should be understood:
- Positional Coordinates
- Assigning Coordinates
- Events
- Hardware Profile
- The Process Flow

### Positional Coordinates

The degree of freedom to which Sensory Devices can be installed in a playback environment is almost limitless. To translate from an infinite number of positions in our playback environment to a finite scale that a computer can understand we imagine a Battleship-style, two-dimensional grid overlaying the space with our media image (TV, projected image, laptop) in cell/square (0, 0).

![Room with Grid Overlay](Documentation/Readme/gridroom.png?raw=true "Coordinates - Room Grid")

In Afferent Cinema we set one cell to approximately 1m x 1m or about the size of a single seating position.

![1-Meter Measurements on Grid](Documentation/Readme/gridsize.png?raw=true "Coordinates - Grid Size")

The cells are numbered on both the ‘X’ and ‘Y’ axis as pictured.

![Grid with X/Y Labeled](Documentation/Readme/gridroom_screen.png?raw=true "Coordinates - Grid X/Y")

In the following example setup the TV is at (0, 0), the single-recliner is at (0, -3), the lamp is at (-2, -4), and the subwoofer is at (2, 1).

![Example Devices in Grid](Documentation/Readme/gridroom_numbered.png?raw=true "Coordinates - Example Devices")

### Assigning Coordinates

Assigning Positional Coordinates to a Sensory Device should be carefully considered. Coordinates are target-oriented and are not based on where a device is physically located within the two dimensional grid i.e. the location the intended sensation is experienced may not be the same where the device is located. In many instances you may find the device target and physical location will be the same. In the event that a device targets multiple locations, the rule of the thumb is to specify the most central and forward location. The following examples should help clarify.

A recessed light is physically located at (-2, -1). The target is the immediate vicinity of the fixture; (-2, -1). Regardless of where the viewer is seated in the room, the effect of the recessed light is perceived from the same target location.

![Example Recessed Light](Documentation/Readme/recessed_light.png?raw=true "Hardware Profile - Recessed Light Example")

A spot light is physically located at (+2, -4). A viewer is not suppose to be viewing the spot light itself, but the effect it creates shining on a surface. In this example, the effect is targeted at (0, -2). When logging this device into the Hardware Directory its coordinates are (0, -2). This is another example where a viewer can be seated anywhere within the room and the perception of the effect doesn’t change.

![Example Spot Light](Documentation/Readme/spotlight.png?raw=true "Hardware Profile - Spot Light Example")

A fan is located at (-1, +1). The viewer seated in (0, -3) is the target recipient of the fan, so (0, -3) is the device’s coordinates.

![Example Single Fan](Documentation/Readme/single_fan.png?raw=true "Hardware Profile - Single Fan Example")

A fan is located at (0, +1). The viewers in seats (-2, -3), (0, -3), and (+2, -3) are the targeted recipients of the air movement. Since we must define a single location, (0) is the most centrally located x-coordinate and (-3) is the most forward located y-coordinate resulting in (0, -3).

![Example Group Fan](Documentation/Readme/group_fan.png?raw=true "Hardware Profile - Group Fan Example")

LED strips are an interesting scenario due to the way that they can be connected end to end to create one long strip. Following the rule of “most central and forward”, we can find our recommended coordinates.

A. (-3, 0)
B. (0, +1)
C. (+3, 0)

![Example LED Strips](Documentation/Readme/ledroom2.png?raw=true "Hardware Profile - LED Strips Example")

Be aware, that Events that call for Patterns that create a wave across the room or emanating from the image (as seen in example below) will only appear as a single pulse since the strips are all connected to one output. To get a sweeping wave effect the strips will have to be separated into smaller segments and get their own outputs or implement addressable LED modules like the WS2812.

(Strip on Left, Individual Modules on Right)
(Wave emanating from screen)

![Example LED Room Pulse](Documentation/Readme/ledroompulse.png?raw=true "Hardware Profile - LED Pulse Example")

### Events
An event defines a single output value and the associated Sensory Device(s). An event typically will cause a Sensory Device to change state; off to on, 40% to 70%, etc.

![Light Switch to On](Documentation/Readme/fadeup.png?raw=true "Event - Light On")

Events are stored in Event Lists in JSON format and are denoted by name with a trailing “_events.json”. Each type of Sensory Device gets its own list; ex. house fans, recessed lighting, etc. Because no two films are alike, there is a unique Event List per device for each film located in the Sessions/*name_of_media*/ folder. 
The web has more resources on learning about JSON files and their formatting (dictionaries, keys, and values).

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
* Provide Documentation on Installing/Configuring Audio Recognition

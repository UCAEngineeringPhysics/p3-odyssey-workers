[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7KaPTW5f)
# The Odyssey

## Coffee Transportation Solution

We chose to build a trailer style holder for the coffee cup, it sits like a trailer with a similar hitch that trailers use so that it can turn with the robot, not by its wheels but by the connection at the fron of the trailer.




### Hardware Installation Guide

1. Mobile Base
    The bottom plate of the robot is the base, which are driven by DC motors and a caster wheel, which we have positioned at the back. 
2. Brain, the Pi 5
    The Raspberry Pi 5 is stacked in the middle of the robot underneath the motor driver board and the PCB where the Pico 2 W is. 
3. RP Lidar
    The robot uses Lidar to 'see'. It sits on the very top of the robot, and it connected to one of the USB ports on the Pi 5

## Software Usage Instructions

Workspace for Pi 5 set up
```
mkdir -p ~/homer_ws/src
cd ~/homer_ws/src

source /opt/ros/jazzy/setup.bash
cd ~/homer_ws
```

### Usage
1. Hardware
    Rp Lidar and Pico node (subpub) 
    ```
    ros2 launch coffee_car hardware.launch.py
    ```
2. Mapping
    starts slam-toolbox, drives robot around the room, generates map
    ```
    ros2 launch coffee_car mapping.launch.py
    ```
3. Navigation
    After the map is made, this is used to deliver the coffee
    ```
    ros2 launch coffee_car navigation.launch.py
    ``` 

We can also manually steer the robot and drive it using
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```


The coffee car has to run a few launch systems prior to running itself
    1. The hardware, so RP Lidar and the pico can connect
    2. The mapping, this is where we can run the robot manually to build a map, or it can move by itself 
    3. If we run manually, we launch the teleop_twist_keyboard
    4. To run fully by itself we launch the coffee_car navigation

### Mechanical Design

Base Design:
![Homer_Portrait](drawings/mechanical/Homer_base_design.png)
Roof Design:
![Homer_Portrait](drawings/mechanical/Homer_Roof.png)
Motor Holder Design:
![Homer_Portrait](drawings/mechanical/Motor_Holder.png)
Caster Wheel Design:
![Homer_Portrait](drawings/mechanical/Caster_Wheel.png)
Pi 5 Case (Space Ship):
![Homer_Portrait](drawings/mechanical/Pi5SPACESHIP.png)
Raspberry Pi 5:
![Raspberry Pi 5](drawings/electrical/RaspberryPi5.png)
Motors (with Encoders):
![Motors](drawings/mechanical/Motors.png)
Wheels:
![Wheels](drawings/mechanical/65mm_wheel.png)

## Electrical Designs
![Homer_Portrait](drawings/electrical/Homer_Electrical.png)
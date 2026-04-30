[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7KaPTW5f)
# The Odyssey

## Coffee Transportation Solution

We chose to build a trailer style holder for the coffee cup, it sits like a trailer with a similar hitch that trailers use so that it can turn with the robot, not by its wheels but by the connection at the fron of the trailer.


### Hardware Installation Guide

## Software Usage Instructions

Ros2 Jazzy
```
src /ros/jazzy/setup.bash
cd ~/homer_ws
colcon build coffee_car
source install/setup.bash
```
Then launch:
```

```
The coffee car has to run a few launch systems prior to running itself
    1. The hardware, so RP Lidar and the pico can connect
    2. The mapping, this is where we can run the robot manually to build a map, or it can move by itself 
    3. If we run manually, we launch the teleop_twist_keyboard
    4. To run fully by itself we launch the coffee_car navigation

### Mechanical Design

Base Design:
![Homer_Portrait](images/Homer_base_design.png)
Roof Design:
![Homer_Portrait](images/Homer_Roof.png)
Motor Holder Design:
![Homer_Portrait](images/Motor_Holder.png)
Caster Wheel Design:
![Homer_Portrait](images/Caster_Wheel.png)
Pi 5 Case (Space Ship):
![Homer_Portrait](images/Pi5SPACESHIP.png)
Raspberry Pi 5:
![Raspberry Pi 5](images/RaspberryPi5.png)
Motors (with Encoders):
![Motors](images/Motors.png)
Wheels:
![Wheels](images/65mm_wheel.png)

## Electrical Designs
![Homer_Portrait](drawings/electrical/Homer_Electrical.png)

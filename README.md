[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7KaPTW5f)
# The Odyssey

## Coffee Transportation Solution

We chose to build a trailer style holder for the coffee cup, it sits like a trailer with a similar hitch that trailers use so that it can turn with the robot, not by its wheels but by the connection at the fron of the trailer.

For the drawings, they're all named drawing, sorry bro.


Trailer Mount-Mount?
![Wheels](images/Drawing1.png)
Wheel-Rim
![Wheels](images/Drawin2.png)
Wheel-Tire
![Wheels](images/Drawing3.png)
Coffe Cup trailer/chariot 
![Wheels](images/Drawing4.png)
On trailer trailer mount
![Wheels](images/Drawing5.png)
On Robot trailer mount
![Wheels](images/Drawing6.png)


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
git pull https://github.com/UCAEngineeringPhysics/p3-odyssey-workers
cd ~/homer_ws
sudo apt install python3-rosdep
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon buid
source install/setup.bash
sudo apt install -y chrony
echo 'export ROS_DOMAIN_ID=90'
source ~/.bashrc
```
Workspace for server set up
```
mkdir -p ~/homer_ws/src
cd ~/homer_ws/src
git pull https://github.com/UCAEngineeringPhysics/p3-odyssey-workers
cd ~/homer_ws
sudo apt install python3-rosdep
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon buid
source install/setup.bash
sudo apt install chrony
echo 'export ROS_DOMAIN_ID=90'
source ~/.bashrc
```
### Usage
1. Hardware
    Rp Lidar and Pico communication packages (launch on pi)
    ```
    ros2 launch coffee_car homer_launch.py
    ```
2. Mapping
    starts slam-toolbox, user drives robot around the room, generates map
    ```
    ros2 launch coffee_car create_map.launch.py
    ```
    Once map is made type in the path in which you want to save the file.
    You then need to add that same path to the localization_params.yaml map flie name
4. Navigation
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
![Homer_Portrait](images/Homer_Electrical.png)

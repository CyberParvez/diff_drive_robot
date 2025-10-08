<<<<<<< HEAD
# diff_drive_robot
A ROS 2 simulation package for differential drive robots using ROS 2 Jazzy and Gazebo Harmonic.
=======
# Diff Drive Robot Simulation

A ROS 2 simulation package for differential drive robots using ROS 2 Jazzy and Gazebo Harmonic.

## Features

- Differential drive robot with lidar sensor
- Gazebo Harmonic simulation
- Tele-operation control (keyboard and joystick)
- RViz2 visualization
- Modular URDF with xacro

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic

## Installation

### Install ROS 2 Packages

```bash
sudo apt install -y \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-xacro \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-teleop-twist-joy
    ros-jazzy-cartographer \
```

## Install

To use this package please download all of the necessary dependencies first and then follow these steps

```bash
mkdir -p ros2_ws/src
cd ros2_ws/src
git clone https://github.com/adoodevv/diff_drive_robot.git
cd ..
colcon build --packages-select diff_drive_robot --symlink-install
```

### Launch Gazebo simulation together with Rviz

After sourcing ROS and this package we can launch the 2-wheeled differential drive robot simulation with the following command:

```bash
source install/setup.bash
ros2 launch diff_drive_robot robot.launch.py 
```

### Controlling the robot

Currently, only keyboard control works. Run this in another terminal:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard 
```

## TODO

Package is still being worked on, though the core funtionality is pretty much done, I will be adding some more sensors and functionalities soon.
>>>>>>> 9ee3866 (Create)

#!/bin/bash

source /opt/ros/indigo/setup.bash
source /home/pi/Projects/catkin_ws/devel/setup.sh

export ROS_MASTER_URI=http://192.168.1.107:11311
export ROS_IP=192.168.1.107


#Lanzar el script
#
echo "iniciando"

roscd domopin_central
roslaunch domopin_central domopin.launch







 


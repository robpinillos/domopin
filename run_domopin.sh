#!/bin/bash

source /opt/ros/kinetic/setup.bash
source /home/robpin/catkin_ws/devel/setup.sh

#source /home/pi/Projects/catkin_ws/devel/setup.sh

export ROS_MASTER_URI=http://192.168.1.34:11311
export ROS_IP=192.168.1.34


#Lanzar el script
#
echo "Comprobando conexion internet"

roscd domopin_central
while sleep 1
do
	ping_test=`ping -c 2 8.8.8.8 > /dev/null`
	if [ $? == 0 ]
	then sleep 1
		echo "iniciando"
		roslaunch domopin_central multimaster.launch
		break
	fi
	#if [ $count == 5 ]
	#then echo "no se encuentra el master" 
	#	break
	#fi
	#((count++))
	echo "..."
done









 


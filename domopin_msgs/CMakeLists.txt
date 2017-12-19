cmake_minimum_required(VERSION 2.8.3)
project(domopin_msgs)
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs std_srvs  message_generation)



## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
#catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################
add_message_files(
  DIRECTORY msg
)

add_service_files(
  DIRECTORY srv

)

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs 
 )


# Use this to define what the package will export (e.g. libs, headers).
# Since the default here is to produce only a binary, we don't worry about
# exporting anything. 
catkin_package(

DEPENDS std_msgs message_runtime
)

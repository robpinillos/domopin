cmake_minimum_required(VERSION 2.8.3)
project(domopin_central)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs std_srvs domopin_msgs)


## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)


## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

catkin_package(

DEPENDS std_msgs 
)

#catkin_install_python(PROGRAMS scripts/domopin_main.py
#         DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)

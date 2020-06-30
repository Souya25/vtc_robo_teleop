cmake_minimum_required(VERSION 2.8.3)
project(vtc_teleop)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
)

## Generate added messages and services with any dependencies listed here
 #generate_messages(
  # DEPENDENCIES
  #std_msgs
# )

catkin_package(
  #INCLUDE_DIRS include
  LIBRARIES vtc_teleop
  CATKIN_DEPENDS roscpp rospy std_msgs
  DEPENDS system_lib
)

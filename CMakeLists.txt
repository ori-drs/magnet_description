cmake_minimum_required(VERSION 3.0.2)
project(magnet_description)

find_package(catkin REQUIRED COMPONENTS hesai_description xacro)

catkin_package(CATKIN_DEPENDS xacro hesai_description)

set(xacro_files
  ${CMAKE_CURRENT_SOURCE_DIR}/urdf/standalone.urdf.xacro
)

xacro_add_files(${xacro_files} INSTALL DESTINATION urdf)

install(DIRECTORY config launch urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
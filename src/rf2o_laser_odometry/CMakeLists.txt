cmake_minimum_required(VERSION 3.5)
project(rf2o_laser_odometry)


if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2  REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)

## System dependencies are found with CMake's conventions
find_package(Boost REQUIRED)
message(STATUS "Boost_FOUND=${Boost_FOUND}")
message(STATUS "Boost include dirs: ${Boost_INCLUDE_DIRS}")

find_package(eigen3_cmake_module REQUIRED)
message(STATUS "eigen3_cmake_module_FOUND=${eigen3_cmake_module_FOUND}")

find_package(Eigen3 3.3 REQUIRED NO_MODULE)
message(STATUS "Eigen3 FOUND=${Eigen3_FOUND}")
if (TARGET Eigen3::Eigen)
  message(STATUS "Eigen3 target available")
endif()


set(EXECUTABLE_NAME "rf2o_laser_odometry_node")

## Specify additional locations of header files
## Your package locations should be listed before other locations
add_executable(${EXECUTABLE_NAME} 
    src/CLaserOdometry2DNode.cpp
    src/CLaserOdometry2D.cpp)

include_directories(
  include include/
)

include_directories(  
  ${Boost_INCLUDE_DIRS}
  ##${EIGEN3_INCLUDE_DIRS}
)

set(DEPENDENCIES
  "rclcpp"           
  "std_msgs"         
  "geometry_msgs" 
  "tf2_geometry_msgs"
  "tf2"
  "tf2_ros"
  "sensor_msgs"
  "nav_msgs"
  "eigen3_cmake_module"
)

##target_include_directories(${PROJECT_NAME} PUBLIC ${Eigen3_INCLUDE_DIRS})
ament_target_dependencies(${EXECUTABLE_NAME} ${DEPENDENCIES})

## Declare a cpp library
add_library(${PROJECT_NAME} src/CLaserOdometry2D.cpp)

## Declare a cpp executable
ament_target_dependencies(${PROJECT_NAME} ${DEPENDENCIES})

install(TARGETS ${EXECUTABLE_NAME}
  DESTINATION lib/${PROJECT_NAME})

install(
  DIRECTORY launch  
  DESTINATION share/${PROJECT_NAME})

ament_package()


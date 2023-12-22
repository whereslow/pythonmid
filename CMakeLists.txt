cmake_minimum_required(VERSION 3.20)

project(pymid)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_executable(pymid src/main.cpp src/method.cpp)
target_include_directories(pymid PUBLIC src)

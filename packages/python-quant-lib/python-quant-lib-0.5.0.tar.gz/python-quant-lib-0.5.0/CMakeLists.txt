cmake_minimum_required(VERSION 3.4...3.18)
project(python_quant_lib)

# Set the C++ standard to C++17 (or any other desired version)
set(CMAKE_CXX_STANDARD 17)

add_subdirectory(external/pybind11)

pybind11_add_module(python_quant_lib src/bindings.cpp)

add_subdirectory("src/core")
add_subdirectory("src/date")
add_subdirectory("src/rates")

# Set the path to the Eigen library headers
include_directories(${CMAKE_SOURCE_DIR}/external/Eigen)

# Add the Eigen library to the project
add_library(Eigen INTERFACE)
target_include_directories(Eigen INTERFACE ${CMAKE_SOURCE_DIR}/external/Eigen)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(python_quant_lib
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})


                           

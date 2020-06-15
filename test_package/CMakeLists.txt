cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
find_package(Ogre3D MODULE REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Ogre3D::Ogre3D)

cmake_minimum_required(VERSION 3.15)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

find_package(Ogre3D REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} Ogre3D::Components)
if(TEST_IMGUI)
  target_compile_definitions(${PROJECT_NAME} PRIVATE TEST_IMGUI)
endif()

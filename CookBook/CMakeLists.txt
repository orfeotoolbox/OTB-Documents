CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

# This is the Orfeo ToolBox cookbook : a guide for non-developpers
PROJECT(CookBook)

# Include latex cmake mode
INCLUDE(CMake/UseLATEX.cmake)

# need an OTB build dir
FIND_PACKAGE(OTB REQUIRED)
FIND_PACKAGE(PythonInterp REQUIRED)

ADD_SUBDIRECTORY(Latex)



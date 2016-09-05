CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

# This is the Orfeo ToolBox cookbook : a guide for non-developpers
PROJECT(CookBook)

message(WARNING "The official CookBook has been merged into the OTB repository. This version is outdated and will likely be removed")

# Include latex cmake mode
INCLUDE(CMake/UseLATEX.cmake)

# need an OTB build dir
FIND_PACKAGE(OTB REQUIRED)
FIND_PACKAGE(PythonInterp REQUIRED)

set(OTB_VERSION_STRING_FULL "${OTB_VERSION_MAJOR}.${OTB_VERSION_MINOR}.${OTB_VERSION_PATCH}")
configure_file(
  ${CMAKE_SOURCE_DIR}/Latex/OTBTexMacros.tex.in
  ${CMAKE_SOURCE_DIR}/Latex/OTBTexMacros.tex
  @ONLY)

ADD_SUBDIRECTORY(Latex)

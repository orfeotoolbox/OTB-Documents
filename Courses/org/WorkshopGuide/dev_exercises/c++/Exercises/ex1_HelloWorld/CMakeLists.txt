# This project is designed to be built outside the OTB source tree.
PROJECT(Exercise1)

cmake_minimum_required(VERSION 2.8)

# Find OTB.
FIND_PACKAGE(OTB)  
IF(OTB_FOUND)  
  INCLUDE(${OTB_USE_FILE})  
ELSE(OTB_FOUND)  
  MESSAGE(FATAL_ERROR  
      "Cannot build OTB project without OTB.  Please set OTB_DIR.")  
ENDIF(OTB_FOUND)  

#required for windows. might be needed on other CMakeLists.txt also
include_directories(${OTB_INCLUDE_DIRS})

ADD_EXECUTABLE(HelloWorld HelloWorld.cxx )
TARGET_LINK_LIBRARIES(HelloWorld ${OTB_LIBRARIES}) 

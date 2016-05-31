PROJECT(Tutorials)  
 
cmake_minimum_required(VERSION 2.6)  
 
FIND_PACKAGE(OTB)  
IF(OTB_FOUND)  
  INCLUDE(${OTB_USE_FILE})  
ELSE(OTB_FOUND)  
  MESSAGE(FATAL_ERROR  
      "Cannot build OTB project without OTB.  Please set OTB_DIR.")  
ENDIF(OTB_FOUND)  
 
ADD_EXECUTABLE(LS8_Extract LS8_Extract.cxx)  
set_property(TARGET LS8_Extract PROPERTY CXX_STANDARD 11)
set_property(TARGET LS8_Extract PROPERTY CXX_STANDARD_REQUIRED ON)
TARGET_LINK_LIBRARIES(LS8_Extract ${OTB_LIBRARIES}) 

# This project is designed to be built outside the OTB source tree.
PROJECT(Exercise2)

# Find OTB.
FIND_PACKAGE(OTB)  
IF(OTB_FOUND)  
  INCLUDE(${OTB_USE_FILE})  
ELSE(OTB_FOUND)  
  MESSAGE(FATAL_ERROR  
      "Cannot build OTB project without OTB.  Please set OTB_DIR.")  
ENDIF(OTB_FOUND)  
 
ADD_EXECUTABLE(Pipeline Pipeline.cxx )  
TARGET_LINK_LIBRARIES(Pipeline ${OTB_LIBRARIES}) 

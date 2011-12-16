CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

# This is the Orfeo ToolBox cookbook : a guide for non-developpers
PROJECT(CookBook)

# Include latex cmake mode
INCLUDE(CMake/UseLATEX.cmake)

# need an OTB build dir
FIND_PACKAGE(OTB REQUIRED)
FIND_PACKAGE(PythonInterp REQUIRED)



configure_file(CMake/RunApplicationsDocGenerator.sh.cmake.in
               ${CMAKE_CURRENT_BINARY_DIR}/RunApplicationsDocGenerator.sh
               @ONLY
               )

#add_custom_command(OUTPUT Applications.tex
#                   COMMAND bash ${CMAKE_CURRENT_BINARY_DIR}/RunApplicationsDocGenerator.sh )

add_custom_target(ApplicationsDoc
                  ALL
                  COMMAND bash ${CMAKE_CURRENT_BINARY_DIR}/RunApplicationsDocGenerator.sh
                  COMMENT "Running otbGenerateWrappersLatexDoc.py"
                  )
                  

ADD_SUBDIRECTORY(Latex)



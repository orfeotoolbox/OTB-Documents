# Auto-generate reference documentation in build directory
CONFIGURE_FILE(${CookBook_SOURCE_DIR}/CMake/RunApplicationsDocGenerator.sh.cmake.in
               ${CMAKE_CURRENT_BINARY_DIR}/RunApplicationsDocGenerator.sh
               @ONLY
               )

ADD_CUSTOM_TARGET(AppRefDocTex
                  ALL
                  COMMAND bash ${CMAKE_CURRENT_BINARY_DIR}/RunApplicationsDocGenerator.sh
                  COMMENT "Auto-generating Application Reference Documentation"
                  )

# Find part files
FILE(GLOB  RELATED_SRCS RELATIVE "${CookBook_SOURCE_DIR}/Latex" "*")

# Add the main latex doc
ADD_LATEX_DOCUMENT(CookBook.tex INPUTS ${RELATED_SRCS} MANGLE_TARGET_NAMES DEFAULT_PDF IMAGE_DIRS ../Art ../Art/MonteverdiImages USE_INDEX)

ADD_DEPENDENCIES(CookBook_pdf AppRefDocTex)

FIND_PROGRAM(TEX4HT_COMPILER
  NAMES htlatex
  PATHS ${MIKTEX_BINARY_PATH}
        /usr/bin
)

IF(NOT TEX4HT_COMPILER)
  MESSAGE("htlatex executable was not found")
ENDIF(NOT TEX4HT_COMPILER)


# Option for html generation
SET(TEX4HT_OPTIONS html,4,subsubsections+)
SET (HTML_OUTPUT "Html")

IF(LATEX_COMPILER)
  SET(ITK_TEXINPUTS ${CookBook_SOURCE_DIR}/../Latex:${CookBook_SOURCE_DIR}/Latex:${CookBook_SOURCE_DIR}/Art:${CookBook_BINARY_DIR}/Art:${CookBook_BINARY_DIR}/Latex)
  IF (TEX4HT_COMPILER)
    CONFIGURE_FILE(${CookBook_SOURCE_DIR}/Tex4htWrapper.sh.in
      ${CookBook_BINARY_DIR}/Tex4htWrapper.sh)
    SET (TEX4HT_WRAPPER1 ${CookBook_BINARY_DIR}/Tex4htWrapper.sh)
    SET (TEX4HT_WRAPPER2 "")

    ADD_CUSTOM_TARGET(AppDocHTML
                      ALL
                      COMMAND sh ${CookBook_BINARY_DIR}/Tex4htWrapper.sh CookBook
                      WORKING_DIRECTORY ${CookBook_BINARY_DIR}
                      COMMENT "Building HTML documentation"
                      )
    ADD_DEPENDENCIES(AppDocHTML CookBook_pdf)
  ENDIF (TEX4HT_COMPILER)
ENDIF(LATEX_COMPILER)


# Find part files
FILE(GLOB  RELATED_SRCS RELATIVE "${CookBook_SOURCE_DIR}/Latex" "*")

MESSAGE("${RELATED_SRCS}")

# Add the main latex doc
ADD_LATEX_DOCUMENT(CookBook.tex INPUTS ${RELATED_SRCS} MANGLE_TARGET_NAMES DEFAULT_PDF IMAGE_DIRS ../Art ../Art/MonteverdiImages USE_INDEX)


FIND_PROGRAM(TEX4HT_COMPILER
  NAMES htlatex
  PATHS ${MIKTEX_BINARY_PATH}
        /usr/bin
)
MARK_AS_ADVANCED(TEX4HT_COMPILER)

IF(NOT TEX4HT_COMPILER)
  MESSAGE("htlatex executable was not found. Please pass to advanced mode and provide its full path")
ENDIF(NOT TEX4HT_COMPILER)


# Option for html generation
SET(TEX4HT_OPTIONS html,4,subsubsections+)
SET (HTML_OUTPUT "Html")

IF(LATEX_COMPILER)
  MESSAGE("Have latex compiler")
  SET(ITK_TEXINPUTS ${CookBook_SOURCE_DIR}/../Latex:${CookBook_SOURCE_DIR}/Latex:${CookBook_SOURCE_DIR}/Art:${CookBook_BINARY_DIR}/Art:${CookBook_BINARY_DIR}/Latex)
  IF (TEX4HT_COMPILER)
    CONFIGURE_FILE(${CookBook_SOURCE_DIR}/Tex4htWrapper.sh.in
      ${CookBook_BINARY_DIR}/Tex4htWrapper.sh)
    SET (TEX4HT_WRAPPER1 ${CookBook_BINARY_DIR}/Tex4htWrapper.sh)
    SET (TEX4HT_WRAPPER2 "")
  ENDIF (TEX4HT_COMPILER)
ENDIF(LATEX_COMPILER)

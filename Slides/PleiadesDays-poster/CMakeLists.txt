project(pleiades_days)

cmake_minimum_required(VERSION 2.6)
include(UseLATEX.cmake)

add_latex_document(otb-poster.tex MANGLE_TARGET_NAMES DEFAULT_PDF IMAGE_DIRS Pictures)

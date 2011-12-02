#!/bin/bash

# set the handout option for the beamer class and recompile the .tex

pdfjam 01-Intro.pdf 02-Geometrie.pdf 03-Radiometrie.pdf 04-Primitives.pdf 05-Classification.pdf 06-Changements.pdf --landscape --frame true --nup 2x2 --outfile Tutorial-handout.pdf

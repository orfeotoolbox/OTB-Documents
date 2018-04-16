#!/bin/bash

# Export install guide

for f in *.tex
do
 filename=$(basename "$f")
 extension="${filename##*.}"
 filename="${filename%.*}"
 # export to pdf
 pdflatex -interaction nonstopmode $filename.tex
 pdflatex -interaction nonstopmode $filename.tex
done

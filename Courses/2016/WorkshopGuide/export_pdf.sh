#!/bin/bash

for f in workshopSlides-*.org
do
 filename=$(basename "$f")
 extension="${filename##*.}"
 filename="${filename%.*}"
 echo "Processing $f"
 emacs $filename.org --batch -f org-beamer-export-to-latex --kill
 #add pdf version
 sed -i '1 i \\\pdfminorversion=4' $filename.tex
 #export to pdf
 pdflatex -interaction nonstopmode $filename.tex
 pdflatex -interaction nonstopmode $filename.tex
done

for f in workshopGuide-*.org
do
 filename=$(basename "$f")
 extension="${filename##*.}"
 filename="${filename%.*}"
 echo "Processing $f"
 emacs $filename.org --batch -f org-latex-export-to-latex --kill
 #add pdf version
 sed -i '1 i \\\pdfminorversion=4' $filename.tex
 #export to pdf
 pdflatex -interaction nonstopmode $filename.tex
 pdflatex -interaction nonstopmode $filename.tex
done

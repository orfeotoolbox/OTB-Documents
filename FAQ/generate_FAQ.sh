#/bin/sh

latex2rtf OTB-FAQ.tex
latex2html -split 0 -local_icons -info "" OTB-FAQ.tex
pdflatex OTB-FAQ.tex
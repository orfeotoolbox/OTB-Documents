#/bin/sh

TEXINPUTS=$TEXINPUTS:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide/../Latex:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide/Latex:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide/Art:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide/Examples:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide/Art:/usr/local/stok/OTB/trunk/OTB-Documents/SoftwareGuide/Latex
export TEXINPUTS

latex2rtf OTB-FAQ.tex
latex2html -split 0 -local_icons -info "" OTB-FAQ.tex
perl -pi -e 's/http\:\/\/www.melaneum.com\/OTB\/doxygen\/classotb_1_1StreamingImageFileWriter.htmlotb\:\:StreamingImageFileWriter/\<a href=\"http\:\/\/www.melaneum.com\/OTB\/doxygen\/classotb_1_1StreamingImageFileWriter.html\"\>otb\:\:StreamingImageFileWriter\<\/a\>/g' OTB-FAQ/OTB-FAQ.html
perl -pi -e 's/http\:\/\/www.melaneum.com\/OTB\/doxygen\/classitk_1_1StreamingImageFilter.htmlitk\:\:StreamingImageFilter/\<a href=\"http\:\/\/www.melaneum.com\/OTB\/doxygen\/classitk_1_1StreamingImageFilter.html\"\>itk\:\:StreamingImageFilter\<\/a\>/g' OTB-FAQ/OTB-FAQ.html
perl -pi -e 's/\<\/BODY\>/\<script src="http:\/\/www.google-analytics.com\/urchin.js" type="text\/javascript"\> \<\/script\> \<script type="text\/javascript"\> _uacct = "UA-1482698-1"; urchinTracker(); \<\/script\> \<\/BODY\>/g' OTB-FAQ/OTB-FAQ.html
pdflatex OTB-FAQ.tex

#!/usr/bin/python

import sys, subprocess,re,os

def main():
    for dirname,dirnames,filenames in os.walk(str(args[0])):
        band_list=[]
        for i in range(1,8):
            band_list.append('B'+str(i))
        
        for filename in filenames:
            if re.match(r'(.*)_concat.tif($)',filename):
                print "filename ",os.path.join(dirname, filename)
                argv = ['otbcli_BandMath']
                argv.append('-il')
                argv.append(os.path.join(dirname, filename))
                argv.append('-out')
                argv.append(os.path.splitext(os.path.join(dirname,filename))[0] + '_ndvi.tif')
                argv.append('float')
                argv.append('-exp')
                argv.append('ndvi(im1b4,im1b5)')

                subprocess.check_call(argv)        
if __name__ == '__main__':
    main(sys.argv[1:])

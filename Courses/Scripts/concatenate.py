#!/usr/bin/python

import sys, subprocess,re,os

def main(args):
    for dirname, dirnames, filenames in os.walk(str(args[0])):

        band_list=[]
        for i in range(1,8):
            band_list.append('B'+str(i))
        
        for subdirname in dirnames:
            if subdirname.find('LC8') != -1:
                print "subdir ",os.path.join(dirname, subdirname)
                img_list=[]
                process = ['otbcli_ConcatenateImages']
                process.append('-ram 512')
                process.append('-out')
                output_file=
                process.append(os.path.join(dirname, subdirname) 
                               + '_concat.tif' 
                               + '?&box=1540:680:3000:3000')
                #process.append('?&box=1438:613:3015:2586"') 
                process.append('uint16')
                process.append('-il')
                #print process
                for band in band_list:
                    process.append(os.path.join(
                                   os.path.join(dirname, subdirname),
                                   subdirname + '_' + band + '.TIF'))
                print process
                
                subprocess.check_call(process)

if __name__ == '__main__':
    main(sys.argv[1:])

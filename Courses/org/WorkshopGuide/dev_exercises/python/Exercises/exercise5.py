#! /usr/bin/python

from sys import argv
import otbApplication


if __name__ == "__main__":
    
    ''' Resampling and thresholding of Pekel Image
        - arg1 : occurrence level (0-100 values)
    '''

    # INPUTS    
    d={}
    d["occurrence_name"] = "ref/occurrence_90W_0N.tif"
    d["B3_image"] =  "ref/B3_ref.tif"  


    ########################################  
    #  App 1 : Resampling Occurrence Tile     #
    ###################################
    
    # The following line creates an instance of the Superimpose application
    app1 = otbApplication.Registry.CreateApplication("Superimpose")

    # The following lines set all the application parameters:
    app1.SetParameterString("inm",d["occurrence_name"])
    app1.SetParameterString("inr",d["B3_image"])
    app1.SetParameterString("out", "GSW_resampled.tif")
    app1.SetParameterFloat("fv",255)
    app1.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
    
    print("Launching... Resampling")
    # The following line execute the application
    app1.ExecuteAndWriteOutput()
    print("End of Resampling \n")

    ########################################  
    #  App 2 : Thresholding Occurrence Tile     #
    ###################################
    
    # The following line creates an instance of the Superimpose application
    app2 = otbApplication.Registry.CreateApplication("BandMath")

    # The following lines set all the application parameters:

    # Define Input im1: pre-final mask
    app2.AddImageToParameterInputImageList("il",app1.GetParameterOutputImage("out"))
    app2.SetParameterString("exp","im1b1>" + argv[1]+"?1:0")
    app2.SetParameterString("out", "GSW_"+argv[1]+".tif")
    app2.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
    
    print("Launching... Threshold ")
    # The following line execute the application
    app2.ExecuteAndWriteOutput()
    print("End of Threshold \n")


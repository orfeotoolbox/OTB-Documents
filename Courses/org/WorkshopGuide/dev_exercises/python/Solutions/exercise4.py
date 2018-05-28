#! /usr/bin/python

from sys import exit,argv
import otbApplication


if __name__ == "__main__":

    # Initialization of a dictonnary for the input data paths  
    d= {}
    
    # ---
    # FILL THE GAP 1 : Complete your dataset_folder with the 
    #                  WorkshopDataset app-python/images path  
    #        
    # Example:   
    # d["dataset_folder"] = "/home/WorkshopData/app-python/images"
    #
    d["dataset_folder"] = "images"
    #
    # END OF GAP 
    # ---
    if len(argv) > 1:
        d["image_name"] = argv[1]
    else:
        d["image_name"] = "SENTINEL2A_20170407-154054-255_L2A_T17MNP_D_V1-4" 

    if not "dataset_folder" in d:
        exit("Your data folder (\'d[\"dataset_folder\"]\') is not set.")
        
    d["input_path"] = d["dataset_folder"] + "/" + d["image_name"] +"/"
    d["B3_image"] =  d["image_name"] + "_FRE_B3.tif"  
    d["B4_image"] =  d["image_name"] + "_FRE_B4.tif"  
    d["B5_image"] =  d["image_name"] + "_FRE_B5.tif"  
    d["B8A_image"] = d["image_name"] + "_FRE_B8A.tif"  
    d["B11_image"] = d["image_name"] + "_FRE_B11.tif"  
    d["clouds_image"] = "MASKS/" + d["image_name"] + "_CLM_R1.tif" 


    ###################################  
    #  App 1 : Resampling B8A (NIR)   #
    ###################################
    
    # The following line creates an instance of the Superimpose application
    app1 = otbApplication.Registry.CreateApplication("Superimpose")

    # The following lines set all the application parameters:
    app1.SetParameterString("inr",str( d["input_path"] + d["B4_image"]))
    app1.SetParameterString("inm",str( d["input_path"] + d["B8A_image"]))
    app1.SetParameterFloat("fv",-10000)
    app1.SetParameterString("out", "B8A_10m.tif")
    
    print "Launching... Resampling"
    # The following line execute the application
    app1.Execute()
    print "End of Resampling \n" 

    ###################################  
    #  App 2  : NDVI Mask             #
    ###################################
    # Create the necessary OTB Applications
    app2 = otbApplication.Registry.CreateApplication("BandMath")

    # The following lines set all the application parameters:
    # Define Input im1: Band NIR (B8A Resampled)
    app2.AddImageToParameterInputImageList("il",app1.GetParameterOutputImage("out"))
    # Define Input im2: Band Red (B4)
    app2.AddParameterStringList("il",str(d["input_path"] + d["B4_image"]))
    app2.SetParameterString("out", "ndvi_mask.tif")
    app2.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
    app2.SetParameterString("exp", "(im1b1-im2b1)/(im1b1+im2b1)<0?1:0")
    
    # The following line execute the application
    print "Launching... BandMath : Mask ndvi "
    app2.Execute()
    print "End of BandMath \n" 



    ###################################
    #  App 3  : Final Land/Water Mask #
    ###################################
    # Create the necessary OTB Applications
    app3 = otbApplication.Registry.CreateApplication("BandMath")

    # The following lines set all the application parameters:
    # Define Input im1: pre-final mask
    app3.AddImageToParameterInputImageList("il",app2.GetParameterOutputImage("out"))
    # Define Input im2 : No data mask
    app3.AddParameterStringList("il",str(d["input_path"] + d["clouds_image"]))
    app3.SetParameterString("out", "ndvi_mask_clouds.tif")
    app3.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_uint8)
    # ---
    # FILL THE GAP 2 : Complete the bandmath expression to apply the 255 value to
    #                  the pixels where clouds image is different from 0 and keep
    #                  the NDVI Mask values where clouds image is equal to zero  
    #
    #                  Remember the inputs:
    #                       - im1b1 = water mask from app2;
    #                       - im2b1 = clouds image 
    #        
    # Exemple:   
    # app3.SetParameterString("exp", "??????")
    app3.SetParameterString("exp", "im2b1!=0?255:im1b1")
    #
    # END OF GAP 
    # ---

    # The following line execute the application
    print "Launching... BandMath : Land/Water mask"
    app3.Execute()
    print "End of BandMath \n" 


    ###############################
    # Check: Apply NODATA => 255 value
    ##############################
    print "Apply NODATA value = 255 \n" 
    ###################################
    #  App 4  : Final Land/Water Mask #
    ###################################
    # Create the necessary OTB Applications
    app4 = otbApplication.Registry.CreateApplication("ManageNoData")

    # The following lines set all the application parameters:
    # Define Input im1: water mask with wrong NODATA
    app4.SetParameterInputImage("in",app3.GetParameterOutputImage("out"))
    # Define Input im2 : No data mask
    app4.SetParameterString("mode","changevalue")
    app4.SetParameterString("mode.changevalue.newv","255")
    app4.SetParameterString("out", "water_mask_"+d["image_name"]+".tif")
    
    # The following line execute the application
    print "Launching... Manage No DATA : Land/Water mask"
    app4.ExecuteAndWriteOutput()
    print "End of BandMath \n" 

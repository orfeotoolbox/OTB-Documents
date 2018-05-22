#! /usr/bin/python

import otbApplication


if __name__ == "__main__":

     
    # Initialization of a dictonnary for the input images paths  
    d= {}
    
    # ---
    # FILL THE GAP 1 : Complete your dataset_folder with the 
    #                  WorkshopDataset app-python/images path  
    #        
    # Exemple:   
    # d["dataset_folder"] = "/home/WorkshopData/app-python/images"
    #
    d["dataset_folder"] = "images"
    #
    # END OF GAP 
    # ---

    d["image_name"] = "SENTINEL2A_20170407-154054-255_L2A_T17MNP_D_V1-4" 
    d["input_path"] = d["dataset_folder"] + "/" + d["image_name"] +"/"
    d["B3_image"] =  d["image_name"] + "_FRE_B3.tif"  
    d["B4_image"] =  d["image_name"] + "_FRE_B4.tif"  
    d["B8A_image"] = d["image_name"] + "_FRE_B8A.tif"  
    d["B11_image"] = d["image_name"] + "_FRE_B11.tif"  

    ##########################################  
    #  Exercise 2  : Chaining applications   #
    ##########################################
    
    
    ########### Application 1 : Resampling
    # 
    # The following line creates an instance of the Superimpose application
    application1 = otbApplication.Registry.CreateApplication("Superimpose")
     
    # ---
    # FILL THE GAP 2 : Complete the input and output parameters 
    #        
    # Exemple:   
    # 
    #application1.SetParameterString("inr",str( d["input_path"] + d["????"]))
    #application1.SetParameterString("inm",str( d["input_path"] + d["????"]))
    #application1.SetParameterString("out", "????.tif")
    application1.SetParameterString("inr",str( d["input_path"] + d["B4_image"]))
    application1.SetParameterString("inm",str( d["input_path"] + d["B8A_image"]))
    application1.SetParameterString("out", "B8A_10.tif")
    #
    # END OF GAP 
    # ---

    print "Launching... Resampling"
    # The following line execute the application
    application1.ExecuteAndWriteOutput()
    print "End of Resampling \n" 


    ########### Application 2 : NDVI Calculation
    #
    # Create the necessary OTB Applications
    application2 = otbApplication.Registry.CreateApplication("BandMath")


    # ---
    # FILL THE GAP 3 : Complete the input and output parameters of the BandMath
    #        
    # Example:   
    #application2.SetParameterStringList("il",["????.tif", str(d["input_path"] + d["?????"])])
    #application2.SetParameterString("out", "????.tif")
    #application2.SetParameterString("exp", "?????")
    application2.SetParameterStringList("il",["B8A_10.tif", str(d["input_path"] + d["B4_image"])])
    application2.SetParameterString("out", "ndvi.tif")
    application2.SetParameterString("exp", "(im1b1-im2b1)/(im1b1+im2b1)")
    # 
    #
    # END OF GAP 
    # ---
    # The following line execute the application
    print "Launching... BandMath : NDVI"
    application2.ExecuteAndWriteOutput()
    print "End of BandMath NDVI \n" 

    ########### Application 3: Mask Threshold
    #
    # Create the necessary OTB Applications
    application3 = otbApplication.Registry.CreateApplication("BandMath")

    # ---
    # FILL THE GAP 4 : Complete the input and output parameters of the BandMath
    #        
    # Exemple:   
    #application3.SetParameterStringList("il",["????.tif"])
    #application3.SetParameterString("out", "????.tif")
    #application3.SetParameterString("exp", "????")
    application3.SetParameterStringList("il",["ndvi.tif"])
    application3.SetParameterString("out", "water_mask.tif")
    application3.SetParameterString("exp", "im1b1<0?1:0")
    #
    # END OF GAP 
    # ---
    # The following line execute the application
    print "Launching... BandMath : Threshold mask on NDVI"
    application3.ExecuteAndWriteOutput()
    print "End of BandMath : Threshold Mask \n" 
 

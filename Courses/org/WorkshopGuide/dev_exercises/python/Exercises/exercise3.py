#! /usr/bin/python

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
     
    application1.SetParameterString("inr",str( d["input_path"] + d["B4_image"]))
    application1.SetParameterString("inm",str( d["input_path"] + d["B8A_image"]))
    application1.SetParameterString("out", "B8A_10m.tif")

    print("Launching... Resampling")
    # The following line execute the application
    application1.Execute()
    print("End of Resampling \n")


    ########### Application 2 : NDVI Calculation
    #
    # Create the necessary OTB Applications
    application2 = otbApplication.Registry.CreateApplication("BandMath")
    
    # ---
    # FILL THE GAP 2 : In-memory connection:
    #                  declare the application1 output as the application2
    #                  input (input name "il", StringList type)
    #        
    # Example:   
    # application?.AddImageToParameterInputImageList("il",application?.GetParameterOutputImage("???"))
    #
    # END OF GAP 
    # ---
    
    # Declare the input list : the first element is declared alone (im1 = Red-B4)
    application2.AddParameterStringList("il",str(d["input_path"] + d["B4_image"]))
    application2.SetParameterString("out", "ndvi_mask.tif")
  

    # ---
    # FILL THE GAP 3 : Complete the BandMath expression 
    #        
    # Example:   
    # application2.SetParameterString("exp", "?????")
    # 
    # END OF GAP 
    # ---
    # The following line execute the application
    print("Launching... BandMath : Water Mask by NDVI")
    application2.ExecuteAndWriteOutput()
    print("End of BandMath NDVI \n")


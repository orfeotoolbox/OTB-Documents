#! /usr/bin/python

from sys import exit
import otbApplication

if __name__ == "__main__":

    # Print the available applications
    print str(otbApplication.Registry.GetAvailableApplications())

    # Initialization of a dictonnary for the input data paths  
    d= {}
    
    ###############
    # FILL THE GAP 1 : Complete your dataset_folder with the 
    #                  WorkshopDataset app-python/data path  
    #        
    # Exemple:   
    # d["dataset_folder"] = "/home/WorkshopData/app-python/images"
    #
    d["dataset_folder"] = "images"
    #
    # END OF GAP 
    ###############

    if not "dataset_folder" in d:
        exit("Your data folder (\'d[\"dataset_folder\"]\') is not set.")
        
    d["image_name"] = "SENTINEL2A_20170407-154054-255_L2A_T17MNP_D_V1-4" 
    d["input_path"] = d["dataset_folder"] + "/" + d["image_name"] +"/"
    d["B3_image"] =  d["image_name"] + "_FRE_B3.tif"  
    d["B4_image"] =  d["image_name"] + "_FRE_B4.tif"  
    d["B5_image"] =  d["image_name"] + "_FRE_B5.tif"  
    d["B8A_image"] = d["image_name"] + "_FRE_B8A.tif"  
    d["B11_image"] = d["image_name"] + "_FRE_B11.tif"  
 



    #############################################   
    #  Application 1 : Resampling operation     #
    ############################################ #
    
    ###############
    # FILL THE GAP 2 : Create an instance of the Superimpose application 
    #                  WorkshopDataset app-python/data path  
    #        
    # Exemple:   
    # Superimpose = otbApplication.Registry.CreateApplication("???")
    #
    Superimpose = otbApplication.Registry.CreateApplication("Superimpose")
    #
    # END OF GAP 
    ###############

    # The following lines set the necessary application parameters:
    # ---
    # FILL THE GAP 3 : Complete the input and output parameters 
    #        
    # Example:   
    # 
    Superimpose.SetParameterString("inr",str( d["input_path"] + d["B4_image"]))
    Superimpose.SetParameterString("inm",str( d["input_path"] + d["B8A_image"]))
    Superimpose.SetParameterString("out", "B8A_10m.tif")
    #
    # END OF GAP 
    # ---
    

    # The following line execute the application
    Superimpose.ExecuteAndWriteOutput()


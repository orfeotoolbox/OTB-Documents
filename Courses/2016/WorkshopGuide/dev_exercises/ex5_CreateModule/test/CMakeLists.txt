otb_module_test()

#${otb-module} will be the name of this module and will not need to be
#changed when this module is renamed.

# TODO: change to your local directory path 
SET(INPUTDATA "/home/grizonnetm/data/THEIA2016/Data/stegano")

#test Divisor application
otb_test_application(NAME otbDividerAppTest
  APP  MyApp
  OPTIONS -in ${INPUTDATA}/image1.tif
  -out image1_divide_by_2.tif
  -divisor 2
  )

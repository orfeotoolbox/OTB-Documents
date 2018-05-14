otb_module_test()

#${otb-module} will be the name of this module and will not need to be
#changed when this module is renamed.

set(${otb-module}Tests
  otbEmptyTestDriver.cxx
  otbEmptyTest.cxx
)

add_executable(otbEmptyTestDriver ${${otb-module}Tests})
target_link_libraries(otbEmptyTestDriver ${${otb-module}-Test_LIBRARIES})
otb_module_target_label(otbEmptyTestDriver)

otb_add_test(NAME otbDeleteMeEmptyTest
  COMMAND otbEmptyTestDriver otbEmptyTest "argument1" "..." )

#test application
otb_test_application(NAME otbEmptyAppTest
                     APP  EmptyApp
                     )

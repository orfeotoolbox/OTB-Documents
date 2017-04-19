set(DOCUMENTATION "OTB divider module.")

# OTB_module() defines the module dependencies in DividerModule
# ExternalTemplate depends on OTBCommon and OTBApplicationEngine
# The testing module in ExternalTemplate depends on OTBTestKernel
# and OTBCommandLine

# define the dependencies of the include module and the tests
otb_module(Divider
  DEPENDS
    OTBCommon
    OTBApplicationEngine
  TEST_DEPENDS
    OTBTestKernel
    OTBCommandLine
  DESCRIPTION
    "${DOCUMENTATION}"
)

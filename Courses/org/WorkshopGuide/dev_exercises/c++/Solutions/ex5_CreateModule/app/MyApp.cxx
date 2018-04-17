#include "otbWrapperApplication.h"
#include "otbWrapperApplicationFactory.h"

#include "DividerImageFilter.h"

namespace otb
{

namespace Wrapper
{

class MyApp : public Application
{
public:
  typedef MyApp Self;
  typedef itk::SmartPointer<Self> Pointer; 

  itkNewMacro(Self);
  itkTypeMacro(MyApp, Application);

  typedef otb::DividerImageFilter<FloatImageType,FloatImageType> FilterType;
  
private:
  void DoInit()
  {
    SetName("MyApp");
    SetDescription("Divider application.");

    SetDocLongDescription("This application performs a division of all pixels by a common number. The divisor is provided as a parameter.\n"
      );

    //Optional descriptors
    SetDocLimitations("None");
    SetDocAuthors("OTB-Team");
    SetDocSeeAlso(" ");
    AddDocTag("Miscellaneous");

    //Parameter declarations
    AddParameter(ParameterType_InputImage,  "in",   "Input image");
    SetParameterDescription("in", "Image to perform computation on.");

    AddParameter(ParameterType_OutputImage, "out", "Output Image");
    SetParameterDescription("out","Output image.");

    AddParameter(ParameterType_Float, "divisor", "Divisor value");
    SetParameterDescription("divisor",
                            "The divisor value");
  }

  void DoUpdateParameters()
  {
  }

  void DoExecute()
  {
    FloatImageType::Pointer inImage = GetParameterImage<FloatImageType>("in");

    m_Filter = FilterType::New();
    m_Filter->SetInput( inImage );
  
    const float divisor = GetParameterFloat("divisor");

    m_Filter->SetDivisor( divisor );

    SetParameterOutputImage("out", m_Filter->GetOutput());
  }

  // Declare filter as attribute of the application class MyApp (mandatory)
  FilterType::Pointer       m_Filter;
};

} // namespace Wrapper
} // namespace otb

OTB_APPLICATION_EXPORT(otb::Wrapper::MyApp)

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
  void DoInit() ITK_OVERRIDE
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

    // TODO: Declare a new parameter to allow to set divisor value
  }

  void DoUpdateParameters() ITK_OVERRIDE
  {
  }

  void DoExecute() ITK_OVERRIDE
  {
    FloatImageType::Pointer inImage = GetParameterImage<FloatImageType>("in");

    m_Filter = FilterType::New();
    m_Filter->SetInput( inImage );

    float divisor = 1.;
    
    // TODO: Retrieve divisor value using OTB App API and set filter value
    // TIPS: You can change the divisor declaration and use const float instead

    // TODO: Change pipeline wiring and plug filter output to the output image
    SetParameterOutputImage<FloatImageType>("out", inImage);
  }

  // Declare filter as attribute of the application class MyApp (mandatory)
  FilterType::Pointer       m_Filter;
};

} // namespace Wrapper
} // namespace otb

OTB_APPLICATION_EXPORT(otb::Wrapper::MyApp)

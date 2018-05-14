
#include "DividerImageFilter.h"

#include "otbImage.h"

#include "otbImageFileReader.h"
#include "otbImageFileWriter.h"

int main(int argc, char * argv []) 
{
  if( argc < 4 )
    {
    std::cerr << "Missing arguments" << std::endl;
    std::cerr << "Usage: " << argv[0];
    std::cerr << "inputImage outputImage divisor" << std::endl;
    return EXIT_FAILURE;
    }
  
  typedef otb::Image< unsigned int,  2 > InputImageType;
  typedef otb::Image< unsigned int, 2 > OutputImageType;

  typedef otb::DividerImageFilter< 
                              InputImageType, 
                              OutputImageType 
                                            > FilterType;

  FilterType::Pointer filter = FilterType::New();

  typedef otb::ImageFileReader< InputImageType  >  ReaderType;
  typedef otb::ImageFileWriter< OutputImageType >  WriterType;

  ReaderType::Pointer reader = ReaderType::New();
  WriterType::Pointer writer = WriterType::New();

  reader->SetFileName( argv[1] );
  writer->SetFileName( argv[2] );
  
  filter->SetInput( reader->GetOutput() );
  writer->SetInput( filter->GetOutput() );

  typedef FilterType::InputRealType    DivisorType;
  
  DivisorType divisor = atof( argv[3] );

  filter->SetDivisor( divisor );

  try
    {
    writer->Update();
    }
  catch( itk::ExceptionObject & excp )
    {
    std::cerr << "Exception caught !" << std::endl;
    std::cerr << excp << std::endl;
    }
  
  return 0;
}


#include "otbImage.h"
#include "otbImageFileReader.h"
#include "otbImageFileWriter.h"

#include "itkGradientMagnitudeImageFilter.h" 

int main(int argc, char * argv[])
{
  if (argc != 3)
    {
    std::cerr << "Usage: "
              << argv[0]
              << " <input_filename> <output_filename>"
              << std::endl;
    return EXIT_FAILURE;
    }

  typedef otb::Image<unsigned int, 2> ImageType;
  typedef otb::ImageFileReader<ImageType> ReaderType;
  ReaderType::Pointer reader = ReaderType::New();
  
  typedef otb::ImageFileWriter<ImageType> WriterType;
  WriterType::Pointer writer = WriterType::New();
  
  reader->SetFileName(argv[1]);
  writer->SetFileName(argv[2]);
  
  typedef itk::GradientMagnitudeImageFilter <ImageType, ImageType> FilterType; 

  FilterType::Pointer filter = FilterType::New();

  // TODO: Modify line 34 to add the GradientMagnitudeImageFilter in
  // between the reader and the writer
  writer->SetInput(reader->GetOutput());
  
  writer->Update();

  return EXIT_SUCCESS;
}

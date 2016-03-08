#include "otbImage.h"
#include "otbImageFileReader.h"
#include "otbImageFileWriter.h"
#include "otbMultiChannelExtractROI.h"
#include <iostream>
#include <string>

int main(int argc, char * argv[])
{
  const std::vector<const char*> dates = {
  "20140212",
  "20140309",
  "20140316",
  "20140401",
  "20140410",
  "20140417",
  "20140519",
  "20140528",
  "20140613",
  "20140620",
  "20140722",
  "20140731",
  "20140816",
  "20140901",
  "20140917",
  "20141003",
  "20141019",
  "20141026",
  "20141120",
  "20141222",
  "20141229"
  };

  if (argc != 2)
  {
    std::cerr << "Usage: LS8_Extract <path to LS8 image>" << std::endl;
    return EXIT_FAILURE;
  }

  const std::string LS8_path(argv[1]);

  // Load LS8 image
  typedef otb::VectorImage<float, 2> InputType;
  typedef otb::VectorImage<int, 2> OutputType;

  typedef otb::ImageFileReader<InputType> ReaderType; 
  ReaderType::Pointer reader = ReaderType::New(); 

  std::cout << LS8_path << std::endl;
  reader->SetFileName(LS8_path);

  // Setup channel extract

  // For each date
  for (std::size_t i = 0; i < dates.size(); ++i)
  {
    typedef otb::MultiChannelExtractROI<InputType::InternalPixelType, OutputType::InternalPixelType> ExtractChannelType; 
    ExtractChannelType::Pointer extractChannel = ExtractChannelType::New();

    //extractChannel->SetExtractRegion(reader->
    extractChannel->SetInput(reader->GetOutput());

    // Setup writer
    typedef otb::ImageFileWriter<OutputType> WriterType; 
    WriterType::Pointer writer = WriterType::New(); 
   
    writer->SetInput(extractChannel->GetOutput());

    const std::size_t number_of_bands = 7;

    // Extract the current date
    extractChannel->SetFirstChannel(i*number_of_bands+1); // channel indexing is 1 based
    extractChannel->SetLastChannel(i*number_of_bands + number_of_bands);

    // Set filename and write to disk
    std::string filename = std::string("LANDSAT_MultiTempIm_clip_GapF_") + dates[i] + ".tif";
    std::cout << filename << std::endl;
    writer->SetFileName(filename);
    writer->Update();
  }
}


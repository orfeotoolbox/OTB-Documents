#include "otbImage.h"
#include <iostream>

int main(int itkNotUsed(argc), char * itkNotUsed(argv)[])
{
  typedef otb::Image<unsigned short, 2> ImageType;

  ImageType::Pointer image = ImageType::New();

  std::cout << "OTB Hello World !" << std::endl;

  return EXIT_SUCCESS;
}

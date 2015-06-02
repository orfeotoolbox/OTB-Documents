/*=========================================================================

  Program:   ORFEO Toolbox
  Language:  C++
  Date:      $Date$
  Version:   $Revision$


  Copyright (c) Centre National d'Etudes Spatiales. All rights reserved.
  See OTBCopyright.txt for details.


     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
#include "otbWrapperApplication.h"
#include "otbWrapperApplicationFactory.h"

#include "otbStreamingStatisticsVectorImageFilter.h"

namespace otb
{
namespace Wrapper
{

class AdvancedTileFusion : public Application
{
public:
  /** Standard class typedefs. */
  typedef AdvancedTileFusion            Self;
  typedef Application                   Superclass;
  typedef itk::SmartPointer<Self>       Pointer;
  typedef itk::SmartPointer<const Self> ConstPointer;

  /** Standard macro */
  itkNewMacro(Self);

  itkTypeMacro(AdvancedTileFusion, otb::Application);
  
  typedef otb::ImageFileReader<FloatVectorImageType> ReaderType;
  
  typedef otb::StreamingStatisticsVectorImageFilter<FloatVectorImageType> StatFilterType;

private:
  void DoInit()
  {
    SetName("AdvancedTileFusion");
    SetDescription("Fusion of several tile files.");

    // Documentation
    SetDocName("Advanced Image Tile Fusion");
    SetDocLongDescription("Concatenate several tile files into a single image file using a VRT file.");
    SetDocLimitations("None");
    SetDocAuthors("OTB-Team");
    SetDocSeeAlso(" ");

    AddDocTag(Tags::Manip);

    AddParameter(ParameterType_InputImageList,  "il",   "Input Tile Images");
    SetParameterDescription("il", "Input tiles to concatenate (in lexicographic order : (0,0) (1,0) (0,1) (1,1)).");

    AddParameter(ParameterType_Int, "cols", "Number of tile columns");
    SetParameterDescription("cols", "Number of columns in the tile array");

    AddParameter(ParameterType_Int, "rows", "Number of tile rows");
    SetParameterDescription("rows", "Number of rows in the tile array");

    AddParameter(ParameterType_OutputImage,  "out",   "Output Image");
    SetParameterDescription("out", "Output entire image");
    
    AddParameter(ParameterType_Empty, "dyna", "Dynamic adaptation");
    SetParameterDescription("dyna","Flag to enable a dynamic adaptation between tiles. The first tile is used as a reference");
    DisableParameter("dyna");
    MandatoryOff("dyna");

   // Doc example parameter settings
    SetDocExampleParameterValue("il", "Scene_R1C1.tif Scene_R1C2.tif Scene_R2C1.tif Scene_R2C2.tif");
    SetDocExampleParameterValue("cols","2");
    SetDocExampleParameterValue("rows","2");
    SetDocExampleParameterValue("out", "EntireImage.tif");
  }

  void DoUpdateParameters()
  {
    // Nothing to be done
  }
  
  std::string WriteVRTFile(unsigned int cols,unsigned int rows)
  {
    // Get output path for VRT
    std::string vrtOutputPath;
    std::string outputPath = this->GetParameterString("out");
    std::stringstream vrtName;
    vrtName << itksys::SystemTools::GetFilenameWithoutExtension(outputPath.c_str()) << ".vrt";
    
    std::vector<std::string> vrtParts;
    itksys::SystemTools::SplitPath(outputPath.c_str(), vrtParts);
    
    vrtParts.pop_back();
    vrtParts.push_back(vrtName.str());
    vrtOutputPath = itksys::SystemTools::JoinPath(vrtParts);
    
    // check first image
    std::vector<std::string> pathList = this->GetParameterStringList("il");
    ReaderType::Pointer reader = ReaderType::New();
    reader->SetFileName(pathList[0]);
    reader->UpdateOutputInformation();
    
    unsigned int nbBands = reader->GetOutput()->GetNumberOfComponentsPerPixel();
    std::string dataType;
    switch(reader->GetImageIO()->GetComponentType())
      {
      case otb::ImageIOBase::UCHAR : 
        dataType = "Byte";
        break;
      case otb::ImageIOBase::USHORT : 
        dataType = "UInt16";
        break;
      case otb::ImageIOBase::SHORT : 
        dataType = "Int16";
        break;
      case otb::ImageIOBase::UINT : 
        dataType = "UInt32";
        break;
      case otb::ImageIOBase::INT : 
        dataType = "Int32";
        break;
      case otb::ImageIOBase::FLOAT : 
        dataType = "Float32";
        break;
      case otb::ImageIOBase::DOUBLE : 
        dataType = "Float64";
        break;
      default:
        otbAppLogWARNING("Pixel type (" << 
          reader->GetImageIO()->GetComponentTypeAsString(
            reader->GetImageIO()->GetComponentType()) << 
          ") not handled ! Using Float32 as default");
        dataType = "Float32";
        break;
      }
    
    // parse all images
    unsigned int sizesX[cols];
    unsigned int sizesY[rows];
    unsigned int offsetX[cols];
    unsigned int offsetY[rows];
    unsigned int inputIndex = 0;
    
    StatFilterType::Pointer statFilter = StatFilterType::New();
    statFilter->SetInput(reader->GetOutput());
    StatFilterType::RealPixelType mean_ref(nbBands);
    StatFilterType::RealPixelType stdDev_ref(nbBands);
    std::vector<float> scaleRatio;
    std::vector<float> scaleOffset;
    
    for (unsigned int r = 0; r < rows; ++r)
      {
      for (unsigned int c = 0; c < cols; ++c)
        {
        // Get image dimensions
        reader->SetFileName(pathList[inputIndex]);
        reader->UpdateOutputInformation();
        FloatVectorImageType::SizeType imgSize = 
          reader->GetOutput()->GetLargestPossibleRegion().GetSize();
        
        // Get statistics info
        if (this->IsParameterEnabled("dyna"))
          {
          statFilter->Update();
          if (inputIndex)
            {
            StatFilterType::RealPixelType mean(nbBands);
            StatFilterType::RealPixelType stdDev(nbBands);
            mean = statFilter->GetMean();
            for (unsigned int k=0 ; k<nbBands ; ++k)
              {
              stdDev[k] = vcl_sqrt((statFilter->GetCovariance())(k,k));
              }
            float curRatio = 0.0;
            float curOffset = 0.0;
            for (unsigned int k=0 ; k<nbBands ; ++k)
              {
              curRatio += stdDev_ref[k] / stdDev[k];
              curOffset += mean_ref[k] - mean[k] * stdDev_ref[k] / stdDev[k];
              }
            scaleRatio.push_back(curRatio / static_cast<float>(nbBands));
            scaleOffset.push_back(curOffset / static_cast<float>(nbBands));
            }
          else
            {
            mean_ref = statFilter->GetMean();
            for (unsigned int k=0 ; k<nbBands ; ++k)
              {
              stdDev_ref[k] = vcl_sqrt((statFilter->GetCovariance())(k,k)); 
              }
            scaleRatio.push_back(1.0);
            scaleOffset.push_back(0.0);
            }
          }
        
        // compute layout dimensions : sizeX, sizeY, offsetX, offsetY
        if (c == 0)
          {
          sizesY[r] = imgSize[1];
          offsetY[r] = 0;
          for (unsigned int i=0 ; i < r ; ++i)
            {
            offsetY[r] += sizesY[i];
            }
          }
        else
          {
          if (sizesY[r] != imgSize[1])
            {
            otbAppLogWARNING("Wrong tile size : got " << imgSize[1] << " , expected " << sizesY[r]);
            }
          }
        
        if (r == 0)
          {
          sizesX[c] = imgSize[0];
          offsetX[c] = 0;
          for (unsigned int i=0 ; i < c ; ++i)
            {
            offsetX[c] += sizesX[i];
            }
          }
        else
          {
          if (sizesX[c] != imgSize[0])
            {
            otbAppLogWARNING("Wrong tile size : got " << imgSize[0] << " , expected " << sizesX[c]);
            }
          }
        
        ++inputIndex;
        }
      }
    
    // Compute total size
    unsigned int totalX=0;
    unsigned int totalY=0;
    for (unsigned int i=0 ; i < cols ; ++i)
      {
      totalX += sizesX[i];
      }
    for (unsigned int i=0 ; i < rows ; ++i)
      {
      totalY += sizesY[i];
      }
    
    std::string sourceType("SimpleSource");
    if (this->IsParameterEnabled("dyna"))
      {
      sourceType = "ComplexSource";
      }
    
    // Write VRT
    std::ofstream ofs(vrtOutputPath.c_str());
    ofs<<"<VRTDataset rasterXSize=\""<<totalX<<"\" rasterYSize=\""<<totalY<<"\">"<<std::endl;
    for (unsigned int k=0 ; k<nbBands ; ++k)
      {
      ofs<<"\t<VRTRasterBand dataType=\""<< dataType <<"\" band=\""<< (k+1) <<"\">"<<std::endl;
      inputIndex = 0;
      for (unsigned int r = 0; r < rows; ++r)
        {
        for (unsigned int c = 0; c < cols; ++c)
          {
          ofs << "\t\t<" << sourceType << ">" << std::endl;
          ofs << "\t\t\t<SourceFilename>"<< pathList[inputIndex] <<"</SourceFilename>" << std::endl;
          ofs << "\t\t\t<SourceBand>"<< (k+1) << "</SourceBand>" << std::endl;
          ofs << "\t\t\t<SrcRect xOff=\""<<0<<"\" yOff=\""<<0<<"\" xSize=\""<<sizesX[c]<<"\" ySize=\""<<sizesY[r]<<"\"/>" << std::endl;
          ofs << "\t\t\t<DstRect xOff=\""<<offsetX[c]<<"\" yOff=\""<<offsetY[r]<<"\" xSize=\""<<sizesX[c]<<"\" ySize=\""<<sizesY[r]<<"\"/>" << std::endl;
          if (this->IsParameterEnabled("dyna"))
            {
            ofs << "\t\t\t<ScaleRatio>"<< scaleRatio[inputIndex] << "</ScaleRatio>" << std::endl;
            ofs << "\t\t\t<ScaleOffset>"<< scaleOffset[inputIndex] << "</ScaleOffset>" << std::endl;
            }
          ofs << "\t\t</" << sourceType << ">" << std::endl;
          ++inputIndex;
          }
        }
      ofs<<"\t</VRTRasterBand>"<<std::endl;
      }
    ofs<<"</VRTDataset>"<<std::endl;
    ofs.close();
    return vrtOutputPath;
  }

  void DoExecute()
  {
    // Call WriteVRTFile
    std::string vrtPath;
    vrtPath = this->WriteVRTFile(this->GetParameterInt("cols"),
                       this->GetParameterInt("rows"));
    
    // Instanciate internal reader
    m_InternalReader = ReaderType::New();
    m_InternalReader->SetFileName(vrtPath);
    
    // Plug output image
    SetParameterOutputImage("out", m_InternalReader->GetOutput());
  }
  
  ReaderType::Pointer m_InternalReader;
};

}
}

OTB_APPLICATION_EXPORT(otb::Wrapper::AdvancedTileFusion)

/*=========================================================================

  Program:   Insight Segmentation & Registration Toolkit
  Module:    $RCSfile: DividerByTwoImageFilter.h,v $
  Language:  C++
  Date:      $Date: 2005/09/25 01:11:06 $
  Version:   $Revision: 1.2 $

  Copyright (c) Insight Software Consortium. All rights reserved.
  See ITKCopyright.txt or http://www.itk.org/HTML/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even 
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
#ifndef __DividerByTwoImageFilter_h
#define __DividerByTwoImageFilter_h

#include "itkUnaryFunctorImageFilter.h"

namespace itk
{
  
/** \class DividerByTwoImageFilter
 * \brief This is a pixel-wise filter that divides by two every
 * pixel in the input image. 
 *
 * \ingroup IntensityImageFilters  Multithreaded
 */
namespace Functor {  
  
template< class TInput, class TOutput>
class Divider
{
public:
  Divider() {}
  ~Divider() {}
  inline TOutput operator()( const TInput & A )
  {
    typedef typename itk::NumericTraits<TInput>::RealType  RealType;
    return static_cast<TOutput>( RealType( A ) / 2.0 );
  }
}; 
}
template <class TInputImage, class TOutputImage>
class ITK_EXPORT DividerByTwoImageFilter :
    public
UnaryFunctorImageFilter<TInputImage,TOutputImage, 
           Functor::Divider< typename TInputImage::PixelType, 
                             typename TOutputImage::PixelType>   >
{
public:
  /** Standard class typedefs. */
  typedef DividerByTwoImageFilter  Self;
  typedef UnaryFunctorImageFilter<TInputImage,TOutputImage, 
                 Functor::Divider< typename TInputImage::PixelType, 
                                   typename TOutputImage::PixelType> > Superclass;
  typedef SmartPointer<Self>   Pointer;
  typedef SmartPointer<const Self>  ConstPointer;

  /** Method for creation through the object factory. */
  itkNewMacro(Self);
  
protected:
  DividerByTwoImageFilter() {}
  virtual ~DividerByTwoImageFilter() {}

private:
  DividerByTwoImageFilter(const Self&); //purposely not implemented
  void operator=(const Self&); //purposely not implemented

};

} // end namespace itk


#endif

/*=========================================================================

  Program:   Insight Segmentation & Registration Toolkit
  Module:    $RCSfile: DividerImageFilter.h,v $
  Language:  C++
  Date:      $Date: 2005/09/25 01:59:15 $
  Version:   $Revision: 1.1 $

  Copyright (c) Insight Software Consortium. All rights reserved.
  See ITKCopyright.txt or http://www.itk.org/HTML/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even 
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
#ifndef DividerImageFilter_h
#define DividerImageFilter_h

#include "itkUnaryFunctorImageFilter.h"

namespace otb
{
  
/** \class DividerImageFilter
 * \brief This is a pixel-wise filter that divides every
 * pixel in the input image by a user-provided number. 
 */
namespace Functor {  
  
template< class TInput, class TOutput>
class Divider
{
public:
  Divider() {m_Divisor = itk::NumericTraits< InputRealType >::One;}
  ~Divider() {}
  typedef typename itk::NumericTraits<TInput>::RealType  InputRealType;
  inline TOutput operator()( const TInput & A )
    {
    return static_cast<TOutput>( InputRealType( A ) / m_Divisor );
    }
  void SetDivisor( const InputRealType & divisor )
    {
    m_Divisor = divisor;
    }
private:
  InputRealType m_Divisor;
}; 
}
template <class TInputImage, class TOutputImage>
class ITK_EXPORT DividerImageFilter :
    public
itk::UnaryFunctorImageFilter<TInputImage,TOutputImage, 
           Functor::Divider< typename TInputImage::PixelType, 
                             typename TOutputImage::PixelType>   >
{
public:
  /** Standard class typedefs. */
  typedef DividerImageFilter  Self;
  typedef itk::UnaryFunctorImageFilter<TInputImage,TOutputImage, 
                 Functor::Divider< typename TInputImage::PixelType, 
                                   typename TOutputImage::PixelType> > Superclass;
  typedef itk::SmartPointer<Self>   Pointer;
  typedef itk::SmartPointer<const Self>  ConstPointer;

  /** Method for creation through the object factory. */
  itkNewMacro(Self);
  
  /** Explicit typedef for the FunctorType from the Superclass */
  typedef typename  Superclass::FunctorType    FunctorType;

  /** Get the divisor type from the functor type */
  typedef typename  FunctorType::InputRealType  InputRealType;

  void SetDivisor( const InputRealType & divisor )
    {
    this->GetFunctor().SetDivisor( divisor );
    }

protected:
  DividerImageFilter() {}
  virtual ~DividerImageFilter() {}

private:
  DividerImageFilter(const Self&); //purposely not implemented
  void operator=(const Self&); //purposely not implemented

};

} // end namespace otb


#endif

#pragma once
#ifndef INTEGRALIMAGE_H
#define INTEGRALIMAGE_H

#include <cassert>
#include <iostream>
#include <memory>
#include <vector>

#ifndef uchar
typedef unsigned char uchar;
#endif

#include "LogFile.h"

/*
template<typename T>
class BaseImage
{
public:
        BaseImage(int W, int H)
        {
                mWidth = W;
                mHeight = H;
                int nSize = mWidth*mHeight;
                pData = new T[nSize];
        }
        virtual ~BaseImage()
        {
                delete pData;
        };
        virtual T Pixel(int x, int y) const
        {
                return *(pData + mWidth*y + x);
        }
        int Width()const{ return mWidth; };
        int Height()const{ return mHeight; };
        const T *Pointer()const { return pData; };
        T * & Pointer() { return pData; };
protected:
        int mWidth;
        int mHeight;
private:
        T *pData;

};*/

template <class T, class container = std::vector<T>, int nDim = 2>
class IntegralImage {
public:
  IntegralImage(const container &Src, int nWidth, int nHeight, int nDepth = 1)
      : mWidth(nWidth), mHeight(nHeight), mDepth(nDepth) {
    size_t N = (size_t)nWidth * nHeight * nDepth;
    Data.resize(N);
    LogFile::WriteData("kriging.log",
                       "long long N = (size_t)nWidth*nHeight*nDepth: ", N);
    std::vector<int>::iterator it = Data.begin();
    typename container::const_iterator pSrc = Src.cbegin();
    int I = 0;
    if (nDim == 2) {
      for (size_t k = 0; k < nDepth; k++) {
        I = 0;
        for (size_t j = 0; j < mWidth; j++) {
          I += *pSrc++;
          *(it++) = I;
        }
        for (size_t i = 1; i < mHeight; i++) {
          I = 0;
          *(it++) = (*pSrc++) + *(it - mWidth);
          for (size_t j = 1; j < mWidth; j++) {
            I = *pSrc++;
            *(it++) = I + *(it - 1) + *(it - mWidth) - *(it - mWidth - 1);
          }
        }
      }
    }

    /*	container<uchar> dbg(27);
            for (int i = 0; i < dbg.size(); i++)
                    dbg[i] = Data[i];*/

    if (nDim == 3) {
      I = 0;
      for (size_t j = 0; j < mWidth; j++) {
        I += *pSrc++;
        *(it++) = I;
      }
      for (size_t i = 1; i < mHeight; i++) {
        I = 0;
        *(it++) = (*pSrc++) + *(it - mWidth);
        for (size_t j = 1; j < mWidth; j++) {
          I = *pSrc++;
          *(it++) = I + *(it - 1) + *(it - mWidth) - *(it - mWidth - 1);
        }
      }
      for (size_t k = 1; k < mDepth; k++) {
        int I = 0;
        for (int j = 0; j < mWidth; j++) {
          I += *pSrc++;
          *(it++) = I;
        }
        for (size_t i = 1; i < mHeight; i++) {
          I = 0;
          *(it++) = (*pSrc++) + *(it - mWidth);
          for (size_t j = 1; j < mWidth; j++) {
            I = *pSrc++;
            *(it++) = I + *(it - 1) + *(it - mWidth) - *(it - mWidth - 1);
          }
        }
      }
      // for (int i = 0; i < dbg.size(); i++)
      //	dbg[i] = Data[i];
      it = Data.begin() + mWidth * mHeight;
      for (size_t k = 1; k < mDepth; k++) {
        for (size_t i = 0; i < mHeight; i++) {
          for (size_t j = 0; j < mWidth; j++) {
            *it = *it + *(it - mWidth * mHeight);
            it++;
          }
        }
      }
    }
  };

  /*IntegralImage(const BaseImage<unsigned char> &Src);
  IntegralImage(const BaseImage<unsigned char> &Src);*/
  virtual ~IntegralImage(){};
  int BlockSumm(int bottom, int top, int right, int left) const {
    /*assert(top>0 || top<mHeight || top<bottom);
    assert(bottom<mHeight);
    assert(left>0 || left<mWidth || left<right);
    assert(right<mWidth);*/
    int br = bottom * mWidth + right;
    int bl = bottom * mWidth + left;

    if (top <= 0) {
      if (left <= 0)
        return Data[br];
      else
        return Data[br] - Data[bl];
    }
    int tr = top * mWidth + right;
    if (left <= 0)
      return Data[br] - Data[tr];

    int tl = top * mWidth + left;

    return Data[br] - Data[bl] + Data[tl] - Data[tr];
  }

  int BlockSumm(int bottom, int top, int right, int left, int frn,
                int bhnd) const {
    LogFile::Assert(top <= bottom, "top <= bottom", "kriging.log");
    LogFile::Assert(left <= right, "left <= right,", "kriging.log");
    LogFile::Assert(frn <= bhnd, "frn <= bhnd", "kriging.log");
    size_t bbr = (size_t)bhnd * mWidth * mHeight + bottom * mWidth + right;
    size_t fbr = (size_t)frn * mWidth * mHeight + bottom * mWidth + right;
    size_t bbl = bbr - right + left;
    size_t fbl = fbr - right + left;
    size_t btr = bbr - bottom * mWidth + top * mWidth;
    size_t btl = btr - right + left;
    size_t ftl = fbl - bottom * mWidth + top * mWidth;
    size_t ftr = ftl - left + right;

    int v = Data[bbr];
    if (frn > 0) {
      v -= Data[fbr];
      if (left > 0) {
        v += Data[fbl];
      }
      if (top > 0) {
        v += Data[ftr];
        if (left > 0)
          v -= Data[ftl];
      }
    }
    if (left > 0) {
      v -= Data[bbl];
    }
    if (top > 0) {
      v -= Data[btr];
      if (left > 0)
        v += Data[btl];
    }
    assert(v >= 0);
    return v;
    // return pImageData[d*mWidth*mHeight + h*mWidth + w] -
    // pImageData[d*mWidth*mHeight + h*mWidth] - pImageData[h*mWidth + w] +
    // pImageData[h*mWidth] - pImageData[d*mWidth*mHeight + w] +
    // pImageData[d*mWidth*mHeight] + pImageData[w] - pImageData[0]; bbr
    // //bbl											//fbr					//fbl				//btr								//btl
    // //ftr
    // //ftl
  }

  // std::VECTOR_GENERATOR<int>::result Data;
  // std::vector<int, 4, std::lru_pager<4>, 24 * 1024 * 1024>::iterator
  typedef typename std::vector<int>::iterator IntImageIterator;
  typedef typename std::vector<int>::const_iterator IntImageConstIterator;
  std::vector<int> Data;
  int Width() const { return mWidth; };
  int Height() const { return mHeight; };
  int Depth() const { return mDepth; };

protected:
  //		int *pData;
private:
  void CopyData(int *pData, int size_W, int size_H);
  int mWidth;
  int mHeight;
  int mDepth;
};

#endif

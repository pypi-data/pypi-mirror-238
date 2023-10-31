#ifndef HESSIANSEGMENTATION_H
#define HESSIANSEGMENTATION_H 
#include <vector>
#include "DynamicArray.h"
#include "Config.h"
#include <cmath>
#include "IntegralImage.h"
#include "threshold.h"
#include "Point.h"
#include "LatticeModel.h"
#include "RandomNumbers.h"
#define HFactor 1

struct HessianSettings
{
	HessianSettings() :Order(3), Threshold(20), Sgn(1),Gain(1),nPhases(2){};
	int Order;
	int Threshold;
	double Gain;
	int Sgn;
	int nScales;
	bool IsAuto;
	bool UseScales;
	int nPhases;
};

template <class T, class container = std::vector<T>, int nDim = 2>
class HessianLayer
{
	using LatticeIterator = typename container::iterator;
	using LatticeConstIterator = typename container::const_iterator;

public:
	HessianLayer(const IntegralImage<T, container, nDim> &Src, HessianSettings &Hss) :Order(Hss.Order), mFiltW(3 * Hss.Order), mBlobDirection(1), mSigma(-1)
	{
		LogFile::WriteData("kriging.log", "(const IntegralImage<T, container, nDim> &Src, HessianSettings &Hss)");
		assert(nDim == 2 || nDim == 3);
		mHessianImg.resize((size_t)Src.Width()*Src.Height()*Src.Depth());

		this->mWidth = Src.Width();
		this->mHeight = Src.Height();
		this->mDepth = Src.Depth();

		if (Hss.Sgn == 1)
			mBlobDirection = -1;
		else
		if (Hss.Sgn == 2)
			mBlobDirection = 2;
		SetOrder(Hss.Order);
	}
	void SetDirection(int dir)
	{
		mBlobDirection = dir;
	}
	void Perform(const IntegralImage<T, container, nDim> &Src)
	{
		typename IntegralImage<T, container, nDim>::IntImageConstIterator pSrc = Src.Data.cbegin();// it top-left corner of fragment of integral image
		HessianLayer::HessImgIterator pDest= mHessianImg.begin();

		double dxx, dyy, dxy, dxy2, dxz, dxz2, dzz, dyz, dyz2;
				
		//pDest += ((3 * Order - 1) / 2)*this->mWidth + ((3 * Order - 1) / 2);
		int mFiltW_2 = mFiltW / 2;
		
		double Scale = 1.0 / (mFiltW*(mFiltW - mIntactFld * 2)*(mFiltW - mIntactFld * 2));
		if (this->mDepth==1)
			 Scale = 1.0 / (mFiltW_2*Order*2);

		std::fill(mHessianImg.begin(), mHessianImg.end(), 0);
		double S_dest = 0; int n_dest = 0;
		for (int z = 0; z < Src.Depth(); z++)// for pseudo3D otherwise z=Src.Depth()-mFiltW
		{
		//	pSrc = Src.Data.cbegin() + Src.Width()*Src.Height()*z;
			size_t shift = (size_t)Src.Width()*Src.Height()*z + mFiltW_2*Src.Width();// +mFiltW_2;
			pDest = mHessianImg.begin() + shift;// ((3 * Order - 1) / 2)*this->mWidth + ((3 * Order - 1) / 2);
			
			for (int y = 0; y < Src.Height(); ++y)
			{
				size_t shift = (size_t)Src.Width()*Src.Height()*z + y*Src.Width();// +mFiltW_2;
				pDest = mHessianImg.begin() + shift;
				for (int x = 0; x < Src.Width(); ++x)
				{
					if (z == 9 && y == 127 && x == 57)
						int sdsd = 7;
					int denomenator =0;
					if (x>mFiltW_2 && x < Src.Width() - mFiltW_2 - 1)
					{
						dxx = ResponseDXX(Src, x, y, z)*Scale;
						denomenator++;
					}
					else
						dxx = 0;
					if (y>mFiltW_2 && y < Src.Height() - mFiltW_2 - 1)
					{
						dyy = ResponseDYY(Src, x, y, z)*Scale;
						denomenator++;
					}
					else
						dyy = 0;
					if (z>mFiltW_2 && z < Src.Depth() - mFiltW_2 - 1)
					{
						dzz = ResponseDZZ(Src, x, y, z)*Scale;
						denomenator++;
					}
					else
						dzz = 0;
					if (x>mFiltW_2 && x < Src.Width() - mFiltW_2 - 1 && y>mFiltW_2 && y < Src.Height() - mFiltW_2 - 1)
					{
						Point pt = ResponseDXY(Src, x, y, z);
						dxy = pt.x()*Scale;
						dxy2 = pt.y()*Scale;
						denomenator+=2;
					}
					else
					{
						dxy = 0;
						dxy2 =0;
					}

					if (x>mFiltW_2 && x < Src.Width() - mFiltW_2 - 1 && z>mFiltW_2 && z < Src.Depth() - mFiltW_2 - 1)
					{
						Point pt = ResponseDXZ(Src, x, y, z);
						dxz = pt.x()*Scale;
						dxz2 = pt.y()*Scale;
						denomenator+=2;
					}
					else
					{
						dxz = 0;
						dxz2 = 0;
					}

					if (y>mFiltW_2 && y < Src.Height() - mFiltW_2 - 1 && z>mFiltW_2 && z < Src.Depth() - mFiltW_2 - 1)
					{
						Point pt = ResponseDYZ(Src, x, y, z);
						dyz = pt.x()*Scale;
						dyz2 = pt.y()*Scale;
						denomenator+=2;
					}
					else
					{
						dyz = 0;
						dyz2 = 0;
					}

     /*               
					dxx = mBlobDirection*dxx > 0 ? dxx : 0;
					dyy = mBlobDirection*dyy > 0 ? dyy : 0;
					dzz = mBlobDirection*dzz > 0 ? dzz : 0;
					dxy = mBlobDirection*dxy > 0 ? dxy : 0;
					dxy2 = mBlobDirection*dxy2 > 0 ? dxy2 : 0;
					dxz = mBlobDirection*dxz > 0 ? dxz : 0;
					dxz2 = mBlobDirection*dxz2 > 0 ? dxz2 : 0;
					dyz = mBlobDirection*dyz > 0 ? dyz : 0;
					dyz2 = mBlobDirection*dyz2 > 0 ? dyz2 : 0;
					
					
*/
#ifdef USE_DET_HSS 
					float det = dxx*(dyy*dzz - dyz*dyz2) - dxy*(dxy2*dzz - dyz*dxz) + dxz*(dxy2*dyz2 - dxz2*dyy);

					det = det > 0 ? det:0;
					int v = 100 * det;
					*pDest = v;

					if (*pDest > 10000000)
					{
						LogFile::WriteData("kriging.log", " *pDest > 10000000 *pDest = ", *pDest);
						LogFile::WriteData("kriging.log", " *pDest > 10000000 x = ", x);
						LogFile::WriteData("kriging.log", " *pDest > 10000000 y=  ", y);
						LogFile::WriteData("kriging.log", " *pDest > 10000000 z = ", z);
					}
#endif				

#ifndef USE_DET_HSS 
					dxx = mBlobDirection*dxx > 0 ? dxx : 0;
					dyy = mBlobDirection*dyy > 0 ? dyy : 0;
					dzz = mBlobDirection*dzz > 0 ? dzz : 0;
					dxy = mBlobDirection*dxy > 0 ? dxy : 0;
					dxy2 = mBlobDirection*dxy2 > 0 ? dxy2 : 0;
					dxz = mBlobDirection*dxz > 0 ? dxz : 0;
					dxz2 = mBlobDirection*dxz2 > 0 ? dxz2 : 0;
					dyz = mBlobDirection*dyz > 0 ? dyz : 0;
					dyz2 = mBlobDirection*dyz2 > 0 ? dyz2 : 0;

					int v = 0;
					if (denomenator > 0)
						v = HFactor * static_cast<int>(sqrt((dxx*dxx + dyy*dyy + dzz*dzz + dxy*dxy + dxy2*dxy2 + dxz*dxz + dxz2*dxz2 + dyz2*dyz2 + dyz*dyz) / denomenator));
					else
						v = 0;
					v = v<=255 ? v : 255;
					*pDest = v;

					if (v > 0)
					{
						S_dest += v;
						n_dest++;
					}
#endif
					pDest++;
					shift++;
				}
			}	
		}
	//	auto maxit = std::max_element(mHessianImg.begin(), mHessianImg.end());
		int maxval = static_cast<int>(S_dest / n_dest*4);
		if (S_dest < EPS || n_dest == 0)
			maxval = 1;
		LogFile::WriteData("kriging.log", " int maxval = ", maxval);
		for (HessianLayer::HessImgIterator pDest = mHessianImg.begin(); pDest != mHessianImg.end(); pDest++)
		{
			int v = static_cast<int>(double((*pDest) * 255 ) / maxval);
			v = v <= 255 ? v : 255;
			*pDest = v;
		}


	}

	void  Stats(double & m, double &s)
	{
		if (mSigma >= 0)
		{
			s = mSigma;
			m = mMean;
			return;
		}
			
		double sum = std::accumulate(this->mHessianImg.begin(), this->mHessianImg.end(), 0.0);
		double mean = sum / this->mHessianImg.size();

		std::vector<double> diff(this->mHessianImg.size());
		std::transform(this->mHessianImg.begin(), this->mHessianImg.end(), diff.begin(), [mean](double x) { return x - mean; });
		double sq_sum = std::inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);
		mSigma = std::sqrt(sq_sum / this->mHessianImg.size());

		int BloabDir = this->BlobDirection();

		mSigma /= HFactor;
		mMean = mean / HFactor;
	}

	void Stats(double & m, double &s)const
	{
		assert(mSigma >= 0);
		s=mSigma;
		m=mMean;
		return;
	}



	void ToGrayScale(std::vector<unsigned char> &Dest)
	{
		assert(1 == 1);
		assert(Dest.size() == this->mWidth*this->mHeight*this->mDepth);

		std::vector<uchar>::iterator pDest = Dest.begin();
		HessianLayer::HessImgIterator pSrc = mHessianImg.begin() + ((3 * Order - 1) / 2)*this->mWidth + ((3 * Order - 1) / 2);

	///	pDest += ((3 * Order - 1) / 2)*this->mWidth + ((3 * Order - 1) / 2);
		int mFiltW_2 = mFiltW / 2;
		for (size_t z = 0; z <this->mDepth; z++)// for pseudo 3D, otherwise z = this->mDepth-mFiltW
		{ 
			pSrc = mHessianImg.begin() + (size_t)this->mWidth*this->mHeight*z + mFiltW_2*this->mWidth;// +mFiltW_2;
			pDest = Dest.begin() + (size_t)this->mWidth*this->mHeight*z + mFiltW_2*this->mWidth;// +mFiltW_2;// ((3 * Order - 1) / 2)*this->mWidth + ((3 * Order - 1) / 2);


			for (size_t y = 0; y < this->mHeight; ++y)
			{
				size_t shift = this->mWidth*this->mHeight*z + y*this->mWidth;
				pSrc = mHessianImg.begin() + shift;
				pDest = Dest.begin() + shift;
				for (size_t x = 0; x < this->mWidth; ++x)
				{
					//if (*pDest == 255)// to avoid owerwriting of already segmented data
						//continue;
					int v = (*pSrc);
					int destval = (unsigned char)(v<255 ? (v>0 ? v : 0) : 255);
					if(*pDest < destval) 
						*pDest=destval;// to avoid overwriting of already segmented data
					pSrc++;
					pDest++;
				}
			//	pDest += mFiltW;
			///	pSrc += mFiltW;

			}
		}

	}

	void Enhancement(container &Dest, int dir, double Gain)
	{
		assert(1 == 1);
		assert(Dest.size() == this->mWidth*this->mHeight*this->mDepth);

		LatticeIterator pDest = Dest.begin();
		HessianLayer::HessImgIterator pSrc = mHessianImg.begin(); 

		for (size_t z = 0; z <this->mDepth; z++)
		{
			for (size_t y = 0; y < this->mHeight; ++y)
			{
				size_t shift = this->mWidth*this->mHeight*z + y*this->mWidth;
				pSrc = mHessianImg.begin() + shift;
				pDest = Dest.begin() + shift;
				for (size_t x = 0; x < this->mWidth; ++x)
				{
					int v = static_cast<int>(dir*(*pSrc)*Gain);
					int destval = *pDest + v;
					destval = destval>255 ? 255 : (destval < 0 ? 0 : destval);
					*pDest = destval;// to avoid overwriting of already segmented data
					pSrc++;
					pDest++;
				}
			}
		}
	}

	void Tresholding(std::vector<unsigned char>&Out, int Thr)
	{
		assert(Out.size() == mHessianImg.size());
		HessianLayer::HessImgIterator it = mHessianImg.begin();
		std::vector<unsigned char>::iterator outit=Out.begin();
		for (; it < mHessianImg.end(); it++, outit++)
			*outit = *it>Thr;
	}
	int Order;
	void SetOrder(int o)
	{
		Order = o;
		mFiltW = Order * 3;
		mIntactFld = (Order - 1) / 2 + 1;
		mIntactFld_xy = (Order - 1) / 2;
		if (Order == 1)
		{
			mIntactFld = 0;
			mIntactFld_xy = 0;
		}
	}
	std::vector<int>  mHessianImg;
	typedef typename std::vector<int>::iterator HessImgIterator;
	int BlobDirection()const{ return mBlobDirection; }
private:
	
	int mWidth;
	int mHeight;
	int mDepth;
	int mFiltW; //=Order*3
	int mIntactFld;
	int mIntactFld_xy;
	int mBlobDirection;
	double mSigma;
	double mMean;
	

	inline int IntegralSum(std::vector<int>::const_iterator pImageData, int w, int h) {
		return *pImageData - *(pImageData+w) - *(pImageData+h*this->mWidth) + *(pImageData+h*this->mWidth + w);
	}

	inline int IntegralSum3D(std::vector<int>::const_iterator pImageData, int w, int h, int d) {
		return pImageData[d*this->mWidth*this->mHeight + h*this->mWidth + w] - pImageData[d*this->mWidth*this->mHeight + h*this->mWidth] - pImageData[h*this->mWidth + w] + pImageData[h*this->mWidth] - pImageData[d*this->mWidth*this->mHeight + w] + pImageData[d*this->mWidth*this->mHeight] + pImageData[w] + pImageData[0];
	}

	inline int ResponseDXX(std::vector<int>::const_iterator pImage) {
		return IntegralSum(pImage + mIntactFld*this->mWidth, mFiltW, mFiltW - 2 * mIntactFld) -
			3 * IntegralSum(pImage + mIntactFld*this->mWidth + Order, Order, mFiltW - 2 * mIntactFld);
	}

	inline int ResponseDXX(const IntegralImage<T, container, 3> &Src,int x,int y, int z) {
		int mFiltW_2 = mFiltW / 2;
		int O_2 = Order / 2;
		int bt = y - mFiltW_2 + mIntactFld; bt = bt > 0 ? bt : 0;
		int tp = y + mFiltW_2 - mIntactFld; tp = tp < (this->mHeight - 1) ? tp : (this->mHeight - 1);
		int lt = x - mFiltW_2; lt = lt>0 ? lt : 0; lt = (lt + Order)>(this->mWidth-1) ? (this->mWidth - Order-1) : lt;
		int rt = x + mFiltW_2+1; rt = rt<(this->mWidth - 1) ? rt : (this->mWidth - 1); rt = (rt - Order)>0 ? rt : Order;
		int ft = z - mFiltW_2 + mIntactFld; ft = ft > 0 ? ft : 0;
		int bk = z + mFiltW_2 - mIntactFld; bk = bk < this->mDepth - 1 ? bk : this->mDepth - 1;
		assert(rt - Order>=0);
		assert(lt + Order <= this->mWidth);
		return Src.BlockSumm( tp, bt,rt, lt, ft, bk) - 3 * Src.BlockSumm(tp,bt,  rt - Order, lt + Order, ft, bk);

	}

	inline int ResponseDYY(std::vector<int>::const_iterator pImage) {
		return IntegralSum(pImage + mIntactFld, mFiltW - 2 * mIntactFld, mFiltW) -
			3 * IntegralSum(pImage + mIntactFld + Order*this->mWidth, mFiltW - 2 * mIntactFld, Order);
	}

	inline int ResponseDYY(const IntegralImage<T, container, 3> &Src, int x, int y, int z) {
		int mFiltW_2 = mFiltW / 2;
		int bt = y - mFiltW_2; bt = bt > 0 ? bt : 0; bt = (bt + Order)>(this->mHeight - 1) ? (this->mHeight - Order - 1) : bt;
		int tp = y + mFiltW_2+1; tp = tp < (this->mHeight - 1) ? tp : (this->mHeight - 1); tp = (tp - Order)>0 ? tp : Order;
		int lt = x - mFiltW_2 + mIntactFld; lt = lt>0 ? lt : 0;
		int rt = x + mFiltW_2 - mIntactFld; rt = rt<(this->mWidth - 1) ? rt : (this->mWidth - 1);
		int ft = z - mFiltW_2 + mIntactFld;	ft = ft > 0 ? ft : 0;
		int bk = z + mFiltW_2 - mIntactFld; bk = bk < this->mDepth - 1 ? bk : this->mDepth - 1;
		

		return Src.BlockSumm( tp,bt, rt, lt, ft, bk) - 3 * Src.BlockSumm( tp-Order,bt+Order, rt, lt, ft, bk);

	}

	inline int ResponseDZZ(const IntegralImage<T, container, 3> &Src, int x, int y, int z) {
		int mFiltW_2 = mFiltW / 2;
		int bt = y - mFiltW_2 + mIntactFld; bt = bt > 0 ? bt : 0;
		int tp = y + mFiltW_2 - mIntactFld; tp = tp < (this->mHeight - 1) ? tp : (this->mHeight - 1);
		int lt = x - mFiltW_2 + mIntactFld; lt = lt>0 ? lt : 0;
		int rt = x + mFiltW_2 - mIntactFld; rt = rt<(this->mWidth - 1) ? rt : (this->mWidth - 1);
		int ft = z - mFiltW_2; ft = ft > 0 ? ft : 0; ft = (ft + Order)>(this->mDepth - 1) ? (this->mDepth - Order - 1) : ft;
		int bk = z + mFiltW_2+1; bk = bk < this->mDepth - 1 ? bk : this->mDepth - 1; bk = (bk - Order)>0 ? bk : Order;

		return Src.BlockSumm( tp, bt,rt, lt, ft, bk) - 3 * Src.BlockSumm(tp, bt, rt, lt, ft + Order, bk - Order);
	}

	inline int ResponseDXY(std::vector<int>::const_iterator pImage) {
		return IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth, Order, Order) -
			IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth + 1 + Order, Order, Order) -
			IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth + Order*this->mWidth + this->mWidth, Order, Order) +
			IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth + Order*this->mWidth + this->mWidth + 1 + Order, Order, Order);
	}


	inline int ResponseDZZ3D(std::vector<int>::const_iterator pImage) {
		return IntegralSum(pImage + mIntactFld*this->mWidth*this->mHeight, mFiltW - 2 * mIntactFld, mFiltW) -
			3 * IntegralSum(pImage + mIntactFld*this->mWidth*this->mHeight, +Order*this->mWidth, mFiltW - 2 * mIntactFld, Order);
	}

	inline Point ResponseDXY(const IntegralImage<T, container, 3> &Src, int x, int y, int z) {
		int mFiltW_2 = mFiltW / 2;
		int O_2 = Order / 2;
		int bt = y - mFiltW_2; bt = bt > 0 ? bt : 0;
		int tp = y + mFiltW_2 +1 ; tp = tp < (this->mHeight - 1) ? tp : (this->mHeight - 1);
		int lt = x - mFiltW_2; lt = lt>0 ? lt : 0; lt = (lt + Order)>(this->mWidth - 1) ? (this->mWidth - Order - 1) : lt;
		int rt = x + mFiltW_2 + 1; rt = rt<(this->mWidth - 1) ? rt : (this->mWidth - 1); rt = (rt - Order)>0 ? rt : Order;
		int ft = z - mFiltW_2 + mIntactFld_xy; ft = ft > 0 ? ft : 0;
		int bk = z + mFiltW_2 +1- mIntactFld_xy; bk = bk < this->mDepth - 1 ? bk : this->mDepth - 1;
		assert(rt - Order >= 0);
		assert(lt + Order <= this->mWidth);
		SimplePoint3d a1, b1, a2, b2, a3, b3, a4, b4; 
		a1.x = lt + mIntactFld_xy;
		a1.y = bt + mIntactFld_xy;
		b1.x = lt + Order + mIntactFld_xy;
		b1.y = bt + mIntactFld_xy + Order;

		a2.x = a1.x + mIntactFld_xy + Order;
		a2.y = a1.y;
		b2.x = b1.x + Order + mIntactFld_xy;
		b2.y = b1.y;

		a3.x = a1.x;
		a3.y = a1.y + mIntactFld_xy + Order;
		b3.x = b1.x;
		b3.y = b1.y + mIntactFld_xy + Order;
		
		a4.x = a1.x + mIntactFld_xy + Order;
		a4.y = a1.y + mIntactFld_xy + Order;
		b4.x = b1.x + mIntactFld_xy + Order;
		b4.y = b1.y + mIntactFld_xy + Order;

		int xy= -Src.BlockSumm(b1.y,  a1.y, b1.x, a1.x, ft, bk) + 
			Src.BlockSumm(b2.y,a2.y,  b2.x, a2.x, ft, bk) +
			Src.BlockSumm(b3.y,a3.y,  b3.x, a3.x, ft, bk) -
			Src.BlockSumm(b4.y,a4.y,  b4.x, a4.x, ft, bk);
		int yx = Src.BlockSumm(b1.y,  a1.y,  b1.x, a1.x, ft, bk) -
			Src.BlockSumm(b2.y,a2.y,  b2.x, a2.x, ft, bk) -
			Src.BlockSumm(b3.y,a3.y,  b3.x, a3.x, ft, bk) +
			Src.BlockSumm(b4.y,a4.y,  b4.x, a4.x, ft, bk);

		Point pt(xy, yx);
			return pt;
	}


	inline Point ResponseDYZ(const IntegralImage<T, container, 3> &Src, int x, int y, int z) {
		int mFiltW_2 = mFiltW / 2;
		int O_2 = Order / 2;
		int bt = y - mFiltW_2; bt = bt > 0 ? bt : 0;
		int tp = y + mFiltW_2 + 1; tp = tp < (this->mHeight - 1) ? tp : (this->mHeight - 1);
		int lt = x - mFiltW_2; lt = lt>0 ? lt : 0; lt = (lt + Order)>(this->mWidth - 1) ? (this->mWidth - Order - 1) : lt;
		int rt = x + mFiltW_2 + 1; rt = rt<(this->mWidth - 1) ? rt : (this->mWidth - 1); rt = (rt - Order)>0 ? rt : Order;
		int ft = z - mFiltW_2 + mIntactFld_xy; ft = ft > 0 ? ft : 0;
		int bk = z + mFiltW_2 + 1 - mIntactFld_xy; bk = bk < this->mDepth - 1 ? bk : this->mDepth - 1;
		assert(rt - Order >= 0);
		assert(lt + Order <= this->mWidth);

		SimplePoint3d a1, b1, a2, b2, a3, b3, a4, b4;

		a1.y = bt + mIntactFld_xy;
		a1.z = ft + mIntactFld_xy;
		b1.y = bt + Order + mIntactFld_xy;
		b1.z = ft + mIntactFld_xy + Order;

		a2.y = a1.y + mIntactFld_xy + Order;
		a2.z = a1.z;
		b2.y = b1.y + Order + mIntactFld_xy;
		b2.z = b1.z;

		a3.y = a1.y;
		a3.z = a1.z + mIntactFld_xy + Order;
		b3.y = b1.y;
		b3.z = b1.z + mIntactFld_xy + Order;

		a4.y = a1.y + mIntactFld_xy + Order;
		a4.z = a1.z + mIntactFld_xy + Order;
		b4.y = b1.y + mIntactFld_xy + Order;
		b4.z = b1.z + mIntactFld_xy + Order;


		int yz = -Src.BlockSumm(b1.y,a1.y, rt, lt,  a1.z, b1.z) +
			Src.BlockSumm(b2.y,a2.y,  rt, lt, a2.z, b2.z) +
			Src.BlockSumm(b3.y,a3.y,  rt, lt, a3.z, b3.z) -
			Src.BlockSumm(b4.y,a4.y,  rt, lt, a4.z, b4.z);
		int zy = Src.BlockSumm(b1.y, a1.y, rt, lt, a1.z, b1.z) -
			Src.BlockSumm(b2.y,a2.y,  rt, lt, a2.z, b2.z) -
			Src.BlockSumm(b3.y,a3.y,  rt, lt, a3.z, b3.z) +
			Src.BlockSumm(b4.y,a4.y,  rt, lt, a4.z, b4.z);

		Point pt(yz, zy);
		return pt;
	}

	inline Point ResponseDXZ(const IntegralImage<T, container, 3> &Src, int x, int y, int z) {
		int mFiltW_2 = mFiltW / 2;
		int O_2 = Order / 2;
		int bt = y - mFiltW_2; bt = bt > 0 ? bt : 0;
		int tp = y + mFiltW_2 + 1; tp = tp < (this->mHeight - 1) ? tp : (this->mHeight - 1);
		int lt = x - mFiltW_2; lt = lt>0 ? lt : 0; lt = (lt + Order)>(this->mWidth - 1) ? (this->mWidth - Order - 1) : lt;
		int rt = x + mFiltW_2 + 1; rt = rt<(this->mWidth - 1) ? rt : (this->mWidth - 1); rt = (rt - Order)>0 ? rt : Order;
		int ft = z - mFiltW_2 + mIntactFld_xy; ft = ft > 0 ? ft : 0;
		int bk = z + mFiltW_2 + 1 - mIntactFld_xy; bk = bk < this->mDepth - 1 ? bk : this->mDepth - 1;
		assert(rt - Order >= 0);
		assert(lt + Order <= this->mWidth);

		SimplePoint3d a1, b1, a2, b2, a3, b3, a4, b4;

		a1.x = lt + mIntactFld_xy;
		a1.z = ft + mIntactFld_xy;
		b1.x = lt + Order + mIntactFld_xy;
		b1.z = ft + mIntactFld_xy + Order;

		a2.x = a1.x + mIntactFld_xy + Order;
		a2.z = a1.z;
		b2.x = b1.x + Order + mIntactFld_xy;
		b2.z = b1.z;

		a3.x = a1.x;
		a3.z = a1.z + mIntactFld_xy + Order;
		b3.x = b1.x;
		b3.z = b1.z + mIntactFld_xy + Order;

		a4.x = a1.x + mIntactFld_xy + Order;
		a4.z = a1.z + mIntactFld_xy + Order;
		b4.x = b1.x + mIntactFld_xy + Order;
		b4.z = b1.z + mIntactFld_xy + Order;


		int xz = -Src.BlockSumm(tp, bt,  b1.x, a1.x,  a1.z, b1.z) +
			Src.BlockSumm(tp,bt,  b2.x, a2.x, a2.z, b2.z) +
			Src.BlockSumm(tp,bt,  b3.x, a3.x, a3.z, b3.z) -
 			Src.BlockSumm(tp,bt,  b4.x, a4.x, a4.z, b4.z);
		int zx = Src.BlockSumm(tp,bt,  b1.x, a1.x, a1.z, b1.z) -
			Src.BlockSumm(tp,bt,  b2.x, a2.x, a2.z, b2.z) -
			Src.BlockSumm(tp,bt,  b3.x, a3.x, a3.z, b3.z) +
			Src.BlockSumm(tp,bt,  b4.x, a4.x, a4.z, b4.z);

		Point pt(xz, zx);
		return pt;
	}





	inline int ResponseDXY2(std::vector<int>::const_iterator pImage) {
		return -IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth, Order, Order) +
			IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth + 1 + Order, Order, Order) +
			IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth + Order*this->mWidth + this->mWidth, Order, Order) -
			IntegralSum(pImage + mIntactFld_xy + mIntactFld_xy*this->mWidth + Order*this->mWidth + this->mWidth + 1 + Order, Order, Order);
	}

	inline bool NonMaxTest(std::vector<int>::const_iterator pImageData)
	{
		int  v = *pImageData;
		return (v>pImageData[1]) && (v>pImageData[-1]) && (v>pImageData[+this->mWidth]) && (v>pImageData[-this->mWidth]) &&
			(v>pImageData[-this->mWidth + 1]) && (v>pImageData[-this->mWidth - 1]) && (v>pImageData[+this->mWidth - 1]) && (v>pImageData[+this->mWidth + 1]);
	}
};

class HessianSegmentation
{
public:
	HessianSegmentation(){};
	~HessianSegmentation(){};
	void Perform(const DynamicArray<unsigned char> &img, DynamicArray<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D);
	void PerformGrayscale(const DynamicArray<unsigned char> &img, DynamicArray<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D);
private:
	int mWidth;
	int mHeight;
	int mDepth;
};

class HessianEnhancement
{
public:
	HessianEnhancement(){};
	~HessianEnhancement(){};
	void Perform(const std::vector<unsigned char> &img, std::vector<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D);
	//void PerformGrayscale(const array<unsigned char> &img, array<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D);
private:
	int mWidth;
	int mHeight;
	int mDepth;
};

struct HWSSettings
{
	HWSSettings() :nLabels(2), FreezingSpeed(0.98), TStart(4.0), nSteps(3), Radius(5), HessianOrder(3), Strength(20)
	{};
	int nLabels;
	int Radius;
	int nPhases;
	int nSteps;
	int Strength;
	double TStart;
	double FreezingSpeed;
	int HessianOrder;
};


template <class T = int, class container_type = std::vector<T>, int nDim = 2>
class HessianWindowedSegmantation : public LatticeModel
{
public:
	HessianWindowedSegmantation(int nLabels) :
		LatticeModel(nLabels)
	{
		//mean = new double[this->mLabels];
		//var = new double[this->mLabels];
		mBeta = 0.9;
		mDeltaT = 0.9;
		mT0 = 4;
		mEnergyThresh = 0.01;

	};

	HessianWindowedSegmantation(const HWSSettings &pref) :
		LatticeModel(pref.nLabels), mT0(pref.TStart), mDeltaT(pref.FreezingSpeed)
	{
		//mean = new double[this->mLabels];
		//	var = new double[this->mLabels];
		mEnergyThresh = 0.01;
	}
	~HessianWindowedSegmantation()
	{
		//	delete[] mean;
		//	delete[] var;
	};

	using LatticeIterator = typename container_type::iterator ;
	using LatticeConstIterator = typename container_type::const_iterator;

	void SimulatedAnnealing(const container_type  &img, container_type &Conditional)
	{
		int i, j;
		int r;
		double summa_deltaE;

		double _T = mT0;
		mIterCount = 0;
		do
		{
			summa_deltaE = 0.0;
			LatticeIterator cit = Conditional.begin();// +this->mWidth + 1;
			LatticeConstIterator it = img.begin();// +this->mWidth + 1;

			for (int i = 1; i < this->mHeight - 1; i++)
			{
				for (int j = 1; j < this->mWidth - 1; j++)
				{
					int shift_it = i*this->mWidth + j;
					it = img.begin() + shift_it;
					cit = Conditional.begin() + shift_it;

					if (this->mLabels == 2)
						r = 1 - *cit;
					else
						r = (*cit + (int)(random_numbers::rnd()*(this->mLabels - 1)) + 1) % this->mLabels;
					double n = random_numbers::rnd();
					double delta_E = (Energy(it, cit, *cit) - Energy(it, cit, r));
					if (n <= delta_E / _T)
					{
						summa_deltaE += fabs(delta_E);
						*cit = r;
					}

				}

			}
			_T *= mDeltaT;
			++mIterCount;
		} while (summa_deltaE / (this->mWidth - 2) / (this->mHeight - 2) > mEnergyThresh  && _T > EPS_THINY);
	}

	void SimulatedAnnealing3D(const container_type &img, const container_type &AdjImg, container_type &Conditional)
	{
		int i, j;
		int r;
		double summa_deltaE;

		double _T = mT0;
		mIterCount = 0;
		LogFile::WriteData("kriging.log", "SA statrted");
		do
		{
			summa_deltaE = 0.0;
			LatticeIterator cit = Conditional.begin();// +this->mWidth + 1;
			LatticeConstIterator it = img.begin();// +this->mWidth + 1;
			LatticeConstIterator Hit = AdjImg.begin();// +this->mWidth + 1;

			for (size_t k = 0; k < this->mDepth; k++)
			{
				for (size_t i = 0; i < this->mHeight; i++)
				{
					for (size_t j = 0; j < this->mWidth; j++)
					{
						size_t shift_it = k*this->mWidth*this->mHeight + i*this->mWidth + j;
						it = img.begin() + shift_it;
						cit = Conditional.begin() + shift_it;
						Hit = AdjImg.begin() + shift_it;
						if (this->mLabels == 2)
							r = 1 - *cit;
						else
							r = (*cit + (int)(random_numbers::rnd()*(this->mLabels - 1)) + 1) % this->mLabels;
						double n = random_numbers::rnd();
						double delta_E = (Energy(it, Hit, *cit) - Energy(it, Hit, r));
						if (n <= delta_E / _T)
						{
							summa_deltaE += fabs(delta_E);
							*cit = r;
						}
					}
				}
			}
			_T *= mDeltaT;
			++mIterCount;
			LogFile::WriteData("kriging.log", "Sum of Delta E: ", summa_deltaE);
		} while (summa_deltaE / (this->mWidth) / (this->mHeight) / (this->mDepth) > mEnergyThresh && _T > EPS_THINY);
		LogFile::WriteData("kriging.log", "SA finished ");
	};

	void PerformAdjustment(const container_type &img, container_type &Conditional, Threshold<T, container_type>  &Thresh, int W, int H, int D, 
		HessianSettings& hessianSettings, HWSSettings& hwsSettings)
	{
		LogFile::WriteData("kriging.log", "PerformAdjustment ");
	
		IntegralImage<unsigned char, container_type, 3> II(img, W, H, D);
		//HessianSettings HS; HS.Order = ProjectProfile::HWS().HessianOrder;
		HessianLayer<unsigned char, container_type, 3> HL(II, hessianSettings);
		HL.Perform(II);
		double m, s;
		HL.Stats(m,s);

		this->mWidth = W;
		this->mHeight = H;
		this->mDepth = D;

		Adjustment(II, img, Conditional, HL, hwsSettings);
	}

	void Perform(const container_type &img, container_type &Conditional, container_type &WImg, Threshold<T, container_type> &Thresh, container_type &hssImg, int W, int H, int D,
		HessianSettings& hessianSettings, HWSSettings& hwsSettings)
	{
		LogFile::WriteData("kriging.log", "Thresh method ", Thresh.Method);
		if (Thresh.Method != Th_Manual)
		{
			container_type I(W*H);
			std::copy<LatticeConstIterator, typename container_type::iterator>(img.begin(), img.begin() + W*H, I.begin());
			Thresh.compute_cut_offs(I, W, H, 1);
		}

		IntegralImage<unsigned char, container_type, 3> II(img, W, H, D);
		HessianSettings HS = hessianSettings; 
		HS.Order = hwsSettings.HessianOrder;
		HessianLayer<unsigned char, container_type, 3> HL(II, HS);
		LogFile::WriteData("kriging.log", "HL.Perform(II);	");
		double m, s;
		HL.Perform(II);	
		hssImg.resize((size_t)W*H*D);
		std::copy(HL.mHessianImg.begin(), HL.mHessianImg.end(), hssImg.begin());
		HL.Stats(m, s);

		this->mWidth = W;
		this->mHeight = H;
		
		this->mDepth = D;

		
		
		WImg.resize((size_t)W*H*D);
		LogFile::WriteData("kriging.log", "Adjustment(II, img, WImg, HL, ProjectProfile::HWS());");
		this->Adjustment(II, img, WImg, HL, hwsSettings);

		LogFile::WriteData("kriging.log", "HBFSTat2L");



		//if (Thresh.PhasesCount() == 2)
		//{
			this->Stats2L(img, Thresh.High(), Thresh.Low(), this->means[0], this->means[1], this->vars[0], this->vars[1]);
			this->ConditionalImage2Labels(WImg, Conditional, Thresh);
			//Segment2Labels(WImg, Conditional, Thresh, HL);
		//}
		//else
		//{
		//	StatsNL(img, Thresh.HighThresholds(), Thresh.LowThresholds(), this->means, this->vars);
		//	ConditionalImage(WImg, Conditional, Thresh);
		//}

		LogFile::WriteData("kriging.log", "Stats calculated");

		/*if (this->mDepth > 1)
			SimulatedAnnealing3D(img, WImg, Conditional);
		else
			SimulatedAnnealing(img, Conditional);*/

		LogFile::WriteData("kriging.log", "Conditional filled");
	
	}
private:
	//	double* var;
	//	double* mean;
	double mBeta;
	double	mDeltaT;
	double mT0;
	int mIterCount;
	double mEnergyThresh;
	double Energy(LatticeConstIterator it, LatticeConstIterator Hit, int label)
	{
		double v = *Hit;
		return (CellOwnEnergy(it, label) +CellOwnEnergy(Hit, label))/2;
	};


	double CellOwnEnergy(LatticeConstIterator it, int label)
	{
		double v = log(sqrt(2.0*M_PI*this->vars[label])) + pow(*it - this->means[label], 2) / (2.0*this->vars[label]);
		return v;
	}

	void Adjustment(const IntegralImage<unsigned char, container_type, 3> &II, const container_type &img,
		container_type &Out, const HessianLayer<unsigned char, container_type, 3> &HL, HWSSettings &Settings)
	{
		int nSteps = Settings.nSteps;
		int Radius = Settings.Radius;
		int Strength = Settings.Strength;
		double Wmean = (double)Radius / nSteps;
		int *steps = new int[nSteps];
		double *weights = new double[nSteps];
		int Dist = 0; int x = 0;
		LogFile::WriteData("kriging.log", "Adjustment start");

		for (int i = 0; i < nSteps; i++)
		{
			x = static_cast<int>(round((i + 1)*0.5*Wmean));
			Dist += x;
			steps[i] = Dist;
			
		}
		if (Dist>Radius)
			steps[nSteps - 1] = Radius;
		LatticeIterator OutIt = Out.begin();
		auto HIt = HL.mHessianImg.begin();

		


	/*	double sum = std::accumulate(HL.mHessianImg.begin(), HL.mHessianImg.end(), 0.0);
		double mean = sum / HL.mHessianImg.size();

		std::vector<double> diff(HL.mHessianImg.size());
		std::transform(HL.mHessianImg.begin(), HL.mHessianImg.end(), diff.begin(), [mean](double x) { return x - mean; });
		double sq_sum = std::inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);
		double Sigma = std::sqrt(sq_sum / HL.mHessianImg.size());

		int BloabDir = HL.BlobDirection();
	
		Sigma /= 100;*/
		double mean;
		double Sigma;
		HL.Stats(mean, Sigma);

		int hcount = 0;
		for (int k = 0; k < this->mDepth; k++)
		{
			for (int j = 0; j < this->mHeight; j++)
			{
				for (int i = 0; i < this->mWidth; i++)
				{
					double v = 0;
					double H = double(*HIt)/HFactor;
					double sumW=0;
					if (k == 4 && j == 115 && i == 51)
						int sdsd = 7;
					int bs = 0;
					int bsize = 0;
					for (int q = 0; q < nSteps; q++)
					{
						int w = steps[q];
						double d = double(q + 1);// / nSteps;
						weights[q] = H>(0+EPS)?( exp(-H / Sigma * d*d)):1;// (double)q / nSteps);
						sumW += weights[q];
						//int wx, wy, wz;
						int bt = j + w; bt = bt < (int)this->mHeight ? bt : (int)this->mHeight - 1;
						int tp = j - w + 1; tp = tp>0 ? tp : 0;
						tp = tp<bt ? tp : bt - 1;
						tp = tp>0 ? tp : 0;

						int lt = i - w + 1; lt = lt>0 ? lt : 0;
						int rt = i + w;  rt = rt < (int)this->mWidth ? rt : (int)this->mWidth - 1;
						lt = lt<rt ? lt : rt - 1;
						lt = lt>0 ? lt : 0;

						int ft = k - w+1; ft = ft > 0 ? ft : 0;
						int bk = k + w; bk = bk < (int)this->mDepth ? bk : (int)this->mDepth - 1;
						ft = ft<bk ? ft : bk - 1;
						ft = ft > 0 ? ft : 0;

						int dx = (rt - lt);  dx = lt>0 ? dx : dx + 1;  dx = dx>0 ? dx : 1;   
						int dy = (bt - tp);  dy = tp>0 ? dy : dy + 1;  dy = dy > 0 ? dy : 1;
						int dz = (bk - ft);  dz = ft>0 ? dz : dz + 1;  dz = dz > 0 ? dz : 1;
						int bsize2 = dy * dx * dz ;

						int bs2 = II.BlockSumm(bt, tp, rt, lt, ft, bk);
						int dbs = (bsize2 - bsize);
						dbs = dbs > 0 ? dbs : 1;
						v += weights[q] * (bs2 - bs) / (dbs);
						bs = bs2;
						bsize = bsize2;

					}
					v = v/sumW;
					double delta = Strength * (H - mean) / Sigma;
					if (delta > 0)
						v = v - delta;
					if(v < 0)
						v = 0;
					*OutIt = static_cast<int>(v);
					OutIt++;
					HIt++;
				}
			}
		}
		delete[] steps;
		delete[] weights;
		LogFile::WriteData("kriging.log", "Adjustment finish");
	}

	void ConditionalImage(const container_type &I, container_type &C, Threshold<T> &thresh)
	{
		LatticeIterator cit = C.begin();
		std::vector<double> L = thresh.LowThresholds();
		std::vector<double> H = thresh.HighThresholds();
		for (auto it = I.begin(); it != I.end(); ++it, ++cit)
		{
			*cit = this->mLabels;

			auto v = *it;
			for (int i = 0; i < this->mLabels; i++)
			{
				if ((v > L[i]) && (v < H[i]))
				{
					*cit = i;
					continue;
				}
			}
			if (*cit == this->mLabels)
				*cit = SelectPhase(*cit);
		}
	}

	void ConditionalImage2Labels(const container_type &I, container_type &C, Threshold<T> &thresh)
	{
		LatticeConstIterator it = I.begin();
		int L = thresh.Low();
		int H = thresh.High();

		for (auto cit = C.begin(); cit<C.end(); cit++, it++)
		{
			if (*it>thresh.High())
				*cit = 1;
			else if (*it <= thresh.Low())
				*cit = 0;
			else if (abs(*it - L) / this->vars[0] < abs(*it - H) / this->vars[1])
				*cit = 0;
			else
				*cit = 1;
		};
	}

	void Segment2Labels(const container_type &I, container_type &C, Threshold<T> &thresh, const HessianLayer<unsigned char, container_type, 3> &HL)
	{
		LatticeConstIterator it = I.begin();
		
		double Sigma, m;
		HL.Stats(m, Sigma);
		for (auto cit = C.begin(); cit<C.end(); cit++, it++)
		{
			if (*it>thresh.High())
				*cit = 1;
			else if (*it <= thresh.Low())
				*cit = 0;
			else 
				*cit = 2;
		};

		
		int nbh[2];
		auto cit = C.begin();
		auto HIt = HL.mHessianImg.begin();
		it = I.begin();
		for (int K = 0; K < this->mDepth; K++)
		{
			for (int i = 0; i < this->mHeight; i++)
			{
				for (int J = 0; J < this->mWidth; J++)
				{
					if (J == 118 && i == 64 && K == 27)
						int gfgfg = 56;
					if (*cit != 2)
					{
						cit++;
						HIt++;
						continue;
					}
					for (int l = 0; l < 2; l++)//!!! must be "==i" rather then "!=i"
						nbh[l] = ((i<this->mHeight - 1 && *BotNB(cit) == l) + (i>0 && *TopNB(cit) == l) + (J>0 && *LeftNB(cit) == l) +
						(J < this->mWidth - 1 && * RightNB(cit) == l) + (K<this->mDepth - 1 && *BhdNB(cit) == l) + (K>0 && *FrntNB(cit) == l));
						
					int Snbh = nbh[1] - nbh[0];
					int h = *HIt;
					double Shss = (double )h  / Sigma;
					int 	ii = *it;
					double S = Shss - Snbh +(abs(*it - this->means[0]) / this->vars[0] < abs(*it - this->means[1]) / this->vars[1]);

					if (S>0)
						*cit = 0;
					else
						*cit = 1;
					cit++;
					HIt++;
					it++;
				}
			}
		}/**/
	}

};

#endif
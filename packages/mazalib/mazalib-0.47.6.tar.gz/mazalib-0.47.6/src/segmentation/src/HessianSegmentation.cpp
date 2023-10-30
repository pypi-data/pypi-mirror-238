#include "HessianSegmentation.h"

void HessianSegmentation::Perform(const DynamicArray<unsigned char> &img, DynamicArray<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D)
{
	mWidth = W;
	mHeight = H;
	mDepth = D;
	IntegralImage<unsigned char, std::vector<unsigned char>, 3> Integeral(img, W, H, D);
	HessianLayer<unsigned char, std::vector<unsigned char>,3> mHessian(Integeral, Hss);

	if (Hss.UseScales)
	{
		for (int i = Hss.nScales; i > 0; i--)
		{
			int o = static_cast<int>(3.0 * pow(1.5, i));
			int Order = o % 2 == 0 ? o + 1 : o;
			mHessian.SetOrder(Order);
			mHessian.Perform(Integeral);
			mHessian.ToGrayScale(Conditional);
		}
	}
	else
	{
		mHessian.Perform(Integeral);
		mHessian.ToGrayScale(Conditional);
	}
	Threshold<uchar> T;
	ThresholdSettings ts;
	T.Setup(ts);
	double t1, t2;
	if (Hss.IsAuto)
		T.Schluter(Conditional, W, H, D, t1, t2);// (.HessianCutOff(Conditional, W, H, D, Hss.Threshold);
	Hss.Threshold = static_cast<int>(t1);
	mHessian.Tresholding(Conditional, Hss.Threshold);

	//double f = 255.0;
	for (auto cit = Conditional.begin(); cit != Conditional.end(); cit++)
		*cit *= 255; // *cit *= f;
	
}

void HessianEnhancement::Perform(const std::vector<unsigned char> &img, std::vector<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D)
{
	mWidth = W;
	mHeight = H;
	mDepth = D;
	IntegralImage<unsigned char, std::vector<unsigned char>, 3> Integeral(img, W, H, D);
	HessianLayer<unsigned char, std::vector<unsigned char>, 3> mHessian(Integeral, Hss);
	std::copy(img.begin(), img.end(), Conditional.begin());
	mHessian.SetDirection(1);
	mHessian.Perform(Integeral);
	mHessian.Enhancement(Conditional,-1,Hss.Gain);

/*	mHessian.SetDirection(-1);
	mHessian.Perform(Integeral);
	mHessian.ToGrayScale(Conditional);*/
	

}

void HessianSegmentation::PerformGrayscale(const DynamicArray<unsigned char> &img, DynamicArray<unsigned char> &Conditional, HessianSettings &Hss, int W, int H, int D)
{
	IntegralImage<unsigned char, std::vector<unsigned char>, 3> Integeral(img, W, H, D);
	HessianLayer<unsigned char, std::vector<unsigned char>, 3> mHessian(Integeral, Hss);
	if (Hss.UseScales)
	{
		for (int i = Hss.nScales; i > 0; i--)
		{
			int o = static_cast<int>(3 * pow(1.5, i));
			int Order = o % 2 == 0 ? o + 1 : o;
			mHessian.SetOrder(Order);
			mHessian.Perform(Integeral);
			mHessian.ToGrayScale(Conditional);
		}
	}
	else
	{
		mHessian.Perform(Integeral);
		mHessian.ToGrayScale(Conditional);
	}
}

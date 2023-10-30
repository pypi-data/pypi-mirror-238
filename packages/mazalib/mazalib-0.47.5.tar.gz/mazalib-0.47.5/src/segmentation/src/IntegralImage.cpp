#include "IntegralImage.h"


/*ostream& operator<<(ostream &out, const IntegralImage<class T, int nDim> &Img){
	int W = Img.Width();
	const int *p = Img.Pointer();
	for (int i = 0; i<W; i++)
	{
		for (int j = 0; j<Img.Height(); ++j)
			out << p[i*W + j] << " ";
		out << "\n";
	}
	return out;
}

istream &GrayscaleImage::operator >>(istream &in)
{
	in >> mWidth;
	in >> mHeight;
	Data.resize(mWidth, mHeight);
	unsigned char *pData = Pointer();//new unsigned char [mWidth*mHeight];
	for (int i = 0; !in.eof(); ++i)
	{
		int x;
		in >> x;
		pData[i] = x;
	};
	return in;
}

ostream& operator<<(ostream &out, const GrayscaleImage &Img){
	int W = Img.Width();
	const unsigned char *p = Img.Pointer();
	for (int i = 0; i<W; i++)
	{
		for (int j = 0; j<Img.Height(); ++j)
			out << p[i*W + j] << " ";
		out << "\n";
	}
	return out;
}*/

#include "MRFSegmentation.h"
/*
struct Point3D
{
	int x, y, z;
};

double MRF::rnd()
{
	static int s1 = 10000;
	static int s2 = 15000;
	int k = s1 / 53668;
	double Z;
	s1 = 40014 * (s1 - k * 53668) - k * 12211;
	if (s1<0)
		s1 = s1 + 2147483563;
	k = s2 / 52774;
	s2 = 40692 * (s2 - k * 52774) - k * 3791;
	if (s2<0)
		s2 = s2 + 2147483399;
	Z = s1 - s2;
	if (Z<1)
		Z += 2147483562;
	Z = Z*4.656613e-10;
	return Z;
}

MRF::MRF(int nLlabels) :mLabels(nLlabels)
{
	mean = new double[mLabels];
	var = new double[mLabels];
	mBeta = 0.9;
	mDeltaT = 0.9;
	mT0 = 4;
	mEnergyThresh = 0.01;

};

MRF::MRF(const MRFSettings &pref) :mLabels(pref.nLlabels), mBeta(pref.Beta), mT0(pref.TStart), mDeltaT(pref.FreezingSpeed), Method(pref.Method)
{
	mean = new double[mLabels];
	var = new double[mLabels];
	mEnergyThresh = 0.01;
}

MRF::~MRF()
{
	delete [] mean;
	delete[] var;
};


inline array<unsigned char>::iterator MRF::RightNB(array<unsigned char>::iterator it)
{
	return it + 1;
}

inline array<unsigned char>::iterator MRF::LeftNB(array<unsigned char>::iterator it)
{
	return it - 1;
}

inline array<unsigned char>::iterator MRF::TopNB(array<unsigned char>::iterator it)
{
	return it - mWidth;

}
inline array<unsigned char>::iterator MRF::BotNB(array<unsigned char>::iterator it)
{
	return it + mWidth;
}

inline array<unsigned char>::iterator MRF::BhdNB(array<unsigned char>::iterator it)
{
	return it + mWidth*mHeight;
}

inline array<unsigned char>::iterator MRF::BfrNB(array<unsigned char>::iterator it)
{
	return it - mWidth*mHeight;
}

inline array<unsigned char>::const_iterator MRF::RightNB(array<unsigned char>::const_iterator it)
{
	return it + 1;
}

inline array<unsigned char>::const_iterator MRF::LeftNB(array<unsigned char>::const_iterator it)
{
	return it - 1;
}

inline array<unsigned char>::const_iterator MRF::TopNB(array<unsigned char>::const_iterator it)
{
	return it - mWidth;

}
inline array<unsigned char>::const_iterator MRF::BotNB(array<unsigned char>::const_iterator it)
{
	return it + mWidth;
}

inline array<unsigned char>::const_iterator MRF::BhdNB(array<unsigned char>::const_iterator it)
{
	return it + mWidth*mHeight;
}

inline array<unsigned char>::const_iterator MRF::BfrNB(array<unsigned char>::const_iterator it)
{
	return it - mWidth*mHeight;
}

double MRF::Energy(array<unsigned char>::const_iterator it, array<unsigned char>::iterator cit, int label)
{
	//double NbSum = 0;
	//*BotNB(cit) == label ? NbSum++ : NbSum--;
	//*TopNB(cit) == label ? NbSum++ : NbSum--;
	//*RightNB(cit) == label ? NbSum++ : NbSum--;
	//*LeftNB(cit) == label ? NbSum++ : NbSum--;

	//double v = CellOwnEnergy(it, label) + mBeta*NbSum;
	return CellOwnEnergy(it, label) + mBeta*((*LeftNB(cit) == label + *RightNB(cit) == label + *TopNB(cit) == label + *BotNB(cit) == label) * 2 - 4);
};

double MRF::Energy3D(array<unsigned char>::const_iterator it, array<unsigned char>::iterator cit, int label)
{
	return CellOwnEnergy(it, label) + mBeta*((*LeftNB(cit) == label + *RightNB(cit) == label + *TopNB(cit) == label + *BotNB(cit) == label + *BfrNB(cit) == label + *BhdNB(cit) == label) * 2 - 6);
};

double MRF::Energy3DTop(array<unsigned char>::const_iterator it, array<unsigned char>::iterator cit, int label)
{
	return CellOwnEnergy(it, label) + mBeta*((*LeftNB(cit) == label + *RightNB(cit) == label + *TopNB(cit) == label + *BotNB(cit) == label + *BhdNB(cit) == label) * 2 - 5);
};

double MRF::Energy3DBot(array<unsigned char>::const_iterator it, array<unsigned char>::iterator cit, int label)
{
	return CellOwnEnergy(it, label) + mBeta*((*LeftNB(cit) == label + *RightNB(cit) == label + *TopNB(cit) == label + *BotNB(cit) == label + *BfrNB(cit) == label) * 2 - 5);
};

double MRF::CellOwnEnergy(array<unsigned char>::const_iterator it, int label)
{
	return log(sqrt(2.0*M_PI*var[label])) + pow(*it - mean[label], 2) / (2.0*var[label]);
}

void MRF::ConditionalImage(const array<unsigned char> &I, array<unsigned char> &C)
{
	array<unsigned char>::iterator cit = C.begin();
	for (auto it = I.begin(); it != I.end(); ++it,++cit)
	{
		double d = fabs(*it - mean[0]);
		*cit = 0;
		for (int i = 1; i < mLabels; i++)
		{
			double d1 = fabs(*it - mean[i]);
			if (d1 < d)
			{
				*cit = i;
				d = d1;
			}
		}
	}
}

void MRF::SimulatedAnnealing(const array<unsigned char> &img, array<unsigned char> &Conditional)
{
	int i, j;
	int r;
	double summa_deltaE;

	double T = mT0;
	mIterCount = 0;
	do
	{
		summa_deltaE = 0.0;
		array<unsigned char>::iterator cit = Conditional.begin();// +mWidth + 1;
		array<unsigned char>::const_iterator it = img.begin();// +mWidth + 1;

		for (int i = 1; i < mHeight - 1; i++)
		{
			for (int j = 1; j < mWidth - 1; j++)
			{
				int shift_it =i*mWidth + j;
				it =img.begin()+ shift_it;
				cit = Conditional.begin()+ shift_it;

				if (mLabels == 2)
					r = 1 - *cit;
				else
					r = (*cit + (int)(rnd()*(mLabels - 1)) + 1) % mLabels;
				double n = rnd();
				double delta_E = (Energy(it, cit, *cit) - Energy(it, cit, r));
				if (n <= delta_E / T)
				{
					summa_deltaE += fabs(delta_E);
					*cit = r;
				}
	
			}
		
		}
		T *= mDeltaT;       
		++mIterCount;	      
	} while (summa_deltaE > mEnergyThresh); 
}

void MRF::SimulatedAnnealing3D(const array<unsigned char> &img, array<unsigned char> &Conditional)
{
	int i, j;
	int r;
	double summa_deltaE;

	double T = mT0;
	mIterCount = 0;
	LogFile::WriteData("kriging.log", "SA statrted");
	do
	{
		summa_deltaE = 0.0;
		array<unsigned char>::iterator cit = Conditional.begin();// +mWidth + 1;
		array<unsigned char>::const_iterator it = img.begin();// +mWidth + 1;
		typedef double(MRF::*pEnergy)(array<unsigned char>::const_iterator it, array<unsigned char>::iterator cit, int label);

		for (int k = 0; k < mDepth; k++)
		{
			pEnergy pE = &MRF::Energy3D;
			if (mDepth == 1)
				pE = &MRF::Energy;
			else if (k==0)
			  pE = &MRF::Energy3DTop;
			else if (k == mDepth-1)
			  pE = &MRF::Energy3DBot;

			for (int i = 1; i < mHeight - 1; i++)
			{
				for (int j = 1; j < mWidth - 1; j++)
				{
					int shift_it = k*mWidth*mHeight + i*mWidth + j;
					it = img.begin()+ shift_it;
					cit = Conditional.begin() + shift_it;

					if (mLabels == 2)
						r = 1 - *cit;
					else
						r = (*cit + (int)(rnd()*(mLabels - 1)) + 1) % mLabels;
					double n = rnd();
					double delta_E = ((this->*pE)(it, cit, *cit) - (this->*pE)(it, cit, r));
					if (n <= delta_E / T)
					{
						summa_deltaE += fabs(delta_E);
						*cit = r;
					}
				}
			}
		}
		T *= mDeltaT;
		++mIterCount;
		LogFile::WriteData("kriging.log", "Sum of Delta E: ", summa_deltaE);
	} while (summa_deltaE / (mWidth - 2) / (mHeight - 2) / (mDepth) > mEnergyThresh && T>EPS_THINY);
	LogFile::WriteData("kriging.log", "SA finished ");
}

void MRF::Gibbs(const array<unsigned char> &img, array<unsigned char> &Conditional)
{
	LogFile::WriteData("kriging.log", "Gibbs started ");
	int s;
	double sumE;
	double z;
	double r;

	double *Ek = new double[mLabels];
	double summa_deltaE;
	double T = mT0;
	mIterCount = 0;
	int turnsCount = 0;
	do
	{
		turnsCount = 0;
		array<unsigned char>::iterator cit = Conditional.begin();// +mWidth + 1;
		array<unsigned char>::const_iterator it = img.begin();// +mWidth + 1;
		typedef double(MRF::*pEnergy)(array<unsigned char>::const_iterator it, array<unsigned char>::iterator cit, int label);

		for (int k = 0; k < mDepth; k++)
		{
			pEnergy pE = &MRF::Energy3D;
			if (mDepth == 1)
				pE = &MRF::Energy;
			else if (k == 0)
				pE = &MRF::Energy3DTop;
			else if (k == mDepth - 1)
				pE = &MRF::Energy3DBot;

			for (int i = 1; i < mHeight - 1; i++)
			{
				for (int j = 1; j < mWidth - 1; j++)
				{
					int shift_it = k*mWidth*mHeight + i*mWidth + j;
					it = img.begin() + shift_it;
					cit = Conditional.begin() + shift_it;

					sumE = 0.0;
					for (s = 0; s<mLabels; s++)
					{
						Ek[s] = exp(-(this->*pE)(it, cit, s) / T);
						sumE += Ek[s];
					}
					r = rnd();	// r is a uniform random number
					z = 0.0;
					for (s = 0; s<mLabels; ++s)
					{
						z += Ek[s] / sumE;
						if (z > r) // choose new label with probabilty exp(-U/T).
						{
							turnsCount+=(*cit!=s);
							*cit = s;
							break;
						}
					}
				}
			}
		}
		T *= mDeltaT;
		++mIterCount;
		LogFile::WriteData("kriging.log","TurnsCount: ", turnsCount);
	} while ((double)turnsCount / (mWidth-2) / (mHeight-2) / mDepth > mEnergyThresh && T>EPS_THINY);
	delete[] Ek;
	LogFile::WriteData("kriging.log", "Gibbs finished ");
}

void MRF::MMD()
{
}

bool MRF::SATest()
{
	array<unsigned char> img(25);
	array<unsigned char> Conditional(25);
	int i = 0;
	auto cit = Conditional.begin();
	for (auto it = img.begin(); it != img.end(); it++)
	{
		*it = i;
		i++;
	};
	Stats2L(img, 20, 4, mean[0], mean[1], var[0], var[1]);
	mWidth = 5;
	mHeight = 5;
	mDepth = 1;
	ConditionalImage(img, Conditional);
	Conditional[7] = 1;
	Conditional[18] = 0;
	Threshold<unsigned char> thresh;
	thresh.SetManualThresholds(4, 20);
	SRG(img, thresh,Conditional,  mWidth, mHeight, mDepth);

	Gibbs(img, Conditional);
	SimulatedAnnealing3D(img, Conditional);
	int s = 0;
	for (auto c = Conditional.begin(); c != Conditional.end(); c++)
		s += *c;
	return s==12;
}

void MRF::Stats2L(const array<unsigned char> &img, double High, double Low, double &LMean, double &HMean, double &LVar, double &HVar)
{
	int h = 0; int l = 0;  double H = 0; double  L = 0;	int idbg = 0;
	for (auto it = img.begin(); it != img.end(); it++)
	{
		if (*it > High)
		{
			H += *it;
			h++;
		}
		else if (*it <= Low)
		{
			L += *it;
			l++;
		}
		idbg++;
	}
	L = L / l;
	H = H / h;

	double dH = 0; double dL = 0;
	idbg = 0;
	for (auto it = img.begin(); it != img.end(); it++)
	{
		if (*it > High)
		{
			double d = (*it - H);
			dH += d*d;
		}
		else if (*it <= Low)
		{
			double d = (*it - L);
			dL += d*d;
		}
		idbg++;
	}
	LMean = L;
	HMean = H;
	HVar = sqrt(dH / h);
	LVar = sqrt(dL / l);
}

void MRF::Perform(const array<unsigned char> &img, array<unsigned char> &Conditional, Threshold<unsigned char> &Thresh, int W, int H, int D)
{
	//array<int>ThCopy(H*W*D);
	//std::copy<array<unsigned char>::const_iterator, array<int>::iterator>(img.begin(), img.end(), ThCopy.begin());
	LogFile::WriteData("kriging.log", "Thresh method ", Thresh.Method);
	if (Thresh.Method != Th_Manual)
		Thresh.compute_cut_offs(img, W, H, D);
//	SATest();
	LogFile::WriteData("kriging.log", "MRF STat2L");
	Stats2L(img, Thresh.High(), Thresh.Low(), mean[0], mean[1], var[0], var[1]);
	LogFile::WriteData("kriging.log", "Stats calculated");
	mWidth = W;
	mHeight = H;
	mDepth = D;
	ConditionalImage(img, Conditional);
	LogFile::WriteData("kriging.log", "Conditional filled");
	if (Method == MRF::MRF_SA)
	{
		if (mDepth > 1)
			SimulatedAnnealing3D(img, Conditional);
		else
			SimulatedAnnealing(img, Conditional);
	};
	if (Method == MRF::MRF_GIBBS)
		Gibbs(img, Conditional);

	double f = 255.0 /(mLabels-1);
	for (auto cit = Conditional.begin(); cit != Conditional.end(); cit++)
		*cit *= f;
}

void MRF::SRG(const array<unsigned char> &img, Threshold<unsigned char> &thresh, array<unsigned char> &Conditional, int W, int H, int D)
{
	//array<int>ThCopy(H*W*D);
//	std::copy<array<unsigned char>::const_iterator, array<int>::iterator>(img.begin(), img.end(), ThCopy.begin());
	if (thresh.Method != Th_Manual)
		thresh.compute_cut_offs(img, W, H, D);
	Stats2L(img, thresh.High(), thresh.Low(), mean[0], mean[1], var[0], var[1]);
	mWidth = W;
	mHeight = H;
	mDepth = D;
	ConditionalImage(img, Conditional);
	vector<unsigned char>::const_iterator it = img.begin();
	for (auto cit = Conditional.begin(); cit<Conditional.end(); cit++, it++)
	{
		if (*it>thresh.High())
			*cit = 1;
		else if (*it <= thresh.Low())
			*cit = 0;
		else
			*cit = mLabels;
	};

	std::queue<Point3D>SSL;

	int i = 0;
	vector<unsigned char>::iterator cit;
	for (int k = 0; k < mDepth; k++)
	{
		for (int i = 1; i < mHeight - 1; i++)
		for (int j = 1; j < mWidth - 1; j++)
		{
			cit = Conditional.begin() + mHeight*mWidth*k+ mWidth*i + j;
			it = img.begin() + mHeight*mWidth*k + mWidth*i + j;
			if ((*cit == 2) && (*BotNB(cit) != 2 || *TopNB(cit) != 2 || *LeftNB(cit) != 2 || *RightNB(cit) != 2))
			{
				SSL.push(Point3D{ j, i, k });
			}
		}
	}

	cit = Conditional.begin();
	vector<int>nbh(mLabels);
	while (!SSL.empty())
	{
		Point3D p = SSL.front();
		SSL.pop();
		int I = p.y;
		int J = p.x;
		int K = p.z;
		if (I <= 0 || J <= 0 || I >= mHeight-1 || J >= mWidth-1)
			continue;
		it = img.begin() + mWidth*mHeight*K +mWidth*I + J;
		cit = Conditional.begin() + mWidth*mHeight*K + mWidth*I + J;
	
		for (int i = 0; i < mLabels; i++)
			nbh[i] = (*BotNB(cit) == i) + (*TopNB(cit) == i) + (*LeftNB(cit) == i) + (*RightNB(cit) == i);// || *BhdNB(cit) != 2 || *BfrNB(cit) != 2
		int nb_max = 0;
		int nb_max_idx = 0;

		for (int i = 0; i < mLabels; i++)
		{
			if (nbh[i]>nb_max)
			{
				nb_max_idx = i;
				nb_max = nbh[i];
			}
		}
		if (nb_max >= 2)
			*cit = nb_max_idx;
		else
		{
			double delta0 = abs(*it - mean[0]) / var[0];
			double delta1 = abs(*it - mean[1]) / var[1];
			if (delta0 < delta1)
				*cit = 0;
			else
				*cit = 1;
		}
		if (*BotNB(cit) == 2)
		{
			SSL.push(Point3D{ J, I + 1, K });
			*BotNB(cit) = 3;
		}
		if (*TopNB(cit) == 2)
		{
			SSL.push(Point3D{J, I - 1, K });
			*TopNB(cit) = 3;
		}
		if (*LeftNB(cit) == 2)
		{
			SSL.push(Point3D{ J - 1 , I, K });
			*LeftNB(cit) = 3;
		}
		if (*RightNB(cit) == 2)
		{
			SSL.push(Point3D{ J + 1, I, K });
			*RightNB(cit) = 3;
		}
	}
	for (auto cit = Conditional.begin(); cit != Conditional.end(); cit++)
		*cit =(*cit>0)*255;
}*/
#ifndef NELDERMEAD_H
#define NELDERMEAD_H


#include <limits>
#include <algorithm>
#include <functional>
#include <iostream>
#include <vector>
#include <assert.h>
/*
Минимизация методом Нелдера -Мида. Реализованный здесь алгоритм и константы описаны здесь: http://www.scholarpedia.org/article/Nelder-Mead_algorithm
Функция которую нужно мимнимизировать описана в наследнике
NelderMeadObjective. Структура NelderMeadSettings задает параметры остановки :
nMaxIter -остановка по достижении максимального числа итераций
Epsilon - ошибка меньше заданной
MinChange - изменение невязки меньше заданной

*/
struct NelderMeadObjective
{
	double operator()(const std::vector<double> &coeffs)const
	{
		return 0;
	}
};

struct NelderMeadSettings
{
	int nMaxIter;
	double Epsilon;
	double MinChange;
};

template<class NMFunctor>
class NelderMead
{
public:
	NelderMead(const NelderMeadSettings &Settings) :h(5.0), e(2.0), alpha(1.0), beta(0.5), gamma(1.0), delta(0.5), mSettings(Settings)
	{}
	int Perform(std::vector<double> &Params, std::vector<double> &LowerBounds, std::vector<double> &UpperBounds, NMFunctor &Objective);
private:
	void Centroid(std::vector<double>& C);
	void Accept(const std::vector<double> X, int Idx, double f);
	void ApplyBounds(std::vector<double> &X, std::vector<double> &LowerBounds, std::vector<double> &UpperBounds);
	inline int StopCondition();
	void RefreshIndices();
	const double e, h, alpha, beta, gamma, delta;
	std::vector<std::vector<double>> mVerteces;
	std::vector<double> mFunctions;
	std::vector<double> mCentroid;
	NelderMeadSettings mSettings;
	double F_best, F_worst, F_2ndworst;
	int I_worst, I_2ndworst, I_best;
	int mIterCount;
};

template<class NMFunctor>
int NelderMead<NMFunctor>::StopCondition()
{
	if (mSettings.Epsilon>F_worst)
		return 1;
	if (F_worst - F_best <= mSettings.MinChange)
		return 2;
	if (mIterCount >= mSettings.nMaxIter)
		return -1;
	return 0;

}

template<class NMFunctor>
void NelderMead<NMFunctor>::Accept(const std::vector<double> X, int Idx, double f)
{
	std::copy(X.begin(), X.end(), mVerteces[Idx].begin());
	mFunctions[Idx] = f;
	RefreshIndices();
}

template<class NMFunctor>
void NelderMead<NMFunctor>::Centroid(std::vector<double>& C)
{
	assert(C.size() == mVerteces[0].size());
	std::fill(C.begin(), C.end(), 0);

	for (int j = 0; j<mVerteces[0].size(); j++)
	{
		for (int i = 0; i<mVerteces.size(); i++)
		{
			if (i != I_worst)
				C[j] += mVerteces[i][j];
		}
		C[j] = C[j] / (mVerteces.size() - 1);
	}
}

template<class NMFunctor>
void NelderMead<NMFunctor>::RefreshIndices()
{
	F_worst = F_2ndworst = F_best = mFunctions[0];
	for (int i = 0; i<mFunctions.size(); i++)
	{

		double f = mFunctions[i];
		if (f<F_best)
		{
			F_best = f;
			I_best = i;
		}
		else if (f + 0.000001>F_2ndworst)
		{
			if (f + 0.000001>F_worst)
			{
				F_2ndworst = F_worst;
				I_2ndworst = I_worst;
				F_worst = f;
				I_worst = i;
			}
			else
			{
				F_2ndworst = f;
				I_2ndworst = i;
			}
		}
	}
}

template<class NMFunctor>
void NelderMead<NMFunctor>::ApplyBounds(std::vector<double> &X, std::vector<double> &LowerBounds, std::vector<double> &UpperBounds)
{
	for (int i = 0; i < X.size(); i++)
	{
		if (X[i] > UpperBounds[i]) 
			X[i] = UpperBounds[i];
		if (X[i] < LowerBounds[i]) 
			X[i] = LowerBounds[i];
	}

}

template<class NMFunctor>
int NelderMead<NMFunctor>::Perform(std::vector<double> &Params, std::vector<double> &LowerBounds, std::vector<double> &UpperBounds, NMFunctor &Objective)
{
	mCentroid.resize(Params.size());
	std::vector<double> Xr(Params.size());
	std::vector<double> Xc(Xr), Xe(Xr);//,Xl(Xr);
	mVerteces.push_back(Params);
	F_best = Objective(Params);

	F_worst = F_2ndworst = F_best;

	I_worst = I_2ndworst = I_best = 0;
	mFunctions.push_back(F_best);

	for (int i = 0; i<Params.size(); i++)
	{
		std::vector<double> V = Params;
		V[i] = e*i*V[i] + h*i;
		mVerteces.push_back(V);
		double f = Objective(V);
		mFunctions.push_back(Objective(V));
	}
	RefreshIndices();
	mIterCount = 0;
	while (StopCondition() == 0)
	{
		mIterCount++;
		Centroid(mCentroid);
		//reflect
		const std::vector<double> &Xh = mVerteces[I_worst];
		for (int i = 0; i<Xh.size(); i++)
			Xr[i] = mCentroid[i] + alpha*(mCentroid[i] - Xh[i]);
		ApplyBounds(Xr, LowerBounds, UpperBounds);
		double fr = Objective(Xr);
		if (fr<F_2ndworst && fr >= F_best)
		{
			Accept(Xr, I_worst, fr);
			continue;
		}
		if (fr<F_best)
		{
			for (int i = 0; i<Xh.size(); i++)
				Xe[i] = mCentroid[i] + gamma*(Xr[i] - mCentroid[i]);
			ApplyBounds(Xe, LowerBounds, UpperBounds);
			double fe = Objective(Xe);
			if (fe<fr)
			{
				Accept(Xe, I_worst, fe);
				continue;
			}
			else
			{
				Accept(Xr, I_worst, fr);
				continue;
			}
		}
		if (fr>F_2ndworst)
		{
			if (fr<F_worst)
			{
				for (int i = 0; i<Xh.size(); i++)
					Xc[i] = mCentroid[i] + beta*(Xr[i] - mCentroid[i]);
				ApplyBounds(Xc, LowerBounds, UpperBounds);
				double fc = Objective(Xc);
				if (fc<fr)
				{
					Accept(Xc, I_worst, fc);
					continue;
				}
			}

			if (fr>F_worst)
			{
				for (int i = 0; i<Xh.size(); i++)
					Xc[i] = mCentroid[i] + beta*(Xh[i] - mCentroid[i]);
				ApplyBounds(Xc, LowerBounds, UpperBounds);
				double fc = Objective(Xc);
				if (fc<F_worst)
				{
					Accept(Xc, I_worst, fc);
					continue;
				}
			}
		}
		std::vector<double>& Xl = mVerteces[I_best];
		for (int j = 0; j<mVerteces.size(); j++)
		{
			if (j != I_best)
			for (int i = 0; i<mVerteces[j].size(); i++)
				mVerteces[j][i] = Xl[i] + delta*(mVerteces[j][i] - Xl[i]);
		}

	};
	Params = mVerteces[I_best];
	return StopCondition();
};

#endif
#ifndef MRF_H
#define MRF_H
#pragma once
#include "DynamicArray.h"
#include "LogFile.h"
#include <assert.h>
#include <queue>
//#define _USE_MATH_DEFINES
#include <cmath>
#include "threshold.h"
#include <string>
#include "LatticeModel.h"
#include "MRFUtils.h"
#include "RandomNumbers.h"

// Подобный тому код, только 2D и в 3 канала:
// https://github.com/ixartz/Markov-segmentation/tree/master/src

#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795
#endif

template <class T = int, class container_type = std::vector<T>, int nDim = 2>
class MRFSegmentation :public LatticeModel
{
	using LatticeIterator = typename container_type::iterator;
	using LatticeConstIterator = typename container_type::const_iterator;
	
	using LatticeModel::mLabels;
	using LatticeModel::mWidth;
	using LatticeModel::mHeight;
	using LatticeModel::mDepth;
	using LatticeModel::means;
	using LatticeModel::vars;

public:
	MRFSegmentation(int nLabels) :
		MRFSegmentation{MRFSettings{nLabels}}
	{ }

	MRFSegmentation(const MRFSettings &pref) :
		LatticeModel{pref.nLabels},
		mAlpha{pref.Alpha},
		mBeta{pref.Beta},
		mDeltaT{pref.FreezingSpeed},
		mT0{pref.TStart},
		mEnergyThresh{pref.EnergyThreshold},
		mIterCount{0},
		mMaxIterations{pref.MaxIterations},
		Method{pref.Method}
	{
		mStatSumms_Mean = new double[mLabels];
		mStatSumms_Sqr = new double[mLabels];
		mStatSumms = new size_t[mLabels];

		InitStatsZero();
	}

	~MRFSegmentation()
	{
		delete[] mStatSumms_Mean;
		delete[] mStatSumms_Sqr;
		delete[] mStatSumms;
	}
	
	MRFMethods Method;
	// bool CopyData(container_type& dest, const container_type& src)
	// {
	// 	const size_t data_len_bytes = src.size() * sizeof(T);
	// 	assert(dest.size() == data_len_bytes);
	// 	memcpy(dest.data(), src.data(), data_len_bytes);
	// }

	void ModifiedMetropolis(const container_type& img, container_type& labeled_img)
	{
		double total_voxels = static_cast<double>(mWidth * mHeight * mDepth);
		
		double _T{mT0};
		mIterCount = 0;
		LogFile::WriteData("kriging.log", "ModifiedMetropolis started");

		double energy = Energy(img, labeled_img);
		double delta_E{0.0};
		/*std::cout << "Initial energy = " << energy << std::endl;*/
		LogFile::WriteData("kriging.log", "Initial energy = ", energy);

		do
		{
			LatticeIterator cit = labeled_img.begin();
			LatticeConstIterator it = img.begin();
		
			size_t shift_it = 0UL;
			size_t changes_accepted = 0UL;
			for (size_t k = 0; k < mDepth; k++)
			{
				for (size_t i = 0; i < mHeight; i++)
				{
					for (size_t j = 0; j < mWidth; j++)
					{
						it = img.begin() + shift_it;
						cit = labeled_img.begin() + shift_it;

						int alternated_label = 1 - *cit;
						if (mLabels > 2)
						{
							alternated_label = (*cit + (int)(random_numbers::rnd() * (mLabels - 1)) + 1) % mLabels;
						}
		
						double delta_E = EnergyDelta(j, i, k, it, cit, alternated_label);
						// double delta_E = EnergyDeltaExt(j, i, k, it, cit, alternated_label);
						// double energy_1 = energy + delta_E;
						
						if (exp(-delta_E / _T) > mAlpha)
						{
							// AdjustStats(alternated_label, *cit, *it);
							*cit = alternated_label;
							changes_accepted++;

							// double energy_2 = Energy(img, labeled_img);
							// std::cout << "Delta E0 = " << delta_E0 << std::endl;
							// std::cout << "Delta E = " << delta_E << std::endl;
							// std::cout << "Energy 1 = " << energy_1 << std::endl;
							// std::cout << "Energy 2 = " << energy_2 << std::endl;
							// std::cout << "Discrepancy = " << fabs(energy_2 - energy_1) << std::endl;
						}
						
						shift_it++;
					}
				}
			}
			_T *= mDeltaT;
			++mIterCount;

			double new_energy = Energy(img, labeled_img);
			delta_E = new_energy - energy;
			energy = new_energy;
			//std::cout << "Iteration " << mIterCount << ", Changed voxels: " << changes_accepted << ", Delta E: " << delta_E << std::endl;
			//std::cout << "Energy = " << energy << std::endl;

			//std::string output = "Iteration " + std::to_string(mIterCount) + ", Changed voxels: " + std::to_string(changes_accepted);
			//LogFile::WriteData("kriging.log", output);
			//output = "Energy = " + std::to_string(new_energy) + ", delta = " + std::to_string(delta_E);
			//LogFile::WriteData("kriging.log", output);
		}
		while (fabs(delta_E) / total_voxels >= mEnergyThresh && _T > EPS_THINY && mIterCount < mMaxIterations);

		LogFile::WriteData("kriging.log", "ModifiedMetropolis finished");
	}

	void OutputPhases()
	{
		double total = mWidth * mHeight * mDepth * 0.01;
		//for (int i = 0; i < mLabels; i++)
		//{
		//	std::cout << "[Phase " << i << "]: Percentage = " << mStatSumms[i] / total << "; Mean = " << means[i] << "; Stddev = " << vars[i] << std::endl;
		//}
	}

	const T OptimalICMLabel(size_t j, size_t i, size_t k, LatticeConstIterator it, LatticeConstIterator cit)
	{
		double opt_energy = VoxelEnergy(j, i, k, it, cit, *cit);
		T opt_label = *cit;
		for (T test_label = 0; test_label < mLabels; test_label++)
		{
			if (test_label != opt_label)
			{
				double test_energy = VoxelEnergy(j, i, k, it, cit, test_label);
				if (test_energy < opt_energy)
				{
					opt_energy = test_energy;
					opt_label = test_label;
				}
			}
		}
		return opt_label;
	}

	void ICM_Segmentation(const container_type& img, container_type& labeled_img)
	{
		double total_voxels = static_cast<double>(mWidth * mHeight * mDepth);
		size_t maxIters{10UL};
		
		double _T{mT0};
		mIterCount = 0;
		LogFile::WriteData("kriging.log", "ICM started");

		double energy = Energy(img, labeled_img);
		double delta_E{0.0};
		//std::cout << "Initial energy = " << energy << std::endl;
		LogFile::WriteData("kriging.log", "Initial energy = ", energy);

		do
		{
			LatticeIterator cit = labeled_img.begin();
			LatticeConstIterator it = img.begin();

			size_t shift_it = 0UL;
			size_t changes_accepted = 0UL;
			for (size_t k = 0; k < mDepth; k++)
			{
				for (size_t i = 0; i < mHeight; i++)
				{
					for (size_t j = 0; j < mWidth; j++)
					{
						it = img.begin() + shift_it;
						cit = labeled_img.begin() + shift_it;

						T optimal_label = *cit;
						if (mLabels == 2)
						{
							T alternated_label = 1 - *cit;
							if (EnergyDelta(j, i, k, it, cit, alternated_label) < 0)
							{
								optimal_label = alternated_label;
								changes_accepted++;
							}
						}
						else
						{
							optimal_label = OptimalICMLabel(j, i, k, it, cit);
						}

						*cit = optimal_label;						
						shift_it++;
					}
				}
			}
			++mIterCount;

			double new_energy = Energy(img, labeled_img);
			delta_E = new_energy - energy;
			energy = new_energy;
			
			std::string output = "Iteration " + std::to_string(mIterCount) + ", Changed voxels: " + std::to_string(changes_accepted);
			LogFile::WriteData("kriging.log", output);
			output = "Energy = " + std::to_string(new_energy) + ", delta = " + std::to_string(delta_E);
			LogFile::WriteData("kriging.log", output);

			//std::cout << "Iteration " << mIterCount << ", Changed voxels: " << changes_accepted << ", Delta E: " << delta_E << std::endl;
			//std::cout << "Energy = " << energy << std::endl;
		}
		while (fabs(delta_E) / total_voxels >= mEnergyThresh && _T > EPS_THINY && mIterCount < mMaxIterations);

		LogFile::WriteData("kriging.log", "ICM finished");
	}

	void Perform(const container_type &img, container_type &Conditional, Threshold<T, container_type>  &Thresh, int W, int H, int D)
	{
		mWidth = W;
		mHeight = H;
		mDepth = D;

		LogFile::WriteData("kriging.log", "Thresh method ", Thresh.Method);
		if (Thresh.Method != Th_Manual)
		{
			container_type I(W*H);
			std::copy<LatticeConstIterator, typename container_type::iterator>(img.begin(), img.begin() + W*H, I.begin());
			Thresh.compute_cut_offs(I, W, H, 1);
		}

		LogFile::WriteData("kriging.log", "MRF segmentation started");
		if (Thresh.PhasesCount() == 2)
		{
			this->Stats2L(img, Thresh.High(), Thresh.Low(), this->means[0], this->means[1], this->vars[0], this->vars[1]);
			this->ConditionalImage2Labels(img, Conditional, Thresh);
		}
		else
		{
			this->StatsNL(img, Thresh.HighThresholds(), Thresh.LowThresholds(), this->means, this->vars);
			this->ConditionalImage(img, Conditional, Thresh);
		}
		LogFile::WriteData("kriging.log", "Preliminary seed image generated");

		if (Method == MRF_ModifiedMetropolis)
		{
			ModifiedMetropolis(img, Conditional);
		}
		else if (Method == MRF_ICM)
		{
			ICM_Segmentation(img, Conditional);
		}
		else
		{
			LogFile::WriteData("kriging.log", "Unknown method, segmentation not performed");
		}
	}

private:

	double mAlpha;
	double mBeta;
	double mDeltaT;
	double mT0;
	double mEnergyThresh;
	int mIterCount;
	int mMaxIterations;

	// Optimization of stats calculation
	double* mStatSumms_Mean;
	double* mStatSumms_Sqr;
	size_t* mStatSumms;

	void InitStatsZero()
	{
		for (size_t i = 0; i < mLabels; i++)
		{
			mStatSumms[i] = 0UL;
			mStatSumms_Mean[i] = 0.0;
			mStatSumms_Sqr[i] = 0.0;
		}
	}
	
	void RecomputeStats(const container_type& image, const container_type& label_image)
	{
		InitStatsZero();

		LatticeConstIterator cit = label_image.begin();
		for (auto it = image.begin(); it != image.end(); it++, cit++)
		{
			int i = *cit;
			const T value = *it;
			mStatSumms_Mean[i] += value;
			mStatSumms_Sqr[i] += value * value;
			mStatSumms[i]++;
		}

		for (int i = 0; i < mLabels; i++)
		{
			if (mStatSumms[i] != 0)
			{
				means[i] = mStatSumms_Mean[i] / mStatSumms[i];
				vars[i] = sqrt(mStatSumms_Sqr[i] / mStatSumms[i] - means[i] * means[i]);
			}
			else
			{
				means[i] = 0.0;
				vars[i] = 0.0;
			}
		}

		OutputPhases();
	}

	double Energy(const container_type& image, const container_type& label_image)
	{
		RecomputeStats(image, label_image);

		double energy_value = 0;
		size_t offset = 0UL;

		for (size_t k = 0; k < mDepth; k++)
		{
			for (size_t i = 0; i < mHeight; i++)
			{
				for (size_t j = 0; j < mWidth; j++)
				{
					LatticeConstIterator it = image.cbegin() + offset;
					LatticeConstIterator cit = label_image.cbegin() + offset;

					auto label = *cit;
					double eigen_energy = LocalEnergy(*it, label);
					double diff_energy = 0.5 * NeighborDiffEnergy(j, i, k, cit, label);
					energy_value += eigen_energy + diff_energy;
					offset++;
				}
			}
		}

		return energy_value;
	}

	double EnergyDelta(const size_t j,
						const size_t i,
						const size_t k,
						LatticeConstIterator val_it,
						LatticeConstIterator label_it,
						int new_label)
	{
		return VoxelEnergy(j, i, k, val_it, label_it, new_label) - VoxelEnergy(j, i, k, val_it, label_it, *label_it);
	}

	void AdjustStats(const size_t incremented_phase, const size_t decremented_phase, const T value)
	{
		assert(incremented_phase >= 0);
		assert(decremented_phase >= 0);
		assert(incremented_phase < mLabels);
		assert(decremented_phase < mLabels);

		mStatSumms[incremented_phase]++;
		mStatSumms_Mean[incremented_phase] += value;
		mStatSumms_Sqr[incremented_phase] += value * value;

		mStatSumms[decremented_phase]--;
		mStatSumms_Mean[decremented_phase] -= value;
		mStatSumms_Sqr[decremented_phase] -= value * value;

		auto mean_inc = mStatSumms_Mean[incremented_phase] / mStatSumms[incremented_phase];
		auto mean_dec = mStatSumms_Mean[decremented_phase] / mStatSumms[decremented_phase];
		means[incremented_phase] = mean_inc;
		means[decremented_phase] = mean_dec;
		vars[incremented_phase] = sqrt(mStatSumms_Sqr[incremented_phase] / mStatSumms[incremented_phase] - mean_inc * mean_inc);
		vars[decremented_phase] = sqrt(mStatSumms_Sqr[decremented_phase] / mStatSumms[decremented_phase] - mean_dec * mean_dec);
	}

	double EnergyDeltaExt(const size_t j,
						const size_t i,
						const size_t k,
						LatticeConstIterator val_it,
						LatticeConstIterator label_it,
						size_t new_label)
	{
		const T old_label = *label_it;
		const T value = *val_it;
		double deltaByVoxel = EnergyDelta(j, i, k, val_it, label_it, new_label);

		double mean_dec_old = means[old_label];
		double mean_inc_old = means[new_label];
		double sigma_dec_old = vars[old_label];
		double sigma_inc_old = vars[new_label];
		size_t N_dec_old = mStatSumms[old_label];
		size_t N_inc_old = mStatSumms[new_label];
		double S_inc_old = mStatSumms_Mean[new_label];
		double S2_inc_old = mStatSumms_Sqr[new_label];
		double S_dec_old = mStatSumms_Mean[old_label];
		double S2_dec_old = mStatSumms_Sqr[old_label];

		// AdjustStats(new_label, old_label, value);

		size_t N_dec_new = N_dec_old - 1;
		size_t N_inc_new = N_inc_old + 1;
		double S_inc_new = S_inc_old + value;
		double S2_inc_new = S2_inc_old + value * value;
		double S_dec_new = S_dec_old - value;
		double S2_dec_new = S2_dec_old - value * value;

		double mean_dec_new = S_dec_new / N_dec_new;
		double mean_inc_new = S_inc_new / N_inc_new;
		double sigma_dec_new = sqrt(S2_dec_new / N_dec_new - mean_dec_new * mean_dec_new);
		double sigma_inc_new = sqrt(S2_inc_new / N_inc_new - mean_inc_new * mean_inc_new);

		double deltaByStats_1 = N_dec_new * log(sqrt(2.0 * M_PI * sigma_dec_new)) +
		                      N_inc_new * log(sqrt(2.0 * M_PI * sigma_inc_new)) -
							  N_dec_old * log(sqrt(2.0 * M_PI * sigma_dec_old)) -
							  N_inc_old * log(sqrt(2.0 * M_PI * sigma_inc_old));
		
		double deltaByStats_2 = (S2_dec_new - 2.0 * mean_dec_new * S_dec_new + N_dec_new * mean_dec_new) / (2.0 * sigma_dec_new * sigma_dec_new) +
								(S2_inc_new - 2.0 * mean_inc_new * S_inc_new + N_inc_new * mean_inc_new) / (2.0 * sigma_inc_new * sigma_inc_new) -
								(S2_dec_old - 2.0 * mean_dec_old * S_dec_old + N_dec_old * mean_dec_old) / (2.0 * sigma_dec_old * sigma_dec_old) -
								(S2_inc_old - 2.0 * mean_inc_old * S_inc_old + N_inc_old * mean_inc_old) / (2.0 * sigma_inc_old * sigma_inc_old);

		//std::cout << "Old label = " << old_label << std::endl;
		//std::cout << "New label = " << new_label << std::endl;
		//std::cout << "Delta by voxel = " << deltaByVoxel << std::endl;
		//std::cout << "Delta by stats 1 = " << deltaByStats_1 << std::endl;
		//std::cout << "Delta by stats 2 = " << deltaByStats_2 << std::endl;

		return deltaByVoxel + deltaByStats_1 + deltaByStats_2;
	}

	double VoxelEnergy(const size_t j,
						const size_t i,
						const size_t k,
						LatticeConstIterator val_it,
						LatticeConstIterator label_it,
						const T label)
	{
		const T value = *val_it;
		return LocalEnergy(value, label) + NeighborDiffEnergy(j, i, k, label_it, label);
	}

	double LocalEnergy(const T value, const T label)
	{
		double sigma = this->vars[label];
		return log(sqrt(2.0 * M_PI * sigma)) + pow(value - means[label], 2) / (2.0 * sigma * sigma);
	}

	double NeighborDiffEnergy(size_t j, size_t i, size_t k, LatticeConstIterator label_it, T inner_label)
	{
	    int mismatched_neighbors = 0;
		if (j > 0 && *this->LeftNB(label_it) != inner_label) { mismatched_neighbors++; }
		if (j < mWidth - 1 && *this->RightNB(label_it) != inner_label) { mismatched_neighbors++; }
		if (i > 0 && *this->TopNB(label_it) != inner_label) { mismatched_neighbors++; }
		if (i < mHeight - 1 && *this->BotNB(label_it) != inner_label) { mismatched_neighbors++; }
		if (k > 0 && *this->FrntNB(label_it) != inner_label) { mismatched_neighbors++; }
		if (k < mDepth - 1 && *this->BhdNB(label_it) != inner_label) { mismatched_neighbors++; }
		return mBeta * (mismatched_neighbors * 2 - 6);
	}

	void ConditionalImage(const container_type &I, container_type &C, Threshold<T, container_type> &thresh)
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
				*cit = this->SelectPhase(*cit);
		}
	}

	void ConditionalImage2Labels(const container_type &I, container_type &C, Threshold<T, container_type> &thresh)
	{
		LatticeConstIterator it = I.begin();

		for (auto cit = C.begin(); cit<C.end(); cit++, it++)
		{
			if (*it>thresh.High())
				*cit = 1;
			else if (*it <= thresh.Low())
				*cit = 0;
			else if (abs(*it - thresh.Low()) < abs(*it - thresh.High()))
				*cit = 0;
			else
				*cit = 1;
		};
	}

};

#endif

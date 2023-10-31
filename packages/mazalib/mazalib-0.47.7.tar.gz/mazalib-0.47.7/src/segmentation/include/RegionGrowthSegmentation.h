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

class RegionGrowthSegmentation :
	public LatticeModel
{
	using LatticeIterator = typename std::vector<int>::iterator;
	using LatticeConstIterator = typename std::vector<int>::const_iterator;

public:
	RegionGrowthSegmentation(int nLabels) :
		LatticeModel(nLabels),
		UNDEFINED(nLabels),
		RESTRICTED(nLabels + 1),
		INTERFACE(nLabels + 2)
	{
	};

	RegionGrowthSegmentation(const MRFSettings &pref) :
		LatticeModel(pref.nLabels),
		UNDEFINED(pref.nLabels),
		RESTRICTED(pref.nLabels + 1),
		INTERFACE(pref.nLabels + 2)
	{
	}

	~RegionGrowthSegmentation()
	{
	};

	MRFMethods Method;

	// TODO: automatic max_stddev as an inflextion point of a histogram. Now threshold is mean + 2 sigma
	void PartialVolumeFiltering(const std::vector<int>& img, std::vector<int>& conditional_image, Threshold<int, std::vector<int>>& threshold, double threshold_coeff = 2.0)
	{
		static int values_cache[33];
		static const float MISSING_VALUE = -1.0f;
		
		if (threshold.PhasesCount() <= 2)
		{
			LogFile::WriteData("kriging.log", "Partial volume filtering not needed, only 2 phases");
			return;
		}

		// Computing stddev globally
		std::vector<float> stddev_img(this->mWidth * this->mHeight * this->mDepth);
		float min_stddev = 0.f;
		double avg_stddev = 0.0;
		size_t values_count = 0;

		auto layer_sz = this->mHeight * this->mWidth;
		auto width = this->mWidth;
		for (size_t k = 0; k < this->mDepth; k++)
		{
			for (size_t i = 0; i < this->mHeight; i++)
			{
				for (size_t j = 0; j < this->mWidth; j++)
				{
					const auto phase = *(conditional_image.begin() + layer_sz*k + width*i + j);
					// Checking if voxel belongs to the intermediate phase
					if (phase > 0 && phase < threshold.PhasesCount() - 1)
					{
						// Collecting adjacent values
						auto cache_top = 0;
						for (size_t m_z = 0; m_z < mask_dim; m_z++)
						{
							for (size_t m_y = 0; m_y < mask_dim; m_y++)
							{
								for (size_t m_x = 0; m_x < mask_dim; m_x++)
								{
									auto mask_pos = m_z * mask_dim * mask_dim + m_y * mask_dim + m_x;
									if (sphere_2_mask[mask_pos] != 0)
									{
										auto target_z = k + (m_z - offset);
										auto target_y = i + (m_y - offset);
										auto target_x = j + (m_x - offset);
										if (target_x > 0 && target_x < width && 
										    target_y > 0 && target_y < this->mHeight &&
											target_z > 0 && target_z < this->mDepth)
										{
											values_cache[cache_top++] = *(img.begin() + layer_sz*target_z + width*target_y + target_x);
										}
									}
								}
							}
						}

						// Computing stddev in point
						float mean = 0.f;
						for (size_t cache_idx = 0; cache_idx < cache_top; cache_idx++)
						{
							mean += float(values_cache[cache_idx]);
						}
						mean /= cache_top;

						float variance = 0.f;
						for (size_t cache_idx = 0; cache_idx < cache_top; cache_idx++)
						{
							float delta = float(values_cache[cache_idx]) - mean;
							variance += delta * delta;
						}
						variance /= cache_top;
						auto stddev = sqrt(variance);

						*(stddev_img.begin() + this->mHeight*this->mWidth*k + this->mWidth*i + j) = stddev;
						min_stddev = stddev < min_stddev ? stddev : min_stddev;
						avg_stddev += double(stddev);
						values_count++;
					}
					else
					{
						*(stddev_img.begin() + this->mHeight*this->mWidth*k + this->mWidth*i + j) = MISSING_VALUE;
					}
				}
			}
		}
		avg_stddev /= values_count;
		
		// Computing threshold value of stddev
		double stddev_var = 0;
		for (size_t k = 0; k < this->mDepth; k++)
		{
			for (size_t i = 0; i < this->mHeight; i++)
			{
				for (size_t j = 0; j < this->mWidth; j++)
				{
					float current_value = *(stddev_img.cbegin() + this->mHeight*this->mWidth*k + this->mWidth*i + j);
					if (current_value != MISSING_VALUE)
					{
						double delta = current_value - avg_stddev;
						stddev_var += delta * delta;
					}					
				}
			}
		}
		stddev_var /= values_count;
		auto stddev_sigma = sqrt(stddev_var);
		auto threshold_value = avg_stddev + threshold_coeff * stddev_sigma;

		// Invalidate phase assumption if stddev exceeds maximum value
		for (size_t k = 0; k < this->mDepth; k++)
		{
			for (size_t i = 0; i < this->mHeight; i++)
			{
				for (size_t j = 0; j < this->mWidth; j++)
				{
					float current_value = *(stddev_img.cbegin() + this->mHeight*this->mWidth*k + this->mWidth*i + j);
					if (current_value != MISSING_VALUE)
					{
						double delta = current_value - avg_stddev;
						if (current_value > threshold_value)
						{
							*(conditional_image.begin() + this->mHeight*this->mWidth*k + this->mWidth*i + j) = this->mLabels;
						}		
					}					
				}
			}
		}
	}

	void SimultaneousGrowing(const std::vector<int> &img, std::vector<int> &Conditional)
	{
		// Defining the front
		std::queue<SimplePoint3d> front_voxels;

		//int i = 0;
		LatticeConstIterator value_it = img.begin();
		LatticeIterator phase_it;
		for (size_t k = 0; k < this->mDepth; k++)
		{
			for (size_t i = 0; i < this->mHeight; i++)
			{
				for (size_t j = 0; j < this->mWidth; j++)
				{
					phase_it = Conditional.begin() + this->mHeight*this->mWidth*k + this->mWidth*i + j;
					value_it = img.begin() + this->mHeight*this->mWidth*k + this->mWidth*i + j;
					if ((*phase_it == UNDEFINED) && ((i < this->mHeight - 1 && *this->BotNB(phase_it) != UNDEFINED) ||
					                                (i > 0 && *this->TopNB(phase_it) != UNDEFINED) ||
													(j > 0 && *this->LeftNB(phase_it) != UNDEFINED) ||
													(j < this->mWidth - 1 && *this->RightNB(phase_it) != UNDEFINED) ||
													(k<this->mDepth - 1 && *this->BhdNB(phase_it) != UNDEFINED) ||
													(k>0 && *this->FrntNB(phase_it) != UNDEFINED)))
					{
						front_voxels.push(SimplePoint3d{ (int)j, (int)i, (int)k });
					}
				}
			}
		}

		// Simultaneous growing
		phase_it = Conditional.begin();

		while (!front_voxels.empty())
		{
			SimplePoint3d p = front_voxels.front();
			front_voxels.pop();
			size_t I = p.y;
			size_t J = p.x;
			size_t K = p.z;
			if (I < 0 || J < 0 || I >this->mHeight - 1 || J > this->mWidth - 1 || K<0 || K>this->mDepth - 1)
				continue;
			value_it = img.begin() + this->mWidth*this->mHeight*K + this->mWidth*I + J;
			phase_it = Conditional.begin() + this->mWidth*this->mHeight*K + this->mWidth*I + J;

			auto n_phases_detected = 0;
			auto phase_last_detected = 0;
			for (int i = 0; i < this->mLabels; i++)
			{
				auto voxels_of_phase = (I<this->mHeight - 1 && *this->BotNB(phase_it) == i) +
				                       (I>0 && *this->TopNB(phase_it) == i) +
			                           (J>0 && *this->LeftNB(phase_it) == i) +
									   (J<this->mWidth - 1 && *this->RightNB(phase_it) == i) +
									   (K<this->mDepth - 1 && *this->BhdNB(phase_it) == i) +
									   (K>0 && *this->FrntNB(phase_it) == i);
				if (voxels_of_phase > 0)
				{
					n_phases_detected++;
					phase_last_detected = i;
				}
			}
			if (n_phases_detected == 1)
			{
				*phase_it = phase_last_detected;
			}
			else
			{
				*phase_it = INTERFACE;
			}

			if (I<this->mHeight - 1 && *this->BotNB(phase_it) == UNDEFINED)
			{
				front_voxels.push(SimplePoint3d{ (int)J, (int)I + 1, (int)K });
				*this->BotNB(phase_it) = RESTRICTED;
			}
			if (I>0 && * this->TopNB(phase_it) == UNDEFINED)
			{
				front_voxels.push(SimplePoint3d{ (int)J, (int)I - 1, (int)K });
				*this->TopNB(phase_it) = RESTRICTED;
			}
			if (J>0 && * this->LeftNB(phase_it) == UNDEFINED)
			{
				front_voxels.push(SimplePoint3d{ (int)J - 1, (int)I, (int)K });
				*this->LeftNB(phase_it) = RESTRICTED;
			}
			if (J<this->mWidth - 1 && *this->RightNB(phase_it) == UNDEFINED)
			{
				front_voxels.push(SimplePoint3d{ (int)J + 1, (int)I, (int)K });
				*this->RightNB(phase_it) = RESTRICTED;
			}
			if (K>0 && *this->FrntNB(phase_it) == UNDEFINED)
			{
				front_voxels.push(SimplePoint3d{ (int)J, (int)I, (int)K - 1 });
				*this->FrntNB(phase_it) = RESTRICTED;
			}
			if (K<this->mDepth - 1 && * this->BhdNB(phase_it) == UNDEFINED)
			{
				front_voxels.push(SimplePoint3d{ (int)J , (int)I, (int)K + 1 });
				*this->BhdNB(phase_it) = RESTRICTED;
			}
		}
	}

	void InterfaceFilling(const std::vector<int> &img, std::vector<int> &Conditional)
	{
		LatticeConstIterator value_it = img.begin();
		LatticeIterator phase_it;

		std::vector<int> counter(this->mLabels);

		std::vector<int> nbh(this->mLabels);
		for (size_t k = 0; k < this->mDepth; k++)
		{
			for (size_t i = 0; i < this->mHeight; i++)
			{
				for (size_t j = 0; j < this->mWidth; j++)
				{
					phase_it = Conditional.begin() + this->mHeight*this->mWidth*k + this->mWidth*i + j;
					assert(*phase_it < UNDEFINED || *phase_it == INTERFACE);
					if (*phase_it == INTERFACE)
					{
						// Assuming phase as the most common between sphere-related neighbors
						auto cache_top = 0;
						for (size_t m_z = 0; m_z < mask_dim; m_z++)
						{
							for (size_t m_y = 0; m_y < mask_dim; m_y++)
							{
								for (size_t m_x = 0; m_x < mask_dim; m_x++)
								{
									auto mask_pos = m_z * mask_dim * mask_dim + m_y * mask_dim + m_x;
									if (sphere_2_mask[mask_pos] != 0)
									{
										auto target_z = k + (m_z - offset);
										auto target_y = i + (m_y - offset);
										auto target_x = j + (m_x - offset);
										if (target_x > 0 && target_x < this->mWidth && 
											target_y > 0 && target_y < this->mHeight &&
											target_z > 0 && target_z < this->mDepth)
										{
											LatticeIterator phase_it_outer = Conditional.begin() +
										        this->mHeight*this->mWidth*target_z + this->mWidth*target_y + target_x;
											nbh[*phase_it_outer]++;
										}
									}
								}
							}
						}

						int nb_max = 0;
						int nb_max_idx = 0;
						bool is_defined = false;
						for (int i = 0; i < this->mLabels; i++)
						{
							if (nbh[i] > nb_max)
							{
								nb_max_idx = i;
								nb_max = nbh[i];
								is_defined = true;
							}
							else if (nbh[i] == nb_max)
							{
								is_defined = false;
							}
						}

						if (is_defined)
						{
							*phase_it = nb_max_idx;
						}
						else
						{
							*phase_it = this->SelectPhaseNormalized(*value_it);
						}
						counter[*phase_it]++;
					}
				}
			}
		}
		for (auto phase = 0; phase < this->mLabels; phase++)
		{
			std::string output = "Phase " + std::to_string(phase) + " : " + std::to_string(counter[phase]);
			LogFile::WriteData("kriging.log", "Stats calculated");
		}
	}

	void Perform(const std::vector<int> &img, std::vector<int> &Conditional, Threshold<int, std::vector<int>> &Thresh, int W, int H, int D,
		ThresholdSettings& thresholdSettings)
	{
		LogFile::WriteData("kriging.log", "Thresh method ", Thresh.Method);
		if (Thresh.Method != Th_Manual)
		{
			std::vector<int> I(W*H);
			std::copy<LatticeConstIterator, typename std::vector<int>::iterator>(img.begin(), img.begin() + W*H, I.begin());
			Thresh.compute_cut_offs(I, W, H, 1);
		}

		LogFile::WriteData("kriging.log", "MRF STat2L");

		if (thresholdSettings.IsMultiphase && Thresh.PhasesCount()>2)
		{
			this->StatsNL(img, Thresh.HighThresholds(), Thresh.LowThresholds(), this->means, this->vars);
			this->ConditionalImage(img, Conditional, Thresh);
		}
		else
		{
			this->Stats2L(img, Thresh.High(), Thresh.Low(), this->means[0], this->means[1], this->vars[0], this->vars[1]);
			this->ConditionalImage2Labels(img, Conditional, Thresh);
		}


		LogFile::WriteData("kriging.log", "Stats calculated");
		this->mWidth = W;
		this->mHeight = H;
		this->mDepth = D;

		LogFile::WriteData("kriging.log", "Partial volume filtering started");
		this->PartialVolumeFiltering(img, Conditional, Thresh);
		LogFile::WriteData("kriging.log", "Partial volume filtering finished");

		//LogFile::WriteData("kriging.log", "Conditional filled");
		//if (Thresh.Method != Th_Manual)
		//{
		//	array<unsigned char> I(W*H);
		//	std::copy<LatticeConstIterator, array<unsigned char>::iterator>(img.begin(), img.begin() + W*H, I.begin());
		//	Thresh.compute_cut_offs(I, W, H, 1);
		//}
		//StatsNL(img, Thresh.HighThresholds(), Thresh.LowThresholds(), mean, var);
		//Stats2L(img, thresh.High(), thresh.Low(), mean[0], mean[1], var[0], var[1]);/**/
		//this->mWidth = W;
		//this->mHeight = H;
		//this->mDepth = D;
		//ConditionalImage(img, Conditional, Thresh);
		

		this->SimultaneousGrowing(img, Conditional);
		this->InterfaceFilling(img, Conditional);
		
	}
private:
	int UNDEFINED;
	int RESTRICTED;
	int INTERFACE;
	static const char mask_dim = 5;
	static const char offset = 2;
	const char sphere_2_mask[125] = 
	                          { 0, 0, 0, 0, 0,
								0, 0, 0, 0, 0,
								0, 0, 1, 0, 0,
								0, 0, 0, 0, 0,
								0, 0, 0, 0, 0,
								
								0, 0, 0, 0, 0,
								0, 1, 1, 1, 0,
								0, 1, 1, 1, 0,
								0, 1, 1, 1, 0,
								0, 0, 0, 0, 0,
								
								0, 0, 1, 0, 0,
								0, 1, 1, 1, 0,
								1, 1, 1, 1, 1,
								0, 1, 1, 1, 0,
								0, 0, 1, 0, 0,
								
								0, 0, 0, 0, 0,
								0, 1, 1, 1, 0,
								0, 1, 1, 1, 0,
								0, 1, 1, 1, 0,
								0, 0, 0, 0, 0,
								
								0, 0, 0, 0, 0,
								0, 0, 0, 0, 0,
								0, 0, 1, 0, 0,
								0, 0, 0, 0, 0,
								0, 0, 0, 0, 0 };
};


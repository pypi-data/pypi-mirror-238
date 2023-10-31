#pragma once

enum MRFMethods { MRF_ModifiedMetropolis, MRF_ICM, MRF_Undefined }; //simulated annealing, Gibbs, not implemented

struct MRFSettings
{
	MRFSettings() :
		MRFSettings{2}
	{}

	MRFSettings(int _nLabels):
		nLabels{_nLabels},
		Beta{0.9},
		TStart{4.0},
		FreezingSpeed{0.98},
		Alpha{0.5},
		EnergyThreshold{0.01},
		MaxIterations{10},
		UnsharpMaskStrength{1.0},
		Method{MRFMethods::MRF_ModifiedMetropolis}
	{}

	int nLabels; // number of phases
	double Beta; //weight of neighbour voxels
	double TStart; //start temperature
	double FreezingSpeed; //speed of freezing in simulated annealing
	double Alpha; // threshold of change acceptance
	double EnergyThreshold; // optimization stopping criterion
	int MaxIterations; // iterations limit
	double UnsharpMaskStrength; // unsharp mask parameter
	MRFMethods Method;
};

#pragma once
#include <cmath>
#include <vector>

#define WIN_PI 3.14159265358979323846

class ExpectedMaximized {
public:
  ExpectedMaximized(const std::vector<int> &data, int nClasses,
                    double *seeds_Mean = NULL, double *seeds_Std = NULL);

  void Estimate();

  void UpdateParams();

  double NormDistr(double x, int nClassNum);

  void EStep();

  bool IsConverged(const std::vector<double> &pi,
                   const std::vector<double> &pi_old, double Eps);
  std::vector<int> mData;
  std::vector<double> pi;
  std::vector<double> sd;
  std::vector<double> mean;
  std::vector<std::vector<double>> class_prob;
  int nClasses;
  size_t nData;
  const double min_std;
};

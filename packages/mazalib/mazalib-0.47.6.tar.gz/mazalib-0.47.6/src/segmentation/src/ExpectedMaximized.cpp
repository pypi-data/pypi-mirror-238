#include "ExpectedMaximized.h"

ExpectedMaximized::ExpectedMaximized(const std::vector<int> &data, int nClasses,
                                     double *seeds_Mean, double *seeds_Std)
    : nClasses(nClasses), min_std(0.001) {
  size_t nDataSize = data.size();
  pi.resize(nClasses);
  sd.resize(nClasses);
  mean.resize(nClasses);
  class_prob.resize(nClasses);

  for (int i = 0; i < nClasses; i++) {
    class_prob[i].resize(nDataSize);
    if (seeds_Mean != NULL)
      mean[i] = seeds_Mean[i];
    if (seeds_Std != NULL)
      sd[i] = seeds_Std[i];

    pi[i] = 1.0 / nClasses;
  }
  mData = data;
  nData = mData.size();
}

void ExpectedMaximized::Estimate() {
  int nIter = 0;
  std::vector<double> pi_old(pi.begin(), pi.end());
  do {
    EStep();
    std::copy(pi.begin(), pi.end(), pi_old.begin());
    UpdateParams();
    nIter++;
  } while (!IsConverged(pi, pi_old, 0.001) && nIter < 1000);
}

void ExpectedMaximized::UpdateParams() {
  // M-Step
  // update pi
  double *SumProb = new double[nClasses];

  for (int j = 0; j < nClasses; j++) {
    SumProb[j] = 0;
    for (int i = 0; i < nData; i++)
      SumProb[j] += class_prob[j][i];
    pi[j] = SumProb[j] / nData;
  }
  // update_mean
  for (int j = 0; j < nClasses; j++) {
    double S1 = 0;
    for (int i = 0; i < nData; i++) {
      S1 += class_prob[j][i] * mData[i];
    }
    mean[j] = S1 / SumProb[j];
  }

  // update_sd
  for (int j = 0; j < nClasses; j++) {
    sd[j] = 0.0;
    for (int i = 0; i < nData; i++) {
      double d = (mData[i] - mean[j]);
      sd[j] += d * d * class_prob[j][i];
    }
    sd[j] /= SumProb[j];
    sd[j] = sqrt(sd[j]) + min_std;
  }

  delete[] SumProb;
}

double ExpectedMaximized::NormDistr(double x, int nClassNum) {
  double delta = (x - mean[nClassNum]);
  double v = 1 / (sqrt(2.0 * WIN_PI) * sd[nClassNum]) *
             exp(-(delta * delta / 2 / sd[nClassNum] / sd[nClassNum]));
  return v;
}

void ExpectedMaximized::EStep() {
  for (int i = 0; i < nData; i++)
    for (int j = 0; j < nClasses; j++) {
      double x = mData[i];
      double S = 0;
      for (int k = 0; k < nClasses; k++)
        S += pi[k] * NormDistr(x, k);

      class_prob[j][i] = pi[j] * NormDistr(x, j) / S;
    };
};

bool ExpectedMaximized::IsConverged(const std::vector<double> &pi,
                                    const std::vector<double> &pi_old,
                                    double Eps) {
  double S = 0;
  for (int j = 0; j < nClasses; j++)
    S = S + abs(pi_old[j] - pi[j]);
  return S < Eps;
}
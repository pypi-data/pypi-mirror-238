#pragma once

#include <cstdint>
#include <ctime>
#include <iostream>
#include <string.h>
#include <vector>

#include "DenoiseParameters.h"

namespace noise {
class NoiseLevel {
public:
  uint64_t n_samples;
  int patchsize;
  int datashape[3];

  NoiseLevel(uint64_t n_samples_, int patchsize_, int shape[3]);
  float *get_noiselevel(float *imagestack, protocol::DenoiseParameters *params);
  std::vector<float> get_noiselevel_2D_RGB(float *R, float *G, float *B,
                                           protocol::DenoiseParameters *params);

private:
  std::vector<long long int> samples;
  int reference_sample_semimanual = 0;
  int reference_sample_semimanualG = 0;
  int reference_sample_semimanualB = 0;
  int ncalls = 0;

  std::vector<long long int> drawsamples(int circular_mask_diameter);
  float *get_patchstd(std::vector<long long int> &samples, float *imagestack);

  std::pair<float, float> create2clusters(float *values, int n_samples,
                                          int firstpos = -1, int lastpos = -1);
  std::vector<std::vector<float>>
  create2clusters_zwindow(std::vector<long long int> &samples, float *values,
                          int windowsize);
};
} // namespace noise

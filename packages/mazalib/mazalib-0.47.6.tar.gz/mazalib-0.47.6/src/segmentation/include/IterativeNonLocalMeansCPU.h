#pragma once

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <math.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <vector>

#include "DenoiseParameters.h"

/*********************************************************************************************************************************************************
 *
 * Location: Helmholtz-Zentrum fuer Material und Kuestenforschung,
 *Max-Planck-Strasse 1, 21502 Geesthacht Author: Stefan Bruns Contact:
 *bruns@nano.ku.dk
 *
 * License: TBA
 *
 *********************************************************************************************************************************************************/

// THIS IS A CPU VERSION

namespace denoise {
class IterativeNonLocalMeansCPU {
  typedef long long int idx_type;

public:
  static float *pad_reflective(float *imagestack, int padding[6],
                               const int inshape[3], int outshape[3]);
  static float *pad_reflective_unrollpatchspace(
      float *imagestack, int padding[6], const int inshape[3], int outshape[3],
      long long int *patchpositions, int nsize_patch);

  static long long int *setup_searchspace(int shape[3],
                                          protocol::DenoiseParameters *params,
                                          int &nsize_search);
  static long long int *setup_patchspace(int shape[3],
                                         protocol::DenoiseParameters *params,
                                         int &nsize_patch);
  static float *setup_distweight(int shape[3],
                                 protocol::DenoiseParameters *params);

  // experimental stuff:
  static float *
  setup_gaussian_searchweight(float sigma, int shape[3],
                              protocol::DenoiseParameters *params);

  // keeping the whole stack in RAM
  float *Run_GaussianNoise(int iter, float *&image_raw, float *&previous_result,
                           float *sigmalist, int shape[3],
                           protocol::DenoiseParameters *params, bool verbose);

  void print_estimatedmemory(int shape[3], protocol::DenoiseParameters *params);

private:
  int nsize_search, nsize_patch; // amount of voxels in search and patch space
  long long int *search_positions,
      *patch_positions; // idx-shift of individual search and patch positions
  float *distweight;

  long long int expected_filesize = 0;

  // 3rd order Pade approximation
  float expapproximation(float x);

  float expapproximation_cutoff =
      -3.56648f; // inform the compiler when the expapproximation becomes
                 // negative

  // Polynomial approximation: float expapproximation(float x)
  // {return 1.00043+x*(1.00946+x*(0.50633+x*(0.15793+x*(0.03117+x*(0.00317)))));}
  // 5th order Pade: float expapproximation(float x){float x2 = x*x; return
  // (1.f+.5f*x+.111111111f*x2+.013888889f*x2*x+.000992063f*x2*x2+.000033069f*x2*x2*x)/(1.f-.5f*x
  //													+.111111111f*x2-.013888889f*x2*x+.000992063f*x2*x2-.000033069f*x2*x2*x);}

  void filterslice(int z0, float divisor, float *image_raw,
                   float *image_prefiltered, float *result, int shape[3],
                   protocol::DenoiseParameters *params);

  // dedicated filter kernel
  void filterslice_p111(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p112(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p113(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p221(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p222(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p331(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p332(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
  void filterslice_p333(int z0, float multiplier, float *image_raw,
                        float *image_previous, float *result, int shape[3],
                        protocol::DenoiseParameters *params);
};
} // namespace denoise

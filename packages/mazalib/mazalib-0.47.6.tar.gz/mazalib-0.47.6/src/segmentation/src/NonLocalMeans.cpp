#include "NonLocalMeans.h"

#include <fstream>
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>

#include "IterativeNonLocalMeansCPU.h"
#include "NoiseLevel.h"

using namespace std;

int *NonLocalMeans::nlm_denoise(const int *data_ptr, int shape[3],
                                int n_iterations, int search_radius,
                                bool verbose) {
  protocol::DenoiseParameters params;

  params.cpu.max_threads = 1;

  params.maxiterations = n_iterations;
  params.radius_searchspace[0] = search_radius;
  params.radius_searchspace[1] = search_radius;
  params.radius_searchspace[2] = search_radius;
  int data_len = shape[0] * shape[1] * shape[2];
  float *tmp_data = new float[data_len];
  float *current = tmp_data;
  const int *current_input = data_ptr;
  for (size_t vx = 0; vx < data_len; vx++) {
    *current = static_cast<float>(*current_input);
    current++;
    current_input++;
  }

  float *output = nullptr;

  denoise::IterativeNonLocalMeansCPU iternlm;
  if (verbose) {
    iternlm.print_estimatedmemory(shape, &params);
    // cout << "--------------------------------------------------" << endl;
  }

  noise::NoiseLevel noise(params.noiselevel.n_samples,
                          params.noiselevel.patchsize, shape);
  for (int iter = 1; iter <= params.maxiterations; iter++) {
    // cout << "Iteration " << iter << endl;
    float *noise_level = noise.get_noiselevel(tmp_data, &params);
    output = iternlm.Run_GaussianNoise(iter, tmp_data, output, noise_level,
                                       shape, &params, verbose);
  }

  // reverse transfer
  current = output;
  int *result = new int[data_len];
  int *current_output = result;
  for (size_t vx = 0; vx < data_len; vx++) {
    *current_output = static_cast<int>(round(*current));
    current++;
    current_output++;
  }
  delete[] tmp_data;
  free(output);
  return result;
}
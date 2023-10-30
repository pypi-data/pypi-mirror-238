#include "IterativeNonLocalMeansCPU.h"

namespace denoise {

void IterativeNonLocalMeansCPU::print_estimatedmemory(
    int shape[3], protocol::DenoiseParameters *params) {
  int searchspace[3];
  searchspace[0] = params->radius_searchspace[0];
  searchspace[1] = params->radius_searchspace[1];
  searchspace[2] = params->radius_searchspace[2];

  int patchspace[3];
  patchspace[0] = params->radius_patchspace[0];
  patchspace[1] = params->radius_patchspace[1];
  patchspace[2] = params->radius_patchspace[2];

  int nslices3Dinfo = params->nslices;
  int n_threads = params->cpu.max_threads;

  setup_patchspace(shape, params, nsize_patch);

  int dim2padding = std::min(nslices3Dinfo / 2, searchspace[2]);

  long long int nslice = shape[0] * shape[1];
  long long int nstack = shape[2] * nslice;
  long long int nstack_blocks = n_threads * nslice;

  long long int nslice_unroll =
      (shape[0] + 2 * searchspace[0]) * (shape[1] + 2 * searchspace[1]);
  long long int nstack_unroll = (shape[2] + 2 * dim2padding) * nslice_unroll;

  long long int nslice_nounroll =
      (shape[0] + 2 * (searchspace[0] + patchspace[0])) *
      (shape[1] + 2 * (searchspace[1] + patchspace[1]));
  long long int nstack_nounroll =
      (shape[2] + 2 * (dim2padding + patchspace[2])) * nslice_nounroll;

  long long int nstack_blocks_unroll =
      (n_threads + 2 * dim2padding) * nslice_unroll;
  long long int nstack_blocks_nounroll =
      (n_threads + 2 * (dim2padding + patchspace[2])) * nslice_nounroll;

  long long int memusage_unroll =
      ((nstack_unroll * (nsize_patch + 1)) + nstack) * sizeof(float);
  long long int memusage_nounroll =
      ((nstack_nounroll * 2) + nstack) * sizeof(float);
  long long int memusage_blocks_unroll =
      ((nstack_blocks_unroll * (nsize_patch + 1)) + 2 * nstack_blocks) *
      sizeof(float);
  long long int memusage_blocks_nounroll =
      ((nstack_blocks_nounroll * 2) + 2 * nstack_blocks) * sizeof(float);

  return;
}

float IterativeNonLocalMeansCPU::expapproximation(float x) {
  return (120.f + 60.f * x + 12.f * x * x + x * x * x) /
         (120.f - 60.f * x + 12.f * x * x - x * x * x);
}

float *IterativeNonLocalMeansCPU::pad_reflective(float *imagestack,
                                                 int padding[6],
                                                 const int inshape[3],
                                                 int outshape[3]) {
  int nx0 = inshape[0];
  int ny0 = inshape[1];
  int nz0 = inshape[2];
  long long int nslice0 = nx0 * ny0;

  outshape[0] = inshape[0] + padding[0] + padding[3];
  outshape[1] = inshape[1] + padding[1] + padding[4];
  outshape[2] = inshape[2] + padding[2] + padding[5];

  int nx1 = outshape[0];
  int ny1 = outshape[1];
  int nz1 = outshape[2];
  long long int nslice1 = nx1 * ny1;
  long long int nstack1 = nslice1 * nz1;

  float *output = (float *)malloc(nstack1 * sizeof(*output));

#pragma omp parallel for
  for (int64_t idx1 = 0; idx1 < nstack1; idx1++) {
    int64_t z1 = idx1 / nslice1;
    int64_t y1 = (idx1 - z1 * nslice1) / nx1;
    int64_t x1 = idx1 - z1 * nslice1 - y1 * nx1;

    int64_t z0 = z1 - padding[2];
    int64_t y0 = y1 - padding[1];
    int64_t x0 = x1 - padding[0];

    while (z0 < 0 || z0 >= nz0 || y0 < 0 || y0 >= ny0 || x0 < 0 || x0 >= nx0) {
      if (z0 < 0)
        z0 = -z0;
      if (y0 < 0)
        y0 = -y0;
      if (x0 < 0)
        x0 = -x0;

      if (z0 >= nz0)
        z0 = 2 * nz0 - z0 - 2;
      if (y0 >= ny0)
        y0 = 2 * ny0 - y0 - 2;
      if (x0 >= nx0)
        x0 = 2 * nx0 - x0 - 2;
    }

    int64_t idx0 = z0 * nslice0 + y0 * nx0 + x0;

    output[idx1] = imagestack[idx0];
  }
  return output;
}
float *IterativeNonLocalMeansCPU::pad_reflective_unrollpatchspace(
    float *imagestack, int padding[6], const int inshape[3], int outshape[3],
    long long int *patchpositions, int nsize_patch) {
  int nx0 = inshape[0];
  int ny0 = inshape[1];
  int nz0 = inshape[2];
  long long int nslice0 = nx0 * ny0;

  outshape[0] = inshape[0] + padding[0] + padding[3];
  outshape[1] = inshape[1] + padding[1] + padding[4];
  outshape[2] = inshape[2] + padding[2] + padding[5];

  int nx1 = outshape[0];
  int ny1 = outshape[1];
  int nz1 = outshape[2];
  long long int nslice1 = nx1 * ny1;
  long long int nstack1 = nslice1 * nz1;

  float *output = (float *)malloc((nstack1 * nsize_patch) * sizeof(*output));

#pragma omp parallel for
  for (int64_t idx1 = 0; idx1 < nstack1; idx1++) {
    int64_t z1 = idx1 / nslice1;
    int64_t y1 = (idx1 - z1 * nslice1) / nx1;
    int64_t x1 = idx1 - z1 * nslice1 - y1 * nx1;

    for (int64_t p = 0; p < nsize_patch; p++) {
      int64_t patchshift = patchpositions[p];
      int64_t zp = patchshift / nslice0;
      int64_t yp = (patchshift - zp * nslice0) / nx0;
      int64_t xp = patchshift - zp * nslice0 - yp * nx0;

      int64_t z0 = z1 - padding[2] + zp;
      int64_t y0 = y1 - padding[1] + yp;
      int64_t x0 = x1 - padding[0] + xp;

      while (z0 < 0 || z0 >= nz0 || y0 < 0 || y0 >= ny0 || x0 < 0 ||
             x0 >= nx0) {
        if (z0 < 0)
          z0 = -z0;
        if (y0 < 0)
          y0 = -y0;
        if (x0 < 0)
          x0 = -x0;

        if (z0 >= nz0)
          z0 = 2 * nz0 - z0 - 2;
        if (y0 >= ny0)
          y0 = 2 * ny0 - y0 - 2;
        if (x0 >= nx0)
          x0 = 2 * nx0 - x0 - 2;
      }

      int64_t idx0 = z0 * nslice0 + y0 * nx0 + x0;

      output[idx1 * nsize_patch + p] = imagestack[idx0];
    }
  }

  return output;
}

long long int *IterativeNonLocalMeansCPU::setup_searchspace(
    int shape[3], protocol::DenoiseParameters *params, int &nsize_search) {
  // precalculate shifts in search space

  // image space
  int nx = shape[0];
  int ny = shape[1];
  long long int nslice = nx * ny;

  // search space
  //////////////////////////////////////////////////////////////////////////////
  int nx_search = params->radius_searchspace[0] * 2 + 1;
  int ny_search = params->radius_searchspace[1] * 2 + 1;
  int nz_search = params->radius_searchspace[2] * 2 + 1;
  long long int nslice_search = nx_search * ny_search;
  long long int nstack_search = nz_search * nslice_search;
  nsize_search = 0;

  float rxs = static_cast<float>(std::max(params->radius_searchspace[0], 1));
  float rys = static_cast<float>(std::max(params->radius_searchspace[1], 1));
  float rzs = static_cast<float>(std::max(params->radius_searchspace[2], 1));

  int nslices_searchspace = params->nslices;

  std::vector<long long int> searchidx;

  for (int64_t idx_search = 0; idx_search < nstack_search; idx_search++) {
    int64_t zs = idx_search / nslice_search;
    int64_t ys = (idx_search - zs * nslice_search) / nx_search;
    int64_t xs = idx_search - zs * nslice_search - ys * nx_search;

    zs -= params->radius_searchspace[2];
    ys -= params->radius_searchspace[1];
    xs -= params->radius_searchspace[0];

    if (abs(zs) > nslices_searchspace / 2)
      continue; // search space out of bounds
    if ((zs == 0) && (ys == 0) && (xs == 0))
      continue; // center will be weighted separately
    if (((xs / rxs) * (xs / rxs) + (ys / rys) * (ys / rys) +
         (zs / rzs) * (zs / rzs)) <= 1.f) {
      nsize_search++;
      searchidx.push_back((zs * nslice + ys * nx + xs));
    }
  }
  //////////////////////////////////////////////////////////////////////////////

  long long int *search_positions =
      (long long int *)malloc(nsize_search * sizeof(*search_positions));
  std::copy(searchidx.begin(), searchidx.end(), search_positions);

  return search_positions;
}
long long int *IterativeNonLocalMeansCPU::setup_patchspace(
    int shape[3], protocol::DenoiseParameters *params, int &nsize_patch) {
  // precalculate shifts in patch space

  // image space
  int nx = shape[0];
  long long int nslice = shape[0] * shape[1];

  // patch space
  //////////////////////////////////////////////////////////////////////////////
  int nx_patch = params->radius_patchspace[0] * 2 + 1;
  int ny_patch = params->radius_patchspace[1] * 2 + 1;
  int nz_patch = params->radius_patchspace[2] * 2 + 1;
  long long int nslice_patch = nx_patch * ny_patch;
  long long int nstack_patch = nz_patch * nslice_patch;

  float rxp = static_cast<float>(std::max(params->radius_patchspace[0], 1));
  float ryp = static_cast<float>(std::max(params->radius_patchspace[1], 1));
  float rzp = static_cast<float>(std::max(params->radius_patchspace[2], 1));

  int nslices_patchspace = params->nslices;

  std::vector<long long int> patchidx;

  patchidx.push_back(0);
  nsize_patch = 1;

  for (int64_t idx_patch = 0; idx_patch < nstack_patch; idx_patch++) {
    int64_t zp = idx_patch / nslice_patch;
    int64_t yp = (idx_patch - zp * nslice_patch) / nx_patch;
    int64_t xp = idx_patch - zp * nslice_patch - yp * nx_patch;

    zp -= params->radius_patchspace[2];
    yp -= params->radius_patchspace[1];
    xp -= params->radius_patchspace[0];

    if (abs(zp) > nslices_patchspace / 2)
      continue; // patch space out of bounds
    if ((zp == 0) && (yp == 0) && (xp == 0))
      continue; // center will be weighted separately
    if (((xp / rxp) * (xp / rxp) + (yp / ryp) * (yp / ryp) +
         (zp / rzp) * (zp / rzp)) <= 1.f) {
      nsize_patch++;
      patchidx.push_back((zp * nslice + yp * nx + xp));
    }
  }
  //////////////////////////////////////////////////////////////////////////////

  long long int *patch_positions =
      (long long int *)malloc(nsize_patch * sizeof(*patch_positions));
  std::copy(patchidx.begin(), patchidx.end(), patch_positions);

  return patch_positions;
}
float *IterativeNonLocalMeansCPU::setup_distweight(
    int shape[3], protocol::DenoiseParameters *params) {
  // patch space
  //////////////////////////////////////////////////////////////////////////////
  int nx_patch = params->radius_patchspace[0] * 2 + 1;
  int ny_patch = params->radius_patchspace[1] * 2 + 1;
  int nz_patch = params->radius_patchspace[2] * 2 + 1;
  long long int nslice_patch = nx_patch * ny_patch;
  long long int nstack_patch = nz_patch * nslice_patch;

  float rxp = static_cast<float>(std::max(params->radius_patchspace[0], 1));
  float ryp = static_cast<float>(std::max(params->radius_patchspace[1], 1));
  float rzp = static_cast<float>(std::max(params->radius_patchspace[2], 1));

  int nslices_patchspace = params->nslices;

  std::vector<float> distanceweight;
  distanceweight.push_back(1.f); // center will be reweighted
  int nsize_patch = 1;
  float maxweight = 0.0f;

  float sq_anisotropy = params->z_anisotropy * params->z_anisotropy;

  for (int64_t idx_patch = 0; idx_patch < nstack_patch; idx_patch++) {
    int64_t zp = idx_patch / nslice_patch;
    int64_t yp = (idx_patch - zp * nslice_patch) / nx_patch;
    int64_t xp = idx_patch - zp * nslice_patch - yp * nx_patch;

    zp -= params->radius_patchspace[2];
    yp -= params->radius_patchspace[1];
    xp -= params->radius_patchspace[0];

    if (abs(zp) > nslices_patchspace / 2)
      continue; // patch space out of bounds
    if ((zp == 0) && (yp == 0) && (xp == 0))
      continue; // center will be weighted separately
    if (((xp / rxp) * (xp / rxp) + (yp / ryp) * (yp / ryp) +
         (zp / rzp) * (zp / rzp)) <= 1.f) {
      // std::cout << xp << " " << yp << " " << zp << std::endl;
      float euclideandistance =
          sqrtf((xp * xp) + (yp * yp) + (zp * zp) * sq_anisotropy);
      float this_distance = 1.f / ((2.f * euclideandistance + 1.f) *
                                   (2.f * euclideandistance +
                                    1.f)); // apply distance function of choice

      if (this_distance > maxweight)
        maxweight = this_distance;

      distanceweight.push_back(this_distance);
      nsize_patch++;
    }
  }
  //////////////////////////////////////////////////////////////////////////////

  distanceweight[0] = maxweight;

  float *outdistanceweight =
      (float *)malloc(nsize_patch * sizeof(*outdistanceweight));

  if (rxp == 1.f && ryp == 1.f && rzp == 1.f && shape[2] > 1)
    for (int i = 0; i < nsize_patch; i++)
      outdistanceweight[i] = 1.f / 7.f; // special case of radius 1
  else
    std::copy(distanceweight.begin(), distanceweight.end(), outdistanceweight);

  return outdistanceweight;
}
float *IterativeNonLocalMeansCPU::setup_gaussian_searchweight(
    float sigma, int shape[3], protocol::DenoiseParameters *params) {
  // additional weighting of search space

  // search space
  //////////////////////////////////////////////////////////////////////////////
  int nx_search = params->radius_searchspace[0] * 2 + 1;
  int ny_search = params->radius_searchspace[1] * 2 + 1;
  int nz_search = params->radius_searchspace[2] * 2 + 1;
  long long int nslice_search = nx_search * ny_search;
  long long int nstack_search = nz_search * nslice_search;
  int nsize_search = 0;

  float rxs = static_cast<float>(std::max(params->radius_searchspace[0], 1));
  float rys = static_cast<float>(std::max(params->radius_searchspace[1], 1));
  float rzs = static_cast<float>(std::max(params->radius_searchspace[2], 1));

  int nslices_searchspace = params->nslices;

  std::vector<float> weights;

  for (int64_t idx_search = 0; idx_search < nstack_search; idx_search++) {
    int64_t zs = idx_search / nslice_search;
    int64_t ys = (idx_search - zs * nslice_search) / nx_search;
    int64_t xs = idx_search - zs * nslice_search - ys * nx_search;

    zs -= params->radius_searchspace[2];
    ys -= params->radius_searchspace[1];
    xs -= params->radius_searchspace[0];

    if (abs(zs) > nslices_searchspace / 2)
      continue; // search space out of bounds
    if ((zs == 0) && (ys == 0) && (xs == 0))
      continue; // center will be weighted separately
    if (((xs / rxs) * (xs / rxs) + (ys / rys) * (ys / rys) +
         (zs / rzs) * (zs / rzs)) <= 1.f) {
      nsize_search++;
      float dist = sqrtf(static_cast<float>(xs * xs + ys * ys + zs * zs));
      weights.push_back(expf((-dist * dist) / (2.f * sigma * sigma)));
    }
  }
  //////////////////////////////////////////////////////////////////////////////

  float *search_weights =
      (float *)malloc(nsize_search * sizeof(*search_weights));
  std::copy(weights.begin(), weights.end(), search_weights);

  return search_weights;
}

float *IterativeNonLocalMeansCPU::Run_GaussianNoise(
    int iter, float *&image_raw, float *&previous_result, float *sigmalist,
    int shape[3], protocol::DenoiseParameters *params, bool verbose = false) {
  long long int nslice = shape[0] * shape[1];
  long long int nstack = shape[2] * nslice;

  int shape_padded[3]; // remembers the shape of the padded data

  // apply padding
  //////////////////////////////////////////////////////////////////////////////
  int padding[6] = {
      params->radius_searchspace[0] + params->radius_patchspace[0],
      params->radius_searchspace[1] + params->radius_patchspace[1],
      std::min(params->nslices / 2, params->radius_searchspace[2]) +
          params->radius_patchspace[2],
      params->radius_searchspace[0] + params->radius_patchspace[0],
      params->radius_searchspace[1] + params->radius_patchspace[1],
      std::min(params->nslices / 2, params->radius_searchspace[2]) +
          params->radius_patchspace[2]};

  if (iter == 1) {
    float *tmp = pad_reflective(image_raw, padding, shape, shape_padded);
    std::swap(tmp, image_raw);
    free(tmp);

    previous_result = image_raw;
  } else {
    float *tmp = pad_reflective(previous_result, padding, shape, shape_padded);

    std::swap(tmp, previous_result);
    free(tmp);
  }
  //////////////////////////////////////////////////////////////////////////////

  if (iter == 1) {
    search_positions = setup_searchspace(shape_padded, params, nsize_search);
    patch_positions = setup_patchspace(shape_padded, params, nsize_patch);
    distweight = setup_distweight(shape_padded, params);
  }

  float *next_result = (float *)malloc(nstack * sizeof(*next_result));

  int evalcounter = 0;
  auto time0 = std::chrono::high_resolution_clock::now();

#pragma omp parallel for
  for (int i = 0; i < shape[2]; i++) {
    float sigma = sigmalist[i];
    float multiplier =
        -1.f / (sigma * sigma *
                params->beta); // changes depending on way of implementation.
                               // Beta is available if control needed

    if (params->radius_patchspace[0] == 1 &&
        params->radius_patchspace[1] == 1 && params->radius_patchspace[2] == 1)
      filterslice_p111(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 1 &&
             params->radius_patchspace[1] == 1 &&
             params->radius_patchspace[2] == 2)
      filterslice_p112(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 1 &&
             params->radius_patchspace[1] == 1 &&
             params->radius_patchspace[2] == 3)
      filterslice_p113(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 2 &&
             params->radius_patchspace[1] == 2 &&
             params->radius_patchspace[2] == 1)
      filterslice_p221(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 2 &&
             params->radius_patchspace[1] == 2 &&
             params->radius_patchspace[2] == 2)
      filterslice_p222(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 3 &&
             params->radius_patchspace[1] == 3 &&
             params->radius_patchspace[2] == 1)
      filterslice_p331(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 3 &&
             params->radius_patchspace[1] == 3 &&
             params->radius_patchspace[2] == 2)
      filterslice_p332(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else if (params->radius_patchspace[0] == 3 &&
             params->radius_patchspace[1] == 3 &&
             params->radius_patchspace[2] == 3)
      filterslice_p333(i, multiplier, image_raw, previous_result, next_result,
                       shape, params);
    else
      filterslice(i, multiplier, image_raw, previous_result, next_result, shape,
                  params);

      // console output
      ////////////////////////////////////////////////////////////////////////////////////////////
#ifdef _OPENMP
    int tid = omp_get_thread_num();
#else
    int tid = 0;
#endif
    if (verbose && tid == 0) {
      evalcounter++;
      auto time_final = std::chrono::high_resolution_clock::now();
      std::chrono::duration<double> elapsed_total = time_final - time0;
      // std::cout << "iteration " << iter << ": " << std::min(shape[2],
      // evalcounter*params->cpu.max_threads) << "/" << shape[2] << ", "
      //		<<
      // round(elapsed_total.count()/evalcounter*10.)/(10.f*params->cpu.max_threads)*(shape[2]-std::min(shape[2],
      // evalcounter*params->cpu.max_threads))
      //		<< " s remaining          \r";
      // std::cout.flush();
    }
    ////////////////////////////////////////////////////////////////////////////////////////////
  }

  // std::cout << "Exit loop" << std::endl;

  auto time_final = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> elapsed_total = time_final - time0;
  // if (verbose)
  //{
  //	std::cout << "iteration " << iter << " took " <<
  // round(elapsed_total.count()*10.)/10. << " s                          " <<
  // std::endl;
  // }

  if (iter != 1)
    free(previous_result);
  //////////////////////////////////////////////////////////////////////////////

  return next_result;
}

/*******************************************************************************************************************************************************************/
/*******************************************************************************************************************************************************************/

void IterativeNonLocalMeansCPU::filterslice(
    int z0, float multiplier, float *image_raw, float *image_prefiltered,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  long long int nslice = nx * ny;
  long long int offset = (z0 + zpad) * nslice;
  long long int nslice_unpadded = shape[0] * shape[1];
  long long int offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      long long int idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      // get patchvalues at origin
      /////////////////////////////////////////////////////////////////////////
      float *values_origin =
          (float *)malloc(nsize_patch * sizeof(*values_origin));

      for (int p = 0; p < nsize_patch; p++)
        values_origin[p] = image_prefiltered[idx0 + patch_positions[p]];
      /////////////////////////////////////////////////////////////////////////

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        long long int idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        for (int p = 0; p < nsize_patch; p++) {
          float tmp =
              image_prefiltered[idx1 + patch_positions[p]] - values_origin[p];
          distance += (tmp * tmp) * distweight[p];
        }
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      free(values_origin);

      // continue image space
    }
  }

  return;
}

void IterativeNonLocalMeansCPU::filterslice_p111(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.142857143f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.142857143f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.142857143f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.142857143f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.142857143f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.142857143f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.142857143f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p112(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.04f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p113(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];
  idx_type ppos9 = patch_positions[9];
  idx_type ppos10 = patch_positions[10];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];
      float val_orig9 = image_previous[idx0 + ppos9];
      float val_orig10 = image_previous[idx0 + ppos10];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos9] - val_orig9;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos10] - val_orig10;
        distance += (tmp * tmp) * 0.0204082f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p221(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];
  idx_type ppos9 = patch_positions[9];
  idx_type ppos10 = patch_positions[10];
  idx_type ppos11 = patch_positions[11];
  idx_type ppos12 = patch_positions[12];
  idx_type ppos13 = patch_positions[13];
  idx_type ppos14 = patch_positions[14];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];
      float val_orig9 = image_previous[idx0 + ppos9];
      float val_orig10 = image_previous[idx0 + ppos10];
      float val_orig11 = image_previous[idx0 + ppos11];
      float val_orig12 = image_previous[idx0 + ppos12];
      float val_orig13 = image_previous[idx0 + ppos13];
      float val_orig14 = image_previous[idx0 + ppos14];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos9] - val_orig9;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos10] - val_orig10;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos11] - val_orig11;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos12] - val_orig12;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos13] - val_orig13;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos14] - val_orig14;
        distance += (tmp * tmp) * 0.111111f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p222(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];
  idx_type ppos9 = patch_positions[9];
  idx_type ppos10 = patch_positions[10];
  idx_type ppos11 = patch_positions[11];
  idx_type ppos12 = patch_positions[12];
  idx_type ppos13 = patch_positions[13];
  idx_type ppos14 = patch_positions[14];
  idx_type ppos15 = patch_positions[15];
  idx_type ppos16 = patch_positions[16];
  idx_type ppos17 = patch_positions[17];
  idx_type ppos18 = patch_positions[18];
  idx_type ppos19 = patch_positions[19];
  idx_type ppos20 = patch_positions[20];
  idx_type ppos21 = patch_positions[21];
  idx_type ppos22 = patch_positions[22];
  idx_type ppos23 = patch_positions[23];
  idx_type ppos24 = patch_positions[24];
  idx_type ppos25 = patch_positions[25];
  idx_type ppos26 = patch_positions[26];
  idx_type ppos27 = patch_positions[27];
  idx_type ppos28 = patch_positions[28];
  idx_type ppos29 = patch_positions[29];
  idx_type ppos30 = patch_positions[30];
  idx_type ppos31 = patch_positions[31];
  idx_type ppos32 = patch_positions[32];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];
      float val_orig9 = image_previous[idx0 + ppos9];
      float val_orig10 = image_previous[idx0 + ppos10];
      float val_orig11 = image_previous[idx0 + ppos11];
      float val_orig12 = image_previous[idx0 + ppos12];
      float val_orig13 = image_previous[idx0 + ppos13];
      float val_orig14 = image_previous[idx0 + ppos14];
      float val_orig15 = image_previous[idx0 + ppos15];
      float val_orig16 = image_previous[idx0 + ppos16];
      float val_orig17 = image_previous[idx0 + ppos17];
      float val_orig18 = image_previous[idx0 + ppos18];
      float val_orig19 = image_previous[idx0 + ppos19];
      float val_orig20 = image_previous[idx0 + ppos20];
      float val_orig21 = image_previous[idx0 + ppos21];
      float val_orig22 = image_previous[idx0 + ppos22];
      float val_orig23 = image_previous[idx0 + ppos23];
      float val_orig24 = image_previous[idx0 + ppos24];
      float val_orig25 = image_previous[idx0 + ppos25];
      float val_orig26 = image_previous[idx0 + ppos26];
      float val_orig27 = image_previous[idx0 + ppos27];
      float val_orig28 = image_previous[idx0 + ppos28];
      float val_orig29 = image_previous[idx0 + ppos29];
      float val_orig30 = image_previous[idx0 + ppos30];
      float val_orig31 = image_previous[idx0 + ppos31];
      float val_orig32 = image_previous[idx0 + ppos32];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos9] - val_orig9;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos10] - val_orig10;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos11] - val_orig11;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos12] - val_orig12;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos13] - val_orig13;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos14] - val_orig14;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos15] - val_orig15;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos16] - val_orig16;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos17] - val_orig17;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos18] - val_orig18;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos19] - val_orig19;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos20] - val_orig20;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos21] - val_orig21;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos22] - val_orig22;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos23] - val_orig23;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos24] - val_orig24;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos25] - val_orig25;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos26] - val_orig26;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos27] - val_orig27;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos28] - val_orig28;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos29] - val_orig29;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos30] - val_orig30;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos31] - val_orig31;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos32] - val_orig32;
        distance += (tmp * tmp) * 0.04f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p331(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];
  idx_type ppos9 = patch_positions[9];
  idx_type ppos10 = patch_positions[10];
  idx_type ppos11 = patch_positions[11];
  idx_type ppos12 = patch_positions[12];
  idx_type ppos13 = patch_positions[13];
  idx_type ppos14 = patch_positions[14];
  idx_type ppos15 = patch_positions[15];
  idx_type ppos16 = patch_positions[16];
  idx_type ppos17 = patch_positions[17];
  idx_type ppos18 = patch_positions[18];
  idx_type ppos19 = patch_positions[19];
  idx_type ppos20 = patch_positions[20];
  idx_type ppos21 = patch_positions[21];
  idx_type ppos22 = patch_positions[22];
  idx_type ppos23 = patch_positions[23];
  idx_type ppos24 = patch_positions[24];
  idx_type ppos25 = patch_positions[25];
  idx_type ppos26 = patch_positions[26];
  idx_type ppos27 = patch_positions[27];
  idx_type ppos28 = patch_positions[28];
  idx_type ppos29 = patch_positions[29];
  idx_type ppos30 = patch_positions[30];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];
      float val_orig9 = image_previous[idx0 + ppos9];
      float val_orig10 = image_previous[idx0 + ppos10];
      float val_orig11 = image_previous[idx0 + ppos11];
      float val_orig12 = image_previous[idx0 + ppos12];
      float val_orig13 = image_previous[idx0 + ppos13];
      float val_orig14 = image_previous[idx0 + ppos14];
      float val_orig15 = image_previous[idx0 + ppos15];
      float val_orig16 = image_previous[idx0 + ppos16];
      float val_orig17 = image_previous[idx0 + ppos17];
      float val_orig18 = image_previous[idx0 + ppos18];
      float val_orig19 = image_previous[idx0 + ppos19];
      float val_orig20 = image_previous[idx0 + ppos20];
      float val_orig21 = image_previous[idx0 + ppos21];
      float val_orig22 = image_previous[idx0 + ppos22];
      float val_orig23 = image_previous[idx0 + ppos23];
      float val_orig24 = image_previous[idx0 + ppos24];
      float val_orig25 = image_previous[idx0 + ppos25];
      float val_orig26 = image_previous[idx0 + ppos26];
      float val_orig27 = image_previous[idx0 + ppos27];
      float val_orig28 = image_previous[idx0 + ppos28];
      float val_orig29 = image_previous[idx0 + ppos29];
      float val_orig30 = image_previous[idx0 + ppos30];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos9] - val_orig9;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos10] - val_orig10;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos11] - val_orig11;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos12] - val_orig12;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos13] - val_orig13;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos14] - val_orig14;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos15] - val_orig15;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos16] - val_orig16;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos17] - val_orig17;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos18] - val_orig18;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos19] - val_orig19;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos20] - val_orig20;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos21] - val_orig21;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos22] - val_orig22;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos23] - val_orig23;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos24] - val_orig24;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos25] - val_orig25;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos26] - val_orig26;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos27] - val_orig27;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos28] - val_orig28;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos29] - val_orig29;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos30] - val_orig30;
        distance += (tmp * tmp) * 0.111111f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p332(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];
  idx_type ppos9 = patch_positions[9];
  idx_type ppos10 = patch_positions[10];
  idx_type ppos11 = patch_positions[11];
  idx_type ppos12 = patch_positions[12];
  idx_type ppos13 = patch_positions[13];
  idx_type ppos14 = patch_positions[14];
  idx_type ppos15 = patch_positions[15];
  idx_type ppos16 = patch_positions[16];
  idx_type ppos17 = patch_positions[17];
  idx_type ppos18 = patch_positions[18];
  idx_type ppos19 = patch_positions[19];
  idx_type ppos20 = patch_positions[20];
  idx_type ppos21 = patch_positions[21];
  idx_type ppos22 = patch_positions[22];
  idx_type ppos23 = patch_positions[23];
  idx_type ppos24 = patch_positions[24];
  idx_type ppos25 = patch_positions[25];
  idx_type ppos26 = patch_positions[26];
  idx_type ppos27 = patch_positions[27];
  idx_type ppos28 = patch_positions[28];
  idx_type ppos29 = patch_positions[29];
  idx_type ppos30 = patch_positions[30];
  idx_type ppos31 = patch_positions[31];
  idx_type ppos32 = patch_positions[32];
  idx_type ppos33 = patch_positions[33];
  idx_type ppos34 = patch_positions[34];
  idx_type ppos35 = patch_positions[35];
  idx_type ppos36 = patch_positions[36];
  idx_type ppos37 = patch_positions[37];
  idx_type ppos38 = patch_positions[38];
  idx_type ppos39 = patch_positions[39];
  idx_type ppos40 = patch_positions[40];
  idx_type ppos41 = patch_positions[41];
  idx_type ppos42 = patch_positions[42];
  idx_type ppos43 = patch_positions[43];
  idx_type ppos44 = patch_positions[44];
  idx_type ppos45 = patch_positions[45];
  idx_type ppos46 = patch_positions[46];
  idx_type ppos47 = patch_positions[47];
  idx_type ppos48 = patch_positions[48];
  idx_type ppos49 = patch_positions[49];
  idx_type ppos50 = patch_positions[50];
  idx_type ppos51 = patch_positions[51];
  idx_type ppos52 = patch_positions[52];
  idx_type ppos53 = patch_positions[53];
  idx_type ppos54 = patch_positions[54];
  idx_type ppos55 = patch_positions[55];
  idx_type ppos56 = patch_positions[56];
  idx_type ppos57 = patch_positions[57];
  idx_type ppos58 = patch_positions[58];
  idx_type ppos59 = patch_positions[59];
  idx_type ppos60 = patch_positions[60];
  idx_type ppos61 = patch_positions[61];
  idx_type ppos62 = patch_positions[62];
  idx_type ppos63 = patch_positions[63];
  idx_type ppos64 = patch_positions[64];
  idx_type ppos65 = patch_positions[65];
  idx_type ppos66 = patch_positions[66];
  idx_type ppos67 = patch_positions[67];
  idx_type ppos68 = patch_positions[68];
  idx_type ppos69 = patch_positions[69];
  idx_type ppos70 = patch_positions[70];
  idx_type ppos71 = patch_positions[71];
  idx_type ppos72 = patch_positions[72];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];
      float val_orig9 = image_previous[idx0 + ppos9];
      float val_orig10 = image_previous[idx0 + ppos10];
      float val_orig11 = image_previous[idx0 + ppos11];
      float val_orig12 = image_previous[idx0 + ppos12];
      float val_orig13 = image_previous[idx0 + ppos13];
      float val_orig14 = image_previous[idx0 + ppos14];
      float val_orig15 = image_previous[idx0 + ppos15];
      float val_orig16 = image_previous[idx0 + ppos16];
      float val_orig17 = image_previous[idx0 + ppos17];
      float val_orig18 = image_previous[idx0 + ppos18];
      float val_orig19 = image_previous[idx0 + ppos19];
      float val_orig20 = image_previous[idx0 + ppos20];
      float val_orig21 = image_previous[idx0 + ppos21];
      float val_orig22 = image_previous[idx0 + ppos22];
      float val_orig23 = image_previous[idx0 + ppos23];
      float val_orig24 = image_previous[idx0 + ppos24];
      float val_orig25 = image_previous[idx0 + ppos25];
      float val_orig26 = image_previous[idx0 + ppos26];
      float val_orig27 = image_previous[idx0 + ppos27];
      float val_orig28 = image_previous[idx0 + ppos28];
      float val_orig29 = image_previous[idx0 + ppos29];
      float val_orig30 = image_previous[idx0 + ppos30];
      float val_orig31 = image_previous[idx0 + ppos31];
      float val_orig32 = image_previous[idx0 + ppos32];
      float val_orig33 = image_previous[idx0 + ppos33];
      float val_orig34 = image_previous[idx0 + ppos34];
      float val_orig35 = image_previous[idx0 + ppos35];
      float val_orig36 = image_previous[idx0 + ppos36];
      float val_orig37 = image_previous[idx0 + ppos37];
      float val_orig38 = image_previous[idx0 + ppos38];
      float val_orig39 = image_previous[idx0 + ppos39];
      float val_orig40 = image_previous[idx0 + ppos40];
      float val_orig41 = image_previous[idx0 + ppos41];
      float val_orig42 = image_previous[idx0 + ppos42];
      float val_orig43 = image_previous[idx0 + ppos43];
      float val_orig44 = image_previous[idx0 + ppos44];
      float val_orig45 = image_previous[idx0 + ppos45];
      float val_orig46 = image_previous[idx0 + ppos46];
      float val_orig47 = image_previous[idx0 + ppos47];
      float val_orig48 = image_previous[idx0 + ppos48];
      float val_orig49 = image_previous[idx0 + ppos49];
      float val_orig50 = image_previous[idx0 + ppos50];
      float val_orig51 = image_previous[idx0 + ppos51];
      float val_orig52 = image_previous[idx0 + ppos52];
      float val_orig53 = image_previous[idx0 + ppos53];
      float val_orig54 = image_previous[idx0 + ppos54];
      float val_orig55 = image_previous[idx0 + ppos55];
      float val_orig56 = image_previous[idx0 + ppos56];
      float val_orig57 = image_previous[idx0 + ppos57];
      float val_orig58 = image_previous[idx0 + ppos58];
      float val_orig59 = image_previous[idx0 + ppos59];
      float val_orig60 = image_previous[idx0 + ppos60];
      float val_orig61 = image_previous[idx0 + ppos61];
      float val_orig62 = image_previous[idx0 + ppos62];
      float val_orig63 = image_previous[idx0 + ppos63];
      float val_orig64 = image_previous[idx0 + ppos64];
      float val_orig65 = image_previous[idx0 + ppos65];
      float val_orig66 = image_previous[idx0 + ppos66];
      float val_orig67 = image_previous[idx0 + ppos67];
      float val_orig68 = image_previous[idx0 + ppos68];
      float val_orig69 = image_previous[idx0 + ppos69];
      float val_orig70 = image_previous[idx0 + ppos70];
      float val_orig71 = image_previous[idx0 + ppos71];
      float val_orig72 = image_previous[idx0 + ppos72];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos9] - val_orig9;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos10] - val_orig10;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos11] - val_orig11;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos12] - val_orig12;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos13] - val_orig13;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos14] - val_orig14;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos15] - val_orig15;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos16] - val_orig16;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos17] - val_orig17;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos18] - val_orig18;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos19] - val_orig19;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos20] - val_orig20;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos21] - val_orig21;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos22] - val_orig22;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos23] - val_orig23;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos24] - val_orig24;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos25] - val_orig25;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos26] - val_orig26;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos27] - val_orig27;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos28] - val_orig28;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos29] - val_orig29;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos30] - val_orig30;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos31] - val_orig31;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos32] - val_orig32;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos33] - val_orig33;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos34] - val_orig34;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos35] - val_orig35;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos36] - val_orig36;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos37] - val_orig37;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos38] - val_orig38;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos39] - val_orig39;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos40] - val_orig40;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos41] - val_orig41;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos42] - val_orig42;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos43] - val_orig43;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos44] - val_orig44;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos45] - val_orig45;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos46] - val_orig46;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos47] - val_orig47;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos48] - val_orig48;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos49] - val_orig49;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos50] - val_orig50;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos51] - val_orig51;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos52] - val_orig52;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos53] - val_orig53;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos54] - val_orig54;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos55] - val_orig55;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos56] - val_orig56;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos57] - val_orig57;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos58] - val_orig58;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos59] - val_orig59;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos60] - val_orig60;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos61] - val_orig61;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos62] - val_orig62;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos63] - val_orig63;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos64] - val_orig64;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos65] - val_orig65;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos66] - val_orig66;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos67] - val_orig67;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos68] - val_orig68;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos69] - val_orig69;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos70] - val_orig70;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos71] - val_orig71;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos72] - val_orig72;
        distance += (tmp * tmp) * 0.04f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
void IterativeNonLocalMeansCPU::filterslice_p333(
    int z0, float multiplier, float *image_raw, float *image_previous,
    float *result, int shape[3], protocol::DenoiseParameters *params) {
  // Image space
  //////////////////////////////////////////////////////////////////////////////
  int xpad = params->radius_searchspace[0] + params->radius_patchspace[0];
  int ypad = params->radius_searchspace[1] + params->radius_patchspace[1];
  int zpad = std::min(params->nslices / 2, params->radius_searchspace[2]) +
             params->radius_patchspace[2];

  int nx = shape[0] + 2 * xpad;
  int ny = shape[1] + 2 * ypad;
  idx_type nslice = nx * ny;
  idx_type offset = (z0 + zpad) * nslice;
  idx_type nslice_unpadded = shape[0] * shape[1];
  idx_type offset_unpadded = z0 * nslice_unpadded;
  //////////////////////////////////////////////////////////////////////////////

  idx_type ppos1 = patch_positions[1];
  idx_type ppos2 = patch_positions[2];
  idx_type ppos3 = patch_positions[3];
  idx_type ppos4 = patch_positions[4];
  idx_type ppos5 = patch_positions[5];
  idx_type ppos6 = patch_positions[6];
  idx_type ppos7 = patch_positions[7];
  idx_type ppos8 = patch_positions[8];
  idx_type ppos9 = patch_positions[9];
  idx_type ppos10 = patch_positions[10];
  idx_type ppos11 = patch_positions[11];
  idx_type ppos12 = patch_positions[12];
  idx_type ppos13 = patch_positions[13];
  idx_type ppos14 = patch_positions[14];
  idx_type ppos15 = patch_positions[15];
  idx_type ppos16 = patch_positions[16];
  idx_type ppos17 = patch_positions[17];
  idx_type ppos18 = patch_positions[18];
  idx_type ppos19 = patch_positions[19];
  idx_type ppos20 = patch_positions[20];
  idx_type ppos21 = patch_positions[21];
  idx_type ppos22 = patch_positions[22];
  idx_type ppos23 = patch_positions[23];
  idx_type ppos24 = patch_positions[24];
  idx_type ppos25 = patch_positions[25];
  idx_type ppos26 = patch_positions[26];
  idx_type ppos27 = patch_positions[27];
  idx_type ppos28 = patch_positions[28];
  idx_type ppos29 = patch_positions[29];
  idx_type ppos30 = patch_positions[30];
  idx_type ppos31 = patch_positions[31];
  idx_type ppos32 = patch_positions[32];
  idx_type ppos33 = patch_positions[33];
  idx_type ppos34 = patch_positions[34];
  idx_type ppos35 = patch_positions[35];
  idx_type ppos36 = patch_positions[36];
  idx_type ppos37 = patch_positions[37];
  idx_type ppos38 = patch_positions[38];
  idx_type ppos39 = patch_positions[39];
  idx_type ppos40 = patch_positions[40];
  idx_type ppos41 = patch_positions[41];
  idx_type ppos42 = patch_positions[42];
  idx_type ppos43 = patch_positions[43];
  idx_type ppos44 = patch_positions[44];
  idx_type ppos45 = patch_positions[45];
  idx_type ppos46 = patch_positions[46];
  idx_type ppos47 = patch_positions[47];
  idx_type ppos48 = patch_positions[48];
  idx_type ppos49 = patch_positions[49];
  idx_type ppos50 = patch_positions[50];
  idx_type ppos51 = patch_positions[51];
  idx_type ppos52 = patch_positions[52];
  idx_type ppos53 = patch_positions[53];
  idx_type ppos54 = patch_positions[54];
  idx_type ppos55 = patch_positions[55];
  idx_type ppos56 = patch_positions[56];
  idx_type ppos57 = patch_positions[57];
  idx_type ppos58 = patch_positions[58];
  idx_type ppos59 = patch_positions[59];
  idx_type ppos60 = patch_positions[60];
  idx_type ppos61 = patch_positions[61];
  idx_type ppos62 = patch_positions[62];
  idx_type ppos63 = patch_positions[63];
  idx_type ppos64 = patch_positions[64];
  idx_type ppos65 = patch_positions[65];
  idx_type ppos66 = patch_positions[66];
  idx_type ppos67 = patch_positions[67];
  idx_type ppos68 = patch_positions[68];
  idx_type ppos69 = patch_positions[69];
  idx_type ppos70 = patch_positions[70];
  idx_type ppos71 = patch_positions[71];
  idx_type ppos72 = patch_positions[72];
  idx_type ppos73 = patch_positions[73];
  idx_type ppos74 = patch_positions[74];
  idx_type ppos75 = patch_positions[75];
  idx_type ppos76 = patch_positions[76];
  idx_type ppos77 = patch_positions[77];
  idx_type ppos78 = patch_positions[78];
  idx_type ppos79 = patch_positions[79];
  idx_type ppos80 = patch_positions[80];
  idx_type ppos81 = patch_positions[81];
  idx_type ppos82 = patch_positions[82];
  idx_type ppos83 = patch_positions[83];
  idx_type ppos84 = patch_positions[84];
  idx_type ppos85 = patch_positions[85];
  idx_type ppos86 = patch_positions[86];
  idx_type ppos87 = patch_positions[87];
  idx_type ppos88 = patch_positions[88];
  idx_type ppos89 = patch_positions[89];
  idx_type ppos90 = patch_positions[90];
  idx_type ppos91 = patch_positions[91];
  idx_type ppos92 = patch_positions[92];
  idx_type ppos93 = patch_positions[93];
  idx_type ppos94 = patch_positions[94];
  idx_type ppos95 = patch_positions[95];
  idx_type ppos96 = patch_positions[96];
  idx_type ppos97 = patch_positions[97];
  idx_type ppos98 = patch_positions[98];
  idx_type ppos99 = patch_positions[99];
  idx_type ppos100 = patch_positions[100];
  idx_type ppos101 = patch_positions[101];
  idx_type ppos102 = patch_positions[102];
  idx_type ppos103 = patch_positions[103];
  idx_type ppos104 = patch_positions[104];
  idx_type ppos105 = patch_positions[105];
  idx_type ppos106 = patch_positions[106];
  idx_type ppos107 = patch_positions[107];
  idx_type ppos108 = patch_positions[108];
  idx_type ppos109 = patch_positions[109];
  idx_type ppos110 = patch_positions[110];
  idx_type ppos111 = patch_positions[111];
  idx_type ppos112 = patch_positions[112];
  idx_type ppos113 = patch_positions[113];
  idx_type ppos114 = patch_positions[114];

  // loop over slice
  for (int y0 = ypad; y0 < ny - ypad; y0++) {
    for (int x0 = xpad; x0 < nx - xpad; x0++) {
      idx_type idx0 = offset + y0 * nx + x0;
      float noisy_value_origin = image_raw[idx0];

      float val_orig0 = image_previous[idx0];
      float val_orig1 = image_previous[idx0 + ppos1];
      float val_orig2 = image_previous[idx0 + ppos2];
      float val_orig3 = image_previous[idx0 + ppos3];
      float val_orig4 = image_previous[idx0 + ppos4];
      float val_orig5 = image_previous[idx0 + ppos5];
      float val_orig6 = image_previous[idx0 + ppos6];
      float val_orig7 = image_previous[idx0 + ppos7];
      float val_orig8 = image_previous[idx0 + ppos8];
      float val_orig9 = image_previous[idx0 + ppos9];
      float val_orig10 = image_previous[idx0 + ppos10];
      float val_orig11 = image_previous[idx0 + ppos11];
      float val_orig12 = image_previous[idx0 + ppos12];
      float val_orig13 = image_previous[idx0 + ppos13];
      float val_orig14 = image_previous[idx0 + ppos14];
      float val_orig15 = image_previous[idx0 + ppos15];
      float val_orig16 = image_previous[idx0 + ppos16];
      float val_orig17 = image_previous[idx0 + ppos17];
      float val_orig18 = image_previous[idx0 + ppos18];
      float val_orig19 = image_previous[idx0 + ppos19];
      float val_orig20 = image_previous[idx0 + ppos20];
      float val_orig21 = image_previous[idx0 + ppos21];
      float val_orig22 = image_previous[idx0 + ppos22];
      float val_orig23 = image_previous[idx0 + ppos23];
      float val_orig24 = image_previous[idx0 + ppos24];
      float val_orig25 = image_previous[idx0 + ppos25];
      float val_orig26 = image_previous[idx0 + ppos26];
      float val_orig27 = image_previous[idx0 + ppos27];
      float val_orig28 = image_previous[idx0 + ppos28];
      float val_orig29 = image_previous[idx0 + ppos29];
      float val_orig30 = image_previous[idx0 + ppos30];
      float val_orig31 = image_previous[idx0 + ppos31];
      float val_orig32 = image_previous[idx0 + ppos32];
      float val_orig33 = image_previous[idx0 + ppos33];
      float val_orig34 = image_previous[idx0 + ppos34];
      float val_orig35 = image_previous[idx0 + ppos35];
      float val_orig36 = image_previous[idx0 + ppos36];
      float val_orig37 = image_previous[idx0 + ppos37];
      float val_orig38 = image_previous[idx0 + ppos38];
      float val_orig39 = image_previous[idx0 + ppos39];
      float val_orig40 = image_previous[idx0 + ppos40];
      float val_orig41 = image_previous[idx0 + ppos41];
      float val_orig42 = image_previous[idx0 + ppos42];
      float val_orig43 = image_previous[idx0 + ppos43];
      float val_orig44 = image_previous[idx0 + ppos44];
      float val_orig45 = image_previous[idx0 + ppos45];
      float val_orig46 = image_previous[idx0 + ppos46];
      float val_orig47 = image_previous[idx0 + ppos47];
      float val_orig48 = image_previous[idx0 + ppos48];
      float val_orig49 = image_previous[idx0 + ppos49];
      float val_orig50 = image_previous[idx0 + ppos50];
      float val_orig51 = image_previous[idx0 + ppos51];
      float val_orig52 = image_previous[idx0 + ppos52];
      float val_orig53 = image_previous[idx0 + ppos53];
      float val_orig54 = image_previous[idx0 + ppos54];
      float val_orig55 = image_previous[idx0 + ppos55];
      float val_orig56 = image_previous[idx0 + ppos56];
      float val_orig57 = image_previous[idx0 + ppos57];
      float val_orig58 = image_previous[idx0 + ppos58];
      float val_orig59 = image_previous[idx0 + ppos59];
      float val_orig60 = image_previous[idx0 + ppos60];
      float val_orig61 = image_previous[idx0 + ppos61];
      float val_orig62 = image_previous[idx0 + ppos62];
      float val_orig63 = image_previous[idx0 + ppos63];
      float val_orig64 = image_previous[idx0 + ppos64];
      float val_orig65 = image_previous[idx0 + ppos65];
      float val_orig66 = image_previous[idx0 + ppos66];
      float val_orig67 = image_previous[idx0 + ppos67];
      float val_orig68 = image_previous[idx0 + ppos68];
      float val_orig69 = image_previous[idx0 + ppos69];
      float val_orig70 = image_previous[idx0 + ppos70];
      float val_orig71 = image_previous[idx0 + ppos71];
      float val_orig72 = image_previous[idx0 + ppos72];
      float val_orig73 = image_previous[idx0 + ppos73];
      float val_orig74 = image_previous[idx0 + ppos74];
      float val_orig75 = image_previous[idx0 + ppos75];
      float val_orig76 = image_previous[idx0 + ppos76];
      float val_orig77 = image_previous[idx0 + ppos77];
      float val_orig78 = image_previous[idx0 + ppos78];
      float val_orig79 = image_previous[idx0 + ppos79];
      float val_orig80 = image_previous[idx0 + ppos80];
      float val_orig81 = image_previous[idx0 + ppos81];
      float val_orig82 = image_previous[idx0 + ppos82];
      float val_orig83 = image_previous[idx0 + ppos83];
      float val_orig84 = image_previous[idx0 + ppos84];
      float val_orig85 = image_previous[idx0 + ppos85];
      float val_orig86 = image_previous[idx0 + ppos86];
      float val_orig87 = image_previous[idx0 + ppos87];
      float val_orig88 = image_previous[idx0 + ppos88];
      float val_orig89 = image_previous[idx0 + ppos89];
      float val_orig90 = image_previous[idx0 + ppos90];
      float val_orig91 = image_previous[idx0 + ppos91];
      float val_orig92 = image_previous[idx0 + ppos92];
      float val_orig93 = image_previous[idx0 + ppos93];
      float val_orig94 = image_previous[idx0 + ppos94];
      float val_orig95 = image_previous[idx0 + ppos95];
      float val_orig96 = image_previous[idx0 + ppos96];
      float val_orig97 = image_previous[idx0 + ppos97];
      float val_orig98 = image_previous[idx0 + ppos98];
      float val_orig99 = image_previous[idx0 + ppos99];
      float val_orig100 = image_previous[idx0 + ppos100];
      float val_orig101 = image_previous[idx0 + ppos101];
      float val_orig102 = image_previous[idx0 + ppos102];
      float val_orig103 = image_previous[idx0 + ppos103];
      float val_orig104 = image_previous[idx0 + ppos104];
      float val_orig105 = image_previous[idx0 + ppos105];
      float val_orig106 = image_previous[idx0 + ppos106];
      float val_orig107 = image_previous[idx0 + ppos107];
      float val_orig108 = image_previous[idx0 + ppos108];
      float val_orig109 = image_previous[idx0 + ppos109];
      float val_orig110 = image_previous[idx0 + ppos110];
      float val_orig111 = image_previous[idx0 + ppos111];
      float val_orig112 = image_previous[idx0 + ppos112];
      float val_orig113 = image_previous[idx0 + ppos113];
      float val_orig114 = image_previous[idx0 + ppos114];

      // loop over search space
      /////////////////////////////////////////////////////////////////////////
      float filtervalue = 0.0f;
      float filterweight = 0.0f;
      float maxweight = 0.0f;

      for (int s = 0; s < nsize_search; s++) {
        idx_type idx1 = idx0 + search_positions[s];
        float noisy_value_searchpos = image_raw[idx1];

        // get patchvalues at search position
        /////////////////////////////////////////////////////////////////////////
        float distance = 0.0f;

        float tmp = 0.0f;
        tmp = image_previous[idx1] - val_orig0;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos1] - val_orig1;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos2] - val_orig2;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos3] - val_orig3;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos4] - val_orig4;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos5] - val_orig5;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos6] - val_orig6;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos7] - val_orig7;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos8] - val_orig8;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos9] - val_orig9;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos10] - val_orig10;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos11] - val_orig11;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos12] - val_orig12;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos13] - val_orig13;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos14] - val_orig14;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos15] - val_orig15;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos16] - val_orig16;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos17] - val_orig17;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos18] - val_orig18;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos19] - val_orig19;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos20] - val_orig20;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos21] - val_orig21;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos22] - val_orig22;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos23] - val_orig23;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos24] - val_orig24;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos25] - val_orig25;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos26] - val_orig26;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos27] - val_orig27;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos28] - val_orig28;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos29] - val_orig29;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos30] - val_orig30;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos31] - val_orig31;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos32] - val_orig32;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos33] - val_orig33;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos34] - val_orig34;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos35] - val_orig35;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos36] - val_orig36;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos37] - val_orig37;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos38] - val_orig38;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos39] - val_orig39;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos40] - val_orig40;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos41] - val_orig41;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos42] - val_orig42;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos43] - val_orig43;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos44] - val_orig44;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos45] - val_orig45;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos46] - val_orig46;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos47] - val_orig47;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos48] - val_orig48;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos49] - val_orig49;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos50] - val_orig50;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos51] - val_orig51;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos52] - val_orig52;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos53] - val_orig53;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos54] - val_orig54;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos55] - val_orig55;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos56] - val_orig56;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos57] - val_orig57;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos58] - val_orig58;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos59] - val_orig59;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos60] - val_orig60;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos61] - val_orig61;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos62] - val_orig62;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos63] - val_orig63;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos64] - val_orig64;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos65] - val_orig65;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos66] - val_orig66;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos67] - val_orig67;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos68] - val_orig68;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos69] - val_orig69;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos70] - val_orig70;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos71] - val_orig71;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos72] - val_orig72;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos73] - val_orig73;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos74] - val_orig74;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos75] - val_orig75;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos76] - val_orig76;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos77] - val_orig77;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos78] - val_orig78;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos79] - val_orig79;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos80] - val_orig80;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos81] - val_orig81;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos82] - val_orig82;
        distance += (tmp * tmp) * 0.111111f;
        tmp = image_previous[idx1 + ppos83] - val_orig83;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos84] - val_orig84;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos85] - val_orig85;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos86] - val_orig86;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos87] - val_orig87;
        distance += (tmp * tmp) * 0.0682275f;
        tmp = image_previous[idx1 + ppos88] - val_orig88;
        distance += (tmp * tmp) * 0.0501801f;
        tmp = image_previous[idx1 + ppos89] - val_orig89;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos90] - val_orig90;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos91] - val_orig91;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos92] - val_orig92;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos93] - val_orig93;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos94] - val_orig94;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos95] - val_orig95;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos96] - val_orig96;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos97] - val_orig97;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos98] - val_orig98;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos99] - val_orig99;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos100] - val_orig100;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos101] - val_orig101;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos102] - val_orig102;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos103] - val_orig103;
        distance += (tmp * tmp) * 0.04f;
        tmp = image_previous[idx1 + ppos104] - val_orig104;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos105] - val_orig105;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos106] - val_orig106;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos107] - val_orig107;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos108] - val_orig108;
        distance += (tmp * tmp) * 0.0333954f;
        tmp = image_previous[idx1 + ppos109] - val_orig109;
        distance += (tmp * tmp) * 0.0287373f;
        tmp = image_previous[idx1 + ppos110] - val_orig110;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos111] - val_orig111;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos112] - val_orig112;
        distance += (tmp * tmp) * 0.0225664f;
        tmp = image_previous[idx1 + ppos113] - val_orig113;
        distance += (tmp * tmp) * 0.0204082f;
        tmp = image_previous[idx1 + ppos114] - val_orig114;
        distance += (tmp * tmp) * 0.0204082f;
        /////////////////////////////////////////////////////////////////////////

        // weight the patch
        /////////////////////////////////////////////////////////////////////////
        distance = distance * multiplier;
        // float this_weight = expf(distance); //primary time sink, using
        // approximation instead
        float this_weight = (distance > expapproximation_cutoff)
                                ? expapproximation(distance)
                                : 0.0f;

        filtervalue += this_weight * noisy_value_searchpos;
        filterweight += this_weight;

        if (this_weight > maxweight)
          maxweight = this_weight;
        /////////////////////////////////////////////////////////////////////////
      }
      /////////////////////////////////////////////////////////////////////////

      if (maxweight > 0.0f) {
        filtervalue += maxweight * noisy_value_origin;
        filterweight += maxweight;

        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            filtervalue / filterweight;
      } else
        result[offset_unpadded + (y0 - ypad) * shape[0] + x0 - xpad] =
            noisy_value_origin;

      // continue image space
    }
  }

  return;
}
} // namespace denoise

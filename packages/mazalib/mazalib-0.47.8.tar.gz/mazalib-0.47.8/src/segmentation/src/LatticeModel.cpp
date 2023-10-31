#include "LatticeModel.h"

LatticeModel::LatticeModel(int nLabels) : mLabels(nLabels) {
  means = new double[mLabels];
  vars = new double[mLabels];
}

LatticeModel::LatticeModel(const LatticeModel &) {}

LatticeModel::~LatticeModel() {
  delete[] means;
  delete[] vars;
}
void LatticeModel::ConditionalImage(const std::vector<int> &I,
                                    std::vector<int> &C,
                                    IThreshold<int, std::vector<int>> &thresh) {
  Iter cit = C.begin();
  std::vector<double> L = thresh.LowThresholds();
  std::vector<double> H = thresh.HighThresholds();
  for (auto it = I.begin(); it != I.end(); ++it, ++cit) {
    *cit = mLabels;
    auto v = *it;
    for (int i = 0; i < mLabels; i++) {
      if ((v >= L[i]) && (v <= H[i])) {
        *cit = i;
        continue;
      }
    }
  }
}
void LatticeModel::ConditionalImage2Labels(
    const std::vector<int> &I, std::vector<int> &C,
    IThreshold<int, std::vector<int>> &thresh) {
  auto it = I.begin();

  for (auto cit = C.begin(); cit < C.end(); cit++, it++) {
    if (*it > thresh.High()) {
      *cit = 1;
    } else {
      if (*it <= thresh.Low()) {
        *cit = 0;
      } else {
        *cit = 2;
      }
    }
  }
}

void LatticeModel::ApplyUnsharpMask(const std::vector<int> &img, size_t w,
                                    size_t h, size_t d,
                                    std::vector<int> &enhanced_img,
                                    float strength_factor) {
  const int mask_dim = 3;
  const int offset = 1;
  static int blur_mask[] = {1, 2, 1, 2, 4, 2, 1, 2, 1,

                            2, 4, 2, 4, 8, 4, 2, 4, 2,

                            1, 2, 1, 2, 4, 2, 1, 2, 1};

  auto layer_sz = h * w;
  for (size_t k = 0; k < d; k++) {
    for (size_t i = 0; i < h; i++) {
      for (size_t j = 0; j < w; j++) {
        // Collecting adjacent values
        int zustatsumme = 0;
        int blurred = 0;
        for (size_t m_z = 0; m_z < mask_dim; m_z++) {
          for (size_t m_y = 0; m_y < mask_dim; m_y++) {
            for (size_t m_x = 0; m_x < mask_dim; m_x++) {
              auto mask_pos = m_z * mask_dim * mask_dim + m_y * mask_dim + m_x;

              auto target_z = k + (m_z - offset);
              auto target_y = i + (m_y - offset);
              auto target_x = j + (m_x - offset);
              if (target_x >= 0 && target_x < w && target_y >= 0 &&
                  target_y < h && target_z >= 0 && target_z < d) {
                int intensity = *(img.cbegin() + layer_sz * target_z +
                                  w * target_y + target_x);
                blurred += blur_mask[mask_pos] * intensity;
                zustatsumme += blur_mask[mask_pos];
              }
            }
          }
        }

        float blurred_f = float(blurred) / zustatsumme;
        float enhanced = float(*(img.cbegin() + layer_sz * k + w * i + j)) *
                             (strength_factor + 1.0f) -
                         blurred_f * strength_factor;
        // if (enhanced < 0.0 || enhanced > 255.0)
        // {
        // 	std::cout << "Enhanced = " << enhanced << std::endl;
        // }
        int v = clamp_byte(int(floor(enhanced + 0.5f)));
        // std::cout << "Enhanced = " << v << std::endl;
        *(enhanced_img.begin() + layer_sz * k + w * i + j) =
            v; // clamp_byte(int(floor(enhanced + 0.5f)));
      }
    }
  }
}

int LatticeModel::SelectPhaseNormalized(const int &intensity_value) {
  int nPhase = 0;
  double delta1 = 10000000000;
  for (int i = 0; i < mLabels; i++) {
    double delta = abs(intensity_value - means[i]) / vars[i];
    if (delta < delta1) {
      delta1 = delta;
      nPhase = i;
    }
  }
  return nPhase;
}

int LatticeModel::SelectPhase(const int &it) {
  int nPhase = 0;
  double delta1 = 10000000000;
  for (int i = 0; i < mLabels; i++) {
    double delta = abs(it - means[i]); // / vars[i];
    if (delta < delta1) {
      delta1 = delta;
      nPhase = i;
    }
  }
  return nPhase;
}

void LatticeModel::Stats2L(const std::vector<int> &img, double High, double Low,
                           double &LMean, double &HMean, double &LVar,
                           double &HVar) {
  long long h = 1;
  long long l = 1;
  double H = High;
  double L = 0;
  int idbg = 0;
  for (auto it = img.begin(); it != img.end(); it++) {
    if (*it > High) {
      H += *it;
      h++;
    } else if (*it <= Low && *it > 0) {
      L += *it;
      l++;
    }
    idbg++;
  }
  L = L / l;
  H = H / h;

  double dH = 0;
  double dL = 0;
  idbg = 0;
  for (auto it = img.begin(); it != img.end(); it++) {
    if (*it > High) {
      double d = (*it - H);
      dH += d * d;
    } else if (*it <= Low && *it > 0) {
      double d = (*it - L);
      dL += d * d;
    }
    idbg++;
  }
  LMean = L;
  HMean = H;
  HVar = sqrt(dH / h);
  LVar = sqrt(dL / l);
}

void LatticeModel::StatsNL(const std::vector<int> &img,
                           const std::vector<double> &Highs,
                           const std::vector<double> &Lows, double *Means,
                           double *Vars) {
  assert(mLabels == Highs.size());
  assert(mLabels == Lows.size());
  double H = 0;
  double L = 0;
  int idbg = 0;

  long long *S = new long long[mLabels];
  for (int i = 0; i < mLabels; i++) {
    S[i] = 0;
    Means[i] = 0;
    Vars[i] = 0;
  }

  for (auto it = img.begin(); it != img.end(); it++) {
    for (int i = 0; i < mLabels; i++) {
      if (*it >= Lows[i] && *it < Highs[i]) {
        Means[i] += *it;
        S[i]++;
      };
    }
  }

  for (int i = 0; i < mLabels; i++) {
    if (S[i] != 0)
      Means[i] = Means[i] / S[i];
    S[i] = 0;
  }

  for (auto it = img.begin(); it != img.end(); it++) {
    auto v = *it;
    for (int i = 0; i < mLabels; i++) {
      if (v >= Lows[i] && v < Highs[i]) {
        double d = (v - Means[i]);
        Vars[i] += d * d;
        S[i]++;
      };
    }
  }

  for (int i = 0; i < mLabels; i++) {
    if (S[i] != 0)
      Vars[i] = sqrt(Vars[i] / S[i]);
  }

  delete[] S;
}

int LatticeModel::clamp_byte(int value) {
  if (value < 0) {
    return 0;
  } else if (value > 255) {
    return 255;
  } else {
    return value;
  }
}
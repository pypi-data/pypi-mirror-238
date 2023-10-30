#include <algorithm>
#include <cmath>
#include <numeric>

#include "threshold.h"
#include "util.h"

Histogram::Histogram(const std::vector<float> &v, int nbin)
    : DynamicArray<double>(nbin) {
  float min, max;
  Utils::minmax(v.begin(), v.end(), min, max);
  min_ = min;
  delta_ = (max - min_) / (size() - 1);
  histogram_generate(v.begin(), v.end(), x_0(), delta(), nbin, begin());
}

Histogram::Histogram(const std::vector<float> &v, float m, float M, int nbin)
    : DynamicArray<double>(nbin), min_(m) {
  std::string fname(
      "Histogram::Histogram(const vector<float>&, float, float, int, )");
  if (nbin < 2) {
    insert(end(), 100 - nbin, 0.0);
    nbin = 100;
  }

  delta_ = (M - min_) / (size() - 1);
  histogram_generate(v.begin(), v.end(), x_0(), delta(), nbin, begin());
}

Histogram::Histogram(const std::vector<int> &v, int nbin)
    : DynamicArray<double>(nbin) {
  int min, max;
  Utils::minmax(v.begin(), v.end(), min, max);
  min_ = double(min);
  delta_ = (max - min_) / (size() - 1);
  histogram_generate(v.begin(), v.end(), x_0(), delta(), nbin, begin());
}

Histogram::Histogram(const std::vector<int> &v, int m, int M, int nbin)
    : DynamicArray<double>(nbin), min_(m) {
  if (nbin < 2) {
    Utils::minmax(v.begin(), v.end(), m, M);

    insert(end(), 100 - nbin, 0.0);
    nbin = 100;
  }

  delta_ = double(M - min_) / (size() - 1);
  histogram_generate(v.begin(), v.end(), x_0(), delta(), nbin, begin());
}

Histogram::Histogram(const std::vector<unsigned char> &v, int nbin)
    : DynamicArray<double>(nbin) {
  int min, max;
  Utils::minmax(v.begin(), v.end(), min, max);
  min_ = double(min);
  delta_ = (max - min_) / (size() - 1);
  histogram_generate(v.begin(), v.end(), x_0(), delta(), nbin, begin());
}

Histogram::Histogram(const std::vector<unsigned char> &v, int m, int M,
                     int nbin)
    : DynamicArray<double>(nbin), min_(m) {
  if (nbin < 2) {
    Utils::minmax(v.begin(), v.end(), m, M);

    insert(end(), 100 - nbin, 0.0);
    nbin = 100;
  }

  delta_ = double(M - min_) / (size() - 1);
  histogram_generate(v.begin(), v.end(), x_0(), delta(), nbin, begin());
}

void Histogram::save(char *fname) const {
  std::ofstream file;
  file.open(fname);
  if (file.is_open()) {
    for (auto it = this->begin(); it != this->end(); it++)
      file << *it << '\n';
  }
  file.close();
}

void Histogram::Stats(double &M, double &V) {
  int i = 0;
  double D = 0;
  double S = 0;
  std::for_each(this->begin(), this->end(), [&](const double d) {
    S += i * delta() * d;
    i++;
    D += d;
  });
  M = S / D;
  S = D = 0;
  i = 0;
  std::for_each(this->begin(), this->end(), [&](const double d) {
    double ds = (i * delta() - M);
    S += ds * ds * d;
    i++;
    D += d;
  });
  V = std::sqrt(S / (D - 1));
}

CDF::CDF(const Histogram &hist)
    : DynamicArray<double>(hist.size() + 2), x_0_(hist.x_0() - hist.delta()),
      delta_(hist.delta()) {
  front() = 0.0;
  partial_sum(hist.begin(), hist.end(), begin() + 1);
  double total = *(end() - 2);
  vector<double>::iterator p;
  for (p = begin(); p < end(); ++p)
    *p /= total;
  back() = 1.0;
}

double CDF::F(double x) const {
  if (x <= x_0())
    return 0.0;
  if (x >= x_n())
    return 1.0;
  int i = int(floor((x - x_0()) / delta()));
  double x0 = x_0() + i * delta();
  return linear_interpolate(x, x0, x0 + delta(), (*this)[i], (*this)[i + 1]);
}

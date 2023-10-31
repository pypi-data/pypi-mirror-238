#pragma once

#include <algorithm>
#include <assert.h>
#include <math.h>
#include <numeric>
#include <string>

#include "DynamicArray.h"
#include "ExpectedMaximized.h"
#include "LogFile.h"
#include "NelderMead.h"
#include "util.h"

struct Mixture {
  double mu0, mu1;
  double sigma0, sigma1;
  double weight0;
};

enum ThreshodMethods {
  Th_nBinoms,
  Th_Manual,
  Th_Schluter,
  Th_PE1,
  Th_PE2,
  Th_entropy
};

struct ThresholdSettings {
  ThresholdSettings()
      : nPeaks(2), LowThreshold(20), HighThreshold(120), IsMultiphase(false),
        alpha(1.85), nPhases(2){};
  int nPeaks;
  int LowThreshold;
  int HighThreshold;
  ThreshodMethods ThresholdMethod;
  bool IsMultiphase;
  int nPhases;
  std::vector<double> Lows;
  std::vector<double> Highs;
  bool ManualThresholding;
  double OutLowThreshold;
  double OutHighThreshold;
  double alpha;
};

typedef struct THRESHOLD_ {
  char method_;
  int ilow, ihigh;
  double low, high;
  bool ManualThreshold;
  int nPeaks;
  double flatness;
  Mixture mix;
  double alpha;
} THRESHOLD;

class Histogram : public DynamicArray<double> {
  double min_;
  double delta_;

public:
  Histogram(const std::vector<float> &, float, float, int);
  Histogram(const std::vector<float> &, int);
  Histogram(const std::vector<int> &, int, int, int);
  Histogram(const std::vector<int> &, int);
  Histogram(const std::vector<unsigned char> &, int, int, int);
  Histogram(const std::vector<unsigned char> &, int);
  double minimum() const { return min_; }
  double x_0() const { return floor(min_ / delta_) * delta_; }
  double x_n() const { return x_0() + (size() - 1) * delta_; }
  double delta() const { return delta_; }
  void Stats(double &M, double &sigma);
  void save(char *fname) const;
};

template <class InputIterator, class OutputIterator>
void histogram_generate(const InputIterator vbegin, const InputIterator vend,
                        const double x0, const double delta, const int size,
                        OutputIterator begin) {
  fill(begin, begin + size, 0.0f);
  InputIterator p = vbegin;
  while (p != vend) {
    if (*p != ::ext_value(*vbegin)) {
      int bin_no = iround(double(*p - x0) / delta);
      if (bin_no >= 0 && bin_no < size)
        begin[bin_no] += 1.0;
    }
    ++p;
  }
}

class CDF : public DynamicArray<double> {
  double x_0_;
  double delta_;

public:
  CDF(const Histogram &);
  CDF(){};
  double x_0() const { return x_0_; }
  double x_n() const { return x_0() + (size() - 1) * delta_; }
  double delta() const { return delta_; }
  double F(double x) const;

  // TODO: Remove not implemented or find implementation
  // void draw(const std::string&, const  std::string= std::string("CDF"))
  // const;
};

template <class T = int, class container_type = std::vector<T>>
class SobelConvolution {
public:
  void compute_sobel(typename container_type::const_iterator &a_it,
                     typename container_type::iterator &a_dit, int ImgWidth,
                     int ImgHeight) {
    int shift_it = ImgWidth + 1;
    int shift_dit = ImgWidth + 1;
    auto it = a_it;
    auto dit = a_dit;
    for (int i = 1; i < ImgHeight - 1; i++) {
      for (int j = 1; j < ImgWidth - 1; j++) {
        shift_it = i * ImgWidth + j;
        it = a_it + shift_it;
        dit = a_dit + shift_it;
        int pm = *(it + ImgWidth - 1);
        int p = *(it + ImgWidth);
        int pp = *(it + ImgWidth + 1);

        int mm = *(it - ImgWidth - 1);
        int m = *(it - ImgWidth);
        int mp = *(it - ImgWidth + 1);

        int _m = *(it - 1);
        int _p = *(it + 1);

        int r = (pm + 2 * p + pp - mm - 2 * m - mp);
        int c = (mm + 2 * _m + pm - mp - 2 * _p - pm);
        T v = static_cast<T>(sqrt((r * r + c * c) / 2));
        *dit = v;
      }
    }
  }

  // Deprecated old version, replaced in Feb 2020
  void compute_sobel3D_old(const container_type &m, container_type &Dest,
                           int ImgWidth, int ImgHeight, int ImgDepth) {
    typename container_type::const_iterator it = m.begin();
    typename container_type::iterator dit = Dest.begin();

    if (ImgDepth == 1) {
      compute_sobel(it, dit, ImgWidth, ImgHeight);
      return;
    };

    for (size_t k = 0; k < ImgDepth; k++) {
      if (k == 0) {
        compute_sobel(it, dit, ImgWidth, ImgHeight);
        it = m.begin();
        dit = Dest.begin();
        continue;
      } else if (k == ImgDepth - 1) {
        compute_sobel(it, dit, ImgWidth, ImgHeight);
        continue;
      }

      for (size_t i = 1; i < ImgHeight - 1; i++) {
        for (size_t j = 1; j < ImgWidth - 1; j++) {
          size_t shift_it = k * ImgWidth * ImgHeight + i * ImgWidth + j;
          it = m.begin() + shift_it;
          dit = Dest.begin() + shift_it;

          int pm = *(it + ImgWidth - 1);
          int p = *(it + ImgWidth);
          int pp = *(it + ImgWidth + 1);

          int mm = *(it - ImgWidth - 1);
          int m = *(it - ImgWidth);
          int mp = *(it - ImgWidth + 1);

          int _m = *(it - 1);
          int _p = *(it + 1);

          int __m = *(it - ImgWidth * ImgWidth);
          int __p = *(it + ImgWidth * ImgWidth);

          int mm_ = *(it - ImgWidth * ImgWidth + ImgWidth);
          int pm_ = *(it + ImgWidth * ImgWidth + ImgWidth);

          int pp_ = *(it + ImgWidth * ImgWidth - ImgWidth);
          int mp_ = *(it - ImgWidth * ImgWidth - ImgWidth);

          int p_m = *(it + ImgWidth * ImgWidth - 1);
          int m_m = *(it - ImgWidth * ImgWidth - 1);

          int m_p = *(it - ImgWidth * ImgWidth + 1);
          int p_p = *(it + ImgWidth * ImgWidth + 1);

          int vert = (pm + 2 * p + pp - mm - 2 * m - mp);
          int hor = (mm + 2 * _m + pm - mp - 2 * _p - pm);

          int depth1 = (mm + 2 * _m + pm - mp - 2 * _p - pm);
          int depth2 = (mm + 2 * m + pm - mp - 2 * p - pm);

          int v = sqrt(
              (vert * vert + hor * hor + depth1 * depth1 + depth2 * depth2) /
              2);

          *dit = v;
        }
      }
    }
  }

  void compute_sobel3D(const container_type &m, container_type &Dest,
                       int ImgWidth, int ImgHeight, int ImgDepth) {
    typename container_type::const_iterator it = m.begin();
    typename container_type::iterator dit = Dest.begin();

    if (ImgDepth == 1) {
      compute_sobel(it, dit, ImgWidth, ImgHeight);
      return;
    };

    for (size_t k = 0; k < ImgDepth; k++) {
      if (k == 0) {
        compute_sobel(it, dit, ImgWidth, ImgHeight);
        it = m.begin();
        dit = Dest.begin();
        continue;
      } else if (k == ImgDepth - 1) {
        compute_sobel(it, dit, ImgWidth, ImgHeight);
        continue;
      }

      int layer_width = ImgHeight * ImgWidth;
      for (size_t i = 1; i < ImgHeight - 1; i++) {
        for (size_t j = 1; j < ImgWidth - 1; j++) {
          size_t shift_it = k * ImgWidth * ImgHeight + i * ImgWidth + j;
          it = m.begin() + shift_it;
          dit = Dest.begin() + shift_it;

          int pm = *(it + ImgWidth - 1);
          int p_ = *(it + ImgWidth);
          int pp = *(it + ImgWidth + 1);

          int mm = *(it - ImgWidth - 1);
          int m_ = *(it - ImgWidth);
          int mp = *(it - ImgWidth + 1);

          int _m = *(it - 1);
          int _p = *(it + 1);

          int prev_pm = *(it - layer_width + ImgWidth - 1);
          int prev_p_ = *(it - layer_width + ImgWidth);
          int prev_pp = *(it - layer_width + ImgWidth + 1);

          int prev_mm = *(it - layer_width - ImgWidth - 1);
          int prev_m_ = *(it - layer_width - ImgWidth);
          int prev_mp = *(it - layer_width - ImgWidth + 1);

          int prev__m = *(it - layer_width - 1);
          int prev__p = *(it - layer_width + 1);

          int prev__ = *(it - layer_width);

          int next_pm = *(it + layer_width + ImgWidth - 1);
          int next_p_ = *(it + layer_width + ImgWidth);
          int next_pp = *(it + layer_width + ImgWidth + 1);

          int next_mm = *(it + layer_width - ImgWidth - 1);
          int next_m_ = *(it + layer_width - ImgWidth);
          int next_mp = *(it + layer_width - ImgWidth + 1);

          int next__m = *(it + layer_width - 1);
          int next__p = *(it + layer_width + 1);

          int next__ = *(it + layer_width);

          int h_x = prev_mm + prev_pm - prev_mp - prev_pp + 2 * prev_m_ -
                    2 * prev__p + 2 * (mm + pm - mp - pp + 2 * _m - 2 * _p) +
                    next_mm + next_pm - next_mp - next_pp + 2 * next__m -
                    2 * next__p;

          int h_y = prev_mm + prev_mp - prev_pm - prev_pp + 2 * prev_m_ -
                    2 * prev_p_ + 2 * (mm + mp - pm - pp + 2 * m_ - 2 * p_) +
                    next_mm + next_mp - next_pm - next_pp + 2 * next_m_ -
                    2 * next_p_;

          int h_z = 1 * (prev_pm + prev_mp + prev_mm + prev_pp) +
                    2 * (prev_p_ + prev_m_ + prev__m + prev__p) + 4 * prev__ -
                    1 * (next_pm + next_mp + next_mm + next_pp) -
                    2 * (next_p_ + next_m_ + next__m + next__p) - 4 * next__;

          T v = static_cast<T>(
              floor(sqrt(h_x * h_x + h_y * h_y + h_z * h_z) + 0.5));
          *dit = v;
        }
      }
    }
  }
};

template <class T = unsigned char, class container_type = DynamicArray<T>>
class IThreshold {
public:
  virtual std::vector<double> LowThresholds() const = 0;
  virtual std::vector<double> HighThresholds() const = 0;
  virtual int Low() const = 0;
  virtual int High() const = 0;
  virtual int PhasesCount() const = 0;
  virtual void compute_cut_offs(const container_type &m, int ImgWidth = 0,
                                int ImgHeight = 0, int ImgDepth = 0) = 0;
};

template <class T = unsigned char, class container_type = DynamicArray<T>>
class Threshold : public IThreshold<T, container_type> {
public:
  Threshold()
      : mFlatness(0.001), ilow(0), ihigh(0), mLow(-1), mHigh(-1),
        mPhasesCount(2){};

  // TODO: Remove not implemented or find implementation
  // Threshold(const Threshold & T);

  // void compute_cut_offs(const DynamicArray<T> &m, int ImgWidth=0, int
  // ImgHeight=0, int ImgDepth=0)
  void compute_cut_offs(const container_type &m, int ImgWidth = 0,
                        int ImgHeight = 0, int ImgDepth = 0) {

    int min = 0;
    int max = 256;

    int n_point = 256;
    Histogram hist(m, min, max, n_point);
    double delta = hist.delta();
    double peak;
    switch (Method) {
    case Th_nBinoms:
      CutOffsBinoms(m, mLow, mHigh);
      break;
    case Th_Schluter:
      CutOffsSchluter(m, ImgWidth, ImgHeight, ImgDepth, mLow, mHigh);
      break;
    case Th_PE1:
      CutOffsPE1(m, ImgWidth, ImgHeight, ImgDepth, mLow, mHigh);
      break;
    case Th_PE2:
      CutOffsPE2(m, ImgWidth, ImgHeight, ImgDepth, mLow, mHigh);
      break;
    case Th_entropy:
      DynamicArray<double> entropy(n_point, 0.0);
      compute_entropy(hist, entropy);
      DynamicArray<double> x(n_point);

      diterator px;
      double thisx;
      int i;

      thisx = hist.x_0();
      px = x.begin();
      for (i = 0; i < n_point; i++, thisx += delta, px++)
        *px = thisx;

      int ipeak = thresholding(entropy, mFlatness, mLow, mHigh);
      mLow = mLow * double(max - min) / n_point + min;
      mHigh = mHigh * double(max - min) / n_point + min;
      peak = ipeak * double(max - min) / n_point + min;
      break;
    }
    mLows.clear();
    mLows.push_back(0);
    mLows.push_back(mHigh);
    mHighs.clear();
    mHighs.push_back(mLow);
    mHighs.push_back(255);
  }
  void compute_entropy(const DynamicArray<T> &m,
                       DynamicArray<double> &entropy) {
    DynamicArray<double> &prob = entropy;
    const int size = m.size();
    const double sum = std::accumulate(m.begin(), m.end(), 0.0);

    double Hn = 0.0;
    diterator p = prob.begin();
    int i = 0;
    for (i = 0; i < size; ++i, ++p) {
      *p = m[i] / sum;
      if (*p > 0)
        Hn -= *p * log(*p);
    }

    i = 0;
    while (prob[i] == 0.0) {
      entropy[i] = 0.0;
      ++i;
    }
    double Ps = prob[i];
    double Hs = -Ps * log(Ps);
    entropy[i] = log(Ps * (1.0 - Ps)) + Hs / Ps + (Hn - Hs) / (1.0 - Ps);
    for (int s = i + 1; s < size - 1; s++) {
      double p = prob[s];
      Ps += p;
      if (p > 0.0 && Ps < 1.0) {
        Hs -= p * log(p);
        entropy[s] = log(Ps * (1.0 - Ps)) + Hs / Ps + (Hn - Hs) / (1.0 - Ps);
      } else
        entropy[s] = entropy[s - 1];
    }
    entropy[size - 1] = Hn;
  }

  void compute_entropy(const Histogram &m, DynamicArray<double> &entropy) {
    DynamicArray<double> &prob = entropy;
    const size_t size = m.size();
    const double sum = std::accumulate(m.begin(), m.end(), 0.0);

    double Hn = 0.0;
    diterator p = prob.begin();
    size_t i = 0;
    for (i = 0; i < size; ++i, ++p) {
      *p = m[i] / sum;
      if (*p > 0)
        Hn -= *p * log(*p);
    }

    i = 0;
    while (prob[i] == 0.0) {
      entropy[i] = 0.0;
      ++i;
    }
    double Ps = prob[i];
    double Hs = -Ps * log(Ps);
    entropy[i] = log(Ps * (1.0 - Ps)) + Hs / Ps + (Hn - Hs) / (1.0 - Ps);
    for (size_t s = i + 1; s < size - 1; s++) {
      double p = prob[s];
      Ps += p;
      if (p > 0.0 && Ps < 1.0) {
        Hs -= p * log(p);
        entropy[s] = log(Ps * (1.0 - Ps)) + Hs / Ps + (Hn - Hs) / (1.0 - Ps);
      } else
        entropy[s] = entropy[s - 1];
    }
    entropy[size - 1] = Hn;
  }

  int thresholding(const DynamicArray<double> &m, const double flat,
                   double &low, double &high) {
    double min, max;
    Utils::minmax(m.begin(), m.end(), min, max);

    DynamicArray<int> threshold(10, 0);
    DynamicArray<int> bottom_of_range(10, 0);
    DynamicArray<int> top_of_range(10, 0);

    int i;
    int n_threshold = 0;

    const double thresh = max * (1.0 - flat);

    std::cout << "Entropy threshold computation\n";
    std::cout << "Maximum entropy value " << max;
    std::cout << ", entropy value at threshold " << thresh << std::endl;

    for (i = 1; i < 256; ++i) {
      if (m[i] >= thresh && m[i - 1] < thresh) {
        bottom_of_range[n_threshold] = i;
        threshold[n_threshold] = i;
      } else if (m[i] >= thresh) {
        if (m[i] >= m[threshold[n_threshold]])
          threshold[n_threshold] = i;
      } else if (m[i] < thresh && m[i - 1] >= thresh) {
        top_of_range[n_threshold] = i - 1;
        ++n_threshold;
      }
    }

    if (n_threshold == 1) {
      low = bottom_of_range[0];
      high = top_of_range[0];
    } else
      error("There is more than 1 threshold.", "");

    return threshold[0];
  }
  ThreshodMethods Method;
  int PeaksCount() const { return mPeaksCount; }
  int &PeaksCount() { return mPeaksCount; }
  double Alpha() const { return mAlpha; }
  double &Alpha() { return mAlpha; }
  int Low() const {
    if (mPhasesCount == 2)
      return (int)mLow;
    else
      return (int)mLows.front();
  }
  int High() const {
    if (mPhasesCount == 2)
      return (int)mHigh;
    else
      return (int)mHighs.back();
  }
  double Flatness() const { return mFlatness; }
  double &Flatness() { return mFlatness; }
  void SetManualThresholds(int nLow, int nHigh) {
    mHigh = nHigh;
    mLow = nLow;
  }
  void Setup(ThresholdSettings &ts) {
    mLow = ts.LowThreshold;
    mHigh = ts.HighThreshold;
    Method = ts.ThresholdMethod;
    mFlatness = 0.005;
    mPeaksCount = ts.nPeaks;
    mAlpha = ts.alpha;
    mLows.push_back(0);
    mLows.push_back(mHigh);
    mHighs.push_back(mLow);
    mHighs.push_back(255);
    if (ts.IsMultiphase) {
      mLows.resize(ts.nPhases);
      mHighs.resize(ts.nPhases);
      std::copy(ts.Lows.begin(), ts.Lows.end(), mLows.begin());
      std::copy(ts.Highs.begin(), ts.Highs.end(), mHighs.begin());
      mPhasesCount = ts.nPhases;
    }
  }
  // void Schluter(const DynamicArray<T> &m, int ImgWidth, int ImgHeight, int
  // ImgDepth, double &Low, double &High)

  // void CutOffsSchluter2(const DynamicArray<T> &m, int ImgWidth, int
  // ImgHeight, int ImgDepth, double &Low, double &High)
  // {
  // 	image_cc * img;

  // 	if (ImgDepth>3)
  // 		img = InitImage(ImgWidth, ImgHeight, ImgDepth, 0);
  // 	else
  // 		img = InitImage(ImgWidth, ImgHeight, 0);
  // 	auto pm = m.cbegin();

  // 	for (int i = 0; i<ImgWidth*ImgHeight*ImgDepth; i++)
  // 	{
  // 		img->pix[i] = *pm;
  // 		pm++;
  // 	}
  // 	int *thrs = GradMaskThresh(img, mAlpha);
  // 	Low = thrs[0];
  // 	High = thrs[1];
  // }

  void Schluter(const container_type &m, int ImgWidth, int ImgHeight,
                int ImgDepth, double &Low, double &High) {
    LogFile::WriteData("kriging.log", "Shlutter Sterted ");

    container_type SobelOut(ImgWidth * ImgHeight * ImgDepth);
    LogFile::WriteData("kriging.log", "Computeing Sobel");
    SobelConvolution<T, container_type> Sobel;
    Sobel.compute_sobel3D(m, SobelOut, ImgWidth, ImgHeight, ImgDepth);
    // compute_sobel3D(m, SobelOut, ImgWidth, ImgHeight, ImgDepth);
    LogFile::WriteData("kriging.log", "Building hist sobel");
    Histogram hist(SobelOut, 256);
    LogFile::WriteData("kriging.log", "Building hist original");
    Histogram hist_m(m, 256);

    NullAtBegin(hist);
    NullAtBegin(hist_m);
    Histogram::iterator max_it = std::max_element(hist_m.begin(), hist_m.end());
    double xmode = (max_it - hist_m.begin()) * hist_m.delta();
    Histogram::iterator hit = std::max_element(hist.begin(), hist.end());
    const double tau = -2; // -1.5;
    double thresh = *hit * exp(tau);
    LogFile::WriteData("kriging.log", "Looking for knee of hist ");
    while (hit != hist.end() && *hit > thresh)
      hit++;
    int pos = static_cast<int>((hit - hist.begin()) * hist.delta());
    LogFile::WriteData("kriging.log", "Pos of knee ", pos);
    std::vector<int> Hist_gray(256);
    double tmax = 0;
    double S = 0;
    for (int i = 0; i < SobelOut.size(); i++) {
      if (SobelOut[i] > pos && m[i] < xmode) {
        tmax += m[i] * SobelOut[i];
        S += SobelOut[i];
      }
    }
    if (S >= 1)
      tmax = tmax / S;
    LogFile::WriteData("kriging.log", "tmax found ", tmax);
    Low = xmode - mAlpha * (xmode - tmax);
    High = tmax;
    LogFile::WriteData("kriging.log", "High ", High);
    LogFile::WriteData("kriging.log", "Low ", Low);
  }

  void SchluterHist(const container_type &m, int ImgWidth, int ImgHeight,
                    int ImgDepth, std::vector<int> &h) {
    LogFile::WriteData("kriging.log", "Shlutter Sterted ");

    container_type SobelOut(ImgWidth * ImgHeight * ImgDepth);
    LogFile::WriteData("kriging.log", "Computeing Sobel");
    SobelConvolution<T, container_type> Sobel;
    Sobel.compute_sobel3D(m, SobelOut, ImgWidth, ImgHeight, ImgDepth);
    // compute_sobel3D(m, SobelOut, ImgWidth, ImgHeight, ImgDepth);
    LogFile::WriteData("kriging.log", "Building hist sobel");
    Histogram hist(SobelOut, 256);
    std::copy(hist.begin(), hist.end(), h.begin());
    LogFile::WriteData("kriging.log", "Building hist original");
    Histogram hist_m(m, 256);

    NullAtBegin(hist);
    NullAtBegin(hist_m);
    Histogram::iterator max_it = std::max_element(hist_m.begin(), hist_m.end());
    double xmode = (max_it - hist_m.begin()) * hist_m.delta();
    Histogram::iterator hit = std::max_element(hist.begin(), hist.end());
    const double tau = -2; // -1.5;
    double thresh = *hit * exp(tau);
    LogFile::WriteData("kriging.log", "Looking for knee of hist ");
    while (hit != hist.end() && *hit > thresh)
      hit++;
    int pos = (hit - hist.begin()) * hist.delta();
    LogFile::WriteData("kriging.log", "Pos of knee ", pos);
    std::vector<int> Hist_gray(256);
    double tmax = 0;
    double S = 0;
    for (int i = 0; i < SobelOut.size(); i++) {
      if (SobelOut[i] > pos && m[i] < xmode) {
        tmax += m[i] * SobelOut[i];
        S += SobelOut[i];
      }
    }
    tmax = tmax / S;
    LogFile::WriteData("kriging.log", "tmax found ", tmax);
    double Low = xmode - mAlpha * (xmode - tmax);
    double High = tmax;
    LogFile::WriteData("kriging.log", "High ", High);
    LogFile::WriteData("kriging.log", "Low ", Low);
  }

  void HessianCutOff(const DynamicArray<T> &m, int ImgWidth, int ImgHeight,
                     int ImgDepth, int &Threshold) {
    Histogram hist_m(m, 256);
    NullAtBegin(hist_m);

    Histogram::iterator max_it = std::max_element(hist_m.begin(), hist_m.end());
    double xmode = (max_it - hist_m.begin()) * hist_m.delta();
    const double tau = -2.0;
    double thresh = *max_it * exp(tau);
    std::vector<double> d(hist_m.size());
    auto itd = d.begin();
    auto it = hist_m.begin();
    while (it != hist_m.end()) {
      *itd = abs(*it - thresh);
      it++;
      itd++;
    }
    std::vector<double>::iterator pos_it = std::min_element(d.begin(), d.end());
    int pos = (pos_it - d.begin()) * hist_m.delta();
    Threshold = pos;
  }

  Mixture mix;
  std::vector<double> LowThresholds() const { return mLows; }
  std::vector<double> HighThresholds() const { return mHighs; }
  int PhasesCount() const { return mPhasesCount; }

  void NBinoms(const DynamicArray<T> &m, int nBinoms, std::vector<double> &M,
               std::vector<double> &V, std::vector<double> &S) {
    int i;
    LogFile::WriteData("kriging.log", "NBinoms started");
    std::vector<int> RandArr(10000);
    GetRandomDynamicArray(m, RandArr, 10000);
    double dummy;
    double whole_mean, whole_var;
    Utils::stats(RandArr.begin(), RandArr.end(), dummy, dummy, whole_mean,
                 whole_var);
    double *mean_seed = new double[nBinoms];
    double *sd_seed = new double[nBinoms];
    double LowRange = (whole_mean - 2 * whole_var);
    LowRange = LowRange > 0 ? LowRange : 0;
    double HighRange = (whole_mean + 2 * whole_var);
    HighRange = HighRange < 255 ? HighRange : 255;
    for (int i = 0; i < nBinoms; i++) {
      mean_seed[i] = LowRange + (HighRange - LowRange) / nBinoms * i;
      sd_seed[i] = 10;
    }

    LogFile::WriteData("kriging.log", "initial parameters calculated");
    ExpectedMaximized em(RandArr, nBinoms, mean_seed, sd_seed);
    em.Estimate();
    for (int i = 0; i < nBinoms; i++) {
      M.push_back(em.mean[i]);
      V.push_back(em.sd[i]);
      S.push_back(em.pi[i]);
    }
    delete[] mean_seed;
    delete[] sd_seed;
  }

  void CutOffsPE3(const DynamicArray<T> &m, int ImgWidth, int ImgHeight,
                  int ImgDepth, int nAtans, std::vector<double> &M,
                  std::vector<double> &V, std::vector<double> &S) {
    DynamicArray<int> SobelOut(ImgWidth * ImgHeight);
    DynamicArray<int> ImgSobelOut(ImgWidth * ImgHeight);
    compute_diff(m, SobelOut, ImgWidth, ImgHeight);
    Histogram hist(SobelOut, 256);
    auto mx = std::max_element(hist.begin() + 2, hist.end());
    int max_sobel_pos = mx - hist.begin();
    int max_sobel_val = max_sobel_pos * hist.delta();

    DynamicArray<int>::iterator itImg = ImgSobelOut.begin();
    typename DynamicArray<T>::const_iterator itM = m.begin();
    const int waste_val_cutoff = 0;
    const int waste_val_cutoff2 = 255;
    for (auto itSobel = SobelOut.begin(); itSobel != SobelOut.end();
         itSobel++, itM++)
      if (*itSobel<max_sobel_val && * itM> waste_val_cutoff &&
          *itM < waste_val_cutoff2) {
        *itImg = *itM;
        itImg++;
      }
    ImgSobelOut.resize(itImg - ImgSobelOut.begin());
    const int nBins = 256;
    Histogram histImg(ImgSobelOut, nBins);
    histImg.save("Hist_PE2.txt");

    double nElements =
        std::accumulate(histImg.begin(), histImg.end(), nElements);
    for (int i = 0; i < histImg.size(); i++) {
      histImg[i] = histImg[i] / nElements;
    }
    /*	class AtanFitObjective :public SAObectiveBase
            {
                    double Calulate(const void *pData, const double *params)
                    {
                            double Sum = 0;
                            for (int i = 0; i<mH.size(); i++)
                            {
                                    double v = 0;
                                    for (int j = 0; j < mAtansCount; j++)
                                    {
                                            double m = params[j];
                                            double b = params[j + mAtansCount];
                                            double a = params[j + 2 *
       mAtansCount]; double dx = (i - m);
                                            //v += a / (1 + b*dx*dx);
                                            v += a *exp(-dx*dx / b / b);
                                    }
                                    double dv = mH[i] - v;
                                    Sum += dv*dv;
                            }
                            Sum = sqrt(Sum / mH.size());


                            return Sum;
                    }

                    const std::vector<double> &mH;
                    int mAtansCount;
            public:
                    AtanFitObjective(const std::vector<double> &H, int nAtans)
       :mH(H), mAtansCount(nAtans)
                    {
                    }
            };

            AtanFitObjective O(histImg, nAtans);
            double *Params = new double[nAtans];

            double *UpperBounds = new double[nAtans * 3];
            double *LowerBounds = new double[nAtans * 3];

            SASettings Settings;
            Settings.EFinish = 0.0005;
            Settings.TFactor = 0.99;
            Settings.TFinish = 0.0000000005;
            Settings.TStart = 0.1;
            SimulatedAnnealing SA;

            for (int i = 0; i < nAtans; i++)
            {
                    Params[i] = 64.0 / nAtans*i;
                    Params[i + nAtans] = 3;
                    Params[i + 2 * nAtans] = 0.1;
                    UpperBounds[i] = 64.0;
                    LowerBounds[i] = 0;
                    UpperBounds[i + nAtans] = 30;
                    LowerBounds[i + nAtans] = 0.01;
                    UpperBounds[i + 2 * nAtans] = 1;
                    LowerBounds[i + 2 * nAtans] = 0.001;
            }

            SA.Settings = Settings;
            SA.Perform(O, Params, NULL, UpperBounds, LowerBounds, 3 * nAtans);
            M.resize(nAtans);
            V.resize(nAtans);
            S.resize(nAtans);
            for (int i = 0; i < nAtans; i++)
            {
                    M[i] = Params[i];
                    V[i] = Params[i + nAtans];
                    S[i] = Params[i + 2 * nAtans];
            }*/
    struct AtanFitObjective : NelderMeadObjective {
      double operator()(const std::vector<double> &coeffs) const {
        double Sum = 0;
        for (int i = 0; i < mH.size(); i++) {
          double v = 0;
          for (int j = 0; j < mAtansCount; j++) {
            double m = coeffs[j];
            double b = coeffs[j + mAtansCount];
            double a = coeffs[j + 2 * mAtansCount];
            double dx = (i - m);
            // v += a / (1 + b*dx*dx);
            v += a * exp(-dx * dx / b / b);
          }
          double dv = mH[i] - v;
          Sum += dv * dv;
        }
        Sum = sqrt(Sum / mH.size());

        return Sum;
      }

      const std::vector<double> &mH;
      int mAtansCount;

    public:
      AtanFitObjective(const std::vector<double> &H, int nAtans)
          : mH(H), mAtansCount(nAtans) {}
    };

    std::vector<double> Params;
    Params.resize(3 * nAtans);
    std::vector<double> UpperBounds;
    UpperBounds.resize(3 * nAtans);
    std::vector<double> LowerBounds;
    LowerBounds.resize(3 * nAtans);
    AtanFitObjective AO(histImg, nAtans);
    for (int i = 0; i < nAtans; i++) {
      Params[i] = nBins / nAtans * i;
      Params[i + nAtans] = 30;
      Params[i + 2 * nAtans] = 0.01;
      UpperBounds[i] = nBins;
      LowerBounds[i] = 5;
      UpperBounds[i + nAtans] = nBins / 2;
      LowerBounds[i + nAtans] = 5;
      UpperBounds[i + 2 * nAtans] = 0.08;
      LowerBounds[i + 2 * nAtans] = 0.001;
    }

    NelderMeadSettings Settings;
    Settings.Epsilon = 0.0001;
    Settings.MinChange = 0.0000000001;
    Settings.nMaxIter = 1000;
    NelderMead<AtanFitObjective> NM(Settings);
    NM.Perform(Params, LowerBounds, UpperBounds, AO);
    M.resize(nAtans);
    V.resize(nAtans);
    S.resize(nAtans);
    for (int i = 0; i < nAtans; i++) {
      M[i] = Params[i];
      V[i] = Params[i + nAtans];
      S[i] = Params[i + 2 * nAtans];
    }
    //}
  }

private:
  // TODO: Remove not implemented or find implementation
  // void estimate_2_normals(const Histogram&, double&, double&, double&,
  // double&, double&);
  void compute_harris(const DynamicArray<T> &m, DynamicArray<int> &Dest,
                      int ImgWidth, int ImgHeight) {
    DynamicArray<int>::const_iterator it = m.begin();
    DynamicArray<int>::iterator dit = Dest.begin();
    for (int i = 1; i < ImgHeight - 1; i++) {
      for (int j = 1; j < ImgWidth - 1; j++) {
        int shift_it = i * ImgWidth + j;
        it = m.begin() + shift_it;
        dit = Dest.begin() + shift_it;

        int pm = *(it + ImgWidth - 1);
        int p = *(it + ImgWidth);
        int pp = *(it + ImgWidth + 1);

        int mm = *(it - ImgWidth - 1);
        int m = *(it - ImgWidth);
        int mp = *(it - ImgWidth + 1);

        int _m = *(it - 1);
        int _p = *(it + 1);

        double Ixx = double(_p + _m - 2 * (*it)) / 4;
        double Iyy = double(p + m - 2 * (*it)) / 4;
        double Ixy = double(mm - pm + pp - mp) / 4;

        int v = abs(floor((Ixx * Iyy - 0.81 * Ixy * Ixy)));

        *dit = v;
      }
    }
  }
  void compute_diff(const DynamicArray<T> &m, DynamicArray<int> &Dest,
                    int ImgWidth, int ImgHeight) {
    typename DynamicArray<T>::const_iterator it = m.begin();
    DynamicArray<int>::iterator dit = Dest.begin();
    const int stick_size = 2;
    it += ImgWidth + 1;
    dit += ImgWidth + 1;
    for (int i = 1; i < ImgHeight - 1; i++) {
      for (int j = 1; j < ImgWidth - stick_size; j++) {
        int v = *(it + stick_size) - *it;
        *dit = abs(v);
        dit++;
        it++;
      }
    }
  }

  void compute_sobel(typename DynamicArray<T>::const_iterator &a_it,
                     DynamicArray<int>::iterator &a_dit, int ImgWidth,
                     int ImgHeight) {
    int shift_it = ImgWidth + 1;
    int shift_dit = ImgWidth + 1;
    auto it = a_it;
    auto dit = a_dit;
    for (int i = 1; i < ImgHeight - 1; i++) {
      for (int j = 1; j < ImgWidth - 1; j++) {
        shift_it = i * ImgWidth + j;
        it = a_it + shift_it;
        dit = a_dit + shift_it;
        int pm = *(it + ImgWidth - 1);
        int p = *(it + ImgWidth);
        int pp = *(it + ImgWidth + 1);

        int mm = *(it - ImgWidth - 1);
        int m = *(it - ImgWidth);
        int mp = *(it - ImgWidth + 1);

        int _m = *(it - 1);
        int _p = *(it + 1);

        int r = (pm + 2 * p + pp - mm - 2 * m - mp);
        int c = (mm + 2 * _m + pm - mp - 2 * _p - pm);
        int v = sqrt(r * r + c * c);
        *dit = v;
      }
    }
  }

  void compute_sobel3D(const DynamicArray<T> &m, DynamicArray<int> &Dest,
                       int ImgWidth, int ImgHeight, int ImgDepth) {
    typename DynamicArray<T>::const_iterator it = m.begin();
    DynamicArray<int>::iterator dit = Dest.begin();

    if (ImgDepth == 1) {
      compute_sobel(it, dit, ImgWidth, ImgHeight);
      return;
    };

    for (size_t k = 0; k < ImgDepth; k++) {
      if (k == 0) {
        compute_sobel(it, dit, ImgWidth, ImgHeight);
        it = m.begin();
        dit = Dest.begin();
        continue;
      } else if (k == ImgDepth - 1) {
        compute_sobel(it, dit, ImgWidth, ImgHeight);
        continue;
      }

      int layer_width = ImgHeight * ImgWidth;
      for (size_t i = 1; i < ImgHeight - 1; i++) {
        for (size_t j = 1; j < ImgWidth - 1; j++) {
          size_t shift_it = k * ImgWidth * ImgHeight + i * ImgWidth + j;
          it = m.begin() + shift_it;
          dit = Dest.begin() + shift_it;

          int pm = *(it + ImgWidth - 1);
          int p_ = *(it + ImgWidth);
          int pp = *(it + ImgWidth + 1);

          int mm = *(it - ImgWidth - 1);
          int m_ = *(it - ImgWidth);
          int mp = *(it - ImgWidth + 1);

          int _m = *(it - 1);
          int _p = *(it + 1);

          int prev_pm = *(it - layer_width + ImgWidth - 1);
          int prev_p_ = *(it - layer_width + ImgWidth);
          int prev_pp = *(it - layer_width + ImgWidth + 1);

          int prev_mm = *(it - layer_width - ImgWidth - 1);
          int prev_m_ = *(it - layer_width - ImgWidth);
          int prev_mp = *(it - layer_width - ImgWidth + 1);

          int prev__m = *(it - layer_width - 1);
          int prev__p = *(it - layer_width + 1);

          int prev__ = *(it - layer_width);

          int next_pm = *(it + layer_width + ImgWidth - 1);
          int next_p_ = *(it + layer_width + ImgWidth);
          int next_pp = *(it + layer_width + ImgWidth + 1);

          int next_mm = *(it + layer_width - ImgWidth - 1);
          int next_m_ = *(it + layer_width - ImgWidth);
          int next_mp = *(it + layer_width - ImgWidth + 1);

          int next__m = *(it + layer_width - 1);
          int next__p = *(it + layer_width + 1);

          int next__ = *(it + layer_width);

          int h_x = prev_mm + prev_pm - prev_mp - prev_pp + 2 * prev_m_ -
                    2 * prev__p + 2 * (mm + pm - mp - pp + 2 * _m - 2 * _p) +
                    next_mm + next_pm - next_mp - next_pp + 2 * next__m -
                    2 * next__p;

          int h_y = prev_mm + prev_mp - prev_pm - prev_pp + 2 * prev_m_ -
                    2 * prev_p_ + 2 * (mm + mp - pm - pp + 2 * m_ - 2 * p_) +
                    next_mm + next_mp - next_pm - next_pp + 2 * next_m_ -
                    2 * next_p_;

          int h_z = 1 * (prev_pm + prev_mp + prev_mm + prev_pp) +
                    2 * (prev_p_ + prev_m_ + prev__m + prev__p) + 4 * prev__ -
                    1 * (next_pm + next_mp + next_mm + next_pp) -
                    2 * (next_p_ + next_m_ + next__m + next__p) - 4 * next__;

          int v = sqrt(h_x * h_x + h_y * h_y + h_z * h_z);
          *dit = v;
        }
      }
    }
  }

  void GetRandomDynamicArray(const container_type &m, std::vector<int> &RandArr,
                             int N) {
    std::vector<int> RandNums(m.size());
    for (int i = 0; i < m.size(); i++)
      RandNums[i] = i;
    int i = 0;
    int j = 0;
    while (i < N && j < m.size()) {
      int r = static_cast<int>((std::rand() * m.size() - 1.0) / RAND_MAX);
      int n = RandNums[r];
      // if (m[n] != 0 && m[n] != 255)
      {
        RandArr[i] = m[n];
        i++;
      }
      RandNums[r] = RandNums[m.size() - j - 1];
      RandNums[m.size() - j - 1] = n;
      j++;
    }
  }
  void peaking(Histogram &h, double &P1, double &P2, int step, double Threshold,
               int WidthThreshold) {
    auto mx = std::max_element(h.begin() + 1, h.end());
    LogFile::WriteData("kriging.log", "peaking started");
    double s = 0;
    for (Histogram::const_iterator itr = h.begin(); itr != h.end(); itr++)
      s += *itr;
    s /= h.size();
    LogFile::WriteData("kriging.log", "Average hist val ", s);
    int sgn = 0;
    std::vector<int> bgs;
    std::vector<int> ends;
    Histogram::const_iterator it = h.begin();
    double l = 0;
    int pos = 0;
    it++; // allow for 0 values at the end
    while (it < h.end() - step) {
      double dy = (*(it + step) - *it) / step / s;
      if (dy > Threshold) {
        l = (*(it + step) + *it) / 2;
        pos = it - h.begin();
        it += step;
      } else {
        it++;
        continue;
      }
      while (*it >= l && it != h.end() - 1)
        it++;

      if ((it - h.begin() - pos) > WidthThreshold) {
        bgs.push_back(pos);
        ends.push_back(it - h.begin());
      } else
        it++;
    }
    LogFile::WriteData("kriging.log", "nEnds ", ends.size());
    LogFile::WriteData("kriging.log", "nBegins ", bgs.size());

    assert(ends.size() > 0 /*, "no one peak found"*/);
    assert(bgs.size() > 0 /*, "no one peak found"*/);

    if (bgs.size() == 1 && abs((h[1] - h[step]) / step / s) > Threshold) {
      bgs.insert(bgs.begin(), 0);
      ends.insert(ends.begin(), step);
    }

    if (bgs.back() > ends.back())
      ends.push_back(h.size() - 1);

    LogFile::WriteData("kriging.log", "nEnds ", ends.size());
    LogFile::WriteData("kriging.log", "nBegins ", bgs.size());

    assert(ends.size() == 2 /*, "wrong anount of peaks found"*/);
    assert(bgs.size() == 2 /*, "wrong anount of peaks found"*/);

    mx = std::max_element(h.begin() + bgs[0] + 1, h.begin() + ends[0]);
    P1 = (mx - h.begin()) * h.delta();
    mx = std::max_element(h.begin() + bgs[1] + 1, h.begin() + ends[1]);
    P2 = (mx - h.begin()) * h.delta();
    LogFile::WriteData("kriging.log", "Low ", P1);
    LogFile::WriteData("kriging.log", "High ", P2);
  }

  void CutOffsSchluter(const container_type &m, int ImgWidth, int ImgHeight,
                       int ImgDepth, double &Low, double &High) {
    // CutOffsSchluter2(m,  ImgWidth, ImgHeight, ImgDepth, Low, High);

    Schluter(m, ImgWidth, ImgHeight, ImgDepth, Low, High);
    if (Low < 0)
      Low = 0;
  }

  void CutOffsBinoms(const container_type &m, double &Low, double &High) {
    LogFile::WriteData("kriging.log", "Cut-off nBinoms started");
    std::vector<int> RandArr(1000);
    GetRandomDynamicArray(m, RandArr, 1000);
    double dummy;
    double whole_mean, whole_var;
    Utils::stats(RandArr.begin(), RandArr.end(), dummy, dummy, whole_mean,
                 whole_var);
    double mean_seed[3];
    mean_seed[0] = whole_mean - sqrt(whole_var);
    mean_seed[1] = whole_mean + sqrt(whole_var);
    mean_seed[2] = 7;
    mean_seed[0] = std::max(0.0, mean_seed[0]);
    mean_seed[1] = std::max(0.0, mean_seed[1]);
    mean_seed[0] = std::min(255.0, mean_seed[0]);
    mean_seed[1] = std::min(255.0, mean_seed[1]);
    double sd_seed[3];
    sd_seed[0] = 10;
    sd_seed[1] = 10;
    sd_seed[2] = 10;
    LogFile::WriteData("kriging.log", "initial parameters calculated");
    ExpectedMaximized em(RandArr, mPeaksCount, mean_seed, sd_seed);
    em.Estimate();
    LogFile::WriteData("kriging.log", "peaks estimated");
    if (mPeaksCount == 3) {
      int idx[3];
      ::sort_idxtbl(em.pi, idx);
      Low = std::min(em.mean[idx[2]], em.mean[idx[1]]);
      High = std::max(em.mean[idx[2]], em.mean[idx[1]]);
    } else {
      Low = std::min(em.mean[0], em.mean[1]);
      High = std::max(em.mean[0], em.mean[1]);
    }
  }
  void CutOffsPE1(const container_type &m, int ImgWidth, int ImgHeight,
                  int ImgDepth, double &Low, double &High) {
    /*DynamicArray<int> SobelOut(ImgWidth*ImgHeight*ImgDepth);
    DynamicArray<int> ImgSobelOut(ImgWidth*ImgHeight*ImgDepth);
    compute_sobel3D(m, SobelOut, ImgWidth, ImgHeight, ImgDepth);
    Histogram hist(SobelOut, 256);
    auto mx = std::max_element(hist.begin() + 2, hist.end());
    int max_sobel_pos = mx - hist.begin();
    int max_sobel_val = max_sobel_pos*hist.delta();

    DynamicArray<int>::iterator itImg = ImgSobelOut.begin();
    container_type::const_iterator itM = m.begin();
    const int waste_val_cutoff = 1;
    const int waste_val_cutoff2 = 255;
    for (auto itSobel = SobelOut.begin(); itSobel != SobelOut.end(); itSobel++,
    itM++) if (*itSobel < max_sobel_val && *itM>waste_val_cutoff && *itM <
    waste_val_cutoff2)
    {
            *itImg = *itM;
            itImg++;
    }
    ImgSobelOut.resize(itImg - ImgSobelOut.begin());
    CutOffsBinoms(ImgSobelOut, Low, High);*/
  }

  void CutOffsPE2(const container_type &m, int ImgWidth, int ImgHeight,
                  int ImgDepth, double &Low, double &High) {
    /*DynamicArray<int> SobelOut(ImgWidth*ImgHeight);
    DynamicArray<int> ImgSobelOut(ImgWidth*ImgHeight);
    compute_diff(m, SobelOut, ImgWidth, ImgHeight);
    Histogram hist(SobelOut, 256);
    auto mx = std::max_element(hist.begin() + 2, hist.end());
    int max_sobel_pos = mx - hist.begin();
    int max_sobel_val = max_sobel_pos*hist.delta();

    DynamicArray<int>::iterator itImg = ImgSobelOut.begin();
    DynamicArray<T>::const_iterator itM = m.begin();
    const int waste_val_cutoff = 0;
    const int waste_val_cutoff2 = 255;
    for (auto itSobel = SobelOut.begin(); itSobel != SobelOut.end(); itSobel++,
    itM++) if (*itSobel < max_sobel_val && *itM>waste_val_cutoff && *itM <
    waste_val_cutoff2)
    {
            *itImg = *itM;
            itImg++;
    }
    ImgSobelOut.resize(itImg - ImgSobelOut.begin());

    Histogram histImg(ImgSobelOut, 64);
    histImg.save("Hist_PE2.txt");
    double P1, P2;
    peaking(histImg, P1, P2, 4, 0.07, 4);
    Low = P1;
    High = P2;*/
  }

  void NullAtBegin(Histogram &hist) {
    int i = 0;
    while (i + 1 < hist.size() && hist[i] > hist[i + 1]) {
      hist[i] = 0;
      i++;
    };
  }
  // char	method_;
  int ilow, ihigh;
  std::vector<double> mLows, mHighs;
  int mPhasesCount;
  double mLow, mHigh;
  double mFlatness;
  int mPeaksCount;
  double mAlpha;
};

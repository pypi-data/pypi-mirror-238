#pragma once
#include "threshold.h"

class LatticeModel {

public:
  using Iter = typename std::vector<int>::iterator;
  using ConstIter = typename std::vector<int>::const_iterator;

  LatticeModel(int nLabels);
  LatticeModel(const LatticeModel &);

  virtual ~LatticeModel();

  void ApplyUnsharpMask(const std::vector<int> &img, size_t w, size_t h,
                        size_t d, std::vector<int> &enhanced_img,
                        float strength_factor);

protected:
  void ConditionalImage2Labels(const std::vector<int> &I, std::vector<int> &C,
                               IThreshold<int, std::vector<int>> &thresh);

  void ConditionalImage(const std::vector<int> &I, std::vector<int> &C,
                        IThreshold<int, std::vector<int>> &thresh);

  int SelectPhase(const int &it);

  int SelectPhaseNormalized(const int &intensity_value);

  void Stats2L(const std::vector<int> &img, double High, double Low,
               double &LMean, double &HMean, double &LVar, double &HVar);

  void StatsNL(const std::vector<int> &img, const std::vector<double> &Highs,
               const std::vector<double> &Lows, double *Means, double *Vars);

  int clamp_byte(int value);

  inline Iter RightNB(Iter it) { return it + 1; }

  inline Iter LeftNB(Iter it) { return it - 1; }

  inline Iter TopNB(Iter it) { return it - mWidth; }
  inline Iter BotNB(Iter it) { return it + mWidth; }

  inline Iter BhdNB(Iter it) { return it + mWidth * mHeight; }

  inline Iter FrntNB(Iter it) { return it - mWidth * mHeight; }

  inline ConstIter RightNB(ConstIter it) { return it + 1; }

  inline ConstIter LeftNB(ConstIter it) { return it - 1; }

  inline ConstIter TopNB(ConstIter it) { return it - mWidth; }
  inline ConstIter BotNB(ConstIter it) { return it + mWidth; }

  inline ConstIter BhdNB(ConstIter it) { return it + mWidth * mHeight; }

  inline ConstIter FrntNB(ConstIter it) { return it - mWidth * mHeight; }

  int mLabels;
  size_t mWidth;
  size_t mHeight;
  size_t mDepth;
  double *means;
  double *vars;
};
#pragma once

#include "LatticeModel.h"

#include "threshold.h"
#include <queue>

struct PointWithSpeed {
  short x, y, z;
  float speed;
};

struct PointWithSpeedLess {
  inline bool operator()(const PointWithSpeed &L, const PointWithSpeed &R) {
    return L.speed < R.speed;
  }
};

struct CACSettings {
  CACSettings() : nPhases(2), UnsharpMaskStrength(1.0){};
  double AlphaI;
  double AlphaG;
  double G0;
  int nPhases;
  bool HessianSpeed;
  float UnsharpMaskStrength;
};

class CACSegmentation : public LatticeModel {
  using LatticeIterator = typename std::vector<int>::iterator;
  using LatticeConstIterator = typename std::vector<int>::const_iterator;

  float Speed(LatticeIterator sit, LatticeConstIterator it, int phase_label,
              CACSettings &Settings, int L, int H);

public:
  CACSegmentation(int LabelsCount);

  ~CACSegmentation();

  void Perform(const std::vector<int> &Src, std::vector<int> &Conditional,
               Threshold<int, std::vector<int>> &Thresh, CACSettings &Settings,
               int Width, int Heigth, int Depth);
  void Perform(const std::vector<int> &Src, std::vector<int> &Conditional,
               std::vector<int> &Hss, Threshold<int, std::vector<int>> &Thresh,
               CACSettings &Settings, int Width, int Heigth, int Depth);

private:
  std::priority_queue<PointWithSpeed, std::vector<PointWithSpeed>,
                      PointWithSpeedLess> *Heap;
  std::vector<int> mHss;
  bool mHessianLoaded;
  const int Undef;
  const int InNB;
  int *nbh;
};

#include "CACSegmentation.h"

#include "DynamicArray.h"
#include "IntegralImage.h"
#include "LogFile.h"
#include "NonLocalMeans.h"

using LatticeIterator = typename std::vector<int>::iterator;
using LatticeConstIterator = typename std::vector<int>::const_iterator;

// TODO: Check this function according to the paper
float CACSegmentation::Speed(LatticeIterator sit, LatticeConstIterator it,
                             int phase_label, CACSettings &Settings, int L,
                             int H) {
  float Fg = 1.0f / (1.0f + pow((float)(*sit) / Settings.G0, Settings.AlphaG));
  // Choose threshold of the opposite phase
  float Intensity =
      phase_label == 0 ? H : L; // abs(*it - L) > abs(*it - H) ? L : H;
  float FI =
      pow(abs((Intensity - (float)*it) / (float)(H - L)), Settings.AlphaI);
  return Fg * FI;
}

CACSegmentation::CACSegmentation(int LabelsCount)
    : LatticeModel{LabelsCount}, Undef{LabelsCount}, InNB{LabelsCount + 1},
      mHessianLoaded{false}, nbh{nullptr} {
  int *nbh = new int[this->mLabels];
}

CACSegmentation::~CACSegmentation() {
  if (nbh != nullptr) {
    delete[] nbh;
  }
}

void CACSegmentation::Perform(const std::vector<int> &Src,
                              std::vector<int> &Conditional,
                              Threshold<int, std::vector<int>> &Thresh,
                              CACSettings &Settings, int Width, int Heigth,
                              int Depth) {
  LogFile::WriteData("kriging.log", "Perform Sheppard");
  this->mDepth = Depth;
  this->mWidth = Width;
  this->mHeight = Heigth;

  int shape[3] = {Width, Heigth, Depth};
  bool verbose = true;
  int *denoised_data =
      NonLocalMeans::nlm_denoise(Src.data(), shape, 1, 1, verbose);
  std::vector<int> Denoised;
  Denoised.assign(denoised_data, denoised_data + Width * Heigth * Depth);

  DynamicArray<int> I(Width * Heigth);
  std::copy<LatticeConstIterator, typename DynamicArray<int>::iterator>(
      Denoised.cbegin(), Denoised.cbegin() + Width * Heigth, I.begin());
  int L, H;

  DynamicArray<int> enhanced(Depth * Width * Heigth);
  std::copy<LatticeConstIterator, typename DynamicArray<int>::iterator>(
      Denoised.cbegin(), Denoised.cend(), enhanced.begin());
  this->ApplyUnsharpMask(Denoised, Width, Heigth, Depth, enhanced,
                         Settings.UnsharpMaskStrength);

  LogFile::WriteData("kriging.log", "Thresholding");
  if (Thresh.Method != ThreshodMethods::Th_Manual)
    Thresh.compute_cut_offs(I, this->mWidth, this->mHeight, 1);
  L = Thresh.Low();
  H = Thresh.High();
  if (Thresh.PhasesCount() == 2) {
    this->ConditionalImage2Labels(enhanced, Conditional, Thresh);
    this->Stats2L(enhanced, H, L, this->means[0], this->means[1], this->vars[0],
                  this->vars[1]);
  } else {
    this->ConditionalImage(enhanced, Conditional, Thresh);
    this->StatsNL(enhanced, Thresh.HighThresholds(), Thresh.LowThresholds(),
                  this->means, this->vars);
  }

  std::vector<int> SobelImg(enhanced.size());
  SobelConvolution<uchar, std::vector<int>> Sobel;
  LogFile::WriteData("kriging.log", "Compute Sobel");
  Sobel.compute_sobel3D(enhanced, SobelImg, Width, Heigth, Depth);

  int i = 0;
  LatticeIterator cit = Conditional.begin();
  LatticeIterator sit = SobelImg.begin();
  // LatticeIterator hit = mHss.begin();
  LatticeConstIterator it = enhanced.begin();
  LogFile::WriteData("kriging.log", "Building the heap");
  std::vector<PointWithSpeed> PQVec;
  PQVec.reserve(this->mDepth * this->mWidth * this->mHeight);
  for (size_t k = 0; k < this->mDepth; k++)
    for (size_t i = 0; i < this->mHeight; i++)
      for (size_t j = 0; j < this->mWidth; j++) {
        if ((*cit == Undef) &&
            ((i < this->mHeight - 1 && *this->BotNB(cit) != Undef) ||
             (i > 0 && *this->TopNB(cit) != Undef) ||
             (j > 0 && *this->LeftNB(cit) != Undef) ||
             (j < this->mWidth - 1 && *this->RightNB(cit) != Undef) ||
             (k < this->mDepth - 1 && *this->BhdNB(cit) != Undef) ||
             (k > 0 && *this->FrntNB(cit) != Undef))) {

          int phase = this->SelectPhase(*it);
          float S = Speed(sit, it, phase, Settings, L, H);
          PQVec.push_back(
              PointWithSpeed{(short)j, (short)i, (short)k, (float)S});
        }
        cit++;
        sit++;
        it++;
      }
  /*	Heap = new std::priority_queue<PointWithSpeed>()
  for (auto it = PQVec.begin(); it != PQVec.end(); it++)
  {
  Heap->push(*it);
  }*/
  Heap =
      new std::priority_queue<PointWithSpeed, std::vector<PointWithSpeed>,
                              PointWithSpeedLess>(PQVec.begin(), PQVec.end());
  /*	int iii = 0;
  std::vector<PointWithSpeed> ptvec; ptvec.resize(PQVec.size());
  while (!Heap->empty())
  {
  ptvec[iii] = Heap->top();
  Heap->pop();
  iii++;
  }*/
  PQVec.clear();
  LogFile::WriteData("kriging.log", "Heap built");

  int nSimilarNeigbours = 1;
  if (this->mDepth == 1)
    nSimilarNeigbours = 1;

  while (!Heap->empty()) {
    PointWithSpeed p = Heap->top();
    Heap->pop();

    size_t I = p.y;
    size_t J = p.x;
    size_t K = p.z;

    it = enhanced.begin() + this->mWidth * this->mHeight * K +
         this->mWidth * I + J;
    cit = Conditional.begin() + this->mWidth * this->mHeight * K +
          this->mWidth * I + J;
    sit = SobelImg.begin() + this->mWidth * this->mHeight * K +
          this->mWidth * I + J;

    // if (mHessianLoaded)
    // 	hit = mHss.begin() + this->mWidth*this->mHeight*K +
    // this->mWidth*I + J;

    for (int i = 0; i < this->mLabels;
         i++) //!!! must be "==i" rather then "!=i"
      nbh[i] =
          ((I < this->mHeight - 1 && *this->BotNB(cit) == i) +
           (I > 0 && *this->TopNB(cit) == i) +
           (J > 0 && *this->LeftNB(cit) == i) +
           (J < this->mWidth - 1 && *this->RightNB(cit) == i) +
           (K < this->mDepth - 1 && *this->BhdNB(cit) == i) +
           (K > 0 &&
            *this->FrntNB(cit) ==
                i)); //(*this->BotNB(cit) == i) + (*this->TopNB(cit) == i) +
                     //(*this->LeftNB(cit) == i) + (*this->RightNB(cit) ==
                     // i);// || *this->BhdNB(cit) != 2 || *BfrNB(cit) != 2
    int nb_max = 0;
    int nb_max_idx = 0;

    for (int i = 0; i < this->mLabels; i++) {
      if (nbh[i] > nb_max) {
        nb_max_idx = i;
        nb_max = nbh[i];
      }
    }

    if (nb_max >= nSimilarNeigbours)
      *cit = nb_max_idx;
    else {
      /*double delta0 = abs(*it - L) ;
      double delta1 = abs(*it - H) ;
      if (delta0 < delta1)
      *cit = 0;
      else
      *cit = 1;*/

      // double delta1 = 10000000;
      // double nPhase = 0;
      // for (int i = 0; i < this->mLabels; i++)
      // {
      // 	double delta = abs(*it - this->means[i]); // this->vars[i];
      // //!!!! 	if (delta < delta1)
      // 	{
      // 		delta1 = delta;
      // 		nPhase = i;
      // 	}
      // }
      // *cit = nPhase;
      *cit = this->SelectPhase(*it);
    }

    int Hss = 0;
    // if (mHessianLoaded)
    // 	Hss = *hit;

    if (I < this->mHeight - 1 && *this->BotNB(cit) == Undef) {
      // double S = Speed(sit, it, Settings, L, H); //, Hss);
      float S = Speed(this->BotNB(sit), this->BotNB(it),
                      this->SelectPhase(*this->BotNB(it)), Settings, L, H);
      Heap->push(PointWithSpeed{static_cast<short>(J),
                                static_cast<short>(I + 1),
                                static_cast<short>(K), S});
      *this->BotNB(cit) = InNB;
    }
    if (I > 0 && *this->TopNB(cit) == Undef) {
      // double S = Speed(sit, it, Settings, L, H); //, Hss);
      // Heap->push(PointWithSpeed{ (short)J, (short)I - 1, (short)K, (float)S
      // });
      float S = Speed(this->TopNB(sit), this->TopNB(it),
                      this->SelectPhase(*this->TopNB(it)), Settings, L, H);
      Heap->push(PointWithSpeed{static_cast<short>(J),
                                static_cast<short>(I - 1),
                                static_cast<short>(K), S});
      *this->TopNB(cit) = InNB;
    }
    if (J > 0 && *this->LeftNB(cit) == Undef) {
      // double S = Speed(sit, it, Settings, L, H); //, Hss);
      // Heap->push(PointWithSpeed{ (short)J - 1, (short)I, (short)K, (float)S
      // });
      float S = Speed(this->LeftNB(sit), this->LeftNB(it),
                      this->SelectPhase(*this->LeftNB(it)), Settings, L, H);
      Heap->push(PointWithSpeed{static_cast<short>(J - 1),
                                static_cast<short>(I), static_cast<short>(K),
                                S});
      *this->LeftNB(cit) = InNB;
    }
    if (J < this->mWidth - 1 && *this->RightNB(cit) == Undef) {
      // double S = Speed(sit, it, Settings, L, H); //, Hss);
      // Heap->push(PointWithSpeed{ (short)J + 1, (short)I, (short)K, (float)S
      // });
      float S = Speed(this->RightNB(sit), this->RightNB(it),
                      this->SelectPhase(*this->RightNB(it)), Settings, L, H);
      Heap->push(PointWithSpeed{static_cast<short>(J + 1),
                                static_cast<short>(I), static_cast<short>(K),
                                S});
      *this->RightNB(cit) = InNB;
    }
    // it seems i forgot z dimension
    if (K < this->mDepth - 1 && *this->BhdNB(cit) == Undef) {
      // double S = Speed(sit, it, Settings, L, H);//, Hss);
      // Heap->push(PointWithSpeed{ (short)J, (short)I,(short)K + 1, (float)S
      // });
      float S = Speed(this->BhdNB(sit), this->BhdNB(it),
                      this->SelectPhase(*this->BhdNB(it)), Settings, L, H);
      Heap->push(PointWithSpeed{static_cast<short>(J), static_cast<short>(I),
                                static_cast<short>(K + 1), S});
      *this->BhdNB(cit) = InNB;
    }
    if (K > 0 && *this->FrntNB(cit) == Undef) {
      // double S = Speed(sit, it, Settings, L, H); //, Hss);
      // Heap->push(PointWithSpeed{ (short)J, (short)I, (short)K - 1, (float)S
      // });
      float S = Speed(this->FrntNB(sit), this->FrntNB(it),
                      this->SelectPhase(*this->FrntNB(it)), Settings, L, H);
      Heap->push(PointWithSpeed{static_cast<short>(J), static_cast<short>(I),
                                static_cast<short>(K - 1), S});
      *this->FrntNB(cit) = InNB;
    }
  } /**/
  for (auto cit = Conditional.begin(); cit != Conditional.end(); cit++) {
    //*cit = (*cit==1) * 255;
    // assert(*cit != InNB);
    assert(*cit < Undef);
  }
}
void CACSegmentation::Perform(const std::vector<int> &Src,
                              std::vector<int> &Conditional,
                              std::vector<int> &Hss,
                              Threshold<int, std::vector<int>> &Thresh,
                              CACSettings &Settings, int Width, int Heigth,
                              int Depth) {
  mHessianLoaded = true;
  mHss = Hss;
  Perform(Src, Conditional, Thresh, Settings, Width, Heigth, Depth);
}
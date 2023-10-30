/*
 *	Copyrighted, Research Foundation of SUNY, 1998
 */

#ifndef SEGMENT_H
#define SEGMENT_H
#include "DynamicArray.h"
#include <Eigen/Dense.h>

#include "Grid.h"
#include "LatticeModel.h"
#include "Variation.h"
#include "threshold.h"
#include <cstring>
// #include <uchar.h>

const float fCAT_0 = 0.0;
const float fCAT_1 = 1.0;
const float fto_be_CAT_0 = 0.3f;
const float fto_be_CAT_1 = 0.7f;
const float fto_be_ESTIMATED_f = 2.0;

const int CAT_0 = 0;
const int CAT_1 = 1;
const int to_be_CAT_0 = 15; //!!!!
const int to_be_CAT_1 = 16;
const int to_be_ESTIMATED_f = 10;

const uc to_be_ESTIMATED = (uc)140;
const uc marked_PORE = (uc)2;
const uc estimated_PORE = (uc)3;
const uc filtered_PORE = (uc)7;
const uc filtered_ROCK = (uc)13;
const uc estimated_ROCK = (uc)16;
const uc marked_ROCK = (uc)20;
const uc marked_exterior = (uc)130;

struct DataDescription {
  int W;
  int H;
  int D;
};

struct KrigingSettings {
  KrigingSettings()
      : Radius(3), VarMethod('m'), OutFormat('v'), CorMethod('i'), nLlabels(2) {
    VarMethod = 'm';
    CorMethod = 'i';
    OutFormat = 'v';
  }
  char VarMethod;
  char CorMethod;
  char DataCorMethod;
  char OutFormat;
  int Radius;
  int SegMethod;
  int nLlabels;
  ThresholdSettings Theshold;
};

template <class T = int, class CT = std::vector<T>>
class KrigingProcessor : public LatticeModel //, public ITestable
{
  using LatticeIterator = typename CT::iterator;
  using LatticeConstIterator = typename CT::const_iterator;

public:
  KrigingProcessor(int LabelsCount)
      : LatticeModel(LabelsCount) //, Undef(LabelsCount), InNB(LabelsCount + 1)
        {};

  void ComputeVriogramBetweenThresholds() {}

  void kriging_2way(const Grid &grid, CT &data_int, CT &status,
                    long long unmarked, const Variation &var,
                    const Threshold<T> &met, int radius) {
    std::string fname("kriging_2way");
    int dim = grid.dim();
    int max_lag = int(sqrt(double(dim)) * 2 * radius);

    LogFile::WriteData("kriging.log", "Hist of DataInt");

    Histogram hist(data_int, 256);
    // cumulative distribution function (CDF)
    //	CDF	cdf0(hist);
    //	CDF	cdf1 = cdf0;
    std::vector<CDF *> cdf;
    cdf.resize(met.PhasesCount());
    for (int i = 0; i < met.PhasesCount(); i++)
      cdf[i] = new CDF(hist);
    /*	else
                    CDF *cdf = new CDF[2];*/

    this->StatsNL(data_int, met.HighThresholds(), met.LowThresholds(),
                  this->means, this->vars);

    double *mid_cut = new double[met.PhasesCount() - 1];
    for (int i = 0; i < met.PhasesCount() - 1; i++) ///!!!
    {
      if (abs(this->vars[i] + this->vars[i + 1]) < EPS_THINY)
        mid_cut[i] = met.HighThresholds()[i];
      else
        mid_cut[i] = met.HighThresholds()[i] +
                     (this->vars[i]) / (this->vars[i] + this->vars[i + 1]) *
                         (met.LowThresholds()[i + 1] - met.HighThresholds()[i]);
    }

    LogFile::WriteData("kriging.log", "smooth_indicator_function");
    for (int i = 0; i < met.PhasesCount() - 1; i++) {
      int cut_idx = i > 0 ? (i - 1) : 0;
      smooth_indicator_function(*(cdf[i]), met.HighThresholds()[i],
                                mid_cut[cut_idx]);
      smooth_indicator_function(*(cdf[i + 1]), mid_cut[cut_idx],
                                met.LowThresholds()[i + 1]);
    }

    LogFile::WriteData("kriging.log",
                       "Allocate data_int.size():", data_int.size());
    std::vector<float> data(data_int.size());
    data.reserve(data_int.size());
    LogFile::WriteData("kriging.log",
                       "Allocate data_int.size() OK:", data_int.size());
    for (auto &&elem : data_int) {
      data.emplace_back(static_cast<float>(elem));
    }
    typename CT::const_iterator pi = status.begin();
    std::vector<float>::const_iterator pdata = data.begin();

    CT unmarked_data(unmarked);

    typename CT::iterator punmarked = unmarked_data.begin();

    while (pi != status.end()) {
      if (*pi == to_be_ESTIMATED) {
        *punmarked++ = static_cast<int>(*pdata);
      }
      ++pi, ++pdata;
    }
    std::vector<float>::iterator ptmp = data.begin();

    pdata = data.begin();
    pi = status.begin();
    int nPhases = met.PhasesCount();
    while (pi != status.end()) {
      if (*pi == marked_exterior)
        *ptmp = ::ext_value(0.0f);
      else if (*pi == to_be_ESTIMATED +
                          1) //(*pi == marked_PORE || *pi == filtered_PORE)
        *ptmp = 1.0;
      else if (*pi ==
               to_be_ESTIMATED +
                   nPhases) //(*pi == marked_ROCK || *pi == filtered_ROCK)
        *ptmp = 0.0;
      else {
        *ptmp = static_cast<float>(cdf[0]->F(*ptmp));
      }
      ++ptmp;
      ++pi; //	++pdata;
    }
    LogFile::WriteData("kriging.log", "var_T0");

    int nx = grid.nx();
    int ny = grid.ny();
    int nz = grid.nz(); // > (radius * 2 + 1) ? (radius * 2 + 1) : grid.nz();

    Point U, L = Point(0.0, 0.0, 0.0);
    int sizes[3];
    if (dim == 3) {
      U = Point((double)nx, (double)ny, (double)nz);
      sizes[0] = nx;
      sizes[1] = ny;
      sizes[2] = nz;
    } else {
      U = Point((double)nx, (double)ny, 0.0);
      sizes[0] = nx;
      sizes[1] = ny;
      sizes[2] = 1;
    }

    Grid var_grid(dim, L, U, sizes, 0, 0);

    std::vector<float> var_data(nx * ny * nz); // .begin(), data_int.end());
    data.resize(data_int.size());
    std::copy<std::vector<float>::iterator, std::vector<float>::iterator>(
        data.begin(), data.begin() + var_data.size(), var_data.begin());
    LogFile::WriteData("kriging.log", "var_data.size:", var_data.size());
    std::vector<Variation *> var_T(met.PhasesCount());
    var_T[0] = new Variation(max_lag, 1.0, var.direction(), mw_semivariogram,
                             Semivariogram, Semivariogram);

    var_T[0]->compute(var_data.begin(), var_grid, 0, 1); // treat data as
    LogFile::WriteData("kriging.log", "var_T0 Computed");
    // compute variances
    for (int i = 1; i < met.PhasesCount(); i++) {
      pdata = data.begin();
      pi = status.begin();
      punmarked = unmarked_data.begin();
      ptmp = data.begin();
      while (pi != status.end()) {
        if (*pi == to_be_ESTIMATED) {
          // This should be fine for *pdata
          // between met.low and met.high
          *ptmp = static_cast<float>(cdf[i]->F(*punmarked++));
        }
        ++ptmp;
        ++pi; //++pdata;
      }
      LogFile::WriteData("kriging.log", "var_T(Ith)");
      var_T[i] = new Variation(max_lag, 1.0, var.direction(), mw_semivariogram,
                               Semivariogram, Semivariogram);

      std::copy<std::vector<float>::iterator, std::vector<float>::iterator>(
          data.begin(), data.begin() + var_data.size(), var_data.begin());

      var_T[i]->compute(var_data.begin(), var_grid, 0,
                        1); // treat data as float
    }

    // recover the original data where to be estimated
    auto data_p = data.begin();
    pi = status.begin();
    punmarked = unmarked_data.begin();
    while (pi != status.end()) {
      if (*pi == to_be_ESTIMATED) {
        *data_p = static_cast<float>(*punmarked++);
      }
      ++pi;
      ++data_p;
    }

    ///!!!
    LogFile::WriteData("kriging.log", "Calc covariance");
    for (int i = 0; i < met.PhasesCount(); i++)
      var_T[i]->make_covariance();

    Point *coord = new Point[ipow(2 * radius + 1, dim)];
    size_t n_of_data = set_coord_sphere(radius, dim, coord);
    size_t size = n_of_data + 1;

    std::vector<DynamicArray<double>> ok_system(met.PhasesCount());
    for (int i = 0; i < met.PhasesCount(); i++)
      ok_system[i].resize(size * size);

    std::vector<DynamicArray<double>> rhs(met.PhasesCount());
    for (int i = 0; i < met.PhasesCount(); i++)
      rhs[i].resize(size);

    LogFile::WriteData("kriging.log", "Setup ordinary kriging");

    for (int i = 0; i < met.PhasesCount(); i++) {
      ok_system_setup2(ok_system[i], n_of_data, *var_T[i], coord);

      diterator rhsit = rhs[i].begin();
      // int info;

      /**/
      Eigen::MatrixXd A1(size, size), A2(size, size);
      Eigen::VectorXd b1(size), b2(size);

      const Point *p = coord;

      for (int row = 0; row < n_of_data; ++row, p++)
        b1[row] = var_T[i]->operator()(p->abs());
      b1[n_of_data] = 1.0;

      for (int u = 0; u < size; u++)
        for (int j = 0; j < size; j++) {
          size_t k = j * size + u;
          A1(u * size + j) = ok_system[0][k];
        }

      Eigen::VectorXd x1(size);
      x1 = A1.fullPivHouseholderQr().solve(b1);

      for (int j = 0; j < rhs[i].size(); j++)
        rhs[i][j] = x1[j];
    }

    for (int i = 0; i < met.PhasesCount(); i++) {
      diterator rhsit = rhs[i].begin();
      double sum = accumulate(rhsit, rhsit + n_of_data, 0.0);
      if ((fabs(sum - 1.0) > EPS_THINY)) {
        std::cout << "The sums are supposed to be 1; actual sums are ";
        std::cout << sum << std::endl;
        error("Kriging system not solved to required precision.", fname);
      }
      correct_weights(rhs[i].begin_pointer(), n_of_data, *var_T[i],
                      coord); //!!!!!!!!!!!1 12.08.2015
    }

    delete[] coord;

    std::vector<DynamicArray<double>> cond_data(met.PhasesCount());
    for (int i = 0; i < met.PhasesCount(); i++)
      cond_data[i].resize(n_of_data);
    typename CT::iterator pind = status.begin();
    // std::cout << "\nTotal no. of voxels " << data.size() << std::endl;

    // int	i;
    long long five_per;
    //	double	P_0, P_1;
    double *P = new double[met.PhasesCount()];

    five_per = status.size() / 20UL;
    if (five_per == 0)
      five_per = 1;

    // Copy pre-segmented data to another array
    CT status_src;
    status_src.reserve(status.size());
    std::copy(status.begin(), status.begin() + status_src.size(),
              status_src.begin());

    auto pdata_int = data_int.cbegin();

    for (size_t i = 0; i < status.size();
         ++i, ++pind, ++pdata_int /*, ++pseg_data_float*/) {
      if (i % five_per == 0) {
        LogFile::WriteData("kriging.log", "percentage:",
                           static_cast<size_t>(5 * i / five_per));
      }
      if (*pind != to_be_ESTIMATED) {

        continue;
      }

      for (int k = 0; k < nPhases - 1; k++) {
        if (*pdata_int < met.LowThresholds()[k] ||
            *pdata_int > met.LowThresholds()[k + 1])
          continue;
        set_neighbor_sphere(
            i, radius, grid, status_src, data_int, // data,
            cond_data[k].begin_pointer(), /*cond_data1_.begin_pointer(),*/
            *cdf[k], to_be_ESTIMATED + 1 + k + 1 /*, cdf1*/); /**/

        set_neighbor_sphere(i, radius, grid, status_src, data_int, // data,
                            cond_data[k + 1].begin_pointer(),
                            /*cond_data1_.begin_pointer(),*/ *cdf[k + 1],
                            to_be_ESTIMATED + 1 + k + 1 /*, cdf1*/); /**/

        double P_0 =
            std::inner_product(rhs[k].begin(), rhs[k].begin() + n_of_data,
                               cond_data[k].begin(), 0.0);
        double P_1 = std::inner_product(rhs[k + 1].begin(),
                                        rhs[k + 1].begin() + n_of_data,
                                        cond_data[k + 1].begin(), 0.0);
        if (P_0 > 1.0 - P_1)
          *pind = to_be_ESTIMATED + 1 + k;
        else
          *pind = to_be_ESTIMATED + 1 + k + 1;
      }
    }
  }

  void correct_weights(double *wgt, size_t n, const Variation &covar,
                       const Point *coord) {
    LogFile::WriteData("kriging.log",
                       "correct_weights(double* wgt, size_t n, const "
                       "Variation& covar, const Point* coord)");
    DynamicArray<long long> index(n);
    int j = 0;
    double avg = 0.0;
    double Cavg = 0.0;
    int i;
    for (i = 0; i < n; ++i) {
      if (wgt[i] < 0.0) {
        avg -= wgt[i];
        Cavg += covar(coord[i].abs());
        index[j++] = i;
      }
    }
    if (j == 0)
      return;

    int n_negative = j;
    avg /= n_negative;
    Cavg /= n_negative;
    double sum = 0.0;
    for (i = 0; i < n; ++i) {
      if (wgt[i] < 0.0)
        wgt[i] = 0.0;
      else if (covar(coord[i].abs()) < Cavg && wgt[i] < avg)
        wgt[i] = 0.0;
      sum += wgt[i];
    }
    for (i = 0; i < n; ++i)
      wgt[i] /= sum;
    LogFile::WriteData("kriging.log", "correct_weights finished");
  }

  void segment(CT &data, const Grid &grid, const Variation &var,
               Threshold<T> &Thresh, KrigingSettings &sp,
               ThresholdSettings &ts) {
    LogFile::WriteData("kriging.log", "Kriging segment procedure started");

    size_t i;
    int radius;
    int tbc0 = 0;
    int tbc1 = 0;

    if (Thresh.Method != Th_Manual) {
      LogFile::WriteData("kriging.log", "Calc threahold");
      int ImgSize = grid.n_x() * grid.n_y();
      DynamicArray<T> I(ImgSize);
      std::copy(data.begin(), data.begin() + ImgSize, I.begin());
      Thresh.compute_cut_offs(I, grid.n_x(), grid.n_y(), 1); //!!!
    }

    LogFile::WriteData("kriging.log", "Low threshold", +Thresh.Low());
    LogFile::WriteData("kriging.log", "High threshold", +Thresh.High());

    CT status(data.size());
    for (auto it = status.begin(); it != status.end(); it++)
      *it = 0;
    long long unmarked = mark(data, status, Thresh);
    if (grid.dim() == 2)
      radius = sp.Radius;
    else if (grid.dim() == 3)
      radius = sp.Radius;

    if (Thresh.Low() != Thresh.High()) {
      LogFile::WriteData("kriging.log", "kriging_2way");
      kriging_2way(grid, data, status, unmarked, var, Thresh, radius);
      LogFile::WriteData("kriging.log", "Krig_2way finished");
    }
    ///!!!
    // median_filter(status,grid,0.6);
    ts.OutHighThreshold = Thresh.High();
    ts.OutLowThreshold = Thresh.Low();

    auto pi = status.begin();
    auto pd = data.begin();
    for (i = 0; i < status.size(); ++i, ++pi, ++pd) {
      if (*pi == marked_exterior) {
        *pd = ext_value(int(0));
      } else {
        *pd = (*pi - to_be_ESTIMATED - 1);
      }
    }
    //	cout << tbc0 << " voxels are kriged as pop_0 (VOID)" << endl;
    //	cout << tbc1 << " voxels are kriged as pop_1 (GRAIN)" << endl;
    LogFile::WriteData("kriging.log", "Krig_2way finished");
  }

  void prepare(char method, Grid &grid, Variation &var, Threshold<T> &thr,
               KrigingSettings &sp, ThresholdSettings &ts,
               const DataDescription &dd) {
    LogFile::WriteData("kriging.log",
                       "prepare(char method,	Grid &grid, Variation	&var, "
                       "Threshold<T>	&thr, KrigingSettings &sp, "
                       "ThresholdSettings &ts, const DataDescription &dd)");
    Point L, U;
    int size[3];

    size_t nx, ny, nz; // , nxyz;
    int seg_dim = 2;
    if (dd.D > 1)
      seg_dim = 3;

    int max_lag = 10;
    double unit_lag = 1.0;
    var = Variation(max_lag, unit_lag, V_direction::Horizontal,
                    V_method::classic_semivariogram, Semivariogram,
                    Semivariogram);

    if (method == 'k') {
      var.set_method(sp.VarMethod);
      var.set_direction(sp.CorMethod);
      var.set_type(sp.OutFormat);
    }

    thr.Flatness() = 0.07;
    thr.Method = ts.ThresholdMethod;
    thr.SetManualThresholds(ts.LowThreshold, ts.HighThreshold);
    thr.PeaksCount() = ts.nPeaks;
    thr.Alpha() = ts.alpha;
    thr.Setup(ts);

    nx = dd.W;
    ny = dd.H;
    nz = dd.D;
    L = Point(0.0, 0.0, 0.0);
    if (seg_dim == 3) {
      U = Point((double)nx, (double)ny, (double)nz);
      size[0] = static_cast<int>(nx);
      size[1] = static_cast<int>(ny);
      size[2] = static_cast<int>(nz);
    } else {
      U = Point((double)nx, (double)ny, 0.0);
      size[0] = static_cast<int>(nx);
      size[1] = static_cast<int>(ny);
      size[2] = 1;
    }

    grid.set(seg_dim, L, U, size, 0, 0);
  }

  // extern	"C"
  void krig_driver(char method, CT &idat, CT &outdat, const DataDescription &dd,
                   KrigingSettings &sp, ThresholdSettings &ts) {
    LogFile::WriteData("kriging.log",
                       "krig_driver(char method, CT	&idat, "
                       "CT &outdat, const DataDescription &dd, "
                       "KrigingSettings &sp, ThresholdSettings &ts)");
    std::ios::sync_with_stdio();
    Grid grid;
    Variation var;
    int seg_dim;

    size_t nx, ny, nxy;
    int z_no;
    size_t n;
    int gmin, gmax;

    Threshold<T> Thresh;
    LogFile::WriteData("kriging.log", "prepare");
    prepare(method, grid, var, Thresh, sp, ts, dd);

    nx = grid.n_x();
    ny = grid.n_y();
    nxy = nx * ny;
    /* This loop does complete 2d kriging segmentation */
    /* For 3d segmentation, all it does is load idat */

    seg_dim = grid.dim();

    gmin = gmax = 0;

    if (seg_dim == 2) {
      krig_dat(method, idat, grid, var, Thresh, sp, ts);
      auto puc = outdat.begin();
      auto pidat = idat.begin();
      for (n = 0; n < nxy; n++, puc++, pidat++) {
        *puc = *pidat;
      }
    }

    /* 3d segmentation */
    if (seg_dim == 3) {
      LogFile::WriteData("kriging.log", "krig_dat");
      krig_dat(method, idat, grid, var, Thresh, sp, ts /*,&Jmer*/);

      auto pidat = idat.begin();
      auto ppidat = idat.begin();

      DynamicArray<uc> ucdat(nx * ny);
      auto puc = outdat.begin();
      LogFile::WriteData("kriging.log", "Fillong output");
      for (z_no = 0; z_no < grid.n_z(); z_no++, pidat += nxy) {
        ppidat = pidat;
        for (n = 0; n < nxy; n++, puc++, ppidat++) {
          *puc = *ppidat;
        }
      }
    }
  }

  //
  // This function is called for both kriging segmentation and
  // Mardia-Hainsworth segmentation
  //
  void krig_dat(char method, CT &raw_data, const Grid &grid, Variation &var,
                Threshold<T> &Thresh, KrigingSettings &sp,
                ThresholdSettings &ts) {

    double mean, variance;
    int seg_dim = grid.dim();
    size_t data_size = raw_data.size();
    size_t nx = grid.n_x();
    size_t ny = grid.n_y();
    size_t nz = grid.n_z();
    int nv, ng;
    int min, max;

    size_t nxy = nx * ny;
    DynamicArray<uc> ucdat(nxy);

    if (method == 'k') {
      LogFile::WriteData("kriging.log", "compute variogram");
      // var.compute(raw_data.begin(), grid, 0, 1);
      LogFile::WriteData("kriging.log", "segmentation");
      segment(raw_data, grid, var, Thresh, sp, ts /*,jmer*/);
    }

    CT &segmented = raw_data;
    data_size = segmented.size();
    auto pseg = segmented.begin();
    nv = ng = 0;
    for (size_t i = 0; i < data_size; i++, pseg++) {
      if (*pseg == CAT_0)
        ++nv;
      else if (*pseg == to_be_CAT_0) {
        *pseg = CAT_0;
        ++nv;
      } else if (*pseg == CAT_1)
        ++ng;
      else if (*pseg == to_be_CAT_1) {
        *pseg = CAT_1;
        ++ng;
      }
    }
    Utils::stats(segmented.begin(), segmented.end(), min, max, mean, variance);
  }

  long long mark(const CT &data, CT &status, Threshold<T> &met) {
    const int ext_value = ::ext_value(int(0));
    auto p = data.begin();

    LogFile::WriteData("kriging.log", "Mark procedure");
    double dp;
    double sum0, sum1, sqsum0, sqsum1;

    size_t i;
    long long n_0, n_1, n_e;
    size_t size;

    n_0 = n_1 = n_e = 0;
    sum0 = sqsum0 = sum1 = sqsum1 = 0.0;

    size = data.size();
    typename CT::iterator pi = status.begin();
    int nPhases = met.PhasesCount();
    bool stop = false;
    for (i = 0; i < size; ++i, ++p, ++pi) {
      dp = double(*p);
      int j = 0;
      stop = false;
      while (j < nPhases && !stop) {
        if (dp == ext_value) {
          *pi = marked_exterior;
          stop = true;
        } else if (dp >= met.LowThresholds()[j] - EPS_THINY &&
                   dp <= met.HighThresholds()[j] + EPS_THINY) {

          *pi = to_be_ESTIMATED + 1 + j;
          stop = true;
        } else {
          ++n_e;
          *pi = to_be_ESTIMATED;
        }
        j++;
      }
    }
    return n_e;
  }

  void smooth_indicator_function(CDF &cdf, double low, double high) {
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) low",
        low);
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) high",
        high);

    double x0 = cdf.x_0();
    double xn = cdf.x_n();
    double delta = cdf.delta();
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) x0", x0);
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) xn", xn);
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) delta",
        delta);
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) size",
        cdf.size());

    if (low < x0)
      low = x0;
    if (high > xn)
      high = xn;

    double F_low = cdf.F(low);
    double F_high = cdf.F(high);
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) F_low",
        F_low);
    LogFile::WriteData(
        "kriging.log",
        "smooth_indicator_function(CDF& cdf, double low, double high) F_high",
        F_high);
    double x = x0;
    for (diterator p = cdf.begin(); p != cdf.end(); ++p) {
      if (x < low)
        *p = 1.0;
      else if (x < high)
        *p = (F_high - *p) / (F_high - F_low);
      else
        *p = 0.0;
      x += delta;
    }
  }

  double ok_system_setup2(std::vector<double> &mat, size_t n_of_data,
                          const Variation &f, const Point *coord) {
    std::string fname("double ok_system_setup(vector<double> "
                      "&,int,V_Type,const Variation &,const Point *)");

    // setup ordinary kriging system
    // it assumes covariance f, not semivariogram
    // NOTE: In this routine,
    // mat is supposed to be a matrix of (n_of_data+1) by (n_of_data+1)
    // the actual argument passed in may have a bigger memory allocated.
    // Make sure that you correctly use the first (n_of_data+1)x(n_of_data+1)

    if (f.type() != Covariance)
      error("Covariance type is required.", fname);

    size_t cols = n_of_data + 1;
    size_t rows = cols;
    diterator first = mat.begin();

    // setup the matrix

    diterator pm;
    const Point *p = coord;
    const Point *pc;
    for (size_t row = 0; row < n_of_data; ++row, ++p) {
      pc = coord;
      pm = mat.begin() + row * cols;
      for (size_t col = 0; col < row; ++col) { // setup lower triangular part
        double gamma = f(dist(*p, *pc++));
        mat[row * cols + col] = gamma;
        mat[rows * col + row] = gamma;
      }
      mat[row * cols + row] = 0; // diagonal element;
    }
    pm = mat.begin() + n_of_data * cols; // last row
    for (int i = 0; i < n_of_data; ++i) {
      *pm++ = 1.0;
      mat[(i + 1) * cols - 1] = 1;
    }
    *pm = 0.0; // not necessarily mat.end()-1

    return 0.0;
  }

  int set_coord_sphere(int radius, int dim, Point *coord) {

    int n = 0;
    int dist;
    int rsquare = radius * radius;

    if (dim == 2) {
      for (int j = -radius; j <= radius; ++j) {
        for (int i = -radius; i <= radius; ++i) {
          dist = j * j + i * i;
          if (dist > rsquare)
            continue;
          if (j == 0 && i == 0)
            continue;
          coord[n] = Point(i, j, 0);
          ++n;
        }
      }
    } else if (dim == 3) {
      for (int k = -radius; k <= radius; ++k) {
        for (int j = -radius; j <= radius; ++j) {
          for (int i = -radius; i <= radius; ++i) {
            dist = k * k + j * j + i * i;
            if (dist > rsquare)
              continue;
            if (k == 0 && j == 0 && i == 0)
              continue;
            coord[n] = Point(i, j, k);
            ++n;
          }
        }
      }
    }
    return n;
  }

  size_t set_neighbor_sphere(long long w, int radius, const Grid &grid,
                             CT &status, CT &data, double *cond_data0,
                             const CDF &cdf0, unsigned char nPhase) {

    int depth = grid.n_z();
    int rows = grid.n_y();
    int cols = grid.n_x();

    const int z = static_cast<int>(w / (cols * rows));
    const int y = static_cast<int>((w - z * cols * rows) / cols);
    const int x = static_cast<int>((w - z * cols * rows) % cols);

    int dim = grid.dim();

    int from_d, to_d;
    if (dim == 2) {
      from_d = 0;
      to_d = 1;
    } else if (dim == 3) {
      from_d = z - radius;
      to_d = z + radius + 1;
    }
    const int from_r = y - radius;
    const int to_r = y + radius + 1;
    const int from_c = x - radius;
    const int to_c = x + radius + 1;

    int rsquare = radius * radius;

    // the ordering should match with that of set_coord_sphere() above
    size_t n = 0;
    for (long long k = from_d; k < to_d; ++k) {
      for (long long j = from_r; j < to_r; ++j) {
        for (long long i = from_c; i < to_c; ++i) {
          if ((k - z) * (k - z) + (j - y) * (j - y) + (i - x) * (i - x) >
              rsquare)
            continue;
          if ((k == z) && (j == y) && (i == x))
            continue;
          if (k < 0 || k >= depth || j < 0 || j >= rows || i < 0 || i >= cols) {
            cond_data0[n] = 0.5;
            //	cond_data1[n] = 0.5;
          } else {
            size_t index = (k * rows + j) * cols + i;
            uc pi = status[index];
            if (pi == marked_exterior) {
              cond_data0[n] = 0.5;
            } else if (pi == nPhase - 1 /*|| pi==filtered_PORE*/) {
              cond_data0[n] = 1.0; ///!!!!!
            } else if (pi == nPhase /*|| pi==filtered_ROCK*/) {
              cond_data0[n] = 0.0; //!!!!
            } else {
              double value = data[index];
              cond_data0[n] = cdf0.F(value);
              // cond_data1[n] = cdf1.F(value);
            }
          }
          ++n;
        }
      }
    }
    return n;
  }
  // {

  // 	int depth = grid.n_z();
  // 	int rows = grid.n_y();
  // 	int cols = grid.n_x();

  // 	const int	z = static_cast<int>(w / (cols*rows));
  // 	const int	y = static_cast<int>((w - z*cols*rows) / cols);
  // 	const int	x = static_cast<int>((w - z*cols*rows) % cols);

  // 	int dim = grid.dim();

  // 	int from_d, to_d;
  // 	if (dim == 2) {
  // 		from_d = 0;
  // 		to_d = 1;
  // 	}
  // 	else if (dim == 3) {
  // 		from_d = z - radius;
  // 		to_d = z + radius + 1;
  // 	}
  // 	const int	from_r = y - radius;
  // 	const int	to_r = y + radius + 1;
  // 	const int	from_c = x - radius;
  // 	const int	to_c = x + radius + 1;

  // 	int rsquare = radius*radius;

  // 	// the ordering should match with that of set_coord_sphere() above
  // 	size_t n = 0;
  // 	for (long long k = from_d; k<to_d; ++k) {
  // 		for (long long j = from_r; j<to_r; ++j) {
  // 			for (long long i = from_c; i<to_c; ++i) {
  // 				if ((k - z)*(k - z) + (j - y)*(j - y) + (i -
  // x)*(i
  // - x)
  // >
  // rsquare) continue; 				if ((k == z) && (j == y)
  // && (i
  // == x)) continue; 				if (k<0
  // || k >= depth || j<0 || j >= rows || i<0 || i >= cols) {
  // cond_data0[n] = 0.5;
  // 				//	cond_data1[n] = 0.5;
  // 				}
  // 				else {
  // 					size_t index = (k*rows + j)*cols + i;
  // 					uc pi = status[index];
  // 					if (pi == marked_exterior) {
  // 						cond_data0[n] = 0.5;
  // 					}
  // 					else if (pi == nPhase-1 /*||
  // pi==filtered_PORE*/)
  // { 						cond_data0[n] =1.0;///!!!!!
  // 					}
  // 					else if (pi == nPhase /*||
  // pi==filtered_ROCK*/)
  // { 						cond_data0[n] = 0.0;//!!!!
  // 					}
  // 					else
  // 					{
  // 						double value = data[index];
  // 						cond_data0[n] = cdf0.F(value);
  // 						//cond_data1[n] = cdf1.F(value);
  // 					}
  // 				}
  // 				++n;
  // 			}
  // 		}
  // 	}
  // 	return n;
  // }
};

#endif

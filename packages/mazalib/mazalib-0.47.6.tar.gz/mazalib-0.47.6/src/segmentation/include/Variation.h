#pragma once

#include "DynamicArray.h"
#include "Grid.h"
#include "LogFile.h"
#include "Point.h"
#include "util.h"

enum V_method {
  Unknown_V = 0,
  mw_semivariogram,
  classic_semivariogram,
  classic_covariance
};
enum V_type { Unknown_T = 0, Semivariogram, Covariance };
enum V_direction {
  Unknown_D = 0,
  Vertical,
  Horizontal,
  Isotropic,
  Slice_Isotropic,
  Diagonal
};

class Variation : public DynamicArray<double> {
public:
  double unit_lag_;
  V_direction direction_;
  V_method method_;
  V_type type_;
  V_type print_type_;
  friend std::istream &operator>>(std::istream &, Variation &);
  friend std::ostream &operator<<(std::ostream &, const Variation &);

  Variation(int m = 1, double dist = 1.0, V_direction d = Isotropic,
            V_method v = Unknown_V, V_type type = Semivariogram,
            V_type ptype = Semivariogram)
      : DynamicArray<double>(m + 1, 0.0), unit_lag_(dist), direction_(d),
        method_(v), type_(type), print_type_(ptype) {}
  Variation(const Variation &v)
      : DynamicArray<double>(v), unit_lag_(v.unit_lag_),
        direction_(v.direction_), method_(v.method_), type_(v.type_) {}
  Variation(std::istream &is)
      : DynamicArray<double>(0), unit_lag_(1.0), direction_(Isotropic),
        method_(mw_semivariogram), type_(Semivariogram) {
    is >> *this;
  };

  void make_covariance() {
    // change to covariance by var-gamma(r)
    if (type_ != Semivariogram)
      return;
    type_ = Covariance;
    print_type_ = Covariance;
    // double variance=back();//
    double variance = front();
    // for(int i=0;i<size();++i) (*this)[i]=variance-(*this)[i];
    for (int i = 1; i < size(); ++i)
      (*this)[i] = variance - (*this)[i];
  }

  void set_direction(char);
  void set_method(char);
  void set_type(char);
  void set_type(V_type t) { type_ = t; }

  void initialize(double d = 0.0) { fill(begin(), end(), d); }

  double variance() const { return (*this)[0]; }
  double unit_lag() const { return unit_lag_; };
  int max_lag() const { return static_cast<int>(size()) - 1; };
  V_direction direction() const { return direction_; };
  V_method method() const { return method_; };
  V_type type() const { return type_; };

  void operator+=(const Variation &v);
  void operator*=(const double m);
  void operator/=(const double m) { (*this) *= (1.0 / m); };
  double operator()(const double x) const;

  // Output Implementation

  void print(const char *msgs = "Variation structure is") const;

  // Driver for measured data

  void compute(const vector<float> &, const Point *,
               int dim); // driver for given data

  // Driver for 1d

  template <class Iterator>
  void compute(Iterator m, double mean, int size, int me = 0, int p = 1) {
    var_compute(*this, m, mean, size, me, p);
  }
  template <class Iterator>
  void compute(Iterator m, int *count, double mean, int size, int me = 0,
               int p = 1) {
    var_compute(*this, m, count, mean, size, me, p);
  }

  // Driver for 2d and 3d array

  template <class Iterator>
  void compute(Iterator m, const Grid &grid, int me = 0, int p = 1) {
    var_compute(*this, m, grid, me, p);
  }
  template <class Iterator>
  void variation_i(Iterator m, const Grid &grid, int me, int p) { // isotropic
    var_variation_i(*this, m, grid, me, p);
  }
  template <class Iterator>
  void variation_h(Iterator m, const Grid &grid, int me, int p) { // horizontal
    var_variation_h(*this, m, grid, me, p);
  }
  template <class Iterator>
  void variation_v(Iterator m, const Grid &grid, int me, int p) { // vertical
    var_variation_v(*this, m, grid, me, p);
  }

  template <class Iterator>
  void variation_slice(Iterator m, const Grid &grid, int me,
                       int p) { // 3d driver for slicewise isotropic
    var_variation_slice(*this, m, grid, me, p);
  }
};

template <class T>
void var_compute(Variation &var, const std::vector<T> &, const Point *,
                 int dim);

template <class Iterator>
void var_compute(Variation &var, Iterator m, double mean, int size, int me,
                 int p);

template <class Iterator>
void var_compute(Variation &var, Iterator m, int *count, double mean, int size,
                 int me, int p);

template <class Iterator>
void var_compute(Variation &var, Iterator m, const Grid &grid, int me, int p);

template <class Iterator>
void var_variation_i(Variation &var, Iterator m, const Grid &grid, int me,
                     int p);

template <class Iterator>
void var_variation_h(Variation &var, Iterator m, const Grid &grid, int me,
                     int p);

template <class Iterator>
void var_variation_v(Variation &var, Iterator m, const Grid &grid, int me,
                     int p);

template <class Iterator>
void var_variation_slice(Variation &var, Iterator m, const Grid &grid, int me,
                         int p);

// Moving window variogram

template <class T> // measured data
void mw_variogram(Variation &var, const std::vector<T> &, const Point *, int,
                  int, int);
template <class Iterator> // 1d generic
void mw_variogram(Variation &var, Iterator, int, int, int);
template <class Iterator> // 2d isotropic
void mw_variogram(Variation &var, Iterator, int, int, int, int);
template <class Iterator> // 3d isotropic
void mw_variogram(Variation &var, Iterator, int, int, int, int, int);

void add_derivative_correction(Variation &var, int dim);

// Classic semivariogram

template <class T> // measured data
void classic_variogram(Variation &var, const std::vector<T> &, const Point *,
                       int, int, int);
template <class Iterator> // 1d generic
void classic_variogram(Variation &var, Iterator, int, int, int);
template <class Iterator> // 1d generic
void classic_variogram(Variation &var, Iterator, int *, int, int, int);
template <class Iterator> // 2d isotropic
void classic_variogram(Variation &var, Iterator, int, int, int, int);
template <class Iterator> // 3d isotropic
void classic_variogram(Variation &var, Iterator, int, int, int, int, int);

// Classic covariance

template <class T> // measured data
void covariance(Variation &var, const std::vector<T> &, const Point *, int, int,
                int);
template <class Iterator> // 1d generic
void covariance(Variation &var, Iterator, double, int, int, int);
template <class Iterator> // 1d generic
void covariance(Variation &var, Iterator, int *, double, int, int, int);
template <class Iterator> // 2d isotropic
void covariance(Variation &var, Iterator, int, int, int, int);
template <class Iterator> // 3d isotropic
void covariance(Variation &var, Iterator, int, int, int, int, int);

template <class T>
void var_compute(Variation &var, const std::vector<T> &v, const Point *x,
                 int dim) {
  const int me = mynode();
  const int p = numnodes();

  switch (var.method_) {
  case classic_covariance:
    covariance(var, v.begin(), x, dim, me, p);
    break;
  case classic_semivariogram:
    classic_variogram(var, v.begin(), x, dim, me, p);
    break;
  case mw_semivariogram:
    mw_variogram(var, v.begin(), x, dim, me, p);
    break;
  case Unknown_V:
    // warning("Will not compute the variation");
    break;
  default:
    error("Not a valid method in Variation", "compute(...)");
  }
  var.front() = Utils::variance(v.begin(), v.end());
}

template <class Iterator>
void var_compute(Variation &var, Iterator v, double mean, int size, int me,
                 int p) {
  fill(var.begin(), var.end(), 0.0);

  switch (var.method()) {
  case classic_covariance:
    if (mean == 0.0)
      mean = Utils::mean(v, v + size);
    covariance(var, v, mean, size, me, p);
    break;
  case classic_semivariogram:
    classic_variogram(var, v, size, me, p);
    break;
  case mw_semivariogram:
    mw_variogram(var, v, size, me, p);
    break;
  case Unknown_V:
    // warning("Will not compute the variation");
    break;
  default:
    error("Not a valid method in Variation", "compute(...)");
  }
  var.front() = Utils::variance(v, v + size);
}

template <class Iterator>
void var_compute(Variation &var, Iterator v, int *count, double mean, int size,
                 int me, int p) {
  fill(var.begin(), var.end(), 0.0);

  switch (var.method()) {
  case classic_covariance:
    if (mean == 0.0)
      mean = Utils::mean(v, v + size);
    covariance(var, v, count, mean, size, me, p);
    break;
  case classic_semivariogram:
    classic_variogram(var, v, count, size, me, p);
    break;
  case mw_semivariogram:
    mw_variogram(var, v, size, me, p);
    break;
  case Unknown_V:
    // warning("Will not compute the variation");
    break;
  default:
    error("Not a valid method in Variation", "compute(...)");
  }
  var.front() = Utils::variance(v, v + size);
}

template <class Iterator>
void var_compute(Variation &var, Iterator m, const Grid &grid, int me,
                 int p) // me = 0, p = 1
{
  fill(var.begin(), var.end(), 0.0);
  switch (var.direction()) {
  case Isotropic:
    var.variation_i(m, grid, me, p);
    break;
  case V_direction::Horizontal:
    var.variation_h(m, grid, me, p);
    break;
  case V_direction::Vertical:
    var.variation_v(m, grid, me, p);
    break;
  case Slice_Isotropic:
    var.variation_slice(m, grid, me, p);
    break;
  default:; //  error("No such direction",fname);
  }
  LogFile::WriteData("kriging.log",
                     "	var.front()=::variance(m,m+grid.size());");
  var.front() = Utils::variance(m, m + grid.size());
}

template <class T>
void mw_variogram(Variation &var, const std::vector<T> &v, const Point *x,
                  int dim, int me, int p) {

  int n = v.size();
  int n_node = v.size(), n_offset = 0;

  DynamicArray_2d<double> m(n, var.size(), 0.0);
  DynamicArray_2d<double> D(n, var.size(), 0.0);
  int lag;
  for (int i = n_offset; i < n_offset + n_node; i++) {
    for (int j = 0; j < n; j++) {
      lag = iround((x[j] - x[i]).abs() / var.unit_lag());
      double *pm = m[i] + lag;
      double *pD = D[i] + lag;
      double square_diff = (v[j] - v[i]) * (v[j] - v[i]);
      for (int k = lag; k < var.size(); k++, pm++, pD++) {
        (*pm)++;
        (*pD) += square_diff;
      }
    }
  }

  auto pv = var.begin() + 1;
  for (lag = 1; lag < var.size(); lag++, pv++) {
    *pv = 0.0;
    auto pD = D.begin() + lag;
    auto pm = m.begin() + lag;
    for (int i = 0; i < n; i++, pD += D.cols(), pm += m.cols()) {
      if (*pm > 0)
        *pv += (*pD) / (*pm);
    }
    *pv /= (2.0 * n);
  }
  add_derivative_correction(var, dim);
}

template <class Iterator>
void mw_variogram(Variation &var, Iterator v, int length, int me, int p) {
  typedef typename Iterator::value_type T;
  const T ext_value = ::ext_value(T(0));
  int x_node = length, x_offset = 0;
  DynamicArray<double> Dh(length, 0.0);
  DynamicArray<int> mh(length, 0);

  for (int h = 1; h < var.size(); h++) {
    Iterator pv = v + x_offset;
    for (int x = x_offset; x < x_offset + x_node; ++x, ++pv) {
      if (*pv == ext_value)
        continue;
      // update Dh[index] and mh[index]
      double diff;
      if (x - h >= 0) { // left end
        if (*(pv - h) == ext_value)
          continue;
        diff = double(*(pv - h) - *pv);
        Dh[x] += float(diff * diff);
        mh[x]++;
      }
      if (x + h < length) { // right end
        if (*(pv + h) == ext_value)
          continue;
        diff = double(*(pv + h) - *pv);
        Dh[x] += diff * diff;
        mh[x]++;
      }
      var[h] += Dh[x] / mh[x];
    }
  }

  var /= double(2 * length);
  add_derivative_correction(var, 1);
}

template <class Iterator>
void classic_variogram(Variation &var, Iterator v, int length, int me, int p) {
  DynamicArray<int> count(var.size());
  classic_variogram(var, v, count.begin_pointer(), length, me, p);
}

template <class T>
void classic_variogram(Variation &var, const std::vector<T> &v, const Point *x,
                       int dim, int me, int p) {

  int n = v.size(), n_node = v.size(), n_offset = 0;

  DynamicArray<int> m(var.size(), 0);

  int h;
  for (int i = n_offset; i < n_offset + n_node; i++) {
    for (int j = 0; j < n; j++) {
      h = iround((x[j] - x[i]).abs() / var.unit_lag_);
      if (h > 0 && h < var.size()) {
        var[h] += (v[i] - v[j]) * (v[i] - v[j]);
        m[h]++;
      }
    }
  }
  for (h = 1; h < var.size(); h++) {
    if (m[h] > 0)
      var[h] *= (0.5 / m[h]);
  }
}

template <class Iterator>
void classic_variogram(Variation &var, Iterator v, int *count, int length,
                       int me, int p) {
  typedef typename Iterator::value_type T;
  const T ext_value = ::ext_value(T(0));
  count[0] = 0;

  int h;
  for (h = 1; h < var.size(); h++) {
    count[h] = 0;
    var[h] = 0.0;
    Iterator pv = v + me;
    for (int x = me; x < length - h; x += p, pv += p) {
      if (*pv == ext_value || *(pv + h) == ext_value)
        continue;
      double diff = (double)(*(pv + h) - *pv);
      var[h] += diff * diff;
      (count[h])++;
    }
  }
  for (h = 1; h < var.size(); h++) {
    if (count[h] > 0)
      var[h] /= (2.0 * count[h]);
  }

  var.front() = Utils::variance(v, v + length);
}

template <class T>
void covariance(Variation &var, const std::vector<T> &v, const Point *x,
                int dim, int me, int p) {
  int n = v.size(), n_node = v.size(), n_offset = 0;

  double mean = 0.0, variance = 0.0;
  Utils::stats(v.begin(), v.end(), mean, variance);
  var.front() = variance;

  DynamicArray<int> m(var.size(), 0);

  int h;
  for (int i = n_offset; i < n_offset + n_node; i++) {
    for (int j = 0; j < n; j++) {
      h = iround((x[j] - x[i]).abs() / var.unit_lag_);
      if (h > 0 && h < var.size()) {
        var[h] += (v[i] - mean) * (v[j] - mean);
        m[h]++;
      }
    }
  }
  for (h = 1; h < var.size(); h++) {
    if (m[h] > 0)
      var[h] /= m[h];
  }
}

template <class Iterator>
void covariance(Variation &var, Iterator v, double mean, int length, int me,
                int p) {
  DynamicArray<int> count(var.size());
  covariance(var, v, count.begin_pointer(), mean, length, me, p);
}

template <class Iterator>
void covariance(Variation &var, Iterator v, int *count, double mean, int length,
                int me, int p) {
  typedef typename Iterator::value_type T;
  const T ext_value = ::ext_value(T(0));
  count[0] = 0;

  if (mean == 0.0)
    mean = Utils::mean(v, v + length);

  int h;
  for (h = 0; h < var.size(); h++) {
    count[h] = 0;
    var[h] = 0.0;
    Iterator pv = v + me;
    for (int x = me; x < length - h; x += p, pv += p) {
      if (*pv == ext_value || *(pv + h) == ext_value)
        continue;
      var[h] += double((*(pv + h) - mean) * (*pv - mean));
      ++count[h];
    }
  }

  for (h = 1; h < var.size(); h++) {
    if (count[h] > 0)
      var[h] /= count[h];
  }
}

#include "var_2d.h"
#include "var_3d.h"

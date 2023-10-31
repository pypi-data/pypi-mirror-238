#pragma once
#include "Variation.h"
#include <exception>
template <class T>
void compute_D(const T *, std::vector<double> &, int, int, int, int, int);

template <class Iterator>
void var_variation_slice(Variation &var, Iterator m, const Grid &grid, int me,
                         int p)
// template <class T>
// void var_variation_slice(Variation& var, const T *m, const Grid& grid,
//			 int me, int p)
{
  std::string fname("void var_variation_slice(Variation& var, const T *,const "
                    "Grid&,int,int)");

  fill(var.begin(), var.end(), 0.0);
  Variation slice_var(var.max_lag(), var.unit_lag(), Isotropic, var.method(),
                      var.type());
  const int depth = grid.n_z();

  const int s_size = grid.n_x() * grid.n_y();
  typedef typename Iterator::value_type T;
  //  typedef float T;
  DynamicArray<T> slice(s_size);

  Grid fake = grid;
  fake.change_dim(2);
  for (int d = 0; d < depth; ++d) {
    if (d % p != me)
      continue;
    fill(slice_var.begin(), slice_var.end(), 0.0);
    copy(m + d * s_size, m + (d + 1) * s_size, slice.begin());
    slice_var.variation_i(slice.begin(), fake, me, 1);
    diterator pv = var.begin();
    diterator ps = slice_var.begin();
    while (pv < var.end()) {
      *pv += *ps;
      ++pv;
      ++ps;
    }
  }
  var.set_type(slice_var.type());
#ifdef MPI
  if (p > 1)
    global_sum(var.begin(), var.size());
#endif
  diterator pv = slice_var.begin();
  while (pv < var.end()) {
    *pv *= (1.0 / depth);
    ++pv;
  }
}

template <class Iterator>
void mw_variogram(Variation &var, Iterator m, int nx, int ny, int nz, int me,
                  int p) {
  std::string fname(
      "void mw_variogram(Variation&,Iterator,int,int,int,int,int)");
  LogFile::WriteData("kriging.log",
                     "mw_variogram(Variation &var, Iterator m,	int nx, int "
                     "ny, int nz, int me, int p)");

  int maxlag = var.max_lag();

  const int size_ = static_cast<int>(var.size());
  DynamicArray<double> D(size_, 0.0);

  LogFile::WriteData("kriging.log", "D Size:", D.size());

  typedef typename Iterator::value_type T;
  const T ext_val = ext_value(T(0));

  LogFile::WriteData("kriging.log", "nx:", nx);
  LogFile::WriteData("kriging.log", "ny:", ny);
  LogFile::WriteData("kriging.log", "nz:", nz);

  size_t offset = 0;
  size_t n_node = (size_t)nx * ny * nz;

#ifdef MPI
  if (p > 1)
    divide_by_pnodes(nx * ny * nz, n_node, offset, me, p);
#endif
  size_t to = offset + n_node;
  Iterator pp = m + offset;
  var.print();
  const int nSamples = 500;
  size_t index_inc = n_node / nSamples;
  LogFile::WriteData("kriging.log", "n_node:", n_node);
  LogFile::WriteData("kriging.log", "nSamples:", nSamples);
  LogFile::WriteData("kriging.log", "index_inc:", index_inc);

  try {
    for (size_t index = offset; index < to - index_inc;
         index += index_inc, pp += index_inc) {
      if (*pp == ext_val)
        continue;
      compute_D(m, D, nx, ny, nz, index, maxlag);
      for (int h = 1; h < size_; ++h)
        var[h] += D[h];
      LogFile::WriteData("kriging.log",
                         "or (size_t index = offset; index<to - index_inc; "
                         "index += index_inc, pp += index_inc)",
                         index_inc);
    }

#ifdef MPI
    if (p > 1)
      global_sum(var.begin(), var.size());
#endif
    var.print();
    diterator pv = var.begin();
    while (pv < var.end()) {
      *pv *= (0.5 / (n_node));
      ++pv;
    }

    LogFile::WriteData("kriging.log", "add_derivative_correction(var, 3);");

    add_derivative_correction(var, 3);
    LogFile::WriteData("kriging.log",
                       "add_derivative_correction(var, 3) finished;");
    var.print();
  } catch (std::exception &e) {
    LogFile::WriteData("kriging.log", "Exception caught in mw_variogram: ");
    LogFile::WriteData("kriging.log", e.what());
  }
}

template <class Iterator>
void compute_D(Iterator m, std::vector<double> &D, int cols, int rows,
               int depth, long long index, int lag) {
  LogFile::WriteData("kriging.log", "compute_D");
  const int nxy = rows * cols;

  const long long z = index / nxy;
  const long long y = (index - z * nxy) / cols;
  const long long x = (index - z * nxy) % cols;
  //	LogFile::WriteData("kriging.log", "compute_D index", index);
  long long i, j, k, mh = 0;
  D[0] = 0.0;

  long long startd, tod;
  long long startr, tor;
  long long startc, toc;

  double diff, tmpDh, Dh_1;
  Iterator p;
  typedef typename Iterator::value_type T;
  const T center = m[index];
  // LogFile::WriteData("kriging.log", "compute_D    ext_val;", index);
  const T ext_val = ext_value(T(0));
  // LogFile::WriteData("kriging.log", "compute_D    register T v;", index);
  register T v;

  //  for (int h=0;h<=lag;++h) {
  for (int h = 1; h <= lag; ++h) {
    // LogFile::WriteData("kriging.log", " for (int h=1;h<=lag;++h) h:",h);
    Dh_1 = mh * D[h - 1];
    tmpDh = 0.0;

    startr = std::max<long long>(y - h, 0);
    tor = std::min<long long>(y + h + 1, rows);
    startc = std::max<long long>(x - h, 0);
    toc = std::min<long long>(x + h + 1, cols);

    // update D[h] and mh by adding the contributioins
    // from the boundary of the window

    // LogFile::WriteData("kriging.log", "compute_D    if ((k=z-h) >= 0) {
    // ;", index);
    if ((k = z - h) >= 0) {
      for (j = startr; j < tor; ++j) {
        p = m + (k * rows + j) * cols + startc;
        for (i = startc; i < toc; ++i, ++p) {
          if ((v = *p) == ext_val)
            continue;
          diff = (double)(v - center);
          tmpDh += diff * diff;
          ++mh;
        }
      }
    }
    //	LogFile::WriteData("kriging.log", "compute_D   if ((k=z+h) < depth) {
    //;", index);
    if ((k = z + h) < depth) {
      for (j = startr; j < tor; ++j) {
        p = m + (k * rows + j) * cols + startc;
        for (i = startc; i < toc; ++i, ++p) {
          if ((v = *p) == ext_val)
            continue;
          diff = (double)(v - center);
          tmpDh += diff * diff;
          ++mh;
        }
      }
    }
    //	LogFile::WriteData("kriging.log", "compute_D startd = max<size_t>(z - h
    //+ 1, 0);", index);
    startd = std::max<long long>(z - h + 1, 0);
    tod = std::min<long long>(z + h, depth);
    if ((j = y - h) >= 0) {
      for (k = startd; k < tod; ++k) {
        p = m + (k * rows + j) * cols + startc;
        for (i = startc; i < toc; ++i, ++p) {
          if ((v = *p) == ext_val)
            continue;
          diff = (double)(v - center);
          tmpDh += diff * diff;
          ++mh;
        }
      }
    }
    // LogFile::WriteData("kriging.log", "compute_D if ((j=y+h)<rows) {",
    // index);
    if ((j = y + h) < rows) {
      for (k = startd; k < tod; ++k) {
        p = m + (k * rows + j) * cols + startc;
        for (i = startc; i < toc; ++i, ++p) {
          if ((v = *p) == ext_val)
            continue;
          diff = (double)(v - center);
          tmpDh += diff * diff;
          ++mh;
        }
      }
    }
    // LogFile::WriteData("kriging.log", "startr=max<size_t>(y-h+1,0);", index);
    startr = std::max<long long>(y - h + 1, 0);
    tor = std::min<long long>(y + h, rows);
    if ((i = x - h) >= 0) {
      for (k = startd; k < tod; ++k) {
        long long idx = (k * rows + startr) * cols + i;
        // LogFile::WriteData("kriging.log", "idx", idx);
        p = m + idx;

        // for(j=startr;j<tor;++j,p+=rows) {
        for (j = startr; j < tor - 1; ++j, p += rows) {
          if ((v = *p) == ext_val)
            continue;
          diff = (double)(v - center);
          tmpDh += diff * diff;
          ++mh;
        }
      }
    }
    //	LogFile::WriteData("kriging.log", "if( (i=x+h) <cols) {", index);
    if ((i = x + h) < cols) {
      for (k = startd; k < tod; ++k) {
        long long idx = (k * rows + startr) * cols + i;
        //		LogFile::WriteData("kriging.log", "idx", idx);
        p = m + idx;
        //	for(j=startr;j<tor;++j,p+=rows) {
        for (j = startr; j < tor - 1; ++j, p += rows) {
          if ((v = *p) == ext_val)
            continue;
          diff = (double)(v - center);
          tmpDh += diff * diff;
          ++mh;
        }
      }
    }
    if (mh > 0) {
      // LogFile::WriteData("kriging.log", "if (mh > 0) { h:", h);
      // LogFile::WriteData("kriging.log", "if (mh > 0) { mh:", mh);
      D[h] = (Dh_1 + tmpDh) / mh;
    }
  }
}

template <class Iterator>
void classic_variogram(Variation &var, Iterator m, int nx, int ny, int nz,
                       int me, int p) {
  const std::string fname(
      "void classic_variogram(Variation&,const T *m, int, int, int, int, int)");
  test(fname);

  const int maxlag = var.max_lag();
  const int depth = nz;
  const int rows = ny;
  const int cols = nx;

  DynamicArray<size_t> count(var.size(), static_cast<const size_t &>(0UL));
  fill(var.begin(), var.end(), 0.0);
  size_t h;
  double diff;
  typedef typename Iterator::value_type T;
  T v, v1;
  const T ext_val = ext_value(T(0));

  for (int k = me; k < depth; k += p) {

    const int from_z = std::max<int>(0, k - maxlag);
    const int to_z = std::min<int>(depth, k + maxlag + 1);

    for (int j = 0; j < rows; j += p) {

      const int from_y = std::max<int>(0, j - maxlag);
      const int to_y = std::min<int>(rows, j + maxlag + 1);

      for (int i = 0; i < cols; ++i) {

        if ((v = m[(k * rows + j) * cols + i]) == ext_val)
          continue;

        const int from_x = std::max<int>(0, i - maxlag);
        const int to_x = std::min<int>(cols, i + maxlag + 1);

        for (int z = from_z; z < to_z; ++z) {
          for (int y = from_y; y < to_y; ++y) {
            Iterator pm = m + (z * rows + y) * cols + from_x;
            for (int x = from_x; x < to_x; ++x, ++pm) {
              if ((v1 = *pm) == ext_val)
                continue;
              h = iround(sqrt(double((x - i) * (x - i) + (y - j) * (y - j) +
                                     (z - k) * (z - k))));
              if (h > maxlag)
                continue;
              diff = double(v1) - double(v);
              var[h] += diff * diff;
              ++count[h];
            }
          }
        }
      }
    }
  }

#ifdef MPI
  if (p > 1) {
    global_sum(var.begin(), var.size());
    global_sum(count.begin(), count.size());
  }
#endif
  for (h = 1; h <= maxlag; h++) {
    if (count[h] > 0UL)
      var[h] /= (2.0 * count[h]);
  }
}

template <class Iterator>
void covariance(Variation &var, Iterator m, int nx, int ny, int nz, int me,
                int p) {
  std::string fname("void covariance(Variation&,Iterator,int,int,int,int,int)");
  test(fname);

  double mean = Utils::mean(m, m + nx * ny * nz);

  const int maxlag = var.max_lag();
  const int depth = nz;
  const int rows = ny;
  const int cols = nx;

  DynamicArray<int> count(var.size(), 0);
  fill(var.begin(), var.end(), 0.0);
  int h;
  double v, v1;
  typedef typename Iterator::value_type T;
  const T ext_val = ext_value(T(0));

  for (int k = me; k < depth; k += p) {

    const int from_z = std::max(0, k - maxlag);
    const int to_z = std::min(depth, k + maxlag + 1);

    for (int j = 0; j < rows; ++j) {

      const int from_y = std::max(0, j - maxlag);
      const int to_y = std::min(rows, j + maxlag + 1);

      for (int i = 0; i < cols; ++i) {

        if ((v = m[(k * rows + j * cols) + i]) == ext_val)
          continue;

        const int from_x = std::max(0, i - maxlag);
        const int to_x = std::min(cols, i + maxlag + 1);

        for (int z = from_z; z < to_z; ++z) {
          for (int y = from_y; y < to_y; ++y) {
            for (int x = from_x; x < to_x; ++x) {
              if ((v1 = m[(z * rows + y) * cols + x]) == ext_val)
                continue;
              h = iround(sqrt(double((x - i) * (x - i) + (y - j) * (y - j) +
                                     (z - k) * (z - k))));
              if (h > maxlag)
                continue;
              var[h] += (v1 - mean) * (v - mean);
              ++count[h];
            }
          }
        }
      }
    }
  }

#ifdef MPI
  if (p > 1) {
    global_sum(var.begin(), var.size());
    global_sum(count.begin(), count.size());
  }
#endif
  for (h = 1; h <= maxlag; h++) {
    if (count[h] > 0)
      var[h] /= count[h];
  }
}

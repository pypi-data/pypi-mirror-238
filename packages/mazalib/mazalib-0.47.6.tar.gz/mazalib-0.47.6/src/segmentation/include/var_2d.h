#pragma once
/*
 *	Copyrighted, Research Foundation of SUNY, 1998
 */

template <class T>
void compute_D(const T *, std::vector<double> &, int, int, int, int);

template <class Iterator>
void var_variation_i(Variation &var, Iterator m, const Grid &grid, int me,
                     int p) {
  std::string fname(
      "void var_variation_i(Variation&,const T *,const Grid&,int,int)");
  LogFile::WriteData("kriging.log", "var_variation_i");

  int nx = grid.n_x();
  int ny = grid.n_y();
  int nz = grid.n_z();

  int dim = grid.dim();

  if (dim == 2) {
    switch (var.method()) {
    case mw_semivariogram:
      mw_variogram(var, m, nx, ny, me, p);
      break;
    case classic_semivariogram:
      classic_variogram(var, m, nx, ny, me, p);
      break;
    case classic_covariance:
      covariance(var, m, nx, ny, me, p);
      break;
    case Unknown_V:
      warning("Will not compute the variation");
      break;
    default:
      error("No such variatuion method", "");
    }
  } else if (dim == 3) {
    switch (var.method()) {
    case mw_semivariogram:
      var.set_type(Semivariogram);
      mw_variogram(var, m, nx, ny, nz, me, p);
      break;
    case classic_semivariogram:
      var.set_type(Semivariogram);
      classic_variogram(var, m, nx, ny, nz, me, p);
      break;
    case classic_covariance:
      var.set_type(Covariance);
      covariance(var, m, nx, ny, nz, me, p);
      break;
    case Unknown_V:
      warning("Unknown method for semivariogram/covariance", fname.c_str());
      break;
    default:
      error("No such variatuion method", fname);
    }
  }
}

template <class Iterator>
void var_variation_h(Variation &var, Iterator m, const Grid &grid, int me,
                     int p) {
  std::string fname(
      "void var_variation_h(Variation&,const T*, const Grid&, int, int)");
  if (grid.dim() == 2 && grid.n_z() != 1)
    error("Grid error", fname);
  // int * cm=&(*m);
  double mean0 = Utils::mean(m, m + grid.size());

  fill(var.begin(), var.end(), 0.0);
  Variation tmp(var.max_lag(), var.unit_lag(), V_direction::Horizontal,
                var.method(), var.type());
  int col = grid.n_x();
  size_t nyz = grid.n_y() * grid.n_z();
  ;

  DynamicArray<int> count(tmp.size());
  for (size_t j = me; j < nyz; j = j + p) {
    fill(tmp.begin(), tmp.end(), 0.0);
    Iterator pt0 = m + j * col;
    tmp.compute(pt0, count.begin_pointer(), mean0, col);
    diterator pv = var.begin();
    diterator ptmp = tmp.begin();
    while (pv != var.end()) {
      *pv++ += *ptmp++;
    }
  }
#ifdef MPI
  if (p > 1)
    global_sum(var.begin(), var.size());
#endif
  if (nyz > 1) {
    diterator pv = var.begin();
    while (pv < var.end()) {
      *pv++ *= (1.0 / nyz);
    }
  }
}

template <class Iterator>
void var_variation_v(Variation &var, Iterator m, const Grid &grid, int me,
                     int p) {
  std::string fname(
      "void var_variation_v(Variation&,const T*,const Grid&,int,int)");
  not_implemented(fname);

  if (grid.dim() == 2 && grid.n_z() != 1)
    error("Grid error", fname);

  double mean = Utils::mean(m, m + grid.size());

  fill(var.begin(), var.end(), 0.0);

  int cols = grid.n_x();
  int rows = grid.n_y();
  int depth = grid.n_z();

  Variation tmp(var.max_lag(), var.unit_lag(), V_direction::Vertical,
                var.method(), var.type());

  typedef typename Iterator::value_type T;
  DynamicArray<T> column(rows);

  for (int k = 0; k < depth; ++k) {  // process k-th slice
    for (int i = 0; i < cols; ++i) { // process i-th column
      if ((k * cols + i) % p != me)
        continue;
      fill(tmp.begin(), tmp.end(), 0.0);
      auto pt = m + k * cols * rows + i;
      auto pc = column.begin();
      for (int j = 0; j < rows; ++j) {
        *pc++ = *pt;
        pt += cols;
      }
      tmp.compute(column.begin(), mean, rows);
      diterator pv = var.begin();
      diterator ptmp = tmp.begin();
      while (pv < var.end()) {
        *pv += *ptmp;
        ++pv;
        ++ptmp;
      }
    }
  }
  var.set_type(tmp.type());
#ifdef MPI
  if (p > 1)
    global_sum(begin(), size());
#endif
  diterator pv = var.begin();
  while (pv < var.end()) {
    *pv *= (1.0 / cols * depth);
    ++pv;
  }
}

template <class Iterator>
void mw_variogram(Variation &var, Iterator m, int nx, int ny, int me, int p) {
  DynamicArray<double> D(var.size(), 0.0);
  typedef typename Iterator::value_type T;
  const T ext_value = ::ext_value(T(0));

  int offset = 0;
  int n_node = nx * ny;
#ifdef _PARALLEL
  if (p > 1)
    divide_by_pnodes(nx * ny, n_node, offset, me, p);
#endif
  int to = offset + n_node;

  Iterator pp = m + offset;
  for (int index = offset; index < to; ++index, ++pp) {
    if (*pp == ext_value)
      continue;
    compute_D(m, D, nx, ny, index, var.max_lag());
    for (int h = 1; h < var.size(); ++h)
      var[h] += D[h];
  }

#ifdef _PARALLEL
  if (p > 1)
    global_sum(pt, size());
#endif
  diterator pv = var.begin();
  while (pv != var.end()) {
    *pv++ *= (0.5 / (nx * ny));
  }
  add_derivative_correction(var, 2);
}

template <class Iterator>
void compute_D(Iterator m, std::vector<double> &D, int cols, int rows,
               int index, int lag) {
  const int y = index / cols;
  const int x = index % cols;

  int mh = 0;
  D[0] = 0.0;

  int startc, toc;
  int startr, tor;

  double diff, tmpDh, Dh_1;
  Iterator p;
  typedef typename Iterator::value_type T;
  const T center = m[index];
  const T ext_val = ext_value(T(0));

  register T v;

  for (int h = 1; h <= lag; ++h) {

    Dh_1 = mh * D[h - 1];
    tmpDh = 0.0;

    startc = std::max(x - h, 0);
    toc = std::min(x + h + 1, cols);

    // update D[h] and mh by adding the contributioins
    // from the boundary of the window

    if (y - h >= 0) { // bottom side;
      p = m + (y - h) * cols + startc;
      for (int i = startc; i < toc; ++i, ++p) {
        if ((v = *p) == ext_val)
          continue;
        diff = double(v - center);
        tmpDh += diff * diff;
        ++mh;
      }
    }
    if (y + h < rows) { // top side;
      p = m + (y + h) * cols + startc;
      for (int i = startc; i < toc; ++i, ++p) {
        if ((v = *p) == ext_val)
          continue;
        diff = double(v - center);
        tmpDh += diff * diff;
        ++mh;
      }
    }

    startr = std::max(y - h + 1, 0);
    tor = std::min(y + h, rows);
    if (x - h >= 0) { // left side;
      p = m + startr * cols + x - h;
      for (int j = startr; j < tor - 1; ++j, p += rows) {
        if ((v = *p) == ext_val)
          continue;
        diff = double(v - center);
        tmpDh += diff * diff;
        ++mh;
      }
    }
    if (x + h < cols) { // right side;!!!!
      p = m + startr * cols + x + h;
      for (int j = startr; j < tor - 1; ++j, p += rows) {
        if ((v = *p) == ext_val)
          continue;
        diff = double(v - center);
        tmpDh += diff * diff;
        ++mh;
      }
    }
    if (mh > 0)
      D[h] = (Dh_1 + tmpDh) / mh;
  }
}

template <class Iterator>
void classic_variogram(Variation &var, Iterator m, int nx, int ny, int me,
                       int p) {
  std::string fname(
      "void classic_variogram(Variation&,const T*,int,int,int,int)");

  const int maxlag = var.max_lag();
  const int rows = ny;
  const int cols = nx;

  DynamicArray<int> count(var.size(), 0);
  fill(var.begin(), var.end(), 0.0);
  int h;
  register double diff;
  typedef typename Iterator::value_type T;
  register T v, v1, ext_value = ::ext_value(T(0));

  for (int j = me; j < rows; j += p) {

    const int from_y = std::max(0, j - maxlag);
    const int to_y = std::min(rows, j + maxlag + 1);

    for (int i = 0; i < cols; ++i) {

      if ((v = m[j * cols + i]) == ext_value)
        continue;
      const int from_x = std::max(0, i - maxlag);
      const int to_x = std::min(cols, i + maxlag + 1);

      for (int y = from_y; y < to_y; ++y) {
        Iterator pm = m + y * cols + from_x;
        for (int x = from_x; x < to_x; ++x, ++pm) {
          if ((v1 = *pm) == ext_value)
            continue;
          h = iround(sqrt(double((x - i) * (x - i) + (y - j) * (y - j))));
          if (h > maxlag)
            continue;
          diff = double(v1 - v);
          var[h] += diff * diff;
          ++count[h];
        }
      }
    }
  }

#ifdef _PARALLEL
  if (p > 1) {
    global_sum(var.begin(), var.size());
    global_sum(count.begin(), count.size());
  }
#endif
  for (h = 1; h <= maxlag; h++) {
    if (count[h] > 0)
      var[h] /= (2.0 * count[h]);
  }
}

template <class Iterator>
void covariance(Variation &var, Iterator m, int nx, int ny, int me, int p) {
  std::string fname(
      "void Variation::covariance(Variation &var,const T*,int,int,int,int)");

  double mean = Utils::mean(m, m + nx * ny);

  const int maxlag = var.max_lag();
  const int rows = ny;
  const int cols = nx;

  DynamicArray<int> count(var.size(), 0);
  fill(var.begin(), var.end(), 0.0);
  int h;
  typedef typename Iterator::value_type T;
  T v, v1, ext_value = ::ext_value(T(0));

  for (int j = me; j < rows; j += p) {

    const int from_y = std::max(0, j - maxlag);
    const int to_y = std::min(rows, j + maxlag + 1);

    for (int i = 0; i < cols; ++i) {

      if ((v = m[j * cols + i]) == ext_value)
        continue;
      const int from_x = std::max(0, i - maxlag);
      const int to_x = std::min(cols, i + maxlag + 1);

      for (int y = from_y; y < to_y; ++y) {
        for (int x = from_x; x < to_x; ++x) {
          if ((v1 = m[y * cols + x]) == ext_value)
            continue;
          h = iround(sqrt(double((x - i) * (x - i) + (y - j) * (y - j))));
          if (h > maxlag)
            continue;
          var[h] += (double(v1) - mean) * (double(v) - mean);
          ++count[h];
        }
      }
    }
  }
#ifdef _PARALLEL
  if (p > 1) {
    global_sum(var.begin(), var.size());
    global_sum(count.begin(), count.size());
  }
#endif
  for (h = 1; h <= maxlag; h++) {
    if (count[h] > 0)
      var[h] /= (float)count[h];
  }
}

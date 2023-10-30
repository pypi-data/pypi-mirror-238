/*
 *	Copyrighted, Research Foundation of SUNY, 1998
 */

#ifndef _DynamicArray_H_
#define _DynamicArray_H_

#include "Point3d.h"
#include <algorithm>
#include <assert.h>
#include <cinttypes>
#include <exception>
#include <fstream>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "util.h"
// using namespace std;

typedef std::vector<double>::iterator diterator;
typedef std::vector<float>::iterator fiterator;
typedef std::vector<int>::iterator iiterator;
typedef std::vector<unsigned char>::iterator uiterator;

// class DynamicArray is inherited from the class vector
inline float sqr(float a) { return a * a; }

// template <class RAIter>
// struct sort_idxtbl_pair
//{
//	RAIter it;
//	int i;
//	bool operator<(const sort_idxtbl_pair& s)
//	{
//		return (*it) < (*(s.it));
//	}
//	void set(const RAIter& _it, int _i) { it = _it; i = _i; }
//	sort_idxtbl_pair() {}
// };

template <class T> struct IPair {
  IPair() = default;
  IPair(T mval, std::size_t mi) : val(mval), i(mi) {}
  T val{0};
  std::size_t i{0};
};

template <class T> bool myfunc(const IPair<T> &p1, const IPair<T> &p2) {
  return p1.val < p2.val;
}

template <class T> void sort_idxtbl(const std::vector<T> &ar, int *pidxtbl) {

  std::vector<IPair<T>> newv(ar.size());
  for (std::size_t i = 0; i < ar.size(); ++i) {
    newv[i] = IPair<T>(ar[i], i);
  }

  std::sort(newv.begin(), newv.end(), myfunc<T>);

  int *pi = pidxtbl;
  for (std::size_t ind = 0; ind < newv.size(); pi++, ind++) {
    *pi = newv[ind].i;
  }
}

template <class T> class qqq : public std::vector<T> {
public:
  qqq(size_t nsize) : std::vector<T>(nsize){};
};

template <class T>
class DynamicArray : public std::vector<T> // BigDynamicArray<T>// vector<T>
{
protected:
  size_t interior_;

public:
  T *begin_pointer() { return &(*(std::vector<T>::begin())); }
  DynamicArray(const size_t size = 1)
      : std::vector<T>(size),
        interior_(size) { // vector<T>(size), interior_(size) {
  }
  DynamicArray(const size_t size, const T &init)
      : std::vector<T>(size, init), interior_(size) {
    // MEMCHECK((void*)(begin_pointer()),"",sizeof(T)*size);
  }
  DynamicArray(const size_t size, const T *from)
      : std::vector<T>(from, from + size), interior_(size) {
    //  MEMCHECK((void*)(begin_pointer()),"",sizeof(T)*size);
  }
  template <class Iterator>
  DynamicArray(Iterator first, Iterator last)
      : // vector<typename Iterator::value_type>(first,last),
        std::vector<T>(first, last), interior_(last - first) {
    // MEMCHECK((void*)(begin_pointer()),"",sizeof(*first)*(last-first));
  }
  DynamicArray(const T *first, const T *last)
      : std::vector<T>(first, last), interior_(last - first) {
    MEMCHECK((void *)(begin_pointer()), "", sizeof(T) * (last - first));
  }
  DynamicArray(const DynamicArray<T> &from) // This constructior is necessary to
                                            // keep the memory usage correct
      : std::vector<T>(from), interior_(from.size()) {
    // MEMCHECK((void*)(begin_pointer()),"",sizeof(T)*from.size());
  }
  DynamicArray(const std::vector<T> &from)
      : std::vector<T>(from), interior_(from.size()) {
    //  MEMCHECK((void*)(begin_pointer()),"",sizeof(T)*from.size());
  }
  ~DynamicArray() { /* DELETE((void*)(begin_pointer()),sizeof(T)*this->size());
                     */
  }

  DynamicArray(const size_t, const std::string &, const char);
  //  DynamicArray(const Grid&, const vector<Point>&, const T*);

  void operator-() {
    T *p = this->start;
    while (p != this->end()) {
      *p = -(*p);
      ++p;
    }
  }
  void operator*=(const double a);
  void operator/=(const double a) { (*this) *= (1.0 / a); }
  void operator+=(const T a);
  //  void operator-=(const T a) { (*this)+=(-a); }

  DynamicArray<T> operator+(const DynamicArray<T> &) const;
  DynamicArray<T> operator-(const DynamicArray<T> &) const;
  void operator+=(const DynamicArray<T> &);
  void operator-=(const DynamicArray<T> &);

  size_t interior() const { return interior_; }
  void set_interior(const size_t n) { interior_ = n; }

  void initialize(const T &d) { fill(this->begin(), this->end(), d); }

  void print(const char *file, const char *msg = "DynamicArray is ") const;
  void print(std::ostream &os = std::cout,
             const char *msg = "DynamicArray is ") const;
};

template <class T>
DynamicArray<T>::DynamicArray(const size_t n, const std::string &filename,
                              const char type)
    : qqq<T>(n), interior_(n) {
  std::string fname(
      "DynamicArray<T>::DynamicArray(const int, const string&, const char)");
  if (n < 1)
    error("This should not happen", fname);

  // ifstream file(const char *char_string(filename));
  std::ifstream file(filename.c_str()); //. (const char *char_string());
  if (file.fail())
    file_error(filename, fname);

  T *pp = this->begin();
  switch (type) {
  case 'a':
    while (pp != this->end())
      file >> *pp++;
    break;
  case 'b':
    file.read((char *)pp, n * sizeof(T));
    break;
  default:
    error("Only binary or ascii type available", fname);
  }
  file.close();
}

template <class T> void DynamicArray<T>::operator+=(const DynamicArray<T> &m) {
  std::string fname(
      "void DynamicArray<T>::operator+=(const DynamicArray<T>& m)");
  if (this->size() != m.size())
    error("Not compatible size", fname);
  std::transform(this->begin(), this->end(), m.begin(), this->begin(),
                 std::plus<T>());
}

template <class T> void DynamicArray<T>::operator-=(const DynamicArray<T> &m) {
  std::string fname(
      "void DynamicArray<T>::operator-=(const DynamicArray<T>& m)");
  if (this->size() != m.size())
    error("Not compatible size", fname);
  std::transform(this->begin(), this->end(), m.begin(), this->begin(),
                 std::minus<T>());
}

template <class T>
DynamicArray<T> DynamicArray<T>::operator+(const DynamicArray<T> &m) const {
  std::string fname("DynamicArray<T> DynamicArray<T>::operator+(const "
                    "DynamicArray<T>&) const");
  if (this->size() != m.size())
    error("Not compatible size", fname);
  DynamicArray<T> sum(m.size());
  std::transform(this->begin(), this->end(), m.begin(), sum.begin(),
                 std::plus<T>());
  return sum;
}

template <class T>
DynamicArray<T> DynamicArray<T>::operator-(const DynamicArray<T> &m) const {
  std::string fname("DynamicArray<T> DynamicArray<T>::operator-(const "
                    "DynamicArray<T>&) const");
  if (this->size() != m.size())
    error("Not compatible size", fname);
  DynamicArray<T> diff(m.size());
  std::transform(this->begin(), this->end(), m.begin(), diff.begin(),
                 std::minus<T>());
  return diff;
}

template <class T> void DynamicArray<T>::operator*=(const double number) {
  T *p = this->begin();
  while (p != this->end())
    *p++ *= T(number);
}

template <class T> void DynamicArray<T>::operator+=(const T number) {
  T *p = this->begin();
  while (p != this->end())
    *p++ += number;
}

//
// class DynamicArray_2d is inherited from the class DynamicArray
//

template <class T> class DynamicArray_2d : public DynamicArray<T> {
protected:
  int rows_, cols_;

public:
  DynamicArray_2d(int row = 1, int col = 1)
      : DynamicArray<T>(row * col), rows_(row), cols_(col) {}
  DynamicArray_2d(int row, int col, const T &init)
      : DynamicArray<T>(row * col, init), rows_(row), cols_(col) {}
  DynamicArray_2d(int row, int col, const T *from)
      : DynamicArray<T>(row * col, from), rows_(row), cols_(col) {}
  DynamicArray_2d(int rows, int cols, const char *fn, const char flag)
      : DynamicArray<T>(rows * cols, fn, flag), rows_(rows), cols_(cols) {}
  DynamicArray_2d(const DynamicArray_2d<T> &from)
      : DynamicArray<T>(DynamicArray<T>(from)), rows_(from.rows_),
        cols_(from.cols_) {}

  T *operator[](int j) { return this->start + j * cols_; }
  const T *operator[](int j) const { return this->start + j * cols_; }
  T &operator()(int j, int i) {
    return *(this->begin_pointer() + j * cols_ + i);
  }
  const T &operator()(int j, int i) const {
    return *(this->start + j * cols_ + i);
  }

  DynamicArray<T> column(int col) const {
    DynamicArray<T> column_vector(rows_, T(0));
    for (int i = 0; i < rows_; i++)
      column_vector[i] = this->start[i * cols_ + col];
    return column_vector;
  }
  DynamicArray<T> row(int i) const {
    return DynamicArray<T>(cols_, this->start + i * cols_);
  }
  void set_row(int, const DynamicArray<T> &);

  int rows() const { return rows_; }
  int cols() const { return cols_; }

  void transpose(const DynamicArray_2d<T> &);
  void print(std::ostream &os = std::cout,
             const char *msg = "DynamicArray_2d is") const;
};

template <class T>
void DynamicArray_2d<T>::set_row(int i, const DynamicArray<T> &v) {
  std::string fname(
      "void DynamicArray_2d<T>::set_row(int, const DynamicArray<T>&)");

  if (cols_ != v.size())
    error("not compatible in size", fname);
  T *p = this->begin() + i * cols_;
  copy(v.begin(), v.end(), p);
}

template <class T>
void DynamicArray_2d<T>::transpose(const DynamicArray_2d<T> &m) {
  std::string fname(
      "void DynamicArray_2d<T>::transpose(const DynamicArray_2d<T>&)");
  if (cols_ != m.rows() || rows_ != m.cols()) {
    error("Not compatible in size", fname);
  }
  for (int i = 0; i < rows_; i++) {
    const T *from = m.begin();
    T *row = this->start + i * cols_;
    copy(row, from + i, cols_, m.cols());
  }
}

//
// class DynamicArray_3d is inherited from the class DynamicArray
//

template <class T> class DynamicArray_3d : public ::DynamicArray<T> {
protected:
  int depth_, rows_, cols_;

public:
  DynamicArray_3d(const int depth = 1, const int row = 1, const int col = 1)
      : DynamicArray<T>(depth * row * col), depth_(depth), rows_(row),
        cols_(col) {}
  DynamicArray_3d(const int depth, const int row, const int col, const T init)
      : DynamicArray<T>(depth * row * col, init), depth_(depth), rows_(row),
        cols_(col) {}
  DynamicArray_3d(const int depth, const int row, const int col, const T *from)
      : DynamicArray<T>(depth * row * col, from), depth_(depth), rows_(row),
        cols_(col) {}
  DynamicArray_3d(const int depth, const int row, const int col, const char *fn,
                  const char flag)
      : DynamicArray<T>(depth * row * col, fn, flag), depth_(depth), rows_(row),
        cols_(col) {}
  DynamicArray_3d(const DynamicArray_3d<T> &from)
      : DynamicArray<T>(DynamicArray<T>(from)), depth_(from.depth_),
        rows_(from.rows_), cols_(from.cols_) {}

  DynamicArray_2d<T> slice(const int) const;

  int depth() const { return depth_; }
  int rows() const { return rows_; }
  int cols() const { return cols_; }

  T *operator[](int k) const { return this->start + (size_t)k * rows_ * cols_; }
  T *operator()(int k, int j) const {
    return this->start + ((size_t)k * rows_ + j) * cols_;
  }
  T &operator()(int k, int j, int i) {
    return this->start[((size_t)k * rows_ + j) * cols_ + i];
  }
  T operator()(int k, int j, int i) const {
    return this->start[((size_t)k * rows_ + j) * cols_ + i];
  }

  void print(std::ostream &os = std::cout,
             const char *msg = "DynamicArray_3d is") const;
};

template <class T>
DynamicArray_2d<T> DynamicArray_3d<T>::slice(const int i) const {
  return DynamicArray_2d<T>(rows_, cols_, this->start + i * rows_ * cols_);
}

#endif // |_DynamicArray_H_|

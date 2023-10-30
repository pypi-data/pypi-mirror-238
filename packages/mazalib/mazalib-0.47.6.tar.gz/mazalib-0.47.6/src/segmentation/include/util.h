#pragma once

#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <math.h>
#include <type_traits>

#define register

#define EPS_THINY 0.0000001

#include <algorithm>

#include <string>

///////////////////////////////////////

inline void gsync() {}
inline int mynode() { return 0; }
inline int numnodes() { return 1; }

#define PRINT_NODE_NO
#define EVERY_NODE_BEGIN
#define EVERY_NODE_END

void print_prologue(int = 1);
void print_epilogue();

inline void announce(const std::string &msg1, const std::string &msg2 = "",
                     const std::string &msg3 = "") {
  std::cerr << msg1;
  std::cerr << msg2;
  std::cerr << msg3;
  std::cerr.flush();
  std::cout << msg1;
  std::cout << msg2;
  std::cout << msg3;
  std::cout.flush();
}

inline void test(const std::string &where) {
  std::cerr.flush();
  std::cout.flush();
}

inline void todo(const std::string &message, const std::string &where = "") {
  announce("\n\nTO DO: ", message);
  announce(" ", where, "\n\n");
  std::cerr.flush();
  std::cout.flush();
}

inline void warning(const std::string &message, const std::string where = "") {

  if (where == std::string(""))
    announce("\n\nWarning: ");
  else
    announce("\n\nWarning in ", where, ": ");
  announce(message, "\n\n");
  std::cerr.flush();
  std::cout.flush();
}

static int ERROR_;

inline void file_error(const std::string &filename, const std::string &where) {

  if (where == "")
    announce("\n\nError: ");
  else
    announce("\n\nError in ", where, ": ");
  announce("cannot open file ", filename, "\n\n");
  std::cerr.flush();
  std::cout.flush();
  ERROR_ = 1;
  exit(ERROR_);
}

inline void not_implemented(const std::string &name) {

  announce("\n\nERROR: ", name, " is not implemented yet.\n\n");
  std::cerr.flush();
  std::cout.flush();
  ERROR_ = 2;
  exit(ERROR_);
}

inline void not_parallel(const std::string name) {

  announce("\n\nERROR: ", name, " is not in parallel yet.\n\n");
  std::cerr.flush();
  std::cout.flush();
  ERROR_ = 3;
  exit(ERROR_);
}

inline void error(const std::string &message, const std::string &where) {
#ifdef MPI
  PRINT_NODE_NO
#endif
  if (where == "")
    announce("\n\nError: ");
  else
    announce("\n\nError in ", where, ": ");
  announce(message, "\n\n");
  std::cerr.flush();
  std::cout.flush();
  ERROR_ = 4;
  exit(ERROR_);
}

// Some mathematical functions

inline int ipow(int n, int m) {
  int i, power = 1;
  if (m < 0) {
    std::cerr << "\n\nipow()  m must be non-negative.\n";
    exit(1);
  }
  if (m == 0)
    return 1;
  for (i = 1; i <= m; i++) {
    power = power * n;
  }
  return power;
}
inline int iround(double x) {
  int ix = (int)(floor(x));
  if (x - ix >= 0.5)
    return ix + 1;
  else
    return ix;
}

inline int kroneker_delta(int i, int j) { return (i == j); }

inline double linear_interpolate(const double x, const double x0,
                                 const double x1, const double v0,
                                 const double v1) {
  double weight = (x - x0) / (x1 - x0);
  return (1 - weight) * v0 + weight * v1;
}

//////////////////////////////////////////////////

template <class T> void ask(const char *msg, T &input) {

  std::cerr << msg << ": ";
  std::cin >> input;
  std::cerr << input << std::endl;
  std::cout << msg << ": " << input << std::endl;
  char ignore[128];
  std::cin.getline(ignore, 128);
}

inline void ask(const char *msg, std::string &input) {
  char tmp[128];

  std::cerr << msg << ": ";
  std::cin.getline(tmp, 128);
  std::cerr << tmp << std::endl;
  std::cout << msg << ": " << tmp << std::endl;

  input = std::string(tmp);
}

template <class T1, class T2>
void ask(const char *msg, T1 &input1, T2 &input2) {

  std::cerr << msg << ": ";
  std::cin >> input1 >> input2;
  std::cerr << input1 << " " << input2 << std::endl;
  std::cout << msg << ": " << input1 << " " << input2 << std::endl;
  char ignore[128];
  std::cin.getline(ignore, 128);
}

template <class T1, class T2, class T3>
void ask(const char *msg, T1 &input1, T2 &input2, T3 &input3) {

  {
    std::cerr << msg << ": ";
    std::cin >> input1 >> input2 >> input3;
    std::cerr << input1 << " " << input2 << " " << input3 << std::endl;
    std::cout << msg << ": " << input1 << " " << input2 << " " << input3
              << std::endl;
    char ignore[128];
    std::cin.getline(ignore, 128);
  }
}

template <class T> inline void ask(const std::string &msg, T &input) {
  ask(msg.c_str(), input);
}

template <class T1, class T2>
inline void ask(const std::string &msg, T1 &input1, T2 &input2) {
  ask(msg.c_str(), input1, input2);
}

template <class T1, class T2, class T3>
inline void ask(const std::string &msg, T1 &input1, T2 &input2, T3 &input3) {
  ask(msg.c_str(), input1, input2, input3);
}

///////////////////////////////////////////////////////////////

typedef unsigned char uc;

const uc uc_ext_value = 255;
const int i_ext_value = 1 << 31;
const float f_ext_value = -128.0;
const double d_ext_value = -128.0;
inline uc ext_value(const uc) { return uc_ext_value; }
inline int ext_value(const int) { return i_ext_value; }
inline float ext_value(const float) { return f_ext_value; }
inline double ext_value(const double) { return d_ext_value; }

///////////////////////////////////////////////////////////////

// Statistical functions

class Utils {
public:
  template <class T>
  static void stats(const T *begin, const T *end, double &pmean, double &var) {
    pmean = mean<T>(begin, end);
    var = variance<T>(begin, end);
  }

  template <class Iterator, class T>
  static void stats(Iterator first, Iterator last, T &min, T &max,
                    double &pmean, double &var) {
    minmax(first, last, min, max);
    pmean = mean(first, last);

    var = variance(first, last);
  }

  template <class Iterator, class T>
  static void minmax(Iterator begin, Iterator end, T &min, T &max) {
    max = T(-1.0e8);
    min = T(1.0e8);
    const T ext_v = ext_value(T(0));
    Iterator pp = begin;
    while (pp != end) {
      if (*pp != ext_v) {
        if (*pp > max)
          max = *pp;
        else if (*pp < min)
          min = *pp;
      }
      pp++;
    }
  }

  template <class Iterator>
  static double variance(Iterator begin, Iterator end) {
    double pmean = mean(begin, end);
    double s1 = 0.0, s2 = 0.0;
    typedef typename Iterator::value_type T;
    T ext_v = ext_value(T(0));
    register double dev;
    Iterator p = begin;
    long long n = 0;
    while (p != end) {
      if ((dev = *p++) == ext_v)
        continue;
      dev -= pmean;
      s1 += dev * dev;
      s2 += dev;
      ++n;
    }
    return (s1 - s2 * s2 / n) / (n - 1);
  }

  template <class Iterator> static double mean(Iterator begin, Iterator end) {
    double s = 0.0;
    typedef typename Iterator::value_type T;
    const T ext_v = ext_value(T(0));
    int n = 0;
    Iterator p = begin;
    while (p != end) {
      if (*p != ext_v) {
        s += *p;
        ++n;
      }
      ++p;
    }
    return (s / n);
  }

  // corrected two-pass algorithm, see pp. 613 of NR in C
  template <class Iterator>
  static double variance(Iterator begin, Iterator end, const double mean) {
    double s1 = 0.0, s2 = 0.0;
    typedef typename Iterator::value_type T;
    T ext_v = ext_value(T(0));
    register double dev;
    Iterator p = begin;
    int n = 0;
    while (p != end) {
      if ((dev = *p++) == ext_v)
        continue;
      dev -= mean;
      s1 += dev * dev;
      s2 += dev;
      ++n;
    }
    return (s1 - s2 * s2 / n) / (n - 1);
  }
};

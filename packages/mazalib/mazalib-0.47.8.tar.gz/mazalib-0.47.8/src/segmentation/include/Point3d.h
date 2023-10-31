#pragma once

#include <cinttypes>

template <class T = float> struct Point3d {
  Point3d() : x(0), y(0), z(0){};
  Point3d(T x_, T y_, T z_) : x(x_), y(y_), z(z_){};
  Point3d(const Point3d<short> &pt) : x(pt.x), y(pt.y), z(pt.z){};
  Point3d(const Point3d<int> &pt) : x(pt.x), y(pt.y), z(pt.z){};
  Point3d(const Point3d<std::size_t> &pt) : x(pt.x), y(pt.y), z(pt.z){};
  //	Point3d<T> & operator = (const Point3d<short> &pt){ return *this} //:
  // x(pt.x), y(pt.y), z(pt.z){};

  // float Dist(const Point3d &pt)const;
  // Point3d operator - (const Point3d& p)const;
  // Point3d operator * (float lambda)const;
  template <class T2 = float> float Dist(const Point3d<T2> &pt) const {
    return sqrt(sqr(pt.x - this->x) + sqr(pt.y - this->y) +
                sqr(pt.z - this->z));
  }

  Point3d operator-(const Point3d &pt) const {
    Point3d r(this->x - pt.x, this->y - pt.y, this->z - pt.z);
    return r;
  }

  template <class T2 = T> Point3d operator-(const Point3d<T2> &pt) const {
    Point3d r(T(this->x - pt.x), T(this->y - pt.y), T(this->z - pt.z));
    return r;
  }

  template <class T2 = T> Point3d operator+(const Point3d<T2> &pt) const {
    Point3d r(T(this->x + pt.x), T(this->y + pt.y), T(this->z + pt.z));
    return r;
  }

  Point3d operator*(float lambda) const {
    Point3d r(this->x * lambda, this->y * lambda, this->z * lambda);
    return r;
  }
  template <class T2 = T> T operator*(Point3d<T2> &pt) const {
    return this->x * pt.x + this->y * pt.y + this->z * pt.z;
  }
  template <class T2 = T> Point3d operator^(Point3d<T2> &pt) const {
    Point3d<T2> CrossProduct;
    CrossProduct.x = y * pt.z - z * pt.y;
    CrossProduct.y = z * pt.x - x * pt.z;
    CrossProduct.z = x * pt.y - y * pt.x;
    return CrossProduct;
  }

  bool operator==(const Point3d &pt) const {
    return (this->x == pt.x && this->y == pt.y && this->z == pt.z);
  }

  bool operator<(const Point3d &pt) const {
    if (this->z < pt.z)
      return true;
    if (this->z > pt.z)
      return false;

    if (this->y < pt.y)
      return true;
    if (this->y > pt.y)
      return false;

    if (this->x < pt.x)
      return true;

    return false;
  }

  float Norm() {
    return sqrt(this->x * this->x + this->y * this->y + this->z * this->z);
  }

  T x, y, z;
};

struct SimplePoint3d {
  int x, y, z;
};
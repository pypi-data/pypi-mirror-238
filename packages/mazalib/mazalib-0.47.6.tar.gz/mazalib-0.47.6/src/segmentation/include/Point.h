#pragma once

#include <cmath>
#include <iostream>

// using namespace std;

class Point {
  double x_, y_, z_;
  friend class Grid;
  friend bool operator<(const Point &, const Point &);
  friend std::ostream &operator<<(std::ostream &, const Point &);
  friend std::istream &operator>>(std::istream &, Point &);
  friend double dist(const Point &, const Point &);
  friend Point operator*(double, const Point &);

public:
  Point(double x = 0.0, double y = 0.0, double z = 0.0) : x_(x), y_(y), z_(z) {}
  Point(const Point &p) : x_(p.x_), y_(p.y_), z_(p.z_) {}
  //   Point& operator=(const Point& p);

  bool operator<(const Point &p) {
    return (x_ < p.x_) || (!(p.x_ < x_) && y_ < p.y_) ||
           (!(p.x_ < x_) && !(p.y_ < y_) && z_ < p.z_);
  }
  Point operator+(const Point &p) const {
    return Point(x_ + p.x_, y_ + p.y_, z_ + p.z_);
  }
  Point operator-(const Point &p) const {
    return Point(x_ - p.x_, y_ - p.y_, z_ - p.z_);
  }
  ~Point() {}

  double x() const { return x_; }
  double y() const { return y_; }
  double z() const { return z_; }

  void incr_x(double xincr) { x_ += xincr; }
  void incr_y(double yincr) { y_ += yincr; }
  void incr_z(double zincr) { z_ += zincr; }

  double abs() const { return sqrt(x_ * x_ + y_ * y_ + z_ * z_); }
  void print(const char *msg = "Point is ") const { std::cout << msg << *this; }
};

inline bool operator<(const Point &p1, const Point &p2) {
  return ((p1.x() < p2.x()) || ((p1.x() == p2.x()) && (p1.y() < p2.y())) ||
          ((p1.x() == p2.x()) && (p1.y() == p2.y()) && (p1.z() < p2.z())));
}

inline Point operator*(double c, const Point &p) {
  return Point(c * p.x_, c * p.y_, c * p.z_);
}

inline double dist(const Point &p, const Point &q) {
  double x = p.x_ - q.x_;
  double y = p.y_ - q.y_;
  double z = p.z_ - q.z_;
  return sqrt(x * x + y * y + z * z);
}
#pragma once
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <limits>
#include <random>

namespace random_numbers {
static int timenow;
double rnd();
// int hash(int a, int b, int c);
double normrnd(double mu, double sigma);
double lognormrnd(double mu, double sigma, double max, double min);
}; // namespace random_numbers

class RandomNumbers {
public:
  static double lognormrnd(double mu, double sigma, double max, double min);
  static void Seed();

private:
  RandomNumbers();
  std::default_random_engine generator;
  static RandomNumbers *instance() {
    static RandomNumbers theSingleInstance;
    return &theSingleInstance;
  }
  ~RandomNumbers(){

  };
};

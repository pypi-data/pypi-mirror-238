#include "RandomNumbers.h"


double random_numbers::rnd()
{
	
	std::time_t t=time(NULL);
	
	static int s1 = static_cast<int>(t);
	static int s2 = 15000;
	int k = s1 / 53668;
	double Z;
	s1 = 40014 * (s1 - k * 53668) - k * 12211;
	if (s1 < 0)
		s1 = s1 + 2147483563;
	k = s2 / 52774;
	s2 = 40692 * (s2 - k * 52774) - k * 3791;
	if (s2 < 0)
		s2 = s2 + 2147483399;
	Z = s1 - s2;
	if (Z < 1)
		Z += 2147483562;
	Z = Z*4.656613e-10;

	return Z;
};

//int random_numbers::hash(int a, int b, int c)
//{
//	int s1 = a + 10000;
//	double c1=9821 * c + 0.211327;
//	c = (c1 - int(c1)) * 1000000;
//	int s2 = b + c+10000;
//	int k = s1 / 53668;
//	double Z;
//	s1 = 40014 * (s1 - k * 53668) - k * 12211;
//	if (s1 < 0)
//		s1 = s1 + 2147483563;
//	k = s2 / 52774;
//	s2 = 40692 * (s2 - k * 52774) - k * 3791;
//	if (s2 < 0)
//		s2 = s2 + 2147483399;
//	Z = s1 - s2;
//	if (Z < 1)
//		Z += 2147483562;
//	return Z/10000;
//}

double random_numbers::normrnd(double mu, double sigma)
{
	const double epsilon = std::numeric_limits<double>::min();
	const double two_pi = 2.0*3.14159265358979323846;

	static double z0, z1;
	static bool generate;
	generate = !generate;

	if (!generate)
		return z1 * sigma + mu;

	double u1, u2;
	do
	{
		u1 = rnd() * (1.0);
		u2 = rnd() * (1.0);
	} while (u1 <= epsilon);

	z0 = sqrt(-2.0 * log(u1)) * cos(two_pi * u2);
	z1 = sqrt(-2.0 * log(u1)) * sin(two_pi * u2);
	return z0 * sigma + mu;
};

double random_numbers::lognormrnd(double mu, double sigma, double max, double min)
{
	std::default_random_engine generator;

	std::lognormal_distribution<double> distribution(mu, sigma);
	double n = std::numeric_limits<double>::max();
	
	while (n > max || n< min)
		n = distribution(generator);
		
	return n;
};

RandomNumbers::RandomNumbers()
{
	
};
void RandomNumbers::Seed()
{
	instance()->generator.seed(unsigned(time(0)));
}

double RandomNumbers::lognormrnd(double mu, double sigma, double max, double min)
{
	
	std::lognormal_distribution<double> distribution(mu, sigma);
	double n = std::numeric_limits<double>::max();

	while (n > max || n< min)
		n = distribution(instance()->generator);

	return n;
};
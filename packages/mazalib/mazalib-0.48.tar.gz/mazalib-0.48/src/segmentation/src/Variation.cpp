/*
*	Copyrighted, Research Foundation of SUNY, 1998
*/

#include "Variation.h"
#include "threshold.h"


char Variation_method[4][100]={"Unknown_V", "Moving_Window",
			     "Semivariogram", "Covariance" };

char Variation_type[3][100]={"Unknown_V", "Semivariogram", "Covariance" };

char Direction_name[6][20]={"Unknown_D", "Vertical",  "Horizontal",
			    "Isotropic", "Slice_Isotropic", "Diagonal"};


std::istream & operator>>(std::istream & is, Variation &v)
{
    const char*fname="istream & operator>>(istream & is, Variation &v)";
    
    char ans[5];

    announce("\n\tcovariance/semivariogram information\n");
    
	std::cerr << "\nAvailable methods for estimating data correlations\n";
	std::cerr << "\tClassical semivariogram     (v)\n";
	std::cerr << "\tClassical covariance        (c)\n";
	std::cerr << "\tMoving window semivariogram (m)\n";
    
	std::cout << "\nAvailable methods for estimating data correlations\n";
	std::cout << "\tClassical semivariogram     (v)\n";
	std::cout << "\tClassical covariance        (c)\n";
	std::cout << "\tMoving window semivariogram (m)\n";
    
	std::cerr << "Enter choice (v,c,m): ";       is >> ans;
	std::cout << "Enter choice (v,c,m): " << ans << std::endl;

    v.set_method(ans[0]);

	std::cerr << "\nAvailable directions for estimating correlations\n";
	std::cerr << "\tvertical   (v)\n";
	std::cerr << "\thorizontal (h)\n";
	std::cerr << "\tisotropic  (i)\n";
    
	std::cout << "\nAvailable directions for estimating correlations\n";
	std::cout << "\tvertical   (v)\n";
	std::cout << "\thorizontal (h)\n";
	std::cout << "\tisotropic  (i)\n";
    
	std::cerr << "Enter choice (v,h,i): ";       is >> ans;
	std::cout << "Enter choice (v,h,i): " << ans << std::endl;

    v.set_direction(ans[0]);

    int no;
	std::cerr << "\nEnter maximum lag distance: ";       is >> no;
	std::cout << "\nEnter maximum lag distance: " << no << std::endl;

	std::cerr << "\nEnter incremental lag distance: ";   is >> v.unit_lag_;
	std::cout << "\nEnter incremental lag distance: " << v.unit_lag_ << std::endl;

	std::cerr << "\nAvailable correlation output formats\n";
	std::cerr << "\tcovariance     (c)\n";
	std::cerr << "\tsemi_variogram (v)\n";
    
	std::cout << "\nAvailable correlation output formats\n";
	std::cout << "\tcovariance     (c)\n";
	std::cout << "\tsemi_variogram (v)\n";
    
	std::cerr << "Enter choice (c,v): ";         is >> ans;
	std::cout << "Enter choice (c,v): " << ans << std::endl;
    char ignore[128];
    is.getline(ignore,128);
    
    v.set_type(ans[0]);
    
    Variation tmp(no, v.unit_lag(),v.direction(),v.method(),v.type());
    v=tmp;
    return is;
}



void Variation::operator+=(const Variation & v) 
{
    diterator p=begin();
    vector<double>::const_iterator pv=v.begin();
    for(int i=0;i<size();++i) *p++ += *pv++;
}


void Variation::operator*=(const double m) 
{
    diterator p=begin();
    for(int i=0;i<size();++i) {
	*p++ *= m;
    }
}


double Variation::operator()(const double lag_distance) const
{
	const char*fname="double Variation::operator()(const double lag_distance)";
	static	int warning_done = 0;
	double	v;

	if( lag_distance < 0 )
	{
		error("lag_distance must be positive",fname);
		return 0.0;
	}
	int lag=int(lag_distance/unit_lag_);
	if( lag == 0 )
	{
	    if( type_ == Covariance )
		v = linear_interpolate(lag_distance,0,unit_lag_,front(),(*this)[1]);
	    else
		v = linear_interpolate(lag_distance,0,unit_lag_,  0.0,(*this)[1]);
	}    
	else if( lag < max_lag() )
	{
		v = linear_interpolate(lag_distance,lag*unit_lag_,
					(lag+1)*unit_lag_,(*this)[lag],(*this)[lag+1]);
	}
	else if( lag == max_lag() )
		v = linear_interpolate(lag_distance,lag*unit_lag_,
					(lag+1)*unit_lag_,(*this)[lag],front());
	else
	{
	    v = ( type_ == Covariance ) ? 0.0 : front();

	    if( !warning_done )
	    {
		warning("out_of_range",fname);
		warning_done = 1;

		std::cout << "\nMaximum lag requested is " << max_lag()*unit_lag_;
		std::cout << "\nData set requires a of lag " << lag_distance << std::endl;
		std::cout << "Run will continue using extrapolation to larger lags\n";

		std::cerr << "\nMaximum lag requested is " << max_lag()*unit_lag_;
		std::cerr << "\nData set requires a of lag " << lag_distance << std::endl;
		std::cerr << "Run will continue using extrapolation to larger lags\n";
	    }
	}
	/*if( v > back() ) return front();
	if( v <     0 )   return 0.0;*/

	return v;
}


/*double Variation::operator()(const double lag_distance) const
{
	const char*fname="double Variation::operator()(const double lag_distance)";
	static	int warning_done = 0;
	double	v;

	if( lag_distance < 0 )
	{
		error("lag_distance must be positive",fname);
		return 0.0;
	}
	int lag=int(lag_distance/unit_lag_);
	if( lag == 0 )
	{
	    if( type_ == Covariance )
		v = linear_interpolate(lag_distance,0,unit_lag_,front(),(*this)[1]);
	    else
		v = linear_interpolate(lag_distance,0,unit_lag_,  0.0,(*this)[1]);
	}    
	else if( lag < max_lag() )
	{
		v = linear_interpolate(lag_distance,lag*unit_lag_,
					(lag+1)*unit_lag_,(*this)[lag],(*this)[lag+1]);
	}
	else if( lag == max_lag() )
		v = linear_interpolate(lag_distance,lag*unit_lag_,
					(lag+1)*unit_lag_,(*this)[lag],front());
	else
	{
	    v = ( type_ == Covariance ) ? 0.0 : front();

	    if( !warning_done )
	    {
		warning("out_of_range",fname);
		warning_done = 1;

		cout << "\nMaximum lag requested is " << max_lag()*unit_lag_;
		cout << "\nData set requires a of lag " << lag_distance << endl;
		cout << "Run will continue using extrapolation to larger lags\n";

		cerr << "\nMaximum lag requested is " << max_lag()*unit_lag_;
		cerr << "\nData set requires a of lag " << lag_distance << endl;
		cerr << "Run will continue using extrapolation to larger lags\n";
	    }
	}
	if( v > back() ) return front();
	if( v <     0 )   return 0.0;

	return v;
}*/

void Variation::set_method(char s)
{
    if (s=='v' || s=='V')       method_=classic_semivariogram;
    else if (s=='c' || s=='C')  method_=classic_covariance;
    else if (s=='m' || s=='M')  method_=mw_semivariogram;
    else                        method_=Unknown_V;
}


void Variation::set_type(char s)
{
    std::string fname("void Variation::set_type(char s)");
	 if (s=='v' || s=='V')  type_=Semivariogram;
    else if (s=='c' || s=='C')  type_=Covariance;
    else                        error("Unknown type",fname);
}

void Variation::set_direction(char c)
{
    if (c=='h' || c=='H')       direction_=Horizontal;
    else if (c=='i' || c=='I')  direction_=Isotropic;
    else if (c=='v' || c=='V')  direction_=Vertical;
    else                        direction_=Unknown_D;
}


void add_derivative_correction(Variation &var, int dim) 
{
    if( var.method() != mw_semivariogram )
        error("This is only for moving window variogram.","");
    
    int max_lag = var.max_lag();
    DynamicArray<double> a_copy(var.begin(),var.end());
    a_copy[0]=0.0;

    var[1] = a_copy[1] + 1.0/dim*(a_copy[2] - a_copy[1]);	 /*forward diff */
    for (int h=2;h<max_lag;h++) {
        var[h] = a_copy[h] + 0.5*h/dim*(a_copy[h+1]-a_copy[h-1]); /*centered diff*/
    }
    var[max_lag] = a_copy[max_lag]
        + max_lag/dim*(a_copy[max_lag]-a_copy[max_lag-1]); /*backward diff*/
}


void Variation::print(const char *msgs) const
{
	//std::cout << std::endl << msgs << std::endl;
	//std::cout << "Unit lag distance is "    << unit_lag_ << std::endl;
	//std::cout << "Maximum lag distance is " << max_lag()*unit_lag_ << std::endl;
	//std::cout << "Computing method " << Variation_method[method_] << std::endl;
	//std::cout << "Printing type "    << Variation_type[type_] << std::endl;
	//std::cout << "Direction is "     << Direction_name[direction_] << std::endl;
	//std::cout << *this;
}


std::ostream & operator<<(std::ostream & os, const Variation &v)
{
    os << std::endl;
    if (v.type_==Semivariogram) {
	os << 0.0 << " " << 0.0 << std::endl;
    }
    else {
        os << 0.0 << " " << v[0] << std::endl;
    }
    for(int i = 1; i<v.size(); i++) {
	os << i*v.unit_lag_ << " " << v[i] << std::endl;
    }
    os << std::endl;
    return os;
}

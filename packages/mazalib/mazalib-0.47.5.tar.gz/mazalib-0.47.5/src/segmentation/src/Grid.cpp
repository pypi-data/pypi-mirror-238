/*
*	Copyrighted, Research Foundation of SUNY, 1998
*/
#include "util.h"
#include "Grid.h"
#ifdef mips
#include <stdlib.h>
#endif

Grid::Grid()
        : dim_(0), id(0), lmr(1),
          l(0.0,0.0,0.0), u(0.0,0.0,0.0), h(0.0,0.0,0.0) 
{
    gmax[0]=1; 
    gmax[1]=1; 
    gmax[2]=1;
}

Grid::Grid(int d, Point L, Point U, int* size, int Id, int Lmr)
        : dim_(d), id(Id), lmr(Lmr), l(L), u(U) 
{
    gmax[0]=size[0];
    gmax[1]=1;
    gmax[2]=1;
    if (dim_ > 1) gmax[1]=size[1];
    if (dim_ > 2) gmax[2]=size[2];
    set_delta();
}

Grid::Grid(const Grid& g) 
        :dim_(g.dim_), id(g.id), lmr(g.lmr), l(g.l), u(g.u), h(g.h) 
{
    gmax[0]=g.gmax[0];
    gmax[1]=g.gmax[1];
    gmax[2]=g.gmax[2];
}

Grid::Grid(const Grid& g, const int cell_no, const int scale) 
        :dim_(g.dim_), id(cell_no), lmr(g.lmr) 
{
    g.cell_description(cell_no,l,u);
    gmax[0]=scale;
    gmax[1]=scale;
    gmax[2]=scale;
    set_delta(0);
}

void  Grid::change_dim(int new_dim)
{
    if (new_dim==2 && dim_==3) {
        gmax[2]=1;
    }
    else not_implemented("void Grid::change_dim(int)");;
    dim_=new_dim;
}

#ifdef MPI
Grid::Grid(const Grid& g, const int me, const int p)
        :dim_(g.dim_), id(g.id), lmr(g.lmr), l(g.l), u(g.u), h(g.h)
{
    if (p==1 || dim_==1 || dim_ ==3) {
        gmax[0]=g.gmax[0];
        gmax[1]=g.gmax[1];
        gmax[2]=g.gmax[2];
        return;
    }
    
    int n, offset;
    ::divide_by_pnodes(g.gmax[1],n,offset,me,p);
    l.y_=g.l.y_+offset*g.h.y_;
    ::divide_by_pnodes(g.gmax[1],n,offset,me+1,p);
    u.y_=g.l.y_+offset*g.h.y_;
    gmax[0]=g.gmax[0];
    gmax[1]=n;
    gmax[2]=g.gmax[2];
}
#endif

void Grid::set_delta(double* delta) 
{
    if (delta==0) {	
	h.x_=(u.x_-l.x_)/gmax[0];
	h.y_=(u.y_-l.y_)/gmax[1];
	h.z_=(u.z_-l.z_)/gmax[2];
     }
     else {
        h.x_=delta[0]; 
        h.y_=delta[1]; 
        h.z_=delta[2];
     }
}

void Grid::set(int d, Point L, Point U, int* size, int Id,
               int Lmr)
{
    dim_=d;
    l=L;
    u=U;
    gmax[0]=size[0];
    gmax[1]=size[1];
    gmax[2]=size[2];
    id=Id;
    lmr=Lmr;
    set_delta();
    return;
}


Grid& Grid::operator=(const Grid& g) 
{
    if (this == &g) return *this;
    dim_=g.dim_;
    id=g.id;
    lmr=g.lmr;
    l=g.l;
    u=g.u;
    h=g.h;
    gmax[0]=g.gmax[0];
    gmax[1]=g.gmax[1];
    gmax[2]=g.gmax[2];
    return (*this);
}

#ifdef __PGI
#pragma instantiate void ask(const string&, int&)
#pragma instantiate void ask(const string&, int&, int&)
#pragma instantiate void ask(const string&, int&, int&, int&)
#pragma instantiate void ask(const string&, double&, double&)
#pragma instantiate void ask(const string&, double&, double&,double&)
#endif
/*
#ifdef __GNUC__
template void ask(const string&, int&);
template void ask(const string&, int&, int&);
template void ask(const string&, int&, int&);
template void ask(const string&, double&, double&);
template void ask(const string&, double&, double&,double&);
#endif
*/
std::istream& operator>>(std::istream& is, Grid& Grid)
{
    announce("\n\tGrid Information\n\n");
    ask(std::string("Enter the dimension (2,or 3)"),Grid.dim_);
    double x,y,z;
    if (Grid.dim_==2) {
        ask("Enter x,y location of lower LH corner",x,y);
        Grid.l=Point(x,y,0.0);
        ask("Enter x,y location of upper RH corner",x,y);
        Grid.u=Point(x,y,0.0);
        ask("Enter number x,y Grid locations",Grid.gmax[0],Grid.gmax[1]);
	Grid.gmax[2]=1;
    }
    else if (Grid.dim_==3) {
        ask("Enter x,y,z location of lower corner",x,y,z);
        Grid.l=Point(x,y,z);
        ask("Enter x,y,z location of upper corner",x,y,z);
        Grid.u=Point(x,y,z);
        ask("Enter number x,y,z Grid locations",Grid.gmax[0],
	    Grid.gmax[1],Grid.gmax[2]);
    }
    Grid.id=0;
    Grid.lmr=0;
    Grid.set_delta();
    return is;
}

void Grid::center_at_origin()
{
    double c_x=0.5*(l.x_+u.x_);
    double c_y=0.5*(l.y_+u.y_);
    double c_z=0.5*(l.z_+u.z_);
    l.x_ -= c_x;
    l.y_ -= c_y;
    l.z_ -= c_z;
    u.x_ -= c_x;
    u.y_ -= c_y;
    u.z_ -= c_z;
}

Point Grid::corner(const int i) const
{
    if ( (dim_==2 && (i<0 || i>3))  || 
	(dim_==3 && (i<0 || i>7)) ) {
		std::cerr << "dim = " << dim_ << " i = " << i << " ";
		std::cerr << "No such corner " << std::endl;
	exit(1);
    }
    Point pt;
    switch(i) {
      case 0: pt=Point(l.x_,l.y_,l.z_); break;
      case 1: pt=Point(u.x_,l.y_,l.z_); break;
      case 2: pt=Point(u.x_,u.y_,l.z_); break;
      case 3: pt=Point(l.x_,u.y_,l.z_); break;
      case 4: pt=Point(l.x_,l.y_,u.z_); break;
      case 5: pt=Point(u.x_,l.y_,u.z_); break;
      case 6: pt=Point(u.x_,u.y_,u.z_); break;
      case 7: pt=Point(l.x_,u.y_,u.z_); break;
    }
    return pt;
}

#ifdef MPI
Grid  Grid::divide_by_pnodes(int me, int p) const
{
    if (p==1) return (*this);

    int n, offset;
    ::divide_by_pnodes(gmax[1],n,offset,me,p);
    Point L(l.x_, l.y_+offset*h.y_, l.z_);
    ::divide_by_pnodes(gmax[1],n,offset,me+1,p);
    Point U(u.x_,l.y_+offset*h.y_, u.z_);
    int mesh[3];
    mesh[0]=gmax[0];
    mesh[1]=n;
    mesh[2]=gmax[2];
    Grid Grid(dim_, L, U, mesh, id, lmr);
    return Grid;
}	       
#endif

void Grid::print(const char* msg) const
{
    if ( this==0 ) {
		std::cout << "Grid::print() null Pointer.\n";
        return;
    }
    if (msg != 0)  std::cout << msg << std::endl;
    if (id  != 0)  std::cout << "id = "  << id  << std::endl ;
    if (lmr >  1)  std::cout << "lmr = " << lmr << std::endl;
	std::cout << "dim = " << dim_ << std::endl;
    
	std::cout << "L = (" << l.x_ << ", " << l.y_ ;
    if (dim_==3)  std::cout << ", " << l.z_;
	std::cout << ")" << std::endl ;

	std::cout << "U = (" << u.x_ << ", " << u.y_ ;
    if (dim_==3)  std::cout << ", " << u.z_;
	std::cout << ")" << std::endl ;

	std::cout << "gmax = (" << gmax[0] << ", " << gmax[1] ;
    if (dim_==3)  std::cout << ", " << gmax[2];
	std::cout << ")" << std::endl ;

	std::cout << "h = (" << h.x_ << ", " << h.y_ ;
    if (dim_==3)  std::cout << ", " << h.z_ ;
	std::cout << ")" << std::endl ;
}

int Grid::min_mesh() const
{
    if (dim_==1) return gmax[0];
    int tmp= std::min(gmax[0],gmax[1]);
    if (dim_==2) return tmp;
    if (dim_==3) return  std::min(tmp,gmax[2]);
    else return -1;
}

size_t Grid::size() const 
{ 
         if (dim_==1) return gmax[0];
    else if (dim_==2) return gmax[0]*gmax[1];
	else if (dim_ == 3) return (size_t)gmax[0] * gmax[1] * gmax[2];
    else return -1;
}


int Grid::box_containing_Point(const Point& p, int& c, int& r, int& d) const 
{
   // string fname("int Grid::box_containing_Point(const Point&, int&, int&, int&) const");

    int outside=0;
    c=r=d=0;

    switch(dim_) {
	case 3:
	    if (p.z_ > u.z_ || p.z_ < l.z_) outside=1;
	    d=(int)floor((p.z_-l.z_)/h.z_);
	    if (d==gmax[2]) d=gmax[2]-1;
	case 2:
	    if (p.y_ > u.y_ || p.y_ < l.y_) outside=1;
	    r=(int)floor((p.y_-l.y_)/h.y_);
	    if (r==gmax[1]) r=gmax[1]-1;
	case 1:
	    if (p.x_ > u.x_ || p.x_ < l.x_) outside=1;
	    c=(int)floor((p.x_-l.x_)/h.x_);
	    if (c==gmax[0]) c=gmax[0]-1;
	    break;
	default:;//!!!
	  //  error("Wrong dimension in the Grid",fname);
    }
    static int first=1;
    if (outside) {
	/*if (first) {
	    warning("There are Points outside Grid",fname.c_str());
	    cerr << p << " is one of the Points" << endl;
	    first=0;
	}*/
	return -1;
    }
    return (d*gmax[1]+r)*gmax[0]+c;
}

void Grid::cell_description(const int no, Point& L, Point& U) const 
{
    int x,y,z;
    if (dim_ ==2) {
        y=no/gmax[0];
        x=no%gmax[0];
        L=Point(l.x_+x*h.x_,l.y_+y*h.y_);
        U=Point(L.x_+h.x_,  L.y_+h.y_);
    }
    else if (dim_ ==3) {
        z=no/(gmax[0]*gmax[1]);
        y=(no-z*gmax[0]*gmax[1])/gmax[0];
        x=(no-z*gmax[0]*gmax[1])%gmax[0];
        L=Point(l.x_+x*h.x_,l.y_+y*h.y_,l.z_+z*h.z_);
        U=Point(L.x_+h.x_,  L.y_+h.y_,  L.z_+h.z_);
    }
}

Point Grid::getPoint(const int ix, const int iy, const int iz) const
{
    Point pt=start_pt();
    double x,y,z;
    x=pt.x_+ix*h.x_;
    y=pt.y_+iy*h.y_;
    z=pt.z_+iz*h.z_;
    return Point(x,y,z);
}


Point Grid::getPoint(const int i) const
{
    int iz=i/(n_x()*n_y());
    int iy=(i-iz*n_x()*n_y())/n_x();
    int ix=i%n_x();
    return getPoint(ix,iy,iz);
}

bool Grid::next_pt(Point& p) const
{
	std::string fname("void Grid::next_pt(Point& p) const");
    bool valid=true;
    switch (dim()) {
        case 1:
            if (p.x_ + h.x_ <= u.x_) p.x_ += h.x_;
            else valid=false;
            break;
        case 2:
            if (p.x_ + h.x_ <= u.x_) p.x_ += h.x_;
            else {
                p.x_ = start_pt().x_;
                if (p.y_ + h.y_ <= u.y_) {
                    p.y_ += h.y_;
                }
                else valid=false;
            }
            break;
        case 3:
            if (p.x_ + h.x_ <= u.x_) p.x_ += h.x_;
            else {
                p.x_ = start_pt().x_;
                if (p.y_ + h.y_ <= u.y_) p.y_ += h.y_;
                else {
                    p.y_ = start_pt().y_;
                    if (p.z_ + h.z_ <= u.z_) p.z_ += h.z_;
                    else valid=false;
                }
            }
            break;
        default:
            error("Invalid dimension.",fname);
            break;
            
    }
    return valid;
}

/*
*	Copyrighted, Research Foundation of SUNY, 1998
*/
#ifndef Grid_H
#define Grid_H

#include "Point.h"

class Grid {
    int    dim_;       // Dimension of Grid 
    int    id;         // Id number of the Grid 
    int    lmr;        // level of local mesh refinement 
    Point  l;	       // Lower corner of the Grid 
    Point  u;	       // Upper corner of the Grid 
    Point  h;          // Grid spacings of the Grid	 
    int    gmax[3]  ;  // Number of blocks in each direction
    friend  std::istream & operator>>(std::istream &, Grid &);
public:
    Grid();
    Grid(int, Point, Point, int*, int=0, int=1);
    Grid(std::istream & is) { is >> (*this); }
    Grid(const Grid&);
    Grid(const Grid&, const int, const int);
#ifdef MPI
    Grid(const Grid&, const int me, const int p);
#endif
    Grid& operator=(const Grid&);

    void  set(int, Point, Point, int*, int, int);
    void  set_delta(double* delta=0);
    void  set_id(int i)  { id=i; }
    void  set_lmr(int i) { lmr=i;}
    void  change_dim(int new_dim);
    
#ifdef MPI
    Grid  divide_by_pnodes(int, int) const;
#endif
    void  center_at_origin();
    void  print(const char* msg="Grid structure") const;

    int  n_x()  const { return gmax[0]; }
    int  n_y()  const { return gmax[1]; }
    int  n_z()  const { return gmax[2]; }
    size_t  size() const;

    Point get_L()     const { return l; }
    Point get_U()     const { return u; }
    Point center()    const { return 0.5*(l+u); }
    Point start_pt(const int scale=1)  const { 
        return l+Point(0.5*h.x_/scale,0.5*h.y_/scale,0.5*h.z_/scale); 
    }
    Point corner(const int) const;

    int   dim()     const { return dim_; }
    int   get_lmr() const { return lmr; }
    int   get_id()  const { return id; }
    
    /*  Masha addition */
    int  nx() const { return gmax[0]; }    
    int  ny() const { return gmax[1]; }    
    int  nz() const { return gmax[2]; }    
    /**/
    double width()    const { return u.x_-l.x_;}
    double height()   const { return u.y_-l.y_;}
    double depth()    const { return u.z_-l.z_;}
    double del_x()    const { return h.x_; }
    double del_y()    const { return h.y_; }
    double del_z()    const { return h.z_; }
    double diagonal() const { return (l-u).abs(); }
	
    int  min_mesh() const;
    void cell_description(const int no, Point &L, Point & U) const;

    int box_containing_Point(const Point &p) const {
	int tmpc=0, tmpr=0, tmpd=0;
	return  box_containing_Point(p,tmpc,tmpr,tmpd);};
    int box_containing_Point(const Point &p, int &c) const {
	int tmpr=0, tmpd=0;
	return  box_containing_Point(p,c,tmpr,tmpd);};    
    int box_containing_Point(const Point &p, int &c, int &r) const {
	int tmpd=0;
	return  box_containing_Point(p,c,r,tmpd);};
    int box_containing_Point(const Point &p, int &c, int &r, int&d) const;

    Point getPoint(const int xi, const int yi, const int zi=0) const;
    Point getPoint(const int i) const;
    bool  next_pt(Point&) const;
}; 

#endif // |_Grid_H_|

 #ifndef CONFIG_H
#define CONFIG_H

#define SCHLUTTER_ONLY 1
#define LEON_ONLY 2
#define FILTERS_ONLY 8
#define SEGMENTATION_ONLY 16
#define SIZE_LIMITED_250 32
#define ALL_INCLUDED 1024
#define WIN_TITLE "kriging"
#define EPS 1e-6
#define SOLID_PHASE 255//1
#define PORE_PHASE 0
#define PORE_THROAT_SEGMENTATION
#define NOSLISES
//#define DOSLISES
static int License = ALL_INCLUDED;// SIZE_LIMITED_250 | FILTERS_ONLY | SEGMENTATION_ONLY;

#endif
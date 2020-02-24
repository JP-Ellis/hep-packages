#include "ChiSquare.c"
#include "Fluct.c"
#include "Grid.c"
#include "Integrate.c"
#include "Sample.c"
#include "Sobol.c"

#define MINDIM SOBOL_MINDIM

#define MAXDIM SOBOL_MAXDIM

#if NDIM > 0 && NDIM < MAXDIM
#undef MAXDIM
#define MAXDIM NDIM
#endif

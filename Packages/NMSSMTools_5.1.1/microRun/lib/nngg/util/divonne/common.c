static void Explore(void *voidregion, cSamples *samples, cint depth,
                    cint flags);

static void Split(void *voidregion, int depth);

#include "ChiSquare.c"
#include "Explore.c"
#include "FindMinimum.c"
#include "Integrate.c"
#include "Rule.c"
#include "Sample.c"
#include "Sobol.c"
#include "Split.c"

#if KOROBOV_MINDIM > SOBOL_MINDIM
#define MINDIM KOROBOV_MINDIM
#else
#define MINDIM SOBOL_MINDIM
#endif

#if KOROBOV_MAXDIM < SOBOL_MAXDIM
#define MAXDIM KOROBOV_MAXDIM
#else
#define MAXDIM SOBOL_MAXDIM
#endif

#if NDIM > 0 && NDIM < MAXDIM
#undef MAXDIM
#define MAXDIM NDIM
#endif

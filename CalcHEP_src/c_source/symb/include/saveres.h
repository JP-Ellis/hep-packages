#ifndef __SAVERES_
#define __SAVERES_

#include "denominators.h"
#include "physics.h"
#include "polynom.h"

extern denom_struct denom[2 * maxvert - 2];

extern int denrno;

extern void saveanaliticresult(poly rnum, poly factn, poly factd, vcsect vcs,
                               int ndiag, int nFile);

#endif

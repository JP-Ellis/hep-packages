
#ifndef MSSM2LOOP_H
#define MSSM2LOOP_H

extern "C" int effpot_(int *lp,double *mt,double *mg,double *T1,double *T2,double *st,double *ct,double *q2,double *tanb,double *vv,double *l,double *xx,double *as, double DMS[][3][3], double DMP[][3][3]);

#define self_energy_higgs_2loop_at_as_nmssm           effpot_
#define self_energy_higgs_2loop_ab_as_nmssm           effpot_

#endif

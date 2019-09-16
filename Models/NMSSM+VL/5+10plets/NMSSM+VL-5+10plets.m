Off[General::spell]

Model`Name = "NMSSM15";
Model`NameLaTeX ="NMSSM extended by a pair of 5 and 10 of $SU(5)$";
Model`Authors = "F.Staub";
Model`Date = "2016-01-17";




(*-------------------------------------------*)
(*   Particle Content*)
(*-------------------------------------------*)

(* Global symmetries *)

Global[[1]] = {Z[2],RParity};
RpM = {-1,-1,1};
RpP = {1,1,-1};
Global[[2]] = {Z[2], ExtraZ2};

(* Vector Superfields *)

Gauge[[1]]={B,   U[1], hypercharge, g1,False,RpM,1};
Gauge[[2]]={WB, SU[2], left,        g2,True, RpM,1};
Gauge[[3]]={G,  SU[3], color,       g3,False,RpM,1};


(* Chiral Superfields *)

SuperFields[[1]] = {q,  3, {uL,  dL},    1/6, 2, 3, RpM,1};  
SuperFields[[2]] = {l,  3, {vL,  eL},   -1/2, 2, 1, RpM,1};
SuperFields[[3]] = {Hd, 1, {Hd0, Hdm},  -1/2, 2, 1, RpP,1};
SuperFields[[4]] = {Hu, 1, {Hup, Hu0},   1/2, 2, 1, RpP,1};

SuperFields[[5]] = {d, 3, conj[dR],  1/3, 1, -3, RpM,1};
SuperFields[[6]] = {u, 3, conj[uR], -2/3, 1, -3, RpM,1};
SuperFields[[7]] = {e, 3, conj[eR],    1, 1,  1, RpM,1};

SuperFields[[8]] = {d5, 1, conj[dR5], 1/3, 1, -3, RpM,-1};
SuperFields[[9]] = {d5p, 1, dR5p,  -1/3, 1,  3, RpM,-1};

SuperFields[[10]] = {l5,  1, {vL5,  eL5},    -1/2, 2, 1, RpM,-1};
SuperFields[[11]] = {l5p,  1, {conj[eL5p],  conj[vL5p]},    1/2, 2, 1, RpM,-1};  

SuperFields[[12]] = {u10, 1, conj[uR10], -2/3, 1, -3, RpM,-1};
SuperFields[[13]] = {u10p, 1, uR10p,  2/3, 1,  3, RpM,-1};

SuperFields[[14]] = {q10,  1, {uL10,  dL10},    1/6, 2, 3, RpM,-1};
SuperFields[[15]] = {q10p,  1, {conj[dL10p],  conj[uL10p]},    -1/6, 2, -3, RpM,-1};  

SuperFields[[16]] = {e10, 1, conj[eR10],    1, 1,  1, RpM,-1};
SuperFields[[17]] = {e10p, 1, eR10p,    -1, 1,  1, RpM,-1};

SuperFields[[18]] = {s, 1, sR,     0, 1,  1, RpP,1};


(*------------------------------------------------------*)
(* Superpotential *)
(*------------------------------------------------------*)

SuperPotential = Yu u.q.Hu - Yd d.q.Hd - Ye e.l.Hd + \[Mu] Hu.Hd + lambda s.Hu.Hd + MS s.s + kappa/3 s.s.s + tS s \
  + YUp q10.u10.Hu + YUpp  q10p.u10p.Hd + YDp q10.d5.Hd + YDpp  q10p.d5p.Hu  + YEp l5.e10.Hd + YEpp  l5p.e10p.Hu  \
  + MVD d5.d5p + MVL l5.l5p + MVU u10.u10p + MVQ q10.q10p + MVE e10.e10p + lD5 s.d5.d5p + lL5 s.l5.l5p + lQ10 s.q10.q10p + lU10 s.u10.u10p + lE10 s.e10.e10p;

    

(*----------------------------------------------*)
(*   ROTATIONS                                  *)
(*----------------------------------------------*)

NameOfStates={GaugeES, EWSB};


(* ----- After EWSB ----- *)


(* Gauge Sector *)

DEFINITION[EWSB][GaugeSector] =
{ 
  {{VB,VWB[3]},{VP,VZ},ZZ},
  {{VWB[1],VWB[2]},{VWm,conj[VWm]},ZW},
  {{fWB[1],fWB[2],fWB[3]},{fWm,fWp,fW0},ZfW}
};      
          	

(* ----- VEVs ---- *)

DEFINITION[EWSB][VEVs]= 
  {{SHd0, {vd, 1/Sqrt[2]}, {sigmad, \[ImaginaryI]/Sqrt[2]},{phid,1/Sqrt[2]}},
   {SHu0, {vu, 1/Sqrt[2]}, {sigmau, \[ImaginaryI]/Sqrt[2]},{phiu,1/Sqrt[2]}},
   {SsR, {vS, 1/Sqrt[2]}, {sigmaS, \[ImaginaryI]/Sqrt[2]},{phiS,1/Sqrt[2]}}
   
   };


 
(* ---- Mixings ---- *)

DEFINITION[EWSB][MatterSector]= 
{    {{SdL, SdR}, {Sd, ZD}},
     {{SdL10, SdL10p, SdR5, SdR5p}, {Sdp, ZDp}},
     {{SuL10, SuL10p, SuR10, SuR10p}, {Sup, ZUp}},     
     {{SvL}, {Sv, ZV}},
     {{SvL5, SvL5p}, {Svp, ZVp}},
     {{SuL, SuR}, {Su, ZU}},
     {{SeL, SeR}, {Se, ZE}},
     {{SeL5,SeL5p,SeR10,SeR10p},{Sep,ZEp}},
     {{phid, phiu, phiS}, {hh, ZH}},
     {{sigmad, sigmau, sigmaS}, {Ah, ZA}},
     {{SHdm,conj[SHup]},{Hpm,ZP}},
     {{fB, fW0, FHd0, FHu0, FsR}, {L0, ZN}}, 
     {{{fWm, FHdm}, {fWp, FHup}}, {{Lm,UM}, {Lp,UP}}},
     {{{FeL},{conj[FeR]}},{{FEL,ZEL},{FER,ZER}}},
     {{{FdL},{conj[FdR]}},{{FDL,ZDL},{FDR,ZDR}}},
     {{{FuL},{conj[FuR]}},{{FUL,ZUL},{FUR,ZUR}}},
     
     {{{FuL10,FuR10p},{conj[FuL10p],conj[FuR10]}},{{FULp,ZULp},{FURp,ZURp}}},      
     {{{FeL5,FeR10p},{conj[FeL5p],conj[FeR10]}},{{FELp,ZELp},{FERp,ZERp}}},
     {{{FdL10,FdR5p},{conj[FdL10p],conj[FdR5]}},{{FDLp,ZDLp},{FDRp,ZDRp}}}
     }; 
       
DEFINITION[EWSB][Phases]= 
{    {fG, PhaseGlu},
     {FvL5, PhaseV}     
    }; 

	
	
DEFINITION[EWSB][DiracSpinors]={
 Fd ->{  FDL, conj[FDR]},
 Fe ->{  FEL, conj[FER]},
 Fu ->{  FUL, conj[FUR]},
 Fv ->{  FvL, 0},
 Fup -> {FULp, conj[FURp]}, 
 Fep -> {FELp, conj[FERp]}, 
 Fdp -> {FDLp, conj[FDRp]}, 
 Fvp -> {FvL5, FvL5p},
 Chi ->{ L0, conj[L0]},
 Cha ->{ Lm, conj[Lp]},
 Glu ->{ fG, conj[fG]}
};	

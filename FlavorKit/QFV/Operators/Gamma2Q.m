(* Code automatically generated by 'PreSARAH' *) 
(* Expressions for amplitudes are obtained by FeynArts/FormCalc *) 
(* This file is supposed to be loaded and used by SARAH *) 
(* Created at 15:35 on 16.12.2015 *) 
 
 
Print["   ... ",Gamma2Q]; 
NamesParticles =  {bar[BottomQuark], BottomQuark, Photon}; 
 NamesOperators =  {OA2qSL, OA2qSR, OA2qVL, OA2qVR}; 
 NameProcess = Gamma2Q; 
 
Generate[Gamma2Q][file_]:=Block[{i,j,k}, 
 

 (* Creating all possible processes; extract information about involved masses/couplings *) 


(* ------------------------------- *)
(* {bar[BottomQuark], BottomQuark, Photon} *)
(* ------------------------------- *)
 
GetInformtion2Fermion1BosonProcess[bar[BottomQuark],BottomQuark,Photon,Gamma2Q,file]; 
NeededMassesAll=Intersection[NeededMasses];
NeededCouplingsAll=Intersection[NeededCouplings];
WriteCodeObservablePreSARAH[Gamma2Q][NeededMassesAll,NeededCouplingsAll,TreeContributions,WaveContributions,PenguinContributions,file]; 
NeededMassAllSaved[Gamma2Q] = masses 
]; 

WriteCodeObservablePreSARAH[Gamma2Q][masses_,couplings_,tree_,wave_,penguin_,file_] :=Block[{i,j,k,fermions,scalars}, 
 
NeededMassesAllSaved[Gamma2Q] = masses; 
NeededCouplingsAllSaved[Gamma2Q] = couplings; 
NeededCombinations[Gamma2Q] = {{3, 2}}; 
Print["     writing SPheno code for ",Gamma2Q]; 
MakeSubroutineTitle["CalculateGamma2Q",Flatten[{masses,couplings}],{"gt1","gt2","gt3","OnlySM"}, 
{"OA2qSL", "OA2qSR", "OA2qVL", "OA2qVR"},file]; 
WriteString[file,"! ---------------------------------------------------------------- \n"]; 
WriteString[file,"! Code based on automatically generated SARAH extensions by 'PreSARAH' \n"]; 
WriteString[file,"! Expressions for amplitudes are obtained by FeynArts/FormCalc \n"]; 
WriteString[file,"! Based on user input for process Gamma2Q \n"]; 
WriteString[file,"! 'PreSARAH' output has been generated  at 15:35 on 16.12.2015 \n"]; 
WriteString[file,"! ---------------------------------------------------------------- \n \n"]; 
 
 
WriteString[file,"Implicit None \n"]; 
MakeVariableList[Flatten[{couplings,masses}],",Intent(in)",file];
WriteString[file,"Integer,Intent(in) :: gt1, gt2,gt3 \n"];
WriteString[file,"Integer :: gt4 \n"];
WriteString[file,"Logical, Intent(in) :: OnlySM \n"];
WriteString[file,"Integer :: iprop, i1, i2, i3, i4 \n"];
WriteString[file,"Real(dp) :: MassEx1,MassEx2,MassEx3,MassEx12,MassEx22,MassEx32 \n"];
WriteString[file,"Complex(dp), Intent(out) :: OA2qSL \n"]; 
WriteString[file,"Complex(dp), Intent(out) :: OA2qSR \n"]; 
WriteString[file,"Complex(dp), Intent(out) :: OA2qVL \n"]; 
WriteString[file,"Complex(dp), Intent(out) :: OA2qVR \n"]; 
WriteString[file,"Real(dp) ::  MP, MP2, IMP2, IMP, MFin, MFin2, IMFin, IMFin2, Finite  \n"];
WriteString[file,"Real(dp) ::  MS1, MS12, MS2, MS22, MF1, MF12, MF2, MF22, MV1, MV12, MV2, MV22  \n"];
WriteString[file,"Complex(dp) ::  chargefactor  \n"];
WriteString[file,"Complex(dp) ::  coup1L, coup1R, coup2L, coup2R, coup3L, coup3R, coup3, coup4L, coup4R \n\n"];

WriteString[file,"Complex(dp) ::  int1,int2,int3,int4,int5,int6,int7,int8 \n\n"];

WriteString[file,"Iname=Iname+1 \n"];
WriteString[file,"NameOfUnit(Iname)='CalculateGamma2Q' \n
"];
 
AddCalcSquaredMasses[masses,file]; 
(* Initaliziation *)
WriteString[file,"Finite=1._dp \n"];
WriteString[file,"MassEx1="<>SPhenoMass[bar[BottomQuark],gt1]<>"  \n"];
WriteString[file,"MassEx12="<>SPhenoMassSq[bar[BottomQuark],gt1]<>" \n"];
WriteString[file,"MassEx2="<>SPhenoMass[BottomQuark,gt2]<>"  \n"];
WriteString[file,"MassEx22="<>SPhenoMassSq[BottomQuark,gt2]<>" \n"];
WriteString[file,"MassEx3="<>SPhenoMass[Photon,gt3]<>"  \n"];
WriteString[file,"MassEx32="<>SPhenoMassSq[Photon,gt3]<>" \n"];
WriteString[file,"! ------------------------------ \n "];
WriteString[file,"! Amplitudes for external states \n "];
WriteString[file,"! {bar[BottomQuark], BottomQuark, Photon} \n "];
WriteString[file,"! ------------------------------ \n \n"];
WriteString[sphenoTeX,"\\section{External states: $"<>TeXOutput[{bar[BottomQuark][{gt1}], BottomQuark[{gt2}], Photon[{gt3}]}]<>"$} \n"];
WriteString[file,"OA2qSL=0._dp \n"]; 
WriteString[file,"OA2qSR=0._dp \n"]; 
WriteString[file,"OA2qVL=0._dp \n"]; 
WriteString[file,"OA2qVR=0._dp \n"]; 
WriteDiagramsObservable[Gamma2Q,tree, wave, penguin, file];
WriteString[file,"OA2qSL=oo16pi2*OA2qSL \n"]; 
WriteString[file,"OA2qSR=oo16pi2*OA2qSR \n"]; 
WriteString[file,"OA2qVL=oo16pi2*OA2qVL \n"]; 
WriteString[file,"OA2qVR=oo16pi2*OA2qVR \n"]; 
WriteString[file,"Iname=Iname-1\n\n"]; 
WriteString[file,"End Subroutine CalculateGamma2Q \n\n"]; 
]; 
AddTreeResultPreSARAH[Gamma2Q][top_,type_,file_]:=Block[{}, 

 (* This routine returns the generic expression for the amplitude of a given triangle diagram *) 
 
 Switch[top,  (* Check topology *) 
  1, 
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+ 0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+ 0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+ 0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+ 0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
]; 
]; 


AddPenguinResultPreSARAH[Gamma2Q][top_,type_,file_]:=Block[{}, 

 (* This routine returns the generic expression for the amplitude of a given triangle diagram *) 
 
 Switch[top,  (* Check topology *) 
  1, 
  Switch[type,  (* Check the generic type of the diagram *) 
	SFF, 
	 	 WriteString[file,"  int1=B0(0._dp, mF12, mF22)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(0, mF12, mF22)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=C00g(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["C00g(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int3=C0C1C2(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_3= & "<> StringReplace["C0C1C2(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int4=C0g(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_4= & "<> StringReplace["C0g(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int5=C12g(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_5= & "<> StringReplace["C12g(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int6=C1g(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_6= & "<> StringReplace["C1g(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int7=C2C12C22(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_7= & "<> StringReplace["C2C12C22(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int8=C2g(mF22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_8= & "<> StringReplace["C2g(mF22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+2.*chargefactor*(coup1R*coup2L*coup3L*int5*MassEx1 - 1.*coup1L*(coup2R*coup3R*int7*MassEx2 + coup2L*coup3L*int6*mF1 - 1.*coup2L*coup3R*int3*mF2))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["2 chargefactor (coup1R coup2L coup3L I_5 MassEx1 - coup1L (coup2R coup3R I_7 MassEx2 + coup2L coup3L I_6 mF1 - coup2L coup3R I_3 mF2))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,2*(coup1L*coup2L*coup3R*mF2*C0C1C2[mF22, mF12, mS12] + coup1R*coup2L*coup3L*MassEx1*C12g[mF22, mF12, mS12] - coup1L*(coup2L*coup3L*mF1*C1g[mF22, mF12, mS12] + coup2R*coup3R*MassEx2*C2C12C22[mF22, mF12, mS12]))}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+2.*chargefactor*(coup1L*coup2R*coup3R*int5*MassEx1 - 1.*coup1R*(coup2L*coup3L*int7*MassEx2 + coup2R*coup3R*int6*mF1 - 1.*coup2R*coup3L*int3*mF2))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["2 chargefactor (coup1L coup2R coup3R I_5 MassEx1 - coup1R (coup2L coup3L I_7 MassEx2 + coup2R coup3R I_6 mF1 - coup2R coup3L I_3 mF2))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,2*(coup1R*coup2R*coup3L*mF2*C0C1C2[mF22, mF12, mS12] + coup1L*coup2R*coup3R*MassEx1*C12g[mF22, mF12, mS12] - coup1R*(coup2R*coup3R*mF1*C1g[mF22, mF12, mS12] + coup2L*coup3L*MassEx2*C2C12C22[mF22, mF12, mS12]))}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+chargefactor*(2.*coup1R*MassEx1*(-1.*coup2L*coup3L*int8*MassEx2 + coup2R*(-1.*coup3R*int6*mF1 + coup3L*(int4 + int6)*mF2)) + coup1L*(2.*coup2L*MassEx2*(-1.*coup3L*(int6 + int8)*mF1 + coup3R*(int4 + int6 + int8)*mF2) + coup2R*(2.*coup3L*int4*mF1*mF2 + coup3R*(-1.*int1 + 2.*int2 - 1.*int6*MassEx12 + int4*MassEx22 + int6*MassEx22 + int8*MassEx22 - 1.*int4*mS12))))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["chargefactor (2 coup1R MassEx1 (-(coup2L coup3L I_8 MassEx2) + coup2R (-(coup3R I_6 mF1) + coup3L (I_4 + I_6) mF2)) + coup1L (2 coup2L MassEx2 (-(coup3L (I_6 + I_8) mF1) + coup3R (I_4 + I_6 + I_8) mF2) + coup2R (2 coup3L I_4 mF1 mF2 + coup3R (-I_1 + 2 I_2 - I_6 MassEx12 + I_4 MassEx22 + I_6 MassEx22 + I_8 MassEx22 - I_4 mS12))))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,-(coup1L*coup2R*coup3R*bb0[0, mF12, mF22]) + 2*coup1L*coup2R*coup3R*C00g[mF22, mF12, mS12] + coup1L*coup2R*coup3R*MassEx22*C0g[mF22, mF12, mS12] + 2*coup1R*coup2R*coup3L*MassEx1*mF2*C0g[mF22, mF12, mS12] + 2*coup1L*coup2L*coup3R*MassEx2*mF2*C0g[mF22, mF12, mS12] + 2*coup1L*coup2R*coup3L*mF1*mF2*C0g[mF22, mF12, mS12] - coup1L*coup2R*coup3R*mS12*C0g[mF22, mF12, mS12] - coup1L*coup2R*coup3R*MassEx12*C1g[mF22, mF12, mS12] + coup1L*coup2R*coup3R*MassEx22*C1g[mF22, mF12, mS12] - 2*coup1R*coup2R*coup3R*MassEx1*mF1*C1g[mF22, mF12, mS12] - 2*coup1L*coup2L*coup3L*MassEx2*mF1*C1g[mF22, mF12, mS12] + 2*coup1R*coup2R*coup3L*MassEx1*mF2*C1g[mF22, mF12, mS12] + 2*coup1L*coup2L*coup3R*MassEx2*mF2*C1g[mF22, mF12, mS12] - 2*coup1R*coup2L*coup3L*MassEx1*MassEx2*C2g[mF22, mF12, mS12] + coup1L*coup2R*coup3R*MassEx22*C2g[mF22, mF12, mS12] - 2*coup1L*coup2L*coup3L*MassEx2*mF1*C2g[mF22, mF12, mS12] + 2*coup1L*coup2L*coup3R*MassEx2*mF2*C2g[mF22, mF12, mS12]}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+chargefactor*(2.*coup1L*MassEx1*(-1.*coup2R*coup3R*int8*MassEx2 + coup2L*(-1.*coup3L*int6*mF1 + coup3R*(int4 + int6)*mF2)) + coup1R*(2.*coup2R*MassEx2*(-1.*coup3R*(int6 + int8)*mF1 + coup3L*(int4 + int6 + int8)*mF2) + coup2L*(2.*coup3R*int4*mF1*mF2 + coup3L*(-1.*int1 + 2.*int2 - 1.*int6*MassEx12 + int4*MassEx22 + int6*MassEx22 + int8*MassEx22 - 1.*int4*mS12))))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["chargefactor (2 coup1L MassEx1 (-(coup2R coup3R I_8 MassEx2) + coup2L (-(coup3L I_6 mF1) + coup3R (I_4 + I_6) mF2)) + coup1R (2 coup2R MassEx2 (-(coup3R (I_6 + I_8) mF1) + coup3L (I_4 + I_6 + I_8) mF2) + coup2L (2 coup3R I_4 mF1 mF2 + coup3L (-I_1 + 2 I_2 - I_6 MassEx12 + I_4 MassEx22 + I_6 MassEx22 + I_8 MassEx22 - I_4 mS12))))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,-(coup1R*coup2L*coup3L*bb0[0, mF12, mF22]) + 2*coup1R*coup2L*coup3L*C00g[mF22, mF12, mS12] + coup1R*coup2L*coup3L*MassEx22*C0g[mF22, mF12, mS12] + 2*coup1L*coup2L*coup3R*MassEx1*mF2*C0g[mF22, mF12, mS12] + 2*coup1R*coup2R*coup3L*MassEx2*mF2*C0g[mF22, mF12, mS12] + 2*coup1R*coup2L*coup3R*mF1*mF2*C0g[mF22, mF12, mS12] - coup1R*coup2L*coup3L*mS12*C0g[mF22, mF12, mS12] - coup1R*coup2L*coup3L*MassEx12*C1g[mF22, mF12, mS12] + coup1R*coup2L*coup3L*MassEx22*C1g[mF22, mF12, mS12] - 2*coup1L*coup2L*coup3L*MassEx1*mF1*C1g[mF22, mF12, mS12] - 2*coup1R*coup2R*coup3R*MassEx2*mF1*C1g[mF22, mF12, mS12] + 2*coup1L*coup2L*coup3R*MassEx1*mF2*C1g[mF22, mF12, mS12] + 2*coup1R*coup2R*coup3L*MassEx2*mF2*C1g[mF22, mF12, mS12] - 2*coup1L*coup2R*coup3R*MassEx1*MassEx2*C2g[mF22, mF12, mS12] + coup1R*coup2L*coup3L*MassEx22*C2g[mF22, mF12, mS12] - 2*coup1R*coup2R*coup3R*MassEx2*mF1*C2g[mF22, mF12, mS12] + 2*coup1R*coup2R*coup3L*MassEx2*mF2*C2g[mF22, mF12, mS12]} " ];
,
	FSS, 
	 	 WriteString[file,"  int1=C00g(mF12, mS22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["C00g(mF12, mS22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=C0C1C2(mF12, mS22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["C0C1C2(mF12, mS22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int3=C1C12C11(mF12, mS22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_3= & "<> StringReplace["C1C12C11(mF12, mS22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int4=C2C12C22(mF12, mS22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_4= & "<> StringReplace["C2C12C22(mF12, mS22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+2.*chargefactor*coup3*(coup1R*coup2L*int4*MassEx1 + coup1L*coup2R*int3*MassEx2 - 1.*coup1L*coup2L*int2*mF1)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["2 chargefactor coup3 (coup1R coup2L I_4 MassEx1 + coup1L coup2R I_3 MassEx2 - coup1L coup2L I_2 mF1)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,2*coup3*(-(coup1L*coup2L*mF1*C0C1C2[mF12, mS22, mS12]) + coup1L*coup2R*MassEx2*C1C12C11[mF12, mS22, mS12] + coup1R*coup2L*MassEx1*C2C12C22[mF12, mS22, mS12])}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+2.*chargefactor*coup3*(coup1L*coup2R*int4*MassEx1 + coup1R*coup2L*int3*MassEx2 - 1.*coup1R*coup2R*int2*mF1)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["2 chargefactor coup3 (coup1L coup2R I_4 MassEx1 + coup1R coup2L I_3 MassEx2 - coup1R coup2R I_2 mF1)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,2*coup3*(-(coup1R*coup2R*mF1*C0C1C2[mF12, mS22, mS12]) + coup1R*coup2L*MassEx2*C1C12C11[mF12, mS22, mS12] + coup1L*coup2R*MassEx1*C2C12C22[mF12, mS22, mS12])}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+-2.*chargefactor*coup1L*coup2R*coup3*int1\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["-2 chargefactor coup1L coup2R coup3 I_1",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,-2*coup1L*coup2R*coup3*C00g[mF12, mS22, mS12]}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+-2.*chargefactor*coup1R*coup2L*coup3*int1\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["-2 chargefactor coup1R coup2L coup3 I_1",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,-2*coup1R*coup2L*coup3*C00g[mF12, mS22, mS12]} " ];
,
	VFF, 
	 	 WriteString[file,"  int1=B0(0._dp, mF12, mF22)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(0, mF12, mF22)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=C00g(mF22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["C00g(mF22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int3=C0g(mF22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_3= & "<> StringReplace["C0g(mF22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int4=C12C22(mF22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_4= & "<> StringReplace["C12C22(mF22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int5=C1g(mF22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_5= & "<> StringReplace["C1g(mF22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int6=C2C12(mF22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_6= & "<> StringReplace["C2C12(mF22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int7=C2g(mF22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_7= & "<> StringReplace["C2g(mF22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+-4.*chargefactor*(-1.*coup1R*coup2R*coup3R*int6*MassEx1 + coup1L*(coup2L*coup3L*int4*MassEx2 + coup2R*int7*(coup3R*mF1 + coup3L*mF2)))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["-4 chargefactor (-(coup1R coup2R coup3R I_6 MassEx1) + coup1L (coup2L coup3L I_4 MassEx2 + coup2R I_7 (coup3R mF1 + coup3L mF2)))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,-4*(coup1L*coup2L*coup3L*MassEx2*C12C22[mF22, mF12, mV12] + coup2R*(-(coup1R*coup3R*MassEx1*C2C12[mF22, mF12, mV12]) + coup1L*(coup3R*mF1 + coup3L*mF2)*C2g[mF22, mF12, mV12]))}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+chargefactor*(4.*coup1L*coup2L*coup3L*int6*MassEx1 - 4.*coup1R*(coup2R*coup3R*int4*MassEx2 + coup2L*int7*(coup3L*mF1 + coup3R*mF2)))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["chargefactor (4 coup1L coup2L coup3L I_6 MassEx1 - 4 coup1R (coup2R coup3R I_4 MassEx2 + coup2L I_7 (coup3L mF1 + coup3R mF2)))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,-4*(coup1R*coup2R*coup3R*MassEx2*C12C22[mF22, mF12, mV12] + coup2L*(-(coup1L*coup3L*MassEx1*C2C12[mF22, mF12, mV12]) + coup1R*(coup3L*mF1 + coup3R*mF2)*C2g[mF22, mF12, mV12]))}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+chargefactor*(4.*coup1R*coup2R*coup3R*int7*MassEx1*MassEx2 + coup1L*coup2L*(4.*coup3R*int3*mF1*mF2 + coup3L*(Finite - 2.*int1 + 4.*int2 - 2.*int5*MassEx12 + 2.*int3*MassEx22 + 2.*int5*MassEx22 + 2.*int7*MassEx22 - 2.*int3*mV12)))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["chargefactor (4 coup1R coup2R coup3R I_7 MassEx1 MassEx2 + coup1L coup2L (4 coup3R I_3 mF1 mF2 + coup3L (1 - 2 I_1 + 4 I_2 - 2 I_5 MassEx12 + 2 I_3 MassEx22 + 2 I_5 MassEx22 + 2 I_7 MassEx22 - 2 I_3 mV12)))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,4*coup1L*coup2L*coup3R*mF1*mF2*C0g[mF22, mF12, mV12] + 4*coup1R*coup2R*coup3R*MassEx1*MassEx2*C2g[mF22, mF12, mV12] + coup1L*coup2L*coup3L*(Finite - 2*bb0[0, mF12, mF22] + 4*C00g[mF22, mF12, mV12] + 2*MassEx22*C0g[mF22, mF12, mV12] - 2*mV12*C0g[mF22, mF12, mV12] - 2*MassEx12*C1g[mF22, mF12, mV12] + 2*MassEx22*C1g[mF22, mF12, mV12] + 2*MassEx22*C2g[mF22, mF12, mV12])}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+chargefactor*(4.*coup1L*coup2L*coup3L*int7*MassEx1*MassEx2 + coup1R*coup2R*(4.*coup3L*int3*mF1*mF2 + coup3R*(Finite - 2.*int1 + 4.*int2 - 2.*int5*MassEx12 + 2.*int3*MassEx22 + 2.*int5*MassEx22 + 2.*int7*MassEx22 - 2.*int3*mV12)))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["chargefactor (4 coup1L coup2L coup3L I_7 MassEx1 MassEx2 + coup1R coup2R (4 coup3L I_3 mF1 mF2 + coup3R (1 - 2 I_1 + 4 I_2 - 2 I_5 MassEx12 + 2 I_3 MassEx22 + 2 I_5 MassEx22 + 2 I_7 MassEx22 - 2 I_3 mV12)))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,4*coup1R*coup2R*coup3L*mF1*mF2*C0g[mF22, mF12, mV12] + 4*coup1L*coup2L*coup3L*MassEx1*MassEx2*C2g[mF22, mF12, mV12] + coup1R*coup2R*coup3R*(Finite - 2*bb0[0, mF12, mF22] + 4*C00g[mF22, mF12, mV12] + 2*MassEx22*C0g[mF22, mF12, mV12] - 2*mV12*C0g[mF22, mF12, mV12] - 2*MassEx12*C1g[mF22, mF12, mV12] + 2*MassEx22*C1g[mF22, mF12, mV12] + 2*MassEx22*C2g[mF22, mF12, mV12])} " ];
,
	FSV, 
	 	 WriteString[file,"  int1=C0g(mF12, mV22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["C0g(mF12, mV22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=C1g(mF12, mV22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["C1g(mF12, mV22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int3=C2g(mF12, mV22, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_3= & "<> StringReplace["C2g(mF12, mV22, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+-2.*chargefactor*coup1L*coup2R*coup3*int2\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["-2 chargefactor coup1L coup2R coup3 I_2",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,-2*coup1L*coup2R*coup3*C1g[mF12, mV22, mS12]}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+-2.*chargefactor*coup1R*coup2L*coup3*int2\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["-2 chargefactor coup1R coup2L coup3 I_2",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,-2*coup1R*coup2L*coup3*C1g[mF12, mV22, mS12]}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+chargefactor*coup3*(coup1R*coup2L*int3*MassEx1 - 1.*coup1L*(coup2R*int2*MassEx2 + coup2L*int1*mF1))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["chargefactor coup3 (coup1R coup2L I_3 MassEx1 - coup1L (coup2R I_2 MassEx2 + coup2L I_1 mF1))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,-(coup3*(coup1L*coup2L*mF1*C0g[mF12, mV22, mS12] + coup1L*coup2R*MassEx2*C1g[mF12, mV22, mS12] - coup1R*coup2L*MassEx1*C2g[mF12, mV22, mS12]))}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+chargefactor*coup3*(coup1L*coup2R*int3*MassEx1 - 1.*coup1R*(coup2L*int2*MassEx2 + coup2R*int1*mF1))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["chargefactor coup3 (coup1L coup2R I_3 MassEx1 - coup1R (coup2L I_2 MassEx2 + coup2R I_1 mF1))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,-(coup3*(coup1R*coup2R*mF1*C0g[mF12, mV22, mS12] + coup1R*coup2L*MassEx2*C1g[mF12, mV22, mS12] - coup1L*coup2R*MassEx1*C2g[mF12, mV22, mS12]))} " ];
,
	FVS, 
	 	 WriteString[file,"  int1=C0g(mF12, mS22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["C0g(mF12, mS22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=C1g(mF12, mS22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["C1g(mF12, mS22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int3=C2g(mF12, mS22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_3= & "<> StringReplace["C2g(mF12, mS22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+-2.*chargefactor*coup1L*coup2L*coup3*int3\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["-2 chargefactor coup1L coup2L coup3 I_3",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,-2*coup1L*coup2L*coup3*C2g[mF12, mS22, mV12]}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+-2.*chargefactor*coup1R*coup2R*coup3*int3\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["-2 chargefactor coup1R coup2R coup3 I_3",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,-2*coup1R*coup2R*coup3*C2g[mF12, mS22, mV12]}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+-1.*chargefactor*coup3*(coup1R*coup2R*int3*MassEx1 - 1.*coup1L*coup2L*int2*MassEx2 + coup1L*coup2R*int1*mF1)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["-(chargefactor coup3 (coup1R coup2R I_3 MassEx1 - coup1L coup2L I_2 MassEx2 + coup1L coup2R I_1 mF1))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,-(coup3*(coup1L*coup2R*mF1*C0g[mF12, mS22, mV12] - coup1L*coup2L*MassEx2*C1g[mF12, mS22, mV12] + coup1R*coup2R*MassEx1*C2g[mF12, mS22, mV12]))}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+-1.*chargefactor*coup3*(coup1L*coup2L*int3*MassEx1 - 1.*coup1R*coup2R*int2*MassEx2 + coup1R*coup2L*int1*mF1)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["-(chargefactor coup3 (coup1L coup2L I_3 MassEx1 - coup1R coup2R I_2 MassEx2 + coup1R coup2L I_1 mF1))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,-(coup3*(coup1R*coup2L*mF1*C0g[mF12, mS22, mV12] - coup1R*coup2R*MassEx2*C1g[mF12, mS22, mV12] + coup1L*coup2L*MassEx1*C2g[mF12, mS22, mV12]))} " ];
,
	FVV, 
	 	 WriteString[file,"  int1=B0(0._dp, mV12, mV22)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(0, mV12, mV22)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=C00g(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["C00g(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int3=C0g(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_3= & "<> StringReplace["C0g(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int4=C12C11C2(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_4= & "<> StringReplace["C12C11C2(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int5=C12C22C1(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_5= & "<> StringReplace["C12C22C1(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int6=C1C2(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_6= & "<> StringReplace["C1C2(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int7=C1g(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_7= & "<> StringReplace["C1g(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int8=C2g(mF12, mV22, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_8= & "<> StringReplace["C2g(mF12, mV22, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+2.*chargefactor*coup3*(coup1R*coup2R*int5*MassEx1 + coup1L*coup2L*int4*MassEx2 + 3.*coup1L*coup2R*int6*mF1)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["2 chargefactor coup3 (coup1R coup2R I_5 MassEx1 + coup1L coup2L I_4 MassEx2 + 3 coup1L coup2R I_6 mF1)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,2*coup3*(coup1L*coup2L*MassEx2*C12C11C2[mF12, mV22, mV12] + coup1R*coup2R*MassEx1*C12C22C1[mF12, mV22, mV12] + 3*coup1L*coup2R*mF1*C1C2[mF12, mV22, mV12])}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+2.*chargefactor*coup3*(coup1L*coup2L*int5*MassEx1 + coup1R*coup2R*int4*MassEx2 + 3.*coup1R*coup2L*int6*mF1)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["2 chargefactor coup3 (coup1L coup2L I_5 MassEx1 + coup1R coup2R I_4 MassEx2 + 3 coup1R coup2L I_6 mF1)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,2*coup3*(coup1R*coup2R*MassEx2*C12C11C2[mF12, mV22, mV12] + coup1L*coup2L*MassEx1*C12C22C1[mF12, mV22, mV12] + 3*coup1R*coup2L*mF1*C1C2[mF12, mV22, mV12])}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+chargefactor*coup3*(-6.*coup1R*MassEx1*(coup2R*(int7 + int8)*MassEx2 + coup2L*int3*mF1) - 1.*coup1L*(6.*coup2R*int3*MassEx2*mF1 + coup2L*(-1.*Finite + 2.*int1 + 4.*int2 + int8*MassEx12 + int7*MassEx22 + 2.*int3*mF12)))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["chargefactor coup3 (-6 coup1R MassEx1 (coup2R (I_7 + I_8) MassEx2 + coup2L I_3 mF1) - coup1L (6 coup2R I_3 MassEx2 mF1 + coup2L (-1 + 2 I_1 + 4 I_2 + I_8 MassEx12 + I_7 MassEx22 + 2 I_3 mF12)))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,coup3*(coup1L*coup2L*Finite - 2*coup1L*coup2L*bb0[0, mV12, mV22] - 4*coup1L*coup2L*C00g[mF12, mV22, mV12] - 6*coup1R*coup2L*MassEx1*mF1*C0g[mF12, mV22, mV12] - 6*coup1L*coup2R*MassEx2*mF1*C0g[mF12, mV22, mV12] - 2*coup1L*coup2L*mF12*C0g[mF12, mV22, mV12] - 6*coup1R*coup2R*MassEx1*MassEx2*C1g[mF12, mV22, mV12] - coup1L*coup2L*MassEx22*C1g[mF12, mV22, mV12] - coup1L*coup2L*MassEx12*C2g[mF12, mV22, mV12] - 6*coup1R*coup2R*MassEx1*MassEx2*C2g[mF12, mV22, mV12])}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+chargefactor*coup3*(-6.*coup1L*MassEx1*(coup2L*(int7 + int8)*MassEx2 + coup2R*int3*mF1) - 1.*coup1R*(6.*coup2L*int3*MassEx2*mF1 + coup2R*(-1.*Finite + 2.*int1 + 4.*int2 + int8*MassEx12 + int7*MassEx22 + 2.*int3*mF12)))\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["chargefactor coup3 (-6 coup1L MassEx1 (coup2L (I_7 + I_8) MassEx2 + coup2R I_3 mF1) - coup1R (6 coup2L I_3 MassEx2 mF1 + coup2R (-1 + 2 I_1 + 4 I_2 + I_8 MassEx12 + I_7 MassEx22 + 2 I_3 mF12)))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,coup3*(coup1R*coup2R*Finite - 2*coup1R*coup2R*bb0[0, mV12, mV22] - 4*coup1R*coup2R*C00g[mF12, mV22, mV12] - 6*coup1L*coup2R*MassEx1*mF1*C0g[mF12, mV22, mV12] - 6*coup1R*coup2L*MassEx2*mF1*C0g[mF12, mV22, mV12] - 2*coup1R*coup2R*mF12*C0g[mF12, mV22, mV12] - 6*coup1L*coup2L*MassEx1*MassEx2*C1g[mF12, mV22, mV12] - coup1R*coup2R*MassEx22*C1g[mF12, mV22, mV12] - coup1R*coup2R*MassEx12*C2g[mF12, mV22, mV12] - 6*coup1L*coup2L*MassEx1*MassEx2*C2g[mF12, mV22, mV12])} " ];
]; 
];]; 


AddWaveResultPreSARAH[Gamma2Q][top_,type_,file_]:=Block[{}, 

 (* This routine returns the generic expression for the amplitude of a given triangle diagram *) 
 
 Switch[top,  (* Check topology *) 
  1, 
  Switch[type,  (* Check the generic type of the diagram *) 
	FS | SF , 
	 	 WriteString[file,"  int1=B0(MassEx12, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(MassEx12, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=B1(MassEx12, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["B_1(MassEx12, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,0}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,0}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+(chargefactor*coup3L*(-1.*coup1L*coup2R*int2*MassEx12 + coup1R*coup2R*int1*MassEx1*mF1 - 1.*coup1R*coup2L*int2*MassEx1*MFin + coup1L*coup2L*int1*mF1*MFin))/(MassEx12 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["(chargefactor coup3L (-(coup1L coup2R I_2 MassEx12) + coup1R coup2R I_1 MassEx1 mF1 - coup1R coup2L I_2 MassEx1 MFin + coup1L coup2L I_1 mF1 MFin))/(MassEx12 - MFin2)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,(coup3L*(mF1*(coup1R*coup2R*MassEx1 + coup1L*coup2L*MFin)*bb0[MassEx12, mF12, mS12] - (coup1L*coup2R*MassEx12 + coup1R*coup2L*MassEx1*MFin)*bb1[MassEx12, mF12, mS12]))/(MassEx12 - MFin2)}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+(chargefactor*coup3R*(-1.*coup1R*coup2L*int2*MassEx12 + coup1L*coup2L*int1*MassEx1*mF1 - 1.*coup1L*coup2R*int2*MassEx1*MFin + coup1R*coup2R*int1*mF1*MFin))/(MassEx12 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["(chargefactor coup3R (-(coup1R coup2L I_2 MassEx12) + coup1L coup2L I_1 MassEx1 mF1 - coup1L coup2R I_2 MassEx1 MFin + coup1R coup2R I_1 mF1 MFin))/(MassEx12 - MFin2)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,(coup3R*(mF1*(coup1L*coup2L*MassEx1 + coup1R*coup2R*MFin)*bb0[MassEx12, mF12, mS12] - (coup1R*coup2L*MassEx12 + coup1L*coup2R*MassEx1*MFin)*bb1[MassEx12, mF12, mS12]))/(MassEx12 - MFin2)} " ];
,
	FV | VF , 
	 	 WriteString[file,"  int1=B0(MassEx12, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(MassEx12, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=B1(MassEx12, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["B_1(MassEx12, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,0}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,0}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+(-1.*chargefactor*coup3L*(coup1R*MassEx1*(-2.*coup2L*(Finite - 2.*int1)*mF1 + coup2R*(Finite + 2.*int2)*MFin) + coup1L*(coup2L*(Finite + 2.*int2)*MassEx12 - 2.*coup2R*(Finite - 2.*int1)*mF1*MFin)))/(MassEx12 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["-((chargefactor coup3L (coup1R MassEx1 (-2 coup2L (1 - 2 I_1) mF1 + coup2R (1 + 2 I_2) MFin) + coup1L (coup2L (1 + 2 I_2) MassEx12 - 2 coup2R (1 - 2 I_1) mF1 MFin)))/(MassEx12 - MFin2))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,-((coup3L*(Finite*(coup1L*coup2L*MassEx12 - 2*coup1R*coup2L*MassEx1*mF1 + coup1R*coup2R*MassEx1*MFin - 2*coup1L*coup2R*mF1*MFin) + 4*mF1*(coup1R*coup2L*MassEx1 + coup1L*coup2R*MFin)*bb0[MassEx12, mF12, mV12] + 2*(coup1L*coup2L*MassEx12 + coup1R*coup2R*MassEx1*MFin)*bb1[MassEx12, mF12, mV12]))/(MassEx12 - MFin2))}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+(-1.*chargefactor*coup3R*(coup1L*MassEx1*(-2.*coup2R*(Finite - 2.*int1)*mF1 + coup2L*(Finite + 2.*int2)*MFin) + coup1R*(coup2R*(Finite + 2.*int2)*MassEx12 - 2.*coup2L*(Finite - 2.*int1)*mF1*MFin)))/(MassEx12 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["-((chargefactor coup3R (coup1L MassEx1 (-2 coup2R (1 - 2 I_1) mF1 + coup2L (1 + 2 I_2) MFin) + coup1R (coup2R (1 + 2 I_2) MassEx12 - 2 coup2L (1 - 2 I_1) mF1 MFin)))/(MassEx12 - MFin2))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,-((coup3R*(Finite*(coup1R*coup2R*MassEx12 - 2*coup1L*coup2R*MassEx1*mF1 + coup1L*coup2L*MassEx1*MFin - 2*coup1R*coup2L*mF1*MFin) + 4*mF1*(coup1L*coup2R*MassEx1 + coup1R*coup2L*MFin)*bb0[MassEx12, mF12, mV12] + 2*(coup1R*coup2R*MassEx12 + coup1L*coup2L*MassEx1*MFin)*bb1[MassEx12, mF12, mV12]))/(MassEx12 - MFin2))} " ];
]; 
,
  2, 
  Switch[type,  (* Check the generic type of the diagram *) 
	FS | SF , 
	 	 WriteString[file,"  int1=B0(MassEx22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(MassEx22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=B1(MassEx22, mF12, mS12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["B_1(MassEx22, mF12, mS12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,0}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,0}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+(chargefactor*coup3L*(-1.*coup1R*coup2L*int2*MassEx22 + coup1L*coup2L*int1*MassEx2*mF1 - 1.*coup1L*coup2R*int2*MassEx2*MFin + coup1R*coup2R*int1*mF1*MFin))/(MassEx22 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["(chargefactor coup3L (-(coup1R coup2L I_2 MassEx22) + coup1L coup2L I_1 MassEx2 mF1 - coup1L coup2R I_2 MassEx2 MFin + coup1R coup2R I_1 mF1 MFin))/(MassEx22 - MFin2)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,(coup3L*(mF1*(coup1L*coup2L*MassEx2 + coup1R*coup2R*MFin)*bb0[MassEx22, mF12, mS12] - (coup1R*coup2L*MassEx22 + coup1L*coup2R*MassEx2*MFin)*bb1[MassEx22, mF12, mS12]))/(MassEx22 - MFin2)}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+(chargefactor*coup3R*(-1.*coup1L*coup2R*int2*MassEx22 + coup1R*coup2R*int1*MassEx2*mF1 - 1.*coup1R*coup2L*int2*MassEx2*MFin + coup1L*coup2L*int1*mF1*MFin))/(MassEx22 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["(chargefactor coup3R (-(coup1L coup2R I_2 MassEx22) + coup1R coup2R I_1 MassEx2 mF1 - coup1R coup2L I_2 MassEx2 MFin + coup1L coup2L I_1 mF1 MFin))/(MassEx22 - MFin2)",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,(coup3R*(mF1*(coup1R*coup2R*MassEx2 + coup1L*coup2L*MFin)*bb0[MassEx22, mF12, mS12] - (coup1L*coup2R*MassEx22 + coup1R*coup2L*MassEx2*MFin)*bb1[MassEx22, mF12, mS12]))/(MassEx22 - MFin2)} " ];
,
	FV | VF , 
	 	 WriteString[file,"  int1=B0(MassEx22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_1= & "<> StringReplace["B_0(MassEx22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteString[file,"  int2=B1(MassEx22, mF12, mV12)\n" ];
	 	 WriteString[sphenoTeX,"I_2= & "<> StringReplace["B_1(MassEx22, mF12, mV12)",SA`SPhenoTeXSub]<>" \\\\ \n"];
	 	 WriteStringFLB[file,"  OA2qSL=OA2qSL+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSL= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSL,0}, " ];
	 	 WriteStringFLB[file,"  OA2qSR=OA2qSR+0.\n" ];
	 	 WriteString[sphenoTeX,"  OA2qSR= & "<> StringReplace["0",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qSR,0}, " ];
	 	 WriteStringFLB[file,"  OA2qVL=OA2qVL+(-1.*chargefactor*coup3L*(coup1R*MassEx2*(-2.*coup2L*(Finite - 2.*int1)*mF1 + coup2R*(Finite + 2.*int2)*MFin) + coup1L*(coup2L*(Finite + 2.*int2)*MassEx22 - 2.*coup2R*(Finite - 2.*int1)*mF1*MFin)))/(MassEx22 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVL= & "<> StringReplace["-((chargefactor coup3L (coup1R MassEx2 (-2 coup2L (1 - 2 I_1) mF1 + coup2R (1 + 2 I_2) MFin) + coup1L (coup2L (1 + 2 I_2) MassEx22 - 2 coup2R (1 - 2 I_1) mF1 MFin)))/(MassEx22 - MFin2))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVL,-((coup3L*(Finite*(coup1L*coup2L*MassEx22 - 2*coup1R*coup2L*MassEx2*mF1 + coup1R*coup2R*MassEx2*MFin - 2*coup1L*coup2R*mF1*MFin) + 4*mF1*(coup1R*coup2L*MassEx2 + coup1L*coup2R*MFin)*bb0[MassEx22, mF12, mV12] + 2*(coup1L*coup2L*MassEx22 + coup1R*coup2R*MassEx2*MFin)*bb1[MassEx22, mF12, mV12]))/(MassEx22 - MFin2))}, " ];
	 	 WriteStringFLB[file,"  OA2qVR=OA2qVR+(-1.*chargefactor*coup3R*(coup1L*MassEx2*(-2.*coup2R*(Finite - 2.*int1)*mF1 + coup2L*(Finite + 2.*int2)*MFin) + coup1R*(coup2R*(Finite + 2.*int2)*MassEx22 - 2.*coup2L*(Finite - 2.*int1)*mF1*MFin)))/(MassEx22 - 1.*MFin2)\n" ];
	 	 WriteString[sphenoTeX,"  OA2qVR= & "<> StringReplace["-((chargefactor coup3R (coup1L MassEx2 (-2 coup2R (1 - 2 I_1) mF1 + coup2L (1 + 2 I_2) MFin) + coup1R (coup2R (1 + 2 I_2) MassEx22 - 2 coup2L (1 - 2 I_1) mF1 MFin)))/(MassEx22 - MFin2))",SA`SPhenoTeXSub]<>" \\\\ \n" ];
	 	 WriteString[FKout,"  {OA2qVR,-((coup3R*(Finite*(coup1R*coup2R*MassEx22 - 2*coup1L*coup2R*MassEx2*mF1 + coup1L*coup2L*MassEx2*MFin - 2*coup1R*coup2L*mF1*MFin) + 4*mF1*(coup1L*coup2R*MassEx2 + coup1R*coup2L*MFin)*bb0[MassEx22, mF12, mV12] + 2*(coup1R*coup2R*MassEx22 + coup1L*coup2L*MassEx2*MFin)*bb1[MassEx22, mF12, mV12]))/(MassEx22 - MFin2))} " ];
]; 
];]; 



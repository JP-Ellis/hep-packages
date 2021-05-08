 
(* ::Section:: *)
(* FreeIndexFreeQ *)
(* ::Text:: *)
(*FreeIndexFreeQ[exp, {head1, head2, ...}]  returns True if the expression contains uncontracted indices with heads head1, head2, ... and False otherwise. As always in FeynCalc, Einstein summation convention is implicitly assumed. The function is optimized for large expressions, i.e. it is not so good as a criterion in e.g. Select..*)


(* ::Subsection:: *)
(* See also *)
(* ::Text:: *)
(*FCRenameDummyIndices, Contract, DummyIndexFreeQ.*)



(* ::Subsection:: *)
(* Examples *)



FCI[FV[p,\[Mu]] FV[q,\[Nu]]]

FreeIndexFreeQ[%,{LorentzIndex}]

FCI[FV[p,\[Mu]] FV[q,\[Mu]]]

FreeIndexFreeQ[%,{LorentzIndex}]

FCI[SUNT[a,b]]

FreeIndexFreeQ[%,{SUNIndex}]

FCI[SUNT[a,a]]

FreeIndexFreeQ[%,{SUNIndex}]

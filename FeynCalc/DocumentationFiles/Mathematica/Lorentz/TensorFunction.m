 
(* ::Section:: *)
(* TensorFunction *)
(* ::Text:: *)
(*TensorFunction[t, mu, nu, ...] transform into t[LorentzIndex[mu], LorentzIndex[nu], ...], i.e., it can be used as an unspecified tensoriell function t. A symmetric tensor can be obtained by TensorFunction[{t, "S"}, mu, nu, ...], and an antisymmteric one by TensorFunction[{t, "A"}, mu, nu, ...]..*)


(* ::Subsection:: *)
(* See also *)
(* ::Text:: *)
(*FCSymmetrize.*)



(* ::Subsection:: *)
(* Examples *)



TensorFunction[t,\[Mu],\[Nu],\[Tau]]

%//StandardForm

Contract[FV[p,\[Mu]] %]

%//StandardForm

TensorFunction[{f,"S"},\[Alpha],\[Beta]]

TensorFunction[{f,"S"},\[Beta],\[Alpha]]

%//StandardForm

Attributes[f]

ClearAttributes[f,Orderless]
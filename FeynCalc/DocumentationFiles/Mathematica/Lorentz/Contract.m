 
(* ::Section:: *)
(* Contract *)
(* ::Text:: *)
(*Contract[expr] contracts pairs of Lorentz indices of metric tensors, four-vectors and (depending on the optionEpsContract) of Levi-Civita tensors in expr. For the contraction of Dirac matrices with each other use DiracSimplify. Contract[exp1, exp2] contracts (exp1*exp2), where exp1 and exp2 may be larger products of sums of metric tensors and 4-vectors..*)


(* ::Subsection:: *)
(* See also *)
(* ::Text:: *)
(*Pair, CartesianPair, DiracSimplify, MomentumCombine.*)



(* ::Subsection:: *)
(* Examples *)



MT[\[Mu],\[Nu]] FV[p,\[Mu]]

Contract[%]

FV[p,\[Mu]]GA[\[Mu]]

Contract[%]

MT[\[Mu],\[Mu]]


(* ::Text:: *)
(*The default dimension for a metric tensor is 4.*)


Contract[%]


(* ::Text:: *)
(*A short way to enter D-dimensional metric tensors is given by MTD.*)


MTD[\[Mu],\[Nu]]  MTD[\[Mu],\[Nu]]

Contract[%]

FV[p,\[Mu]] FV[q,\[Mu]]

Contract[% ]

FV[p-q,\[Mu]] FV[a-b,\[Mu]]

Contract[%]

FVD[p-q,\[Nu]] FVD[a-b,\[Nu]]

Contract[%]

LC[\[Mu],\[Nu],\[Alpha],\[Sigma]] FV[p,\[Sigma]]

Contract[%]

LC[\[Mu],\[Nu],\[Alpha],\[Beta]] LC[\[Mu],\[Nu],\[Alpha],\[Sigma]] 

Contract[%]

LCD[\[Mu],\[Nu],\[Alpha],\[Beta]] LCD[\[Mu],\[Nu],\[Alpha],\[Sigma]]

Contract[%]//Factor2


(* ::Text:: *)
(*Contractions of Cartesian tensors are also possible. They can live in $3$, $D-1$ or $D-4$ dimensions.*)


KD[i,j]CV[p,i]

Contract[%]

CV[p,i]CGA[i]

Contract[%]

KD[i,i]

Contract[%]

KD[i,j]^2

Contract[%]

CV[p-q,j] CV[a-b,j]

Contract[%]

CLC[i,j,k] CV[p,k]

Contract[%]

CLC[i,j,k] CLC[i,j,l] 

Contract[%]

CLCD[i,j,k] CLCD[i,j,l] 

Contract[%]//Factor2

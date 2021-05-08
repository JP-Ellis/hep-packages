 
(* ::Section:: *)
(* FCGramMatrix *)
(* ::Text:: *)
(*FCGramMatrix[{p1, p2, ...}] creates Gram matrix from the given list of momenta..*)


(* ::Subsection:: *)
(* See also *)
(* ::Text:: *)
(*FCGramDeterminant.*)



(* ::Subsection:: *)
(* Examples *)



FCGramMatrix[{p1,p2}]

FCGramMatrix[{p1,p2,p3}]

FCGramMatrix[{p1,p2,p3},Head->{CartesianPair,CartesianMomentum},Dimension->D-1]

Det[%]

FCGramDeterminant[{p1,p2,p3},Head->{CartesianPair,CartesianMomentum},Dimension->D-1]

(* ::Package:: *)

(* ::Title:: *)
(* FeynRules 2  *)


(* ::Text:: *)
(*Authors : A. Alloul, N. Christensen, C. Degrnade, C. Duhr, B. Fuks 2013*)
(*    *)
(*    *)
(*Wiki-page for the FeynRules package:   http://feynrules.irmp.ucl.ac.be/*)
(**)
(*  *)


(* ::Section:: *)
(*Main call to the package*)


If[!ValueQ[$FeynRulesPath],
   $FeynRulesPath = DirectoryName[$InputFileName];
   Echo[$FeynRulesPath, "Using $FeynRulesPath = "];
]

If[!ValueQ[FR$Parallel],
   FR$Parallel = False;
   Echo[FR$Parallel, "Using FR$Parallel = "];
];


(* If the package is already loaded, then it will not be loaded again *)

If[FR$Loaded =!= True, 
	Get[ToFileName[$FeynRulesPath, "FeynRulesPackage.m"]];
	(*Parallelize - NC*)
	If[FR$Parallel===False,FR$Parallelize=False,FR$Parallelize=True];
	If[FR$Parallelize,
        If[ValueQ[FR$KernelNumber],
           LaunchKernels[FR$KernelNumber],
           LaunchKernels[];
           FR$KernelNumber = $KernelCount
           ];
		DistributeDefinitions[$FeynRulesPath];
		ParallelEvaluate[
			$Output={};
			SetDirectory[$FeynRulesPath];
			Get[ToFileName[$FeynRulesPath, "FeynRulesPackage.m"]];
			$Output={OutputStream["stdout",1]};
		];
	];
	(*End Parallelize - NC*)
	
,
	Print["Package already loaded..."]];

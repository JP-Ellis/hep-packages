
BeginPackage["WeinbergAngle`", {"SARAH`", "Parameters`"}];

ExpressWeinbergAngleInTermsOfGaugeCouplings::usage="";

Begin["`Private`"];

FindWeinbergAngleDef[] :=
    Module[{weinbergAngleDef},
           weinbergAngleDef = Cases[SARAH`ParameterDefinitions,
                                    {SARAH`Weinberg, {___, DependenceNum -> definition_, ___}} :> definition];
           If[Head[weinbergAngleDef] =!= List || weinbergAngleDef === {},
              Print["Error: Could not find definition of Weinberg angle ",
                    SARAH`Weinberg, " in SARAH`ParameterDefinitions"];
              Return[0];
             ];
           If[Length[weinbergAngleDef] > 1,
              Print["Warning: Weinberg angle ", SARAH`Weinberg,
                    " defined multiple times"];
             ];
           weinbergAngleDef = weinbergAngleDef[[1]];
           Return[weinbergAngleDef];
          ];

FindMassW[masses_List] :=
    FindMass[masses, SARAH`VectorW];

FindMassZ[masses_List] :=
    FindMass[masses, SARAH`VectorZ];

FindMass[masses_List, particle_] :=
    Module[{massExpr},
           massExpr = Cases[masses, TreeMasses`FSMassMatrix[{mass_}, particle, ___] :> mass];
           If[Head[massExpr] =!= List || massExpr === {},
              Print["Error: Could not find mass of ", particle,
                    " in masses list."];
              Return[0];
             ];
           Return[massExpr[[1]] /. SARAH`Weinberg[] -> SARAH`Weinberg];
          ];

ExpressWeinbergAngleInTermsOfGaugeCouplings[masses_List] :=
    Module[{eqs, reducedEq, solution, smValue},
           (* SM value of the Weinberg angle *)
           smValue = ArcSin[SARAH`hyperchargeCoupling / Sqrt[SARAH`hyperchargeCoupling^2 + SARAH`leftCoupling^2]] /.
                     Parameters`ApplyGUTNormalization[];
           (* Assumption: the masses contain GUT normalized gauge
              couplings, but the Weinberg angle does not (because we
              take it directly from SARAH`ParameterDefinitions, where
              no GUT normalization has been applied so far)*)
           eqs = {SARAH`Weinberg == FindWeinbergAngleDef[] /.
                                    Parameters`ApplyGUTNormalization[],
                  SARAH`Mass[SARAH`VectorW]^2 == FindMassW[masses],
                  SARAH`Mass[SARAH`VectorZ]^2 == FindMassZ[masses]
                 };
           reducedEq = Eliminate[eqs, {SARAH`Mass[SARAH`VectorW],
                                       SARAH`Mass[SARAH`VectorZ]}];
           solution = Solve[reducedEq, SARAH`Weinberg, Reals];
           If[Head[solution] =!= List || solution === {},
              Print["Error: could not solve the following equation for ",
                    SARAH`Weinberg, ": "];
              Print[reducedEq];
              Print["   I'll use the Standard Model definition for ",
                    SARAH`Weinberg];
              Return[smValue];
             ];
           solution = Simplify[#[[1,2]],
                               Assumptions ->
                               SARAH`Weinberg > 0 && Element[SARAH`Weinberg, Reals] &&
                               SARAH`hyperchargeCoupling > 0 && Element[SARAH`hyperchargeCoupling, Reals] &&
                               SARAH`leftCoupling > 0 && Element[SARAH`leftCoupling, Reals]]& /@ solution;
           solution = Select[solution, !NumericQ[#]&];
           If[solution === {},
              Print["Error: Unable to express the Weinberg angle ", SARAH`Weinberg,
                    " in terms of the gauge couplings"];
              Return[smValue];
             ];
           Sort[solution, ByteCount[#1] < ByteCount[#2]&][[1]]
          ];

End[];

EndPackage[];

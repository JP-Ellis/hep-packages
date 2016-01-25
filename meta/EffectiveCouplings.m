BeginPackage["EffectiveCouplings`", {"SARAH`", "CConversion`", "Parameters`", "SelfEnergies`", "TreeMasses`", "TextFormatting`", "Utils`", "Vertices`", "Observables`"}];

InitializeEffectiveCouplings::usage="";
GetNeededVerticesList::usage="";
CreateEffectiveCouplingsGetters::usage="";
CreateEffectiveCouplingsDefinitions::usage="";
CreateEffectiveCouplingsInit::usage="";
CreateEffectiveCouplingsCalculation::usage="";
CreateEffectiveCouplings::usage="";

Begin["`Private`"];

GetAllowedCouplingsForModel[] :=
    Module[{dim,
            valid = {FlexibleSUSYObservable`CpHiggsPhotonPhoton,
                     FlexibleSUSYObservable`CpHiggsGluonGluon,
                     FlexibleSUSYObservable`CpPseudoScalarPhotonPhoton,
                     FlexibleSUSYObservable`CpPseudoScalarGluonGluon}
           },
           If[FreeQ[TreeMasses`GetParticles[], SARAH`HiggsBoson],
              valid = DeleteCases[valid, a_ /; (a === FlexibleSUSYObservable`CpHiggsPhotonPhoton ||
                                                a === FlexibleSUSYObservable`CpHiggsGluonGluon)];
             ];
           If[FreeQ[TreeMasses`GetParticles[], SARAH`PseudoScalar],
              valid = DeleteCases[valid, a_ /; (a === FlexibleSUSYObservable`CpPseudoScalarPhotonPhoton ||
                                                a === FlexibleSUSYObservable`CpPseudoScalarGluonGluon)];
             ];
           valid
          ];

GetExternalStates[couplingSymbol_] :=
    Module[{particle, vectorBoson},
           Which[couplingSymbol === FlexibleSUSYObservable`CpHiggsPhotonPhoton,
                 particle = SARAH`HiggsBoson;
                 vectorBoson = SARAH`VectorP;,
                 couplingSymbol === FlexibleSUSYObservable`CpHiggsGluonGluon,
                 particle = SARAH`HiggsBoson;
                 vectorBoson = SARAH`VectorG;,
                 couplingSymbol === FlexibleSUSYObservable`CpPseudoScalarPhotonPhoton,
                 particle = SARAH`PseudoScalar;
                 vectorBoson = SARAH`VectorP;,
                 couplingSymbol === FlexibleSUSYObservable`CpPseudoScalarGluonGluon,
                 particle = SARAH`PseudoScalar;
                 vectorBoson = SARAH`VectorG;,
                 True, particle = Null; vectorBoson = Null
                ];
           {particle, vectorBoson}
          ];

(* @todo much of this is either identical or very similar to required functions
   for the GMuonMinus2 branch, and will be required again for decays, it might
   be a good idea to make them general (e.g. defined in Vertices?).             *)
AntiParticle[p_] := If[TreeMasses`IsScalar[p] || TreeMasses`IsVector[p],
                       Susyno`LieGroups`conj[p],
                       SARAH`bar[p]];

NonZeroVertexQ[vertex_] := MemberQ[vertex[[2 ;;]][[All, 1]], Except[0]];

(* @todo extend to multiple non-Abelian groups *)
IsColorOrLorentzIndex[index_] := StringMatchQ[ToString @ index, "ct" ~~ __] ||
                                 StringMatchQ[ToString @ index, "lt" ~~ __];
StripColorAndLorentzIndices[p_Symbol] := p;
StripColorAndLorentzIndices[SARAH`bar[p_]] := SARAH`bar[StripColorAndLorentzIndices[p]];
StripColorAndLorentzIndices[Susyno`LieGroups`conj[p_]] := Susyno`LieGroups`conj[StripColorAndLorentzIndices[p]];
StripColorAndLorentzIndices[p_] :=
    Module[{remainingIndices},
           remainingIndices = Select[p[[1]], (!IsColorOrLorentzIndex[#])&];
           If[Length[remainingIndices] === 0,
              Head[p],
              Head[p][remainingIndices]
             ]
          ];
SetAttributes[StripColorAndLorentzIndices, {Listable}];

(* @todo this is very slow because each possible vertex must be calculated,
   this can be improved by either pre-calculating all vertices or saving
   previous results (e.g. define along the lines of f[p] := f[p] = ...)    *)
GetTwoBodyDecays[particle_] :=
    Module[{i, j, allParticles, combinations, vertex, fields, couplings,
            candidate, found = {}, decays = {}},
           allParticles = Select[TreeMasses`GetParticles[], !TreeMasses`IsGhost[#]&];
           combinations = Table[Sort[{AntiParticle[particle],
                                      AntiParticle[allParticles[[i]]],
                                      allParticles[[j]]}],
                                {i, 1, Length[allParticles]}, {j, 1, Length[allParticles]}];
           combinations = DeleteDuplicates[Flatten[combinations, 1]];
           For[i = 1, i <= Length[combinations], i++,
               vertex = SARAH`Vertex[combinations[[i]], UseDependences -> True];
               If[NonZeroVertexQ[vertex],
                  fields = First[vertex];
                  coupling = Rest[vertex];
                  If[Length[coupling] > 1,
                     coupling = (SARAH`Cp @@ (StripColorAndLorentzIndices @ fields))[SARAH`PL];,
                     coupling = SARAH`Cp @@ (StripColorAndLorentzIndices @ fields);
                    ];
                  candidate = Append[DeleteCases[fields /. head_[{__}] :> head, p_ /; p === AntiParticle[particle], {0, Infinity}, 1], coupling];
                  If[FreeQ[found, C[candidate[[1]], candidate[[2]]]] &&
                     FreeQ[found, C[AntiParticle[candidate[[1]]], AntiParticle[candidate[[2]]]]] ||
                     AntiParticle[particle] =!= particle,
                     If[((!TreeMasses`IsMassless[candidate[[1]]] || !TreeMasses`IsVector[candidate[[1]]]) &&
                        (!TreeMasses`IsMassless[candidate[[2]]] || !TreeMasses`IsVector[candidate[[2]]])) ||
                        !FreeQ[SARAH`AllowDecaysMasslessVectors, SARAH`RE[particle]],
                        decays = Append[decays, candidate];
                        found = Append[found, C[candidate[[1]], candidate[[2]]]];
                       ];
                    ];
                 ];
              ];
           decays
          ];

GetElectricCharge[p_] := SARAH`getElectricCharge[p];

GetParticlesCouplingToVectorBoson[vector_] :=
    Module[{i, charge, allParticles, particles = {}},
           allParticles = Select[TreeMasses`GetParticles[], !TreeMasses`IsGhost[#]&];
           For[i = 1, i <= Length[allParticles], i++,
               If[vector === SARAH`VectorG,
                  (* @note could use defined functions in e.g. TreeMasses, plus check
                     for undefined group factors, but will do it this way for now
                     to ensure consistency with SARAH                                  *)
                  charge = SARAH`Vertex[{AntiParticle[allParticles[[i]]],
                                         allParticles[[i]], SARAH`VectorG},
                                        UseDependences -> True][[2,1]];
                  If[charge =!= 0,
                     particles = Append[particles, allParticles[[i]]];
                    ];,
                  charge = GetElectricCharge[allParticles[[i]]];
                  If[NumericQ[charge],
                     charge = {charge},
                     charge = Cases[SARAH`Vertex[{AntiParticle[allParticles[[i]]],
                                                  allParticles[[i]], SARAH`VectorP},
                                                 UseDependences -> True][[2,1]], _?NumberQ];
                    ];
                  If[charge =!= {} && AntiParticle[allParticles[[i]]] =!= allParticles[[i]] &&
                     charge =!= {0},
                     particles = Append[particles, allParticles[[i]]];
                    ];
                 ];
              ];
           particles
          ];

IsMasslessOrGoldstone[SARAH`bar[p_]] := IsMasslessOrGoldstone[p];
IsMasslessOrGoldstone[Susyno`LieGroups`conj[p_]] := IsMasslessOrGoldstone[p];
IsMasslessOrGoldstone[particle_] :=
    Module[{result},
           result = TreeMasses`IsMassless[particle] ||
                    (TreeMasses`IsGoldstone[particle] && TreeMasses`GetDimension[particle] == 1);
           result
          ];

InitializeEffectiveCouplings[] :=
    Module[{i, couplings, particle, vectorBoson,
            allParticles = {}, allVectorBosons = {},
            twoBodyDecays, vectorBosonInteractions,
            neededTwoBodyDecays, neededVectorBosonInteractions,
            neededCoups, result = {}},
           couplings = GetAllowedCouplingsForModel[];
           {allParticles, allVectorBosons} = DeleteDuplicates /@ {(#[[1]])& /@ (GetExternalStates[#]& /@ couplings),
                                                                  (#[[2]])& /@ (GetExternalStates[#]& /@ couplings)};
           twoBodyDecays = {#, GetTwoBodyDecays[#]}& /@ allParticles;
           vectorBosonInteractions = {#, GetParticlesCouplingToVectorBoson[#]}& /@ allVectorBosons;
           For[i = 1, i <= Length[couplings], i++,
                {particle, vectorBoson} = GetExternalStates[couplings[[i]]];
                neededTwoBodyDecays = First[Select[twoBodyDecays, (#[[1]] === particle)&]];
                neededVectorBosonInteractions = First[Select[vectorBosonInteractions, (#[[1]] === vectorBoson)&]];
                neededCoups = Select[neededTwoBodyDecays[[2]],
                                    (MemberQ[neededVectorBosonInteractions[[2]], #[[1]]] ||
                                     MemberQ[neededVectorBosonInteractions[[2]], #[[2]]])&];
                (* only keep vertices of the form pD -> p AntiParticle[p] *)
                neededCoups = Cases[neededCoups, {p1_, p2_, _} /; p1 === AntiParticle[p2]];
                (* filter out massless states and Goldstones *)
                neededCoups = Select[neededCoups, (!IsMasslessOrGoldstone[#[[1]]] && !IsMasslessOrGoldstone[#[[2]]])&];
                result = Append[result, {couplings[[i]], #[[3]]& /@ neededCoups}];
              ];
           result
          ];

GetNeededVerticesList[couplings_List] :=
    {Null[Null, Join[(#[[2]])& /@ couplings]]};

CreateEffectiveCouplingName[pIn_, pOut_] :=
    "eff_Cp" <> CConversion`ToValidCSymbolString[pIn] <> CConversion`ToValidCSymbolString[pOut] <> CConversion`ToValidCSymbolString[pOut];

CreateEffectiveCouplingsGetters[couplings_List] :=
    Module[{i, couplingSymbols, type, particle,
            vectorBoson, dim, couplingName, getters = ""},
           couplingSymbols = #[[1]]& /@ couplings;
           type = CConversion`CreateCType[CConversion`ScalarType[CConversion`complexScalarCType]];
           For[i = 1, i <= Length[couplingSymbols], i++,
               {particle, vectorBoson} = GetExternalStates[couplingSymbols[[i]]];
               dim = TreeMasses`GetDimension[particle];
               couplingName = CreateEffectiveCouplingName[particle, vectorBoson];
               getters = getters <> type <> " get_" <> couplingName;
               If[dim == 1,
                  getters = getters <> "() const { return " <> couplingName <> "; }\n";,
                  getters = getters <> "(unsigned gO1) const { return " <> couplingName <> "(gO1); }\n";
                 ];
              ];
           getters
          ];

CreateEffectiveCouplingsDefinitions[couplings_List] :=
    Module[{i, couplingSymbols, dim, type, particle, vectorBoson,
            couplingName, defs = ""},
           couplingSymbols = #[[1]]& /@ couplings;
           For[i = 1, i <= Length[couplingSymbols], i++,
               {particle, vectorBoson} = GetExternalStates[couplingSymbols[[i]]];
               couplingName = CreateEffectiveCouplingName[particle, vectorBoson];
               dim = TreeMasses`GetDimension[particle];
               If[dim == 1,
                  type = CConversion`CreateCType[CConversion`ScalarType[CConversion`complexScalarCType]];,
                  type = CConversion`CreateCType[CConversion`ArrayType[CConversion`complexScalarCType, dim]];
                 ];
               defs = defs <> type <> " " <> couplingName <> ";\n";
              ];
           defs
          ];

CreateEffectiveCouplingsInit[couplings_List] :=
    Module[{i, couplingSymbols, particle,
            vectorBoson, couplingName, dim, type, init = ""},
           couplingSymbols = #[[1]]& /@ couplings;
           For[i = 1, i <= Length[couplingSymbols], i++,
               {particle, vectorBoson} = GetExternalStates[couplingSymbols[[i]]];
               couplingName = CreateEffectiveCouplingName[particle, vectorBoson];
               dim = TreeMasses`GetDimension[particle];
               If[dim == 1,
                  type = CConversion`ScalarType[CConversion`complexScalarCType];,
                  type = CConversion`ArrayType[CConversion`complexScalarCType, dim];
                 ];
               init = init <> ", " <> CConversion`CreateDefaultConstructor[couplingName, type];
              ];
           init
          ];

RunToDecayingParticleScale[particle_, idx_:""] :=
    Module[{savedMass, body, result = ""},
           (* running is only done in SUSY models *)
           If[SARAH`SupersymmetricModel,
              savedMass = CConversion`RValueToCFormString[FlexibleSUSY`M[particle]];
              If[idx != "",
                 savedMass = savedMass <> "(" <> idx <> ")";
                ];
              body = "run_to(" <> savedMass <> ");\ncalculate_DRbar_masses();\n";
              result = "if (rg_improve && scale != " <> savedMass <> ") {\n"
                       <> TextFormatting`IndentText[body] <> "}\n"
            ];
           result
          ];

CallEffectiveCouplingCalculation[couplingSymbol_, idx_:""] :=
    Module[{particle, vectorBoson, couplingName, call = ""},
           {particle, vectorBoson} = GetExternalStates[couplingSymbol];
           couplingName = CreateEffectiveCouplingName[particle, vectorBoson];
           call = "calculate_" <> couplingName;
           If[idx != "",
              call = call <> "(" <> idx <> ");";,
              call = call <> "();";
             ];
           call
          ];

CreateEffectiveCouplingsCalculation[couplings_List] :=
    Module[{i, couplingSymbols, particle, couplingsForParticles = {},
            pos, couplingList, mass, savedMass, dim, body, result = ""},
           couplingSymbols = #[[1]]& /@ couplings;
           For[i = 1, i <= Length[couplingSymbols], i++,
               particle = GetExternalStates[couplingSymbols[[i]]][[1]];
               If[FreeQ[couplingsForParticles, particle],
                  couplingsForParticles = Append[couplingsForParticles, {particle, {couplingSymbols[[i]]}}];,
                  pos = Position[couplingsForParticles, {particle, _List}][[1,1]];
                  couplingList = couplingsForParticles[[pos]] /. {p_, coups_} :> {p, Append[coups, couplingSymbols[[i]]]};
                  couplingsForParticles = ReplacePart[couplingsForParticles, pos -> couplingList];
                 ];
              ];
           If[SARAH`SupersymmetricModel,
              result = result <> "const double scale = get_scale();\nconst Eigen::ArrayXd saved_parameters(get());\n";
             ];
           For[i = 1, i <= Length[couplingsForParticles], i++,
               particle = couplingsForParticles[[i,1]];
               If[SARAH`SupersymmetricModel,
                  mass = ToValidCSymbolString[FlexibleSUSY`M[particle]];
                  savedMass = "const auto " <> mass <> " = PHYSICAL(" <> mass <> ");\n";
                  result = result <> savedMass;
                 ];
               dim = TreeMasses`GetDimension[particle];
               If[dim == 1,
                  result = result <> RunToDecayingParticleScale[particle];
                  result = result <> Utils`StringJoinWithSeparator[CallEffectiveCouplingCalculation[#]& /@ couplingsForParticles[[i,2]], "\n"] <> "\n\n";
                  ,
                  result = result <> "for (unsigned gO1 = 0; gO1 < " <> ToString[dim] <> "; ++gO1) {\n";
                  body = RunToDecayingParticleScale[particle, "gO1"];
                  body = body <> Utils`StringJoinWithSeparator[CallEffectiveCouplingCalculation[#, "gO1"]& /@ couplingsForParticles[[i,2]], "\n"] <> "\n";
                  result = result <> TextFormatting`IndentText[body] <> "}\n\n";
                 ];
              ];
           If[SARAH`SupersymmetricModel,
              result = result <> "set_scale(scale);\nset(saved_parameters);\n";
             ];
           result
          ];

CreateEffectiveCouplingPrototype[coupling_] :=
    Module[{couplingSymbol = coupling[[1]], particle, vectorBoson,
            dim, name, result = ""},
           {particle, vectorBoson} = GetExternalStates[couplingSymbol];
           If[particle =!= Null && vectorBoson =!= Null,
              dim = TreeMasses`GetDimension[particle];
              name = CreateEffectiveCouplingName[particle, vectorBoson];
              result = "void calculate_" <> name <> If[dim == 1, "();\n", "(unsigned gO1);\n"];
             ];
           result
          ];

GetQCDCorrections[particle_, vectorBoson_] :=
    Module[{scalarQCD, fermionQCD, parameters = {}, result = ""},
           If[particle === SARAH`HiggsBoson,
              Which[vectorBoson === SARAH`VectorP,
                    scalarQCD = 1 + 2 SARAH`strongCoupling^2 / (3 Pi^2);
                    fermionQCD = 1 - SARAH`strongCoupling^2 / (4 Pi^2);
                    result = "const double qcd_scalar = " <> CConversion`RValueToCFormString[scalarQCD]
                             <> ";\nconst double qcd_fermion = " <> CConversion`RValueToCFormString[fermionQCD]
                             <> ";\n\n";,
                    vectorBoson === SARAH`VectorG,
                    scalarQCD = 1 + 2 SARAH`strongCoupling^2 / (3 Pi^2);
                    result = "const double qcd_scalar = " <> CConversion`RValueToCFormString[scalarQCD]
                             <> ";\nconst double qcd_fermion = qcd_scalar;\n\n",
                    True,
                    result =""
                   ];
               parameters = {SARAH`strongCoupling};
             ];
           {result, parameters}
          ];

GetEffectiveVEV[] :=
    Module[{vev, parameters = {}, result = ""},
           vev = Simplify[2 Sqrt[-SARAH`Vertex[{SARAH`VectorW, Susyno`LieGroups`conj[SARAH`VectorW]}][[2,1]]
                        / SARAH`leftCoupling^2] /. SARAH`sum[a_,b_,c_,d_] :> Sum[d,{a,b,c}]];
           parameters = Parameters`FindAllParameters[vev];
           result = "const auto vev = " <> CConversion`RValueToCFormString[vev] <> ";\n";
           {result, parameters}
          ];

GetMultiplicity[vectorBoson_, internal_] := SARAH`ChargeFactor[vectorBoson, internal, internal];

GetParticleGenerationIndex[particle_, coupling_] :=
    Module[{dim, indexList, result = {}},
           dim = TreeMasses`GetDimension[particle];
           If[dim != 1,
              indexList = Flatten[Cases[Vertices`GetParticleList[coupling],
                                  p_[a_List] /; p === particle :> a, {0, Infinity}]];
              result = Select[indexList, StringMatchQ[ToString[#], "gt" ~~ __] &];
              If[Length[result] > 1,
                 result = {result[[1]]};
                ];
             ];
           result
          ];

(* @todo these are basically identical to those in SelfEnergies,
   it would be better to reuse the definitions there if possible  *)
GetParticleIndicesInCoupling[SARAH`Cp[a__]] := Flatten[Cases[{a}, List[__], Infinity]];

GetParticleIndicesInCoupling[SARAH`Cp[a__][_]] := GetParticleIndicesInCoupling[SARAH`Cp[a]];

CreateCouplingSymbol[coupling_] :=
    Module[{symbol, indices},
           indices = GetParticleIndicesInCoupling[coupling];
           symbol = ToValidCSymbol[coupling /. a_[List[__]] :> a];
           symbol[Sequence @@ indices]
          ];

HasColorCharge[particle_] :=
    Module[{dynkin},
           dynkin = SA`Dynkin[particle,Position[SARAH`Gauge, SARAH`strongCoupling][[1,1]]];
           If[!NumericQ[dynkin], dynkin = 0];
           dynkin == 1/2
          ];

CreateCouplingContribution[particle_, vectorBoson_, coupling_] :=
    Module[{i, internal, particleIndex, indices, dim, factor, qcdfactor,
            mass, massStr, couplingSymbol, couplingName,
            scaleFunction, body = "", result = "", parameters = {}},
           internal = DeleteCases[Vertices`GetParticleList[coupling] /. field_[{__}] :> field,
                                  p_ /; p === particle, 1];
           internal = First[internal /. {SARAH`bar[p_] :> p, Susyno`LieGroups`conj[p_] :> p}];
           dim = TreeMasses`GetDimension[internal];
           mass = FlexibleSUSY`M[internal];
           massStr = CConversion`ToValidCSymbolString[mass];
           If[dim != 1,
              massStr = massStr <> "(gI1)";
             ];
           parameters = Append[parameters, mass];
           Which[TreeMasses`IsScalar[internal],
                 factor = 1/2;
                 If[particle === SARAH`HiggsBoson,
                    scaleFunction = "AS0";
                    If[HasColorCharge[internal],
                       qcdfactor = "qcd_scalar";,
                       qcdfactor = "";
                      ];,
                    Return[{"",{}}];
                   ];,
                 TreeMasses`IsVector[internal],
                 factor = -1/2;
                 If[particle === SARAH`HiggsBoson,
                    scaleFunction = "AS1";
                    qcdfactor = "";,
                    Return[{"",{}}];
                   ];,
                 TreeMasses`IsFermion[internal],
                 factor = 1;
                 If[particle === SARAH`HiggsBoson,
                    scaleFunction = "AS12";
                    If[HasColorCharge[internal],
                       qcdfactor = "qcd_fermion";,
                       qcdfactor = "";
                      ];,
                    scaleFunction = "AP12";
                    qcdfactor = "";
                   ];
                ];
           If[vectorBoson === SARAH`VectorP,
              factor = factor * GetElectricCharge[internal]^2 GetMultiplicity[vectorBoson, internal];
             ];
           indices = GetParticleIndicesInCoupling[coupling];
           particleIndex = GetParticleGenerationIndex[particle, coupling];
           indices = Replace[indices, p_ /; !MemberQ[particleIndex, p] -> SARAH`gI1, 1];
           indices = Replace[indices, p_ /; MemberQ[particleIndex, p] -> SARAH`gO1, 1];
           couplingSymbol = CConversion`ToValidCSymbol[coupling /. a_[List[__]] :> a];
           couplingSymbol = couplingSymbol[Sequence @@ indices];
           couplingName = CConversion`ToValidCSymbolString[CConversion`GetHead[couplingSymbol]];
           couplingName = couplingName <> "(";
           For[i = 1, i <= Length[indices], i++,
               If[i > 1, couplingName = couplingName <> ", ";];
               If[!IntegerQ[indices[[i]]],
                  couplingName = couplingName <> CConversion`ToValidCSymbolString[indices[[i]]];
                 ];
              ];
           couplingName = couplingName <> ")";
           body = "result += " <> If[factor != 1, CConversion`RValueToCFormString[factor] <> " * ", ""]
                    <> If[qcdfactor != "", qcdfactor <> " * ", ""] <> couplingName
                    <> " * vev * " <> scaleFunction <> "(decay_scale / Sqr(" <> massStr <> ")) / "
                    <> massStr <> ";";
           If[particle == SARAH`HiggsBoson && vectorBoson =!= SARAH`VectorG &&
              TreeMasses`IsFermion[internal] && HasColorCharge[internal],
              body = "if (" <> massStr <> " > decay_mass) {\n"
                     <> TextFormatting`IndentText[body] <> "\n} else {\n";
              body = body
                     <> TextFormatting`IndentText["result += "
                                                  <> If[factor != 1, CConversion`RValueToCFormString[factor] <> " * ", ""]
                                                  <> couplingName <> "* vev * " <> scaleFunction
                                                  <> "(decay_scale / Sqr(" <> massStr <> ")) / " <> massStr <> ";"];
              body = body <> "\n}";
             ];
           If[dim == 1,
              result = body <> "\n";,
              result = "for (unsigned gI1 = 0; gI1 < " <> ToString[dim - 1] <> "; ++gI1) {\n";
              result = result <> TextFormatting`IndentText[body] <> "\n}\n";
             ];
           {result, parameters}
          ];

CreateEffectiveCouplingFunction[coupling_] :=
    Module[{i, couplingSymbol = coupling[[1]], neededCouplings = coupling[[2]],
            particle, vectorBoson, dim, type, name, savedMass, mass,
            parameters = {}, currentLine, body = "", result = ""},
           {particle, vectorBoson} = GetExternalStates[couplingSymbol];
           If[particle =!= Null && vectorBoson =!= Null,
              name = CreateEffectiveCouplingName[particle, vectorBoson];
              dim = TreeMasses`GetDimension[particle];
              result = result <> "void " <> FlexibleSUSY`FSModelName
                       <> "_effective_couplings::calculate_" <> name <> "(";
              If[dim == 1,
                 result = result <> ")\n{\n";,
                 result = result <> "unsigned gO1)\n{\n";
                ];

              mass = ToValidCSymbolString[FlexibleSUSY`M[particle]];
              savedMass = "const auto decay_mass = PHYSICAL(" <> mass <> ")";
              If[dim == 1,
                 savedMass = savedMass <> ";\n";,
                 savedMass = savedMass <> "(gO1);\n";
                ];
              body = body <> savedMass;
              body = body <> "const auto decay_scale = 0.25 * Sqr(decay_mass);\n\n";
              {currentLine, parameters} = {#[[1]], Join[parameters, #[[2]]]}& @ (GetQCDCorrections[particle, vectorBoson]);
              body = body <> currentLine;
              {currentLine, parameters} = {#[[1]], Join[parameters, #[[2]]]}& @ (GetEffectiveVEV[]);
              body = body <> currentLine <> "\n";
              body = body <> CConversion`CreateDefaultDefinition["result", CConversion`ScalarType[CConversion`complexScalarCType]] <> ";\n";

              For[i = 1, i <= Length[neededCouplings], i++,
                  {currentLine, parameters} = {#[[1]], Join[parameters, #[[2]]]}& @ (CreateCouplingContribution[particle, vectorBoson, neededCouplings[[i]]]);
                  body = body <> currentLine;
                 ];

              If[vectorBoson === SARAH`VectorG,
                 body = body <> "result *= std::complex<double>(0.75,0.);\n";
                ];

              body = Parameters`CreateLocalConstRefs[DeleteDuplicates[parameters]] <> body <> "\n";

              If[vectorBoson === SARAH`VectorP,
                 body = body <> "result *= "
                        <> CConversion`RValueToCFormString[1 / (2^(3/4) Pi)]
                        <> " * qedqcd.displayAlpha(softsusy::ALPHA) * Sqrt(qedqcd.displayFermiConstant());\n\n";,
                 body = body <> "result *= "
                        <> CConversion`RValueToCFormString[2^(1/4) / (3 Pi)]
                        <> " * qedqcd.displayAlpha(softsusy::ALPHAS) * Sqrt(qedqcd.displayFermiConstant());\n\n";
                ];

              body = body <> name <> If[dim != 1, "(gO1) = ", " = "] <> "result;\n";

              result = result <> TextFormatting`IndentText[TextFormatting`WrapLines[body]] <> "\n}\n";
             ];
           result
          ];

CreateEffectiveCouplingsPrototypes[couplings_List] :=
    Module[{result = ""},
           (result = result <> CreateEffectiveCouplingPrototype[#])& /@ couplings;
           result
          ];

CreateEffectiveCouplingsFunctions[couplings_List] :=
    Module[{result = ""},
           (result = result <> CreateEffectiveCouplingFunction[#] <> "\n")& /@ couplings;
           result
          ];

CreateEffectiveCouplings[couplings_List] :=
    Module[{prototypes = "", functions = ""},
           prototypes = prototypes
                        <> CreateEffectiveCouplingsPrototypes[couplings];
           functions = functions
                       <> CreateEffectiveCouplingsFunctions[couplings];
           {prototypes, functions}
          ];

End[];

EndPackage[];

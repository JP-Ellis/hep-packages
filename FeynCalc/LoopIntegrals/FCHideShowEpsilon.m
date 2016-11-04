(* ::Package:: *)

(* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ *)

(* :Title: FCHideShowEpsilon												*)

(*
	This software is covered by the GNU General Public License 3.
	Copyright (C) 1990-2016 Rolf Mertig
	Copyright (C) 1997-2016 Frederik Orellana
	Copyright (C) 2014-2016 Vladyslav Shtabovenko
*)

(* :Summary:	Substitutes 1/Epsilon - EulerGamma + Log[4Pi] with
				SMP["Delta"] or vice versa									*)

(* ------------------------------------------------------------------------ *)

FCHideEpsilon::usage =
"FCHideEpsilon[expr] substitutes 1/Epsilon - EulerGamma + Log[4Pi] with \
SMP[\"Delta\"]";

FCShowEpsilon::usage =
"FCShowEpsilon[expr] substitutes SMP[\"Delta\"] with 1/Epsilon - \
EulerGamma + Log[4Pi] with";

FCHideEpsilon::failmsg =
"Error! FCHideEpsilon has encountered a fatal problem and must abort the computation. \
The problem reads: `1`";

FCShowEpsilon::failmsg =
"Error! FCShowEpsilon has encountered a fatal problem and must abort the computation. \
The problem reads: `1`";

(* ------------------------------------------------------------------------ *)

Begin["`Package`"]
End[]

Begin["`FCHideShowEpsilon`Private`"]

Options[FCHideEpsilon] = {
	Factoring -> Factor,
	Collecting -> True,
	D -> 4 - 2 Epsilon
};

Options[FCShowEpsilon] = {
	D -> 4 - 2 Epsilon
};

FCHideEpsilon[expr_, OptionsPattern[]] :=
	Block[{tmp,wrap,factoring,pref, dVal},

		factoring = OptionValue[Factoring];
		dVal = OptionValue[D];

		tmp = Collect2[expr,{Epsilon,EpsilonUV,EpsilonIR},Factoring->factoring];

		Which[
			dVal === 4 - 2 Epsilon,
				pref = 1,
			dVal === 4 -  Epsilon,
				pref = 2,
			True,
				Message[FCHideEpsilon::failmsg,"Unknown choice for D"];
				Abort[]
		];



		tmp = tmp/. {	1/Epsilon -> wrap[pref/Epsilon]/pref,
						1/EpsilonUV -> wrap[pref/EpsilonUV]/pref,
						1/EpsilonIR -> wrap[pref/EpsilonIR]/pref
		};

		tmp = tmp /. { 	wrap[pref/Epsilon] -> SMP["Delta"] + EulerGamma - Log[4Pi],
						wrap[pref/EpsilonUV] -> SMP["Delta_UV"] + EulerGamma - Log[4Pi],
						wrap[pref/EpsilonIR] -> SMP["Delta_IR"] + EulerGamma - Log[4Pi]
		};

		If[	OptionValue[Collecting],
			tmp = Collect2[tmp,{SMP["Delta"],SMP["Delta_UV"],SMP["Delta_IR"]},Factoring->factoring]
		];

		tmp

	];

FCShowEpsilon[expr_, OptionsPattern[]] :=
	Block[{tmp,pref, dVal},

		dVal = OptionValue[D];

		Which[
			dVal === 4 - 2 Epsilon,
				pref = 1,
			dVal === 4 -  Epsilon,
				pref = 2,
			True,
				Message[FCShowEpsilon::failmsg,"Unknown choice for D"];
				Abort[]
		];

		tmp = expr/. { SMP["Delta"] -> pref/Epsilon - EulerGamma + Log[4Pi],
					SMP["DeltaUV"] -> pref/EpsilonUV - EulerGamma + Log[4Pi],
					SMP["DeltaIR"] -> pref/EpsilonIR - EulerGamma + Log[4Pi]
		};

		tmp

	];

FCPrint[1,"FCHideShowEpsilon.m loaded."];
End[]

(* ::Package:: *)

(* Mathematica Init File *)

Block[{result},
result={};
AppendTo[result,Row[{Style["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",{GrayLevel[0.5]}],Hyperlink[Mouseover[Style["Susyno",{GrayLevel[0.5]}],Style["Susyno",{Darker[Blue,0.5],Bold}]],"http://renatofonseca.net/susyno.php"],Style[" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",{GrayLevel[0.5]}]}]];
AppendTo[result,Row[{Style["Version: 3.5; Author: Renato Fonseca.\nFor help, use the built-in ",{GrayLevel[0.5]}],Hyperlink["Susyno Tutorial","paclet:Susyno/tutorial/SusynoTutorial"],Style[" and associated documentation pages.",{GrayLevel[0.5]}]}]];
AppendTo[result,Row[{Style["A tutorial exclusively dedicated to the group theory functionalities of the program can be found ",{GrayLevel[0.5]}],Style[Hyperlink["here","http://renatofonseca.net/susyno/group_theory_tutorial.php"],{GrayLevel[0.5]}],Style[".",{GrayLevel[0.5]}]}]];
AppendTo[result,Style["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",{GrayLevel[0.5]}]];

Print[Row[result,"\n",BaseStyle->(FontFamily->"Consolas")]];
];


ClearAll["Susyno`LieGroups`*"];
ClearAll["Susyno`SusyRGEs`*"];
(* ClearAll["Susyno`Susyno`*"]; *)
(* ClearAll["Susyno`SSB`*"]; *)
ClearAll["Susyno`IO`*"];
ClearAll["Susyno`ModelBuilding`*"];
ClearAll["Susyno`Models`"];
ClearAll["Susyno`SimplifyEinsteinNotation`"];
ClearAll["Susyno`SymmetryBreaking`*"];

Get["Susyno`LieGroups`"];
Get["Susyno`ModelBuilding`"];
(* Get["Susyno`SSB`"]; *)
(* Get["Susyno`Susyno`"]; *)
Get["Susyno`SusyRGEs`"];
Get["Susyno`Models`"];
Get["Susyno`IO`"];
Get["Susyno`SimplifyEinsteinNotation`"];
Get["Susyno`SymmetryBreaking`"];

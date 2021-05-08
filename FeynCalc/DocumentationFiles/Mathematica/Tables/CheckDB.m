 
(* ::Section:: *)
(* CheckDB *)
(* ::Text:: *)
(*CheckDB[exp, fil] saves [with Put] or retrieves [with Get] exp from a file fil. It checks if the setting of the option Directory is a valid directory name and if fil is a valid file name and does exist. If it does, Get[fil] is executed. If fil does not exist, exp gets evaluated and saved to  fil. Saving and evaluating can be further controlled with the options ForceSave and NoSave. If the option Check is set to False  the return value is what is evaluated [see above]. If Check is set to True the return value is True or False depending on whether the evaluation of exp agrees with what is loaded from fil or fil does not exist.  Default value of Check : False.If fil ends with ".Gen" or ".Mod", the   setting of Directory is ignored and fil is  saved in the "CouplingVectors"  subdirectory of "Phi". If fil ends with  ".Fac", the setting of Directory is  ignored and fil is saved in the "Factors" subdirectory of "Phi". If fil is a file   name with full path, the setting of  Directory is also ignored.Attributes[CheckDB].*)


(* ::Subsection:: *)
(* See also *)
(* ::Text:: *)
(*The first time the Table function is evaluated and the result saved into the test.s file.*)



(* ::Subsection:: *)
(* Examples *)



CheckDB[Table[WriteString["stdout","test "];i,{i,2}],"test.s"]
test test 


(* ::Text:: *)
(*Executing the same a second time will just load the result from test.s and not evaluate the Table function.*)


CheckDB[Table[WriteString["stdout","test "];i,{i,2}],"test.s"]


(* ::Text:: *)
(*This shows the actual saved value of test.s.*)


Import[ToFileName[Directory/.Options[CheckDB],"test.s"],"Text"]

DeleteFile[ToFileName[Directory/.Options[CheckDB],"test.s"]]
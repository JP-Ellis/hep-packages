 
(* ::Section:: *)
(* FCFeynmanPrepare *)
(* ::Text:: *)
(*FCFeynmanPrepare[int, {q1, q2, ...}] ] is an auxiliary function that returns all necessary building for writing down a Feynman parametrization of the given tensor or scalar multi-loop integral.The integral int can be Lorentzian or Cartesian. The output of the function is a list given by {U,F, pows, M, Q, J, N, r}, where U and F are the Symanzik polynomials, with U = det M, while pows shows the powers of the occurring propagators. The vector Q and the function J are the usual quantities appearing in the definition of the F polynomial. If the integral has free indices, then N encodes its tensor structure, while r gives its tensor rank. For scalar integrals N is always 1 and r is 0. In N the F-polynomial is not substituted but left as FCGV["F"]To ensure a certain correspondence between propagators and Feynman parameters, it is also possible to enter the integral as a list of propagators, e.g. FCFeynmanPrepare[{FAD[{q,m1}],FAD[{q-p,m2}],SPD[p,q]},{q}]. In this case the tensor part of the integral should be the very last element of the list.The definitions of M, Q, J and N follow Eq. 4.17 from the PhD Thesis of Stefan Jahn (Jahn:2020tpj, http://mediatum.ub.tum.de/?id=1524691) and arXiv:1010.1667.The algorithm for deriving the UF-parametrization of a loop integral was adopted from the UF generator available in multiple codes of Alexander Smirnov, such as FIESTA (arXiv:1511.03614) and FIRE (arXiv:1901.07808). The code UF.m was also mentioned in the book "Analytic Tools for Feynman Integrals" by Vladimir Smirnov, Chapter 2.3.*)


(* ::Subsection:: *)
(* Examples *)
FCFeynmanPrepare[SPD[q1,p1]FAD[{q1,m1},{q1-p1+p2,m2}],{q1},Names->x]

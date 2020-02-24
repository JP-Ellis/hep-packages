* defs.h
* internal definitions for the LoopTools routines
* this file is part of LoopTools
* last modified 28 Feb 14 th

#ifdef COMPLEXPARA

#define XAget AgetC
#define XAput AputC
#define XAputnocache AputnocacheC
#define XA0i A0iC
#define XA0 A0C
#define XA00 A00C
#define XAcoeff AcoeffC
#define XBpara BparaC
#define XBget BgetC
#define XBput BputC
#define XBputnocache BputnocacheC
#define XB0i B0iC
#define XB0 B0C
#define XB1 B1C
#define XB00 B00C
#define XB11 B11C
#define XB001 B001C
#define XB111 B111C
#define XDB0 DB0C
#define XDB1 DB1C
#define XDB00 DB00C
#define XDB11 DB11C
#define XDB001 DB001C
#define XB0000 B0000C
#define XB0011 B0011C
#define XB1111 B1111C
#define XBcoeff BcoeffC
#define XBcoeffFF BcoeffFFC
#define XC0func C0funcC
#define XCpara CparaC
#define XCget CgetC
#define XCput CputC
#define XC0nocache C0nocacheC
#define XC0i C0iC
#define XC0 C0C
#define XCcoefx CcoefxC
#define XCcoeff CcoeffC
#define XD0func D0funcC
#define XDpara DparaC
#define XDget DgetC
#define XDput DputC
#define XD0nocache D0nocacheC
#define XD0i D0iC
#define XD0 D0C
#define XDcoefx DcoefxC
#define XDcoeff DcoeffC
#define XE0func E0funcC
#define XEpara EparaC
#define XEget EgetC
#define XEput EputC
#define XE0nocache E0nocacheC
#define XE0i E0iC
#define XE0 E0C
#define XEcoefx EcoefxC
#define XEcoeff EcoeffC
#define XEcoeffa EcoeffaC
#define XEcoeffb EcoeffbC
#define XEcheck EcheckC
#define XInvGramE InvGramEC
#define XSolve SolveC
#define XEigen EigenC
#define XDecomp DecompC
#define XDet DetmC
#define XInverse InverseC
#define XDumpPara DumpParaC
#define XDumpCoeff DumpCoeffC
#define XLi2 Li2C
#define XLi2sub li2csub
#define XLi2omx Li2omxC
#define XLi2omxsub li2omxcsub
#define Xfpij2 cfpij2
#define Xffa0 ffca0
#define Xffb0 ffcb0
#define Xffb1 ffcb1
#define Xffb2p ffcb2p
#define Xffdb0 ffcdb0

#define RC 2
#define DVAR ComplexType
#define QVAR ComplexType
#define QREAL RealType
#define QPREC(x) x
#define QCC(x) Conjugate(x)
#define QRE(x) Re(x)

#else

#define XAget Aget
#define XAput Aput
#define XAputnocache Aputnocache
#define XA0i A0i
#define XA0 A0
#define XA00 A00
#define XAcoeff Acoeff
#define XBpara Bpara
#define XBget Bget
#define XBput Bput
#define XBputnocache Bputnocache
#define XB0i B0i
#define XB0 B0
#define XB1 B1
#define XB00 B00
#define XB11 B11
#define XB001 B001
#define XB111 B111
#define XDB0 DB0
#define XDB1 DB1
#define XDB00 DB00
#define XDB11 DB11
#define XDB001 DB001
#define XB0000 B0000
#define XB0011 B0011
#define XB1111 B1111
#define XBcoeff Bcoeff
#define XBcoeffFF BcoeffFF
#define XC0func C0func
#define XCpara Cpara
#define XCget Cget
#define XCput Cput
#define XC0nocache C0nocache
#define XC0i C0i
#define XC0 C0
#define XCcoefx Ccoefx
#define XCcoeff Ccoeff
#define XD0func D0func
#define XDpara Dpara
#define XDget Dget
#define XDput Dput
#define XD0nocache D0nocache
#define XD0i D0i
#define XD0 D0
#define XDcoefx Dcoefx
#define XDcoeff Dcoeff
#define XE0func E0func
#define XEpara Epara
#define XEget Eget
#define XEput Eput
#define XE0nocache E0nocache
#define XE0i E0i
#define XE0 E0
#define XEcoefx Ecoefx
#define XEcoeff Ecoeff
#define XEcoeffa Ecoeffa
#define XEcoeffb Ecoeffb
#define XEcheck Echeck
#define XInvGramE InvGramE
#define XSolve Solve
#define XEigen Eigen
#define XDecomp Decomp
#define XDet Detm
#define XInverse Inverse
#define XDumpPara DumpPara
#define XDumpCoeff DumpCoeff
#define XLi2 Li2
#define XLi2sub li2sub
#define XLi2omx Li2omx
#define XLi2omxsub li2omxsub
#define Xfpij2 fpij2
#define Xffa0 ffxa0
#define Xffb0 ffxb0
#define Xffb1 ffxb1
#define Xffb2p ffxb2p
#define Xffdb0 ffxdb0

#define RC 1
#define DVAR RealType
#if QUAD
#define QVAR real * 16
#define QPREC(x) QEXT(x)
#else
#define QVAR RealType
#define QPREC(x) x
#endif
#define QREAL QVAR
#define QCC(x) x
#define QRE(x) x

#endif

#define Paa 1
#define Pbb 3
#define Pcc 6
#define Pdd 10
#define Pee 15

#define aa0 1
#define AA0 1 : 3
#define aa00 4
#define AA00 4 : 6
#define Naa 6

#define bb0 1
#define BB0 1 : 3
#define bb1 4
#define BB1 4 : 6
#define bb00 7
#define BB00 7 : 9
#define bb11 10
#define BB11 10 : 12
#define bb001 13
#define BB001 13 : 15
#define bb111 16
#define BB111 16 : 18
#define dbb0 19
#define DBB0 19 : 21
#define dbb1 22
#define DBB1 22 : 24
#define dbb00 25
#define DBB00 25 : 27
#define dbb11 28
#define DBB11 28 : 30
#define dbb001 31
#define DBB001 31 : 33
#define bb0000 34
#define BB0000 34 : 36
#define bb0011 37
#define BB0011 37 : 39
#define bb1111 40
#define BB1111 40 : 42
#define Nbb 42

#define cc0 1
#define CC0 1 : 3
#define cc1 4
#define CC1 4 : 6
#define cc2 7
#define CC2 7 : 9
#define cc00 10
#define CC00 10 : 12
#define cc11 13
#define CC11 13 : 15
#define cc12 16
#define CC12 16 : 18
#define cc22 19
#define CC22 19 : 21
#define cc001 22
#define CC001 22 : 24
#define cc002 25
#define CC002 25 : 27
#define cc111 28
#define CC111 28 : 30
#define cc112 31
#define CC112 31 : 33
#define cc122 34
#define CC122 34 : 36
#define cc222 37
#define CC222 37 : 39
#define cc0000 40
#define CC0000 40 : 42
#define cc0011 43
#define CC0011 43 : 45
#define cc0012 46
#define CC0012 46 : 48
#define cc0022 49
#define CC0022 49 : 51
#define cc1111 52
#define CC1111 52 : 54
#define cc1112 55
#define CC1112 55 : 57
#define cc1122 58
#define CC1122 58 : 60
#define cc1222 61
#define CC1222 61 : 63
#define cc2222 64
#define CC2222 64 : 66
#define Ncc 66

#define dd0 1
#define DD0 1 : 3
#define dd1 4
#define DD1 4 : 6
#define dd2 7
#define DD2 7 : 9
#define dd3 10
#define DD3 10 : 12
#define dd00 13
#define DD00 13 : 15
#define dd11 16
#define DD11 16 : 18
#define dd12 19
#define DD12 19 : 21
#define dd13 22
#define DD13 22 : 24
#define dd22 25
#define DD22 25 : 27
#define dd23 28
#define DD23 28 : 30
#define dd33 31
#define DD33 31 : 33
#define dd001 34
#define DD001 34 : 36
#define dd002 37
#define DD002 37 : 39
#define dd003 40
#define DD003 40 : 42
#define dd111 43
#define DD111 43 : 45
#define dd112 46
#define DD112 46 : 48
#define dd113 49
#define DD113 49 : 51
#define dd122 52
#define DD122 52 : 54
#define dd123 55
#define DD123 55 : 57
#define dd133 58
#define DD133 58 : 60
#define dd222 61
#define DD222 61 : 63
#define dd223 64
#define DD223 64 : 66
#define dd233 67
#define DD233 67 : 69
#define dd333 70
#define DD333 70 : 72
#define dd0000 73
#define DD0000 73 : 75
#define dd0011 76
#define DD0011 76 : 78
#define dd0012 79
#define DD0012 79 : 81
#define dd0013 82
#define DD0013 82 : 84
#define dd0022 85
#define DD0022 85 : 87
#define dd0023 88
#define DD0023 88 : 90
#define dd0033 91
#define DD0033 91 : 93
#define dd1111 94
#define DD1111 94 : 96
#define dd1112 97
#define DD1112 97 : 99
#define dd1113 100
#define DD1113 100 : 102
#define dd1122 103
#define DD1122 103 : 105
#define dd1123 106
#define DD1123 106 : 108
#define dd1133 109
#define DD1133 109 : 111
#define dd1222 112
#define DD1222 112 : 114
#define dd1223 115
#define DD1223 115 : 117
#define dd1233 118
#define DD1233 118 : 120
#define dd1333 121
#define DD1333 121 : 123
#define dd2222 124
#define DD2222 124 : 126
#define dd2223 127
#define DD2223 127 : 129
#define dd2233 130
#define DD2233 130 : 132
#define dd2333 133
#define DD2333 133 : 135
#define dd3333 136
#define DD3333 136 : 138
#define dd00001 139
#define DD00001 139 : 141
#define dd00002 142
#define DD00002 142 : 144
#define dd00003 145
#define DD00003 145 : 147
#define dd00111 148
#define DD00111 148 : 150
#define dd00112 151
#define DD00112 151 : 153
#define dd00113 154
#define DD00113 154 : 156
#define dd00122 157
#define DD00122 157 : 159
#define dd00123 160
#define DD00123 160 : 162
#define dd00133 163
#define DD00133 163 : 165
#define dd00222 166
#define DD00222 166 : 168
#define dd00223 169
#define DD00223 169 : 171
#define dd00233 172
#define DD00233 172 : 174
#define dd00333 175
#define DD00333 175 : 177
#define dd11111 178
#define DD11111 178 : 180
#define dd11112 181
#define DD11112 181 : 183
#define dd11113 184
#define DD11113 184 : 186
#define dd11122 187
#define DD11122 187 : 189
#define dd11123 190
#define DD11123 190 : 192
#define dd11133 193
#define DD11133 193 : 195
#define dd11222 196
#define DD11222 196 : 198
#define dd11223 199
#define DD11223 199 : 201
#define dd11233 202
#define DD11233 202 : 204
#define dd11333 205
#define DD11333 205 : 207
#define dd12222 208
#define DD12222 208 : 210
#define dd12223 211
#define DD12223 211 : 213
#define dd12233 214
#define DD12233 214 : 216
#define dd12333 217
#define DD12333 217 : 219
#define dd13333 220
#define DD13333 220 : 222
#define dd22222 223
#define DD22222 223 : 225
#define dd22223 226
#define DD22223 226 : 228
#define dd22233 229
#define DD22233 229 : 231
#define dd22333 232
#define DD22333 232 : 234
#define dd23333 235
#define DD23333 235 : 237
#define dd33333 238
#define DD33333 238 : 240
#define Ndd 240

#define ee0 1
#define EE0 1 : 3
#define ee1 4
#define EE1 4 : 6
#define ee2 7
#define EE2 7 : 9
#define ee3 10
#define EE3 10 : 12
#define ee4 13
#define EE4 13 : 15
#define ee00 16
#define EE00 16 : 18
#define ee11 19
#define EE11 19 : 21
#define ee12 22
#define EE12 22 : 24
#define ee13 25
#define EE13 25 : 27
#define ee14 28
#define EE14 28 : 30
#define ee22 31
#define EE22 31 : 33
#define ee23 34
#define EE23 34 : 36
#define ee24 37
#define EE24 37 : 39
#define ee33 40
#define EE33 40 : 42
#define ee34 43
#define EE34 43 : 45
#define ee44 46
#define EE44 46 : 48
#define ee001 49
#define EE001 49 : 51
#define ee002 52
#define EE002 52 : 54
#define ee003 55
#define EE003 55 : 57
#define ee004 58
#define EE004 58 : 60
#define ee111 61
#define EE111 61 : 63
#define ee112 64
#define EE112 64 : 66
#define ee113 67
#define EE113 67 : 69
#define ee114 70
#define EE114 70 : 72
#define ee122 73
#define EE122 73 : 75
#define ee123 76
#define EE123 76 : 78
#define ee124 79
#define EE124 79 : 81
#define ee133 82
#define EE133 82 : 84
#define ee134 85
#define EE134 85 : 87
#define ee144 88
#define EE144 88 : 90
#define ee222 91
#define EE222 91 : 93
#define ee223 94
#define EE223 94 : 96
#define ee224 97
#define EE224 97 : 99
#define ee233 100
#define EE233 100 : 102
#define ee234 103
#define EE234 103 : 105
#define ee244 106
#define EE244 106 : 108
#define ee333 109
#define EE333 109 : 111
#define ee334 112
#define EE334 112 : 114
#define ee344 115
#define EE344 115 : 117
#define ee444 118
#define EE444 118 : 120
#define ee0000 121
#define EE0000 121 : 123
#define ee0011 124
#define EE0011 124 : 126
#define ee0012 127
#define EE0012 127 : 129
#define ee0013 130
#define EE0013 130 : 132
#define ee0014 133
#define EE0014 133 : 135
#define ee0022 136
#define EE0022 136 : 138
#define ee0023 139
#define EE0023 139 : 141
#define ee0024 142
#define EE0024 142 : 144
#define ee0033 145
#define EE0033 145 : 147
#define ee0034 148
#define EE0034 148 : 150
#define ee0044 151
#define EE0044 151 : 153
#define ee1111 154
#define EE1111 154 : 156
#define ee1112 157
#define EE1112 157 : 159
#define ee1113 160
#define EE1113 160 : 162
#define ee1114 163
#define EE1114 163 : 165
#define ee1122 166
#define EE1122 166 : 168
#define ee1123 169
#define EE1123 169 : 171
#define ee1124 172
#define EE1124 172 : 174
#define ee1133 175
#define EE1133 175 : 177
#define ee1134 178
#define EE1134 178 : 180
#define ee1144 181
#define EE1144 181 : 183
#define ee1222 184
#define EE1222 184 : 186
#define ee1223 187
#define EE1223 187 : 189
#define ee1224 190
#define EE1224 190 : 192
#define ee1233 193
#define EE1233 193 : 195
#define ee1234 196
#define EE1234 196 : 198
#define ee1244 199
#define EE1244 199 : 201
#define ee1333 202
#define EE1333 202 : 204
#define ee1334 205
#define EE1334 205 : 207
#define ee1344 208
#define EE1344 208 : 210
#define ee1444 211
#define EE1444 211 : 213
#define ee2222 214
#define EE2222 214 : 216
#define ee2223 217
#define EE2223 217 : 219
#define ee2224 220
#define EE2224 220 : 222
#define ee2233 223
#define EE2233 223 : 225
#define ee2234 226
#define EE2234 226 : 228
#define ee2244 229
#define EE2244 229 : 231
#define ee2333 232
#define EE2333 232 : 234
#define ee2334 235
#define EE2334 235 : 237
#define ee2344 238
#define EE2344 238 : 240
#define ee2444 241
#define EE2444 241 : 243
#define ee3333 244
#define EE3333 244 : 246
#define ee3334 247
#define EE3334 247 : 249
#define ee3344 250
#define EE3344 250 : 252
#define ee3444 253
#define EE3444 253 : 255
#define ee4444 256
#define EE4444 256 : 258
#define Nee 258

#define KeyA0 0
#define KeyBget 2
#define KeyC0 4
#define KeyD0 6
#define KeyD0C 8
#define KeyE0 10
#define KeyEget 12
#define KeyEgetC 14

#define DebugA 0
#define DebugB 1
#define DebugC 2
#define DebugD 3
#define DebugE 4

#define memindex integer * 8

#define Ano RC
#define Bno RC + 2
#define Cno RC + 4
#define Dno RC + 6
#define Eno RC + 8
#define Aval(id, p) cache(p + id, Ano)
#define Bval(id, p) cache(p + id, Bno)
#define Cval(id, p) cache(p + id, Cno)
#define Dval(id, p) cache(p + id, Dno)
#define Eval(id, p) cache(p + id, Eno)
#define offsetC 2

#define M(i) para(1, i)
#define P(i) para(1, i + npoint)

#define Sgn(i) (1 - 2 * iand(i, 1))

#define ln(x, s) log(x + (s)*cIeps)

#define lnrat(x, y) log((x - cIeps) / (y - cIeps))

#define MAXDIM 8

#ifndef KIND
#define KIND 1
#endif

*#define WARNINGS

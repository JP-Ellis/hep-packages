#include "SLHAplus.h"
#include "aList.h"

/* transforms routines with variable  number  of  arguments
   into set of routines with fixed number of arguments. It is needed for
   Fortran  and C++ ( in case of Complex arguments) versions of SLHAplus.
   fixArg.c uses substitutions  defined in aList.h
*/

int rDiagonal2(aList3(double)) { return rDiagonal(2, aList3()); }
int rDiagonal3(aList6(double)) { return rDiagonal(3, aList6()); }
int rDiagonal4(aList10(double)) { return rDiagonal(4, aList10()); }
int rDiagonal5(aList15(double)) { return rDiagonal(5, aList15()); }

int rDiagonalA2(aList4(double)) { return rDiagonalA(2, aList4()); }
int rDiagonalA3(aList9(double)) { return rDiagonalA(3, aList9()); }
int rDiagonalA4(aList16(double)) { return rDiagonalA(4, aList16()); }
int rDiagonalA5(aList25(double)) { return rDiagonalA(5, aList25()); }

int cDiagonalH2(aList3(double complex)) { return cDiagonalH(2, aList3()); }
int cDiagonalH3(aList6(double complex)) { return cDiagonalH(3, aList6()); }
int cDiagonalH4(aList10(double complex)) { return cDiagonalH(4, aList10()); }
int cDiagonalH5(aList15(double complex)) { return cDiagonalH(5, aList15()); }

int cDiagonalS2(aList3(double complex)) { return cDiagonalS(2, aList3()); }
int cDiagonalS3(aList6(double complex)) { return cDiagonalS(3, aList6()); }
int cDiagonalS4(aList10(double complex)) { return cDiagonalS(4, aList10()); }
int cDiagonalS5(aList15(double complex)) { return cDiagonalS(5, aList15()); }

int cDiagonalA2(aList4(double complex)) { return cDiagonalA(2, aList4()); }
int cDiagonalA3(aList9(double complex)) { return cDiagonalA(3, aList9()); }
int cDiagonalA4(aList16(double complex)) { return cDiagonalA(4, aList16()); }
int cDiagonalA5(aList25(double complex)) { return cDiagonalA(5, aList25()); }

int System1(char *format) { return System(format); }
int System2(char *format, char *path) { return System(format, path); }

int aPrintF0(char *format) { return aPrintF(format); }
int aPrintF1(char *format, double x1) { return aPrintF(format, x1); }
int aPrintF2(char *format, double x1, double x2) {
  return aPrintF(format, x1, x2);
}
int aPrintF3(char *format, double x1, double x2, double x3) {
  return aPrintF(format, x1, x2, x3);
}
int aPrintF4(char *format, double x1, double x2, double x3, double x4) {
  return aPrintF(format, x1, x2, x3, x4);
}
int aPrintF5(char *format, double x1, double x2, double x3, double x4,
             double x5) {
  return aPrintF(format, x1, x2, x3, x4, x5);
}
int aPrintF6(char *format, double x1, double x2, double x3, double x4,
             double x5, double x6) {
  return aPrintF(format, x1, x2, x3, x4, x5, x6);
}
int aPrintF7(char *format, double x1, double x2, double x3, double x4,
             double x5, double x6, double x7) {
  return aPrintF(format, x1, x2, x3, x4, x5, x6, x7);
}
int aPrintF8(char *format, double x1, double x2, double x3, double x4,
             double x5, double x6, double x7, double x8) {
  return aPrintF(format, x1, x2, x3, x4, x5, x6, x7, x8);
}
int aPrintF9(char *format, double x1, double x2, double x3, double x4,
             double x5, double x6, double x7, double x8, double x9) {
  return aPrintF(format, x1, x2, x3, x4, x5, x6, x7, x8, x9);
}

#include "delList.h"

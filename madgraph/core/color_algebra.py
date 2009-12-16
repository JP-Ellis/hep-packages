################################################################################
#
# Copyright (c) 2009 The MadGraph Development team and Contributors
#
# This file is a part of the MadGraph 5 project, an application which 
# automatically generates Feynman diagrams and matrix elements for arbitrary
# high-energy processes in the Standard Model and beyond.
#
# It is subject to the MadGraph license which should accompany this 
# distribution.
#
# For more information, please visit: http://madgraph.phys.ucl.ac.be
#
################################################################################

"""Classes and methods required for all calculations related 
to QCD color algebra."""

import fractions
import operator

#===============================================================================
# ColorObject
#===============================================================================
class ColorObject(list):
    """Parent class for all color objects like T, Tr, f, d, ... By default,
    implement a list of color indices (with get and set) and template for 
    simplify and pair_simplify. Any new color object MUST inherit
    from this class."""

    def __init__(self, *args):
        """Initialize a color object. Any number of argument can be used, all
        of them being considered as color indices."""

        list.__init__(self)
        self.set_indices(*args)

    def append_index(self, index):
        """Append an index at the end of the current ColorObject"""
        # Check if the input value is an integer
        if not isinstance(index, int):
            raise TypeError, \
                "Object %s is not a valid integer for color index" % str(index)
        self.append(index)

    def set_indices(self, *args):
        """Use arguments (any number) to set  the current indices. Previous
        indices are lost."""

        # Remove all existing elements
        del self[:]
        # Append new ones
        for index in args:
            self.append_index(index)

    def get_indices(self):
        """Returns a list of indices."""

        return list(self)

    def __str__(self):
        """Returns a standard string representation. Can be overwritten for
        each specific child."""

        return '%s(%s)' % (self.__class__.__name__,
                           ','.join([str(i) for i in self]))

    def simplify(self):
        """Called to simplify the current object. Default behavior is to return
        None, but should be overwritten for each child."""

        return None

    def pair_simplify(self):
        """Called to simplify a pair of (multiplied) ColorObject. 
        Default behavior is to return None, but should be overwritten 
        for each child."""

        return None

class f(ColorObject):
    pass

class d(f):
    pass

class ColorString(list):
    """A list of ColorObjects, together with a Fraction coefficient and a tag
    to indicate if the coefficient is real or imaginary. ColorStrings can be 
    simplified, by applying the simplify and pair_simplify rules of their
    elements and adding terms with the same structure."""

    _coeff = fractions.Fraction(1, 1)
    _is_imaginary = False
    _Nc_power = 0

    def __init__(self, *args):
        """Creates a new color string starting from one or several color
        objects."""

        list.__init__(self)
        self.set_color_objects(*args)

    def append_color_object(self, col_obj):
        """Append a color object at the end of the current ColorString"""
        # Check if the input value is a child of ColorObject
        if not isinstance(col_obj, ColorObject):
            raise TypeError, \
                "Object %s is not a valid ColorObject child for color index" % \
                                                           str(col_obj)
        self.append(col_obj)

    def set_color_objects(self, *args):
        """Use arguments (any number) to set  the current color objects. 
        Previous color objects are lost."""

        # Remove all existing elements
        del self[:]
        # Append new ones
        for col_obj in args:
            self.append_color_object(col_obj)

    def __str__(self):
        """Returns a standard string representation based on color object
        representations"""

        coeff_str = str(self._coeff)
        if self._is_imaginary:
            coeff_str += ' I'
        if self._Nc_power > 0:
            coeff_str += ' Nc^%i' % self._Nc_power
        elif self._Nc_power < 0:
            coeff_str += ' 1/Nc^%i' % abs(self._Nc_power)
        return '%s %s' % (coeff_str,
                         ' '.join([str(col_obj) for col_obj in self]))

    def set_coeff(self, frac):
        """Set the coefficient of the ColorString"""

        if not isinstance(frac, fractions.Fraction):
            raise TypeError, \
                "Object %s is not a valid fraction for coefficient" % \
                                                                str(frac)
        self._coeff = frac

    def get_coeff(self):
        """Get the coefficient of the ColorString"""
        return self._coeff

    def set_Nc_power(self, power):
        """Set the Nc power of the ColorString"""

        if not isinstance(power, int):
            raise TypeError, \
                "Object %s is not a valid int for Nc power" % str(power)
        self._Nc_power = power

    def get_Nc_power(self):
        """Get the Nc power of the ColorString"""
        return self._Nc_power

    def set_is_imaginary(self, is_imaginary):
        """Set the is_imaginary flag of the ColorString"""

        if not isinstance(is_imaginary, bool):
            raise TypeError, \
                "Object %s is not a valid boolean for is_imaginary flag" % \
                                                            str(is_imaginary)
        self._is_imaginary = is_imaginary

    def is_imaginary(self):
        """Is the ColorString imaginary ?"""
        return self._is_imaginary

#import copy
#import itertools
#import operator
#import re
#
##===============================================================================
## Regular expression objects (compiled)
##===============================================================================
#
## Match only valid color string object
#re_color_object = re.compile(r""" ^ (T\(((-?\d +)(, -?\d +) *)?\)
#                            |Tr\(((-?\d+)(,-?\d+)*)?\)
#                            |f\(-?\d+,-?\d+,-?\d+\)
#                            |d\(-?\d+,-?\d+,-?\d+\)
#                            |(1/)?Nc
#                            |-?(\d+/)?\d+
#                            |I)$""",
#                            re.VERBOSE)
#
## T trace T(a,b,c,...,i,i), group start is a,b,c,...
#re_T_trace = re.compile(r"""^T\((?P<start>(-?\d+,)*)?
#                            (?P<id>-?\d+),(?P=id)\)$""", re.VERBOSE)
#
## T product T(a,...,i,j)T(b,...,j,k), group start1 is a,...,
## group start2 is b,..., group id1 is i and group id2 is k
#re_T_product1 = re.compile(r"""^T\((?P<start1>(-?\d+,)*)
#                                (?P<id1>-?\d+),(?P<summed>-?\d+)\)
#                                T\((?P<start2>(-?\d+,)*)
#                                (?P=summed),(?P<id2>-?\d+)\)$""", re.VERBOSE)
#
## T product T(b,...,j,k)T(a,...,i,j), group start1 is a,...,
## group start2 is b,..., group id1 is i and group id2 is k
#re_T_product2 = re.compile(r"""^T\((?P<start2>(-?\d+,)*)
#                                (?P<summed>-?\d+),(?P<id2>-?\d+)\)
#                                T\((?P<start1>(-?\d+,)*)
#                                (?P<id1>-?\d+),(?P=summed)\)$""", re.VERBOSE)
#
## Tr()
#re_trace_0_index = re.compile(r"^Tr\(\)$")
#
## Tr(i), group id is i
#re_trace_1_index = re.compile(r"^Tr\((?P<id>-?\d+)\)$")
#
## Tr(a,b,c,...), group elems is a,b,c,...
#re_trace_n_indices = re.compile(r"^Tr\((?P<elems>(-?\d+,)*(-?\d+)?)\)$")
#
## Match a fraction (with denominator or not), group has num/den entries
#re_fraction = re.compile(r"^(?P<num>-?\d+)(/(?P<den>\d+))?$")
#
## Match f(a,b,c) terms, groups elements are a, b and c
#re_f_term = re.compile(r"^f\((?P<a>-?\d+),(?P<b>-?\d+),(?P<c>-?\d+)\)")
#
## Match d(a,b,c) terms, groups elements are a, b and c
#re_d_term = re.compile(r"^d\((?P<a>-?\d+),(?P<b>-?\d+),(?P<c>-?\d+)\)")
#
## Match T(a,...,x,b,...,x,c,...,i,j), groups element are a='a,...',b='b,...,' 
## c='c,...,' (notice commas) and id1=i, id2=j
#re_T_int_sum = re.compile(r"""^T\((?P<a>(-?\d+,)*)
#                                (?P<x>-?\d+),
#                                (?P<b>(-?\d+,)*)
#                                (?P=x),
#                                (?P<c>(-?\d+,)*)
#                                (?P<id1>-?\d+),(?P<id2>-?\d+)\)$""", re.VERBOSE)
#
## Match Tr(a,...,x,b,...,x,c,...), groups element are a='a,...',b='b,...,' 
## c='c,...,' (notice commas) 
#re_trace_int_sum = re.compile(r"""^Tr\((?P<a>(-?\d+,)*)
#                                (?P<x>-?\d+),
#                                (?P<b>(-?\d+,)*)
#                                (?P=x)
#                                (?P<c>(,-?\d+)*)\)$""", re.VERBOSE)
#
## Match Tr(a...,x,b,...)Tr(c...,x,d,...), groups element are a='a,...',
## b='b,...', c='c,...,' and d='d,...' (notice commas) 
#re_trace_product = re.compile(r"""^Tr\((?P<a>(-?\d+,)*)
#                                (?P<x>-?\d+)
#                                (?P<b>(,-?\d+)*)\)
#                                Tr\((?P<c>(-?\d+,)*)
#                                (?P=x)
#                                (?P<d>(,-?\d+)*)\)$""", re.VERBOSE)
#
## Match Tr(a,...,x,b,...)T(c,...,x,d,...,i,j)
#re_trace_T_product1 = re.compile(r"""^Tr\((?P<a>(-?\d+,)*)
#                                (?P<x>-?\d+),
#                                (?P<b>(-?\d+,)*(-?\d+)?)\)
#                                T\((?P<c>(-?\d+,)*)
#                                (?P=x),
#                                (?P<d>(-?\d+,)*)
#                                (?P<id1>-?\d+),(?P<id2>-?\d+)\)$""", re.VERBOSE)
#re_trace_T_product2 = re.compile(r"""^T\((?P<c>(-?\d+,)*)
#                                (?P<x>-?\d+),
#                                (?P<d>(-?\d+,)*)
#                                (?P<id1>-?\d+),(?P<id2>-?\d+)\)
#                                Tr\((?P<a>(-?\d+,)*)
#                                (?P=x)
#                                (?P<b>(,-?\d+)*)\)$""", re.VERBOSE)
#
## Match T(a,...,x,b,...,i,j)T(c,...,x,d,...,k,l)
#re_T_product = re.compile(r"""^T\((?P<a>(-?\d+,)*)
#                                (?P<x>-?\d+),
#                                (?P<b>(-?\d+,)*)
#                                (?P<id1>-?\d+),(?P<id2>-?\d+)\)
#                                T\((?P<c>(-?\d+,)*)
#                                (?P=x),
#                                (?P<d>(-?\d+,)*)
#                                (?P<id3>-?\d+),(?P<id4>-?\d+)\)$""", re.VERBOSE)
#
## Match T(...,i1,i2), ... being indices
#re_T = re.compile(r"""^T\((?P<indices>(-?\d+,)*)
#                            (?P<id1>-?\d+),(?P<id2>-?\d+)\)$""", re.VERBOSE)
#
## Match Tr(...), ... being indices
#re_Tr = re.compile(r"^Tr\((?P<indices>(-?\d+,)*-?\d+)\)$")
#
##===============================================================================
## ColorString
##===============================================================================
#class ColorString(list):
#    """Define a color string as an ordered list of strings corresponding to the
#    different color structures. Different elements are implicitly linked by
#    a product operator."""
#
#    def __init__(self, init_list=None):
#        """Initialization method, if init_list is given, try to fill the 
#        color string with the content."""
#
#        list.__init__(self)
#
#        if init_list:
#            if not isinstance(init_list, list):
#                raise ValueError, \
#                    "Object %s is not a valid list" % init_list
#            for elem in init_list:
#                if self.is_valid_color_object(elem):
#                    self.append(elem)
#                else: raise ValueError, \
#                        "String %s is not a valid color object" % elem
#
#    def is_valid_color_object(self, test_str):
#        """Checks the validity of a given color object stored in 
#        string test_str. Returns True if valid, False otherwise."""
#
#        if not isinstance(test_str, str):
#            raise ValueError, "Object %s is not a valid string." % str(test_str)
#
#        # Check if the string has the right format
#        if re_color_object.match(test_str):
#            return True
#        else:
#            return False
#
#    def append(self, mystr):
#        """Appends an string, but test if valid before."""
#        if not self.is_valid_color_object(mystr):
#            raise ValueError, \
#                        "String %s is not a valid color structure" % mystr
#        else:
#            list.append(self, mystr)
#
#    def insert(self, pos, mystr):
#        """Insert an string at position pos, but test if valid before."""
#        if not self.is_valid_color_object(mystr):
#            raise ValueError, \
#                        "String %s is not a valid color structure" % mystr
#        else:
#            list.insert(self, pos, mystr)
#
#    def extend(self, col_string):
#        """Extend with another color string, but test if valid before."""
#        if not isinstance(col_string, ColorString):
#            raise ValueError, \
#                        "Object %s is not a valid color string" % col_string
#        else:
#            list.extend(self, col_string)
#
#    def simplify(self):
#        """Simplify the current color string as much as possible, using 
#        all possible identities."""
#
#        while True:
#
#            original = copy.copy(self)
#
#            self.__simplify_T_traces()
#            self.__simplify_T_products()
#            self.__simplify_simple_traces()
#            self.__simplify_trace_cyclicity()
#            self.__simplify_coeffs()
#            if self == original:
#                break
#
#    def __simplify_T_traces(self):
#        """Apply the identity T(a,b,c,...,i,i) = Tr(a,b,c,...)"""
#
#        for index, col_obj in enumerate(self):
#            self[index] = re_T_trace.sub(lambda m: "Tr(%s)" % \
#                                         self.__clean_commas(m.group('start')),
#                                         col_obj)
#
#    def __simplify_T_products(self):
#        """Apply the identity T(a,...,i,j)T(b,...,j,k) = T(a,...,b,...,i,k)
#        on the first matching pair"""
#        for index1, mystr1 in enumerate(self):
#            for index2, mystr2 in enumerate(self[index1 + 1:]):
#                # Test both product ordering
#                m = re_T_product1.match(mystr1 + mystr2)
#                if not m:
#                    m = re_T_product2.match(mystr1 + mystr2)
#                if m:
#                    s1s2i1i2 = self.__clean_commas(','.join([m.group('start1'),
#                                                             m.group('start2'),
#                                                             m.group('id1'),
#                                                             m.group('id2')]))
#                    self[index1] = "T(%s)" % s1s2i1i2
#                    del self[index1 + index2 + 1]
#                    return
#
#    def __simplify_simple_traces(self):
#        """Apply the identities Tr(a)=0 (AS) and Tr() = Nc (delta)"""
#
#        for index, col_obj in enumerate(self):
#            if re_trace_0_index.match(col_obj):
#                self[index] = "Nc"
#            if re_trace_1_index.match(col_obj):
#                self[index] = "0"
#
#    def __simplify_trace_cyclicity(self):
#        """Re-order traces using cyclicity to bring smallest id in front"""
#
#        for index, col_obj in enumerate(self):
#            m = re_trace_n_indices.match(col_obj)
#            if m:
#                list_indices = [int(s) for s in m.group('elems').split(',')]
#                pos = list_indices.index(min(list_indices))
#                res_list = list_indices[pos:]
#                res_list.extend(list_indices[:pos])
#                self[index] = 'Tr(%s)' % ','.join([str(i) for i in res_list])
#
#    def __simplify_coeffs(self):
#        """Applies simple algebraic simplifications on scalar coefficients
#        and bring the final result to the first position"""
#
#        # Simplify factors Nc
#        numNc = self.count('Nc') - self.count('1/Nc')
#        while ('Nc' in self): self.remove('Nc')
#        while ('1/Nc' in self): self.remove('1/Nc')
#        if numNc > 0:
#            for dummy in range(numNc):
#                self.insert(0, 'Nc')
#        elif numNc < 0:
#            for dummy in range(abs(numNc)):
#                self.insert(0, '1/Nc')
#
#        # Simplify factors I
#        numI = self.count('I')
#        while ('I' in self): self.remove('I')
#        if numI % 4 == 1:
#            self.insert(0, 'I')
#        elif numI % 4 == 2:
#            self.insert(0, '-1')
#        elif numI % 4 == 3:
#            self.insert(0, 'I')
#            self.insert(0, '-1')
#
#        # Compute numerators and denominators
#        numlist = []
#        denlist = []
#        for elem in self[:]:
#            m = re_fraction.match(elem)
#            if m:
#                self.remove(elem)
#                numlist.append(int(m.group('num')))
#                if m.group('den'):
#                    denlist.append(int(m.group('den')))
#        numerator = reduce(operator.mul, numlist, 1)
#        denominator = reduce(operator.mul, denlist, 1)
#
#        # Deal with 0 coeff
#        if numerator == 0:
#            del self[:]
#          #  self.insert(0, '0')
#            return
#
#        # Try to simplify further fractions
#        dev = self.__gcd(numerator, denominator)
#        numerator //= dev
#        denominator //= dev
#
#        # Output result in a correct way
#        if denominator != 1:
#            self.insert(0, "%i/%i" % (numerator, denominator))
#        elif numerator != 1:
#            self.insert(0, "%i" % numerator)
#
#    def __gcd(self, a, b):
#        """Find the gcd of two integers"""
#        while b: a, b = b, a % b
#        return a
#
#    def __expand_term(self, indices, new_str1, new_str2):
#        """Return two color strings built on self where all indices in the
#        list indices have been removed and, for the first index of the list, 
#        replaced once by new_str1 and once bynew_str2."""
#
#        str1 = copy.copy(self)
#        str2 = copy.copy(self)
#
#        # Remove indices, pay attention to the shift induced by del
#        for i, index in enumerate(indices):
#            del str1[index - i]
#            del str2[index - i]
#
#        # Insert new element at the position given by the first index
#        for i, elem in enumerate(new_str1):
#            str1.insert(indices[0] + i, elem)
#        for i, elem in enumerate(new_str2):
#            str2.insert(indices[0] + i, elem)
#
#        return [str1, str2]
#
#
#    def expand_composite_terms(self):
#        """Expand the first encountered composite term like f,d,... 
#        and returns the corresponding list of ColorString objects. 
#        This method will NOT modify the current color string. If nothing
#        to expand is found, returns an empty list."""
#
#        for index, col_obj in enumerate(self):
#
#            # Deal with d terms
#            m = re_d_term.match(col_obj)
#            if m:
#                return self.__expand_term([index], ['2', 'Tr(%s,%s,%s)' % \
#                                                      (m.group('a'),
#                                                       m.group('b'),
#                                                       m.group('c'))],
#                                                 ['2', 'Tr(%s,%s,%s)' % \
#                                                      (m.group('c'),
#                                                       m.group('b'),
#                                                       m.group('a'))])
#            # Deal with f terms
#            m = re_f_term.match(col_obj)
#            if m:
#                return self.__expand_term([index], ['-2', 'I',
#                                                    'Tr(%s,%s,%s)' % \
#                                                      (m.group('a'),
#                                                       m.group('b'),
#                                                       m.group('c'))],
#                                                 ['2', 'I', 'Tr(%s,%s,%s)' % \
#                                                      (m.group('c'),
#                                                       m.group('b'),
#                                                       m.group('a'))])
#
#        return []
#
#    def expand_T_internal_sum(self):
#        """Expand the first encountered term with an internal sum in T's using
#        T(a,x,b,x,c,i,j) = 1/2(T(a,c,i,j)Tr(b)-1/Nc T(a,b,c,i,j)) and 
#        returns the corresponding list of ColorString objects. 
#        This method will NOT modify the current color string. If nothing
#        to expand is found, returns an empty list."""
#
#        for index, col_obj in enumerate(self):
#
#            m = re_T_int_sum.match(col_obj)
#            if m:
#
#                # Since we don't know exactly if the commas are consistently
#                # written, we have to build and clean the index strings
#                # before actually writing them
#                # --> to be refactored ?
#                b = self.__clean_commas(m.group('b'))
#                aci1i2 = self.__clean_commas(','.join([m.group('a'),
#                                                       m.group('c'),
#                                                       m.group('id1'),
#                                                       m.group('id2')]))
#                abci1i2 = self.__clean_commas(','.join([m.group('a'),
#                                                        m.group('b'),
#                                                       m.group('c'),
#                                                       m.group('id1'),
#                                                       m.group('id2')]))
#                return self.__expand_term([index], ['1/2',
#                                                    'T(%s)' % aci1i2,
#                                                    'Tr(%s)' % b],
#                                                   ['-1/2',
#                                                    '1/Nc',
#                                                    'T(%s)' % abci1i2])
#        return []
#
#    def expand_trace_internal_sum(self):
#        """Expand the first encountered term with an internal sum in a trace
#        using Tr(a,x,b,x,c) = 1/2(Tr(a,c)Tr(b)-1/Nc Tr(a,b,c)) and 
#        returns the corresponding list of ColorString objects. 
#        This method will NOT modify the current color string. If nothing
#        to expand is found, returns an empty list."""
#
#        for index, col_obj in enumerate(self):
#
#            m = re_trace_int_sum.match(col_obj)
#            if m:
#
#                b = self.__clean_commas(m.group('b'))
#                ac = self.__clean_commas(','.join([m.group('a'),
#                                                   m.group('c')]))
#                abc = self.__clean_commas(','.join([m.group('a'),
#                                                    m.group('b'),
#                                                    m.group('c')]))
#                return self.__expand_term([index], ['1/2', 'Tr(%s)' % ac,
#                                                       'Tr(%s)' % b],
#                                                 ['-1/2', '1/Nc',
#                                                  'Tr(%s)' % abc])
#        return []
#
#    def expand_trace_product(self):
#        """Expand the first encountered product of two traces with a summed
#        indices using Tr(a,x,b)Tr(c,x,d) = 1/2(Tr(a,d,c,b)-1/Nc Tr(a,b)Tr(c,d))
#        and returns the corresponding list of ColorString objects. 
#        This method will NOT modify the current color string. If nothing
#        to expand is found, returns an empty list."""
#
#        for index1, mystr1 in enumerate(self):
#            for index2, mystr2 in enumerate(self[index1 + 1:]):
#                m = re_trace_product.match(mystr1 + mystr2)
#                if m:
#                    adcb = self.__clean_commas(','.join([m.group('a'),
#                                                         m.group('d'),
#                                                         m.group('c'),
#                                                         m.group('b')]))
#                    ab = self.__clean_commas(m.group('a') + ',' + m.group('b'))
#                    cd = self.__clean_commas(m.group('c') + ',' + m.group('d'))
#                    return self.__expand_term([index1, index1 + index2 + 1],
#                                              ['1/2', 'Tr(%s)' % adcb],
#                                              ['-1/2', '1/Nc',
#                                                  'Tr(%s)' % ab,
#                                                  'Tr(%s)' % cd])
#        return []
#
#    def expand_trace_T_product(self):
#        """Expand the first encountered product of one trace and one T with 
#        a summed indices using 
#        Tr(a,x,b)T(c,x,d,i,j) = 1/2(T(c,b,a,d,i,j)-1/Nc Tr(a,b)T(c,d,i,j))
#        and returns the corresponding list of ColorString objects. 
#        This method will NOT modify the current color string. If nothing
#        to expand is found, returns an empty list."""
#
#        for index1, mystr1 in enumerate(self):
#            for index2, mystr2 in enumerate(self[index1 + 1:]):
#                m = re_trace_T_product1.match(mystr1 + mystr2)
#                if not m:
#                    m = re_trace_T_product2.match(mystr1 + mystr2)
#                if m:
#                    cbadi1i2 = self.__clean_commas(','.join([m.group('c'),
#                                                           m.group('b'),
#                                                           m.group('a'),
#                                                           m.group('d'),
#                                                           m.group('id1'),
#                                                           m.group('id2')]))
#                    ab = self.__clean_commas(','.join([m.group('a'),
#                                                       m.group('b')]))
#                    cdi1i2 = self.__clean_commas(','.join([m.group('c'),
#                                                           m.group('d'),
#                                                           m.group('id1'),
#                                                           m.group('id2')]))
#                    return self.__expand_term([index1, index1 + index2 + 1],
#                                              ['1/2',
#                                               'T(%s)' % cbadi1i2],
#                                              ['-1/2', '1/Nc',
#                                               'Tr(%s)' % ab,
#                                               'T(%s)' % cdi1i2])
#        return []
#
#    def expand_T_product(self):
#        """Expand the first encountered product of two T's with a summed indicex 
#        using T(a,x,b,i,j)T(c,x,d,k,l) = 1/2(T(a,d,i,l)T(c,b,k,j)
#                                        -1/Nc T(a,b,i,j)T(c,d,k,l))
#        and returns the corresponding list of ColorString objects. 
#        This method will NOT modify the current color string. If nothing
#        to expand is found, returns an empty list."""
#
#        for index1, mystr1 in enumerate(self):
#            for index2, mystr2 in enumerate(self[index1 + 1:]):
#                m = re_T_product.match(mystr1 + mystr2)
#                if m:
#                    adi1i4 = self.__clean_commas(','.join([m.group('a'),
#                                                           m.group('d'),
#                                                           m.group('id1'),
#                                                           m.group('id4')]))
#                    cbi3i2 = self.__clean_commas(','.join([m.group('c'),
#                                                           m.group('b'),
#                                                           m.group('id3'),
#                                                           m.group('id2')]))
#                    abi1i2 = self.__clean_commas(','.join([m.group('a'),
#                                                           m.group('b'),
#                                                           m.group('id1'),
#                                                           m.group('id2')]))
#                    cdi3i4 = self.__clean_commas(','.join([m.group('c'),
#                                                           m.group('d'),
#                                                           m.group('id3'),
#                                                           m.group('id4')]))
#                    return self.__expand_term([index1, index1 + index2 + 1],
#                                              ['1/2',
#                                               'T(%s)' % adi1i4,
#                                               'T(%s)' % cbi3i2],
#                                              ['-1/2', '1/Nc',
#                                               'T(%s)' % abi1i2,
#                                               'T(%s)' % cdi3i4])
#        return []
#
#    def __clean_commas(self, string):
#            """Return a string built on string where multiple commas
#            and commas at the beginning/end have been removed.
#            For example ,1,2,,,3,4,5, --> 1,2,3,4,5"""
#
#            my_str = string.lstrip(',')
#            my_str = my_str.rstrip(',')
#
#            while True:
#                cop_str = my_str
#                my_str = my_str.replace(',,', ',')
#                if cop_str == my_str:
#                    break
#            return my_str
#
#    def is_similar(self, col_str, check_I=True):
#        """Test if self is similar to col_str, i.e. if they have the same
#        tensorial structure (taking into account possible renaming of 
#        summed indices, permutations, ...) and identical powers of Nc/I. If
#        check_I is False, two strings are considered similar even if they
#        don't have the same power of I."""
#
#        l_self = len(self)
#        l_col_str = len(col_str)
#
#        if l_self == 0  or l_col_str == 0:
#            if l_self == 0  and l_col_str == 0:
#                return True
#            else:
#                return False
#
#        if re_fraction.match(self[0]):
#            self_shift = 1
#        else:
#            self_shift = 0
#
#        if re_fraction.match(col_str[0]):
#            col_str_shift = 1
#        else:
#            col_str_shift = 0
#
#        if not check_I:
#            while self[self_shift] == 'I':
#                self_shift += 1
#            while col_str[col_str_shift] == 'I':
#                col_str_shift += 1
#
#        if l_self - self_shift != l_col_str - col_str_shift:
#            return False
#
#        for i in range(l_self - self_shift):
#            if self[i + self_shift] != col_str[i + col_str_shift]:
#                return False
#
#        return True
#
#    def extract_coeff(self, take_I=True):
#        """Returns (coeff,col_str) where coeff is the coefficient of the color
#        string (incl I's if take_I is True) and col_str is the rest. The 
#        current object is nor modified."""
#
#        my_col_str = copy.copy(self)
#
#        if re_fraction.match(my_col_str[0]):
#            shift = 1
#        else:
#            shift = 0
#
#        if take_I:
#            while my_col_str[shift] == 'I':
#                shift += 1
#
#        coeff = ColorString(my_col_str[:shift])
#        remain = ColorString(my_col_str[shift:])
#
#        if not coeff:
#            coeff.append('1')
#
#        return (coeff, remain)
#
#    def add(self, col_str):
#        """Add two color similar strings, i.e. self becomes a new color string with
#        numerical coefficients added."""
#
#        if len(self) == 0:
#            self = copy.copy(col_str)
#            return
#
#        if len(col_str) == 0:
#            return
#
#        match1 = re_fraction.match(self[0])
#        match2 = re_fraction.match(col_str[0])
#
#        if match1:
#            num1 = int(match1.group('num'))
#            if match1.group('den'):
#                den1 = int(match1.group('den'))
#            else:
#                den1 = 1
#        else:
#            num1 = den1 = 1
#            self.insert(0, '1')
#
#        if match2:
#            num2 = int(match2.group('num'))
#            if match2.group('den'):
#                den2 = int(match2.group('den'))
#            else:
#                den2 = 1
#        else:
#            num2 = den2 = 1
#
#        # Simplify the fraction
#        numerator = num1 * den2 + num2 * den1
#        denominator = den1 * den2
#
#        dev = self.__gcd(numerator, denominator)
#        numerator //= dev
#        denominator //= dev
#        if denominator != 1:
#            self[0] = "%i/%i" % (numerator, denominator)
#        elif numerator != 1:
#            self[0] = "%i" % numerator
#        else:
#            del self[0]
#
#    def complex_conjugate(self):
#        """Returns a new color string, complex conjugate of self."""
#
#        ret_str = ColorString()
#
#        for col_obj in self:
#
#            m = re_Tr.match(col_obj)
#            if m:
#                list_index = m.group('indices').split(',')
#                list_index.reverse()
#                ret_str.append('Tr(%s)' % self.__clean_commas(','.join(list_index)))
#                continue
#
#            m = re_T.match(col_obj)
#            if m:
#                list_index = self.__clean_commas(m.group('indices')).split(',')
#                list_index.reverse()
#                Tr_arg = self.__clean_commas(','.join(list_index) + ',' + \
#                                                 m.group('id2') + ',' + \
#                                                 m.group('id1'))
#                ret_str.append('T(%s)' % Tr_arg)
#                continue
#
#            if col_obj == 'I':
#                ret_str.append('-1')
#                ret_str.append('I')
#                continue
#
#        ret_str.simplify()
#
#        return ret_str
#
##===============================================================================
## ColorFactor
##===============================================================================
#class ColorFactor(list):
#    """A list of ColorString object used to store the final result of a given
#    color factor calculation. Different elements are implicitly linked by a
#    sum operator.
#    """
#
#    def __init__(self, init_list=None):
#        """Creates a new ColorFactor object. If a list of ColorString
#        is given, add them."""
#
#        list.__init__(self)
#
#        if init_list is not None:
#            if isinstance(init_list, list):
#                for object in init_list:
#                    self.append(object)
#            else:
#                raise ValueError, \
#                    "Object %s is not a valid list" % repr(init_list)
#
#    def append(self, object):
#        """Appends an ColorString, but test if valid before."""
#        if not isinstance(object, ColorString):
#            raise ValueError, \
#                "Object %s is not a valid ColorString" % repr(object)
#        else:
#            list.append(self, object)
#
#    def insert(self, pos, object):
#        """Insert an ColorString at position pos, but test if valid before."""
#        if not isinstance(object, ColorString):
#            raise ValueError, \
#                "Object %s is not a valid ColorString" % repr(object)
#        else:
#            list.insert(self, pos, object)
#
#    def extend(self, col_factor):
#        """Extend with another ColorFactor, but test if valid before."""
#        if not isinstance(col_factor, ColorFactor):
#            raise ValueError, \
#                        "Object %s is not a valid ColorFactor" % col_factor
#        else:
#            list.extend(self, col_factor)
#
#    def __collect(self):
#        """Do a final simplification by grouping terms which are similars"""
#
#        # Try all combinations
#        for i1, col_str1 in enumerate(self[:]):
#            for i2, col_str2 in enumerate(self[i1 + 1:]):
#                if col_str1.is_similar(col_str2):
#                    self[i1].add(col_str2)
#                    del self[i1 + i2 + 1][:]
#
#    def simplify(self, simplify_T_products=True):
#        """Simplify the current ColorFactor. First apply simplification rules
#        on all ColorStrings, then expand first composite terms and apply the
#        golden rule. Iterate until the result does not change anymore. If
#        simplify_T_products is False, don't simplify T products."""
#
#        while True:
#
#            original = copy.copy(self)
#            # Expand one f/d if possible
#            for index, col_str in enumerate(self[:]):
#                result = col_str.expand_composite_terms()
#                if result:
#                    del self[index][:]
#                    self.append(result[0])
#                    self.append(result[1])
#
#            # Apply rules
#            for index, col_str in enumerate(self[:]):
#                result = col_str.expand_T_internal_sum()
#                if not result:
#                    result = col_str.expand_trace_internal_sum()
#                if not result:
#                    result = col_str.expand_trace_product()
#                if not result:
#                    result = col_str.expand_trace_T_product()
#                if not result and simplify_T_products:
#                    result = col_str.expand_T_product()
#                if result:
#                    del self[index][:]
#                    self.append(result[0])
#                    self.append(result[1])
#            # Simplify
#            for col_str in self:
#                col_str.simplify()
#
#            self.__collect()
#
#            for elem in self:
#                elem.simplify()
#
#            empty = ColorString()
#
#            while(empty in self): self.remove(empty)
#
#            # Iterate until the result does not change anymore
#            if self == original:
#                break
#
#    def fix_Nc(self, Nc=3):
#        """Replace all Nc factors by a given value (3 by default) and simplify
#        the whole color factor. This affects self!"""
#
#        for col_str in self:
#            for index, col_obj in enumerate(col_str):
#                col_str[index] = col_obj.replace('Nc', '3')
#
#        self.simplify()

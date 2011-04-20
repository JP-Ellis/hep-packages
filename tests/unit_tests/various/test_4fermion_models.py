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
"""Unit tests for four-fermion models."""
from __future__ import division

import math
import copy
import os
import sys
import time

import tests.unit_tests as unittest
import madgraph.core.base_objects as base_objects
import madgraph.core.diagram_generation as diagram_generation
import madgraph.core.helas_objects as helas_objects
import madgraph.iolibs.helas_call_writers as helas_call_writers
import madgraph.various.process_checks as process_checks
import models.import_ufo as import_ufo
import models.model_reader as model_reader

_file_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

#===============================================================================
# Models4FermionTest
#===============================================================================
class Models4FermionTest(unittest.TestCase):
    """Base test class for comparing 4-fermion models to resolved models"""

    def uu_to_ttng_test(self, nglue = 0):
        """Test the process u u > t t g for 4fermion models"""

        myleglist = base_objects.LegList()

        myleglist.append(base_objects.Leg({'id':2,
                                           'state':False}))
        myleglist.append(base_objects.Leg({'id':2,
                                           'state':False}))
        myleglist.append(base_objects.Leg({'id':6}))
        myleglist.append(base_objects.Leg({'id':6}))
        myleglist.extend([base_objects.Leg({'id':21}) for i in range(nglue)])

        values = {}
        p = None
        for model in 'scalar', '4ferm':

            base_model = eval('self.base_model_%s' % model)
            full_model = eval('self.full_model_%s' % model)
            myproc = base_objects.Process({'legs':myleglist,
                                           'model':base_model})

            helas_writer = helas_call_writers.PythonUFOHelasCallWriter(\
                                                                     base_model)
        
            evaluator = process_checks.MatrixElementEvaluator(full_model,
                                                              helas_writer,
                                                              reuse = False)

            if not p:
                p, w_rambo = evaluator.get_momenta(myproc)

            amplitude = diagram_generation.Amplitude(myproc)

            matrix_element = helas_objects.HelasMatrixElement(amplitude)

            stored_quantities = {}

            values[model] = evaluator.evaluate_matrix_element(matrix_element,
                                                              p)[0]

            
        self.assertAlmostEqual(values['scalar'], values['4ferm'], 3)

#===============================================================================
# TestSchannelModels
#===============================================================================
class TestSchannelModels(Models4FermionTest):
    """Test class for the s-channel type 4-fermion model"""

    def setUp(self):
        self.base_model_scalar = import_ufo.import_model('sextet_diquarks')
        self.full_model_scalar = \
                               model_reader.ModelReader(self.base_model_scalar)
        self.full_model_scalar.set_parameters_and_couplings()
        self.full_model_scalar.get('parameter_dict')['MSIX'] = 1.e5
        
        self.base_model_4ferm = import_ufo.import_model('uutt_sch_4fermion')
        self.full_model_4ferm = \
                               model_reader.ModelReader(self.base_model_4ferm)
        self.full_model_4ferm.set_parameters_and_couplings()
    
    def test_uu_to_tt_sch(self):
        """Test the process u u > t t between s-channel and 4fermion vertex"""
        self.uu_to_ttng_test(0)

    def test_uu_to_ttg_sch(self):
        """Test the process u u > t t g between s-channel and 4fermion vertex"""
        self.uu_to_ttng_test(1)
        
#===============================================================================
# TestTchannelModels
#===============================================================================
class TestTchannelModels(Models4FermionTest):
    """Test class for the t-channel type 4-fermion model"""

    def setUp(self):
        self.base_model_scalar = import_ufo.import_model('uutt_tch_scalar')
        self.full_model_scalar = \
                               model_reader.ModelReader(self.base_model_scalar)
        self.full_model_scalar.set_parameters_and_couplings()
        
        self.base_model_4ferm = import_ufo.import_model('uutt_tch_4fermion')
        self.full_model_4ferm = \
                               model_reader.ModelReader(self.base_model_4ferm)
        self.full_model_4ferm.set_parameters_and_couplings()
    
    def test_uu_to_tt_tch(self):
        """Test the process u u > t t between t-channel and 4fermion vertex"""
        self.uu_to_ttng_test(0)

    def test_uu_to_ttg_tch(self):
        """Test the process u u > t t g between t-channel and 4fermion vertex"""
        self.uu_to_ttng_test(1)
        

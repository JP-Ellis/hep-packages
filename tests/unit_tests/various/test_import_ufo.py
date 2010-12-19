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
"""Unit test Library for importing and restricting model"""
from __future__ import division

import copy
import os
import sys
import time

import tests.unit_tests as unittest
import madgraph.core.base_objects as base_objects
import models.import_ufo as import_ufo
import models.model_reader as model_reader

_file_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]


#===============================================================================
# TestRestrictModel
#===============================================================================
class TestRestrictModel(unittest.TestCase):
    """Test class for the RestrictModel object"""

    base_model = import_ufo.import_model('sm')

    def setUp(self):
        """Set up decay model"""
        #Read the full SM
        model = copy.deepcopy(self.base_model)
        self.model = import_ufo.RestrictModel(model)
        self.restrict_file = os.path.join(_file_path, os.path.pardir,
                                     'input_files', 'restrict_sm.dat')
        self.model.set_parameters_and_couplings(self.restrict_file)
         
        
    def test_detect_zero_parameters(self):
        """ check that detect zero parameters works"""        
        
        expected = set(['MB', 'ymb', 'yb', 'WT'])
        result = set(self.model.detect_zero_parameters())
        
        self.assertEqual(expected, result)
        
        
    def test_detect_zero_couplings(self):
        """ check that detect zero couplings works"""
        
        expected = set(['GC_24'])
        result = set(self.model.detect_zero_couplings())
        
        self.assertEqual(expected, result)        
        
        
    def test_remove_couplings(self):
        """ check that the detection of irrelevant interactions works """
        
        # first test case where they are all deleted
        # check that we have the valid model
        input = self.model['interactions'][2]
        input2 = self.model['interactions'][25]
        self.assertTrue('GC_6' in input['couplings'].values())
        self.assertTrue('GC_24' in input2['couplings'].values())
        found_6 = 0
        found_24 = 0
        for dep,data in self.model['couplings'].items():
            for param in data:
                if param.name == 'GC_6': found_6 +=1
                elif param.name == 'GC_24': found_24 +=1
        self.assertTrue(found_6>0)
        self.assertTrue(found_24>0)
        
        # make the real test
        result = self.model.remove_couplings(['GC_24','GC_6'])
        self.assertFalse(input in self.model['interactions'])
        self.assertFalse(input2 in self.model['interactions'])
        
        for dep,data in self.model['couplings'].items():
            for param in data:
                self.assertFalse(param.name in  ['GC_6', 'GC_24'])
        
        # Now test case where some of them are deleted and some not
        input = self.model['interactions'][25]
        input2 = self.model['interactions'][38]
        self.assertTrue('GC_14' in input['couplings'].values())
        self.assertTrue('GC_12' in input['couplings'].values())
        self.assertTrue('GC_12' in input2['couplings'].values())
        self.assertTrue('GC_15' in input2['couplings'].values())
        result = self.model.remove_couplings(['GC_12','GC_15'])
        input = self.model['interactions'][25]
        self.assertTrue('GC_14' in input['couplings'].values())
        self.assertFalse('GC_12' in input['couplings'].values())
        self.assertFalse('GC_15' in input2['couplings'].values())
        self.assertFalse('GC_12' in input2['couplings'].values())

    def test_put_parameters_to_zero(self):
        """check that we remove parameters correctly"""
        
        part_t = self.model.get_particle(6)
        # Check that we remove a mass correctly
        self.assertEqual(part_t['mass'], 'MT')
        self.model.put_parameters_to_zero(['MT'])
        self.assertEqual(part_t['mass'], 'ZERO')
        for dep,data in self.model['parameters'].items():
            for param in data:
                self.assertNotEqual(param.name, 'MT')
        
        for particle in self.model['particles']:
            self.assertNotEqual(particle['mass'], 'MT')
                    
        for pdg, particle in self.model['particle_dict'].items():
            self.assertNotEqual(particle['mass'], 'MT')
        
        # Check that we remove a width correctly
        self.assertEqual(part_t['width'], 'WT')
        self.model.put_parameters_to_zero(['WT'])
        self.assertEqual(part_t['width'], 'ZERO')
        for dep,data in self.model['parameters'].items():
            for param in data:
                self.assertNotEqual(param.name, 'WT')

        for pdg, particle in self.model['particle_dict'].items():
            self.assertNotEqual(particle['width'], 'WT')        
        # Check that we can remove correctly other external parameter
        self.model.put_parameters_to_zero(['ymb','yb'])
        for dep,data in self.model['parameters'].items():
            for param in data:
                self.assertFalse(param.name in  ['ymb'])
                if param.name == 'yb':
                    param.expr == 'ZERO'
                        
    def test_restrict_from_a_param_card(self):
        """ check the full restriction chain in once """
        
        interaction = self.model['interactions'][25]
        
        self.model.restrict_model(self.restrict_file)
        
        # check remove interactions
        self.assertFalse(interaction in self.model['interactions'])
        
        # check remove parameters
        for dep,data in self.model['parameters'].items():
            for param in data:
                self.assertFalse(param.name in  ['yb','ymb','MB','WT'])

        # check remove couplings
        for dep,data in self.model['couplings'].items():
            for param in data:
                self.assertFalse(param.name in  ['GC_24'])

        # check masses
        part_b = self.model.get_particle(5)
        part_t = self.model.get_particle(6)
        self.assertEqual(part_b['mass'], 'ZERO')
        self.assertEqual(part_t['width'], 'ZERO')
                
        
        
        
        
        
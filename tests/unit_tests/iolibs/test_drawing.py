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
"""Unit test library for the routine creating the points position for the 
    diagram drawing and for the creation of the EPS file."""

from __future__ import division

# The following two lines (suitably modified) are needed to run the
# diagram generation using __main__
#import sys
#sys.path.append('/home/alwall/MadEvent/MG5/madevent_output')

import os
import pickle
import unittest

import madgraph.core.base_objects as base_objects
import madgraph.iolibs.drawing as drawing
import madgraph.iolibs.drawing_eps as draw_eps
import madgraph.iolibs.import_model_v4 as import_v4
import madgraph.iolibs.files as files

_file_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

# First define a valid model for Standard Model
_model = base_objects.Model()
# Import Particles information
_input_path = os.path.join(_file_path, '../input_files/v4_sm_particles.dat')
_model.set('particles', files.read_from_file(_input_path,
                                            import_v4.read_particles_v4))
# Import Interaction information
_input_path = os.path.join(_file_path , '../input_files/v4_sm_interactions.dat')
_model.set('interactions', files.read_from_file(_input_path, \
                                               import_v4.read_interactions_v4, \
                                               _model.get('particles')))

#===============================================================================
# TestTestFinder
#===============================================================================
class TestFeynmanLine(unittest.TestCase):
    """The TestCase class for the test the FeynmanLine"""

    def setUp(self):
        """ basic building of the class to test """

        self.my_line = drawing.FeynmanLine(11)
        myleglist = base_objects.LegList([base_objects.Leg({'id':3,
                                      'number':5,
                                      'state':True,
                                      'from_group':False})] * 10)
        self.mydict = {'id':3,
                      'legs':myleglist}
        self.vertex = base_objects.Vertex(self.mydict)
        self.my_vertex = drawing.VertexPoint(self.vertex) #extend class
        self.my_vertex2 = drawing.VertexPoint(self.vertex)

    @staticmethod
    def def_line(begin=[0, 0], end=[1, 1], id=11):
        """Fast way to have line with begin-end (each are list)"""

        myleglist = base_objects.LegList([base_objects.Leg({'id':id,
                                      'number':5,
                                      'state':True,
                                      'from_group':False})] * 10)
        mydict = {'id':3,
                      'legs':myleglist}
        vertex = base_objects.Vertex(mydict)

        my_line = drawing.FeynmanLine(id)
        my_vertex = drawing.VertexPoint(vertex)
        my_vertex.def_position(begin[0], begin[1])
        my_line.def_begin_point(my_vertex)

        my_vertex = drawing.VertexPoint(vertex)
        my_vertex.def_position(end[0], end[1])
        my_line.def_end_point(my_vertex)
        return my_line

    @staticmethod
    def def_model_line(id=22):
        """fast way to create a line with a link to a model"""

        leg = base_objects.Leg({'id': id, 'number': 1, 'state':False,
                            'from_group':False})
        #extend the leg to FeynmanLine Object
        my_line = drawing.FeynmanLine(leg.get('id'), base_objects.Leg(leg))
        my_line._def_model(_model)

        return my_line

    def def_full_line(self, id=22, begin=[0, 0], end=[1, 1]):
        """Fast way to define a complete line"""
        my_line = self.def_model_line(id)
        temp_line = self.def_line(begin, end)
        my_line.def_begin_point(temp_line.start)
        my_line.def_end_point(temp_line.end)

        return my_line

    def  test_def_begin_end_point(self):
        """Test assign/reassign/flip vertex associate to line"""

        #test begin point 
        self.my_line.def_begin_point(self.my_vertex)
        self.assertTrue(self.my_line.start is self.my_vertex)
        self.my_line.def_begin_point(self.my_vertex2)
        self.assertTrue(self.my_line.start is self.my_vertex2)

        #test end point
        self.my_line.def_end_point(self.my_vertex2)
        self.assertTrue(self.my_line.end is self.my_vertex2)
        self.my_line.def_end_point(self.my_vertex)
        self.assertTrue(self.my_line.end is self.my_vertex)

        #test if the vertex references the line correctly
        self.assertTrue(self.my_line in self.my_vertex.line)
        self.assertTrue(self.my_line in self.my_vertex2.line)

        #check that the swithching method runs fine.
        self.my_line.inverse_begin_end()
        self.assertTrue(self.my_line.start is self.my_vertex)
        self.assertTrue(self.my_line.end is self.my_vertex2)

    def test_begin_end_wrong_input(self):
        """Test associate vertex fails on wrong input"""

        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          self.my_line.def_begin_point, [0, 0])
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          self.my_line.def_end_point, [0, 0])

    def test_get_type(self):
        """Test associate line to the correct drawing mode"""

        #need to load SM?
        for id in [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15]:
            my_line = drawing.FeynmanLine(id)
            my_line.def_model(_model)
            self.assertEquals(my_line.get_info('line'), 'straight')

        for id in [25]:
            my_line = drawing.FeynmanLine(id)
            my_line.def_model(_model)
            self.assertEquals(my_line.get_info('line'), 'dashed')

        for id in [22, 23, 24, -23, -24]:
            my_line = drawing.FeynmanLine(id)
            my_line.def_model(_model)
            self.assertEquals(my_line.get_info('line'), 'wavy')

        for id in [21]:
            my_line = drawing.FeynmanLine(id)
            my_line.def_model(_model)
            self.assertEquals(my_line.get_info('line'), 'curly')

        id = [21, 22, 23, 24, -23, -24]
        solution = ['g', 'a', 'z', 'w-', 'z', 'w+']
        for i in range(0, len(id)):
            my_line = drawing.FeynmanLine(id[i])
            my_line.def_model(_model)
            self.assertEquals(my_line.get_name('name'), solution[i])


    def test_line_orientation(self):
        """Test define correct flow for S-channel"""

        line = self.def_line(id= -22)
        line.start.def_level(0)
        line.end.def_level(1)

        line.define_line_orientation()
        self.assertEqual(line.start.pos_x, 1)
        self.assertEqual(line.start.pos_y, 1)
        self.assertEqual(line.end.pos_x, 0)
        self.assertEqual(line.end.pos_y, 0)


        line.inverse_part_antipart()
        line.define_line_orientation()
        self.assertEqual(line.start.pos_x, 1)
        self.assertEqual(line.start.pos_y, 1)
        self.assertEqual(line.end.pos_x, 0)
        self.assertEqual(line.end.pos_y, 0)

    def test_inverse_part_antipart(self):
        """Test change particle in anti-particle"""

        line = self.def_line([0, 0], [0, 0])

        line.inverse_part_antipart()
        self.assertEquals(line.get('pid'), -11)
        line.inverse_part_antipart()
        self.assertEquals(line.get('pid'), 11)

    def test_inverse_pid_for_type(self):
        """Test change particle in anti-particle for drawing type"""

        line1 = self.def_model_line(id=24)
        line2 = self.def_model_line(id= -24)
        line3 = self.def_model_line(id=22)
        line4 = self.def_model_line(id=1)

        line1.inverse_pid_for_type('wavy')
        line2.inverse_pid_for_type('wavy')
        line3.inverse_pid_for_type('wavy')
        line4.inverse_pid_for_type('wavy')

        self.assertEquals(line1.get('pid'), -24)
        self.assertEquals(line2.get('pid'), 24)
        self.assertEquals(line3.get('pid'), -22)
        self.assertEquals(line4.get('pid'), 1)

        line1.inverse_pid_for_type()
        line2.inverse_pid_for_type()
        line3.inverse_pid_for_type()
        line4.inverse_pid_for_type()

        self.assertEquals(line1.get('pid'), -24)
        self.assertEquals(line2.get('pid'), 24)
        self.assertEquals(line3.get('pid'), -22)
        self.assertEquals(line4.get('pid'), -1)

    def test_domain_intersection(self):
        """ Test domain intersection between two FeynmanLine """

        my_line1 = self.def_line([0, 0], [1, 1])         #diagonal
        my_line2 = self.def_line([0.5, 0.5], [0.9, 0.9]) # part of the diagonal
        my_line3 = self.def_line([0.1, 0.5], [0.5, 1])# parallel to the diagonal
        my_line4 = self.def_line([0.0, 0.0], [0.0, 1.0]) # y axis 
        my_line5 = self.def_line([0.0, 0.0], [0.3, 0.2])


        self.assertEquals(my_line1.domain_intersection(my_line1), (0, 1))
        self.assertEquals(my_line1.domain_intersection(my_line2), (0.5, 0.9))
        self.assertEquals(my_line1.domain_intersection(my_line3), (0.1, 0.5))
        self.assertEquals(my_line1.domain_intersection(my_line4), (0, 0))
        self.assertEquals(my_line1.domain_intersection(my_line5), (0, 0.3))
        self.assertEquals(my_line2.domain_intersection(my_line3), (0.5, 0.5))
        self.assertEquals(my_line2.domain_intersection(my_line4), (None , None))
        self.assertEquals(my_line2.domain_intersection(my_line5), (None, None))
        self.assertEquals(my_line3.domain_intersection(my_line4), (None, None))
        self.assertEquals(my_line3.domain_intersection(my_line5), (0.1, 0.3))

        self.assertEquals(my_line1.domain_intersection(my_line4, 'x'), (0, 0))
        self.assertEquals(my_line1.domain_intersection(my_line4, 'y'), (0, 1))

    def test_domain_intersection_failure(self):
        """Test domain intersection fails on wrong input"""

        my_line1 = self.def_line([0, 0], [1, 1])
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                           my_line1.domain_intersection, [0, 1])
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                           my_line1.domain_intersection, (0, 1))
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                           my_line1.domain_intersection, ([0, 1], 1))

    def test_hasintersection(self):
        """Test FeynmanLine intersections returns correct value"""

        #def a set of line
        my_line1 = self.def_line([0, 0], [1, 1])         #diagonal
        my_line2 = self.def_line([0.5, 0.5], [0.9, 0.9]) # part of the diagonal
        my_line3 = self.def_line([0.1, 0.1], [0.4, 0.4]) # other part of the diagonal
        my_line4 = self.def_line([0, 0.5], [0.5, 1])     # parallel to the diagonal
        my_line5 = self.def_line([0.0, 0.0], [0.0, 1.0]) # y axis 
        my_line6 = self.def_line([0, 1], [1, 0])         # second diagonal
        my_line7 = self.def_line([0, 1], [0.6, 0.4])     # part of the second 
        my_line8 = self.def_line([0.6, 0.4], [0, 1])     # same part but inverse order
        my_line9 = self.def_line([0, 0.5], [0.9, 1])     # other
        my_line10 = self.def_line([0.5, 0.5], [0.5, 1])    # vertical line center
        my_line11 = self.def_line([0.5, 0], [0.5, 0.5])    # second part
        my_line12 = self.def_line([0.5, 0], [0.5, 0.4])     # just shorther


        #Line 1 intersection
        self.assertTrue(my_line1.has_intersection(my_line1))
        self.assertTrue(my_line1.has_intersection(my_line2))
        self.assertTrue(my_line1.has_intersection(my_line3))
        self.assertFalse(my_line1.has_intersection(my_line4))
        self.assertFalse(my_line1.has_intersection(my_line5)) #cross=begin point
        self.assertTrue(my_line1.has_intersection(my_line6))
        self.assertTrue(my_line1.has_intersection(my_line7))
        self.assertTrue(my_line1.has_intersection(my_line8))
        self.assertFalse(my_line1.has_intersection(my_line9))
        self.assertTrue(my_line1.has_intersection(my_line10))
        self.assertTrue(my_line1.has_intersection(my_line11))
        self.assertFalse(my_line1.has_intersection(my_line12))

        #Line2 intersection
        self.assertTrue(my_line2.has_intersection(my_line1))
        self.assertFalse(my_line2.has_intersection(my_line3))
        self.assertFalse(my_line2.has_intersection(my_line4))
        self.assertFalse(my_line2.has_intersection(my_line5))
        self.assertTrue(my_line2.has_intersection(my_line6))
        self.assertTrue(my_line2.has_intersection(my_line7))
        self.assertTrue(my_line2.has_intersection(my_line8))
        self.assertFalse(my_line2.has_intersection(my_line9))
        self.assertFalse(my_line2.has_intersection(my_line10))
        self.assertFalse(my_line2.has_intersection(my_line11))
        self.assertFalse(my_line2.has_intersection(my_line12))

        #Line3 intersection
        self.assertFalse(my_line3.has_intersection(my_line4))
        self.assertFalse(my_line3.has_intersection(my_line5))
        self.assertFalse(my_line3.has_intersection(my_line6))
        self.assertFalse(my_line3.has_intersection(my_line7))
        self.assertFalse(my_line3.has_intersection(my_line8))
        self.assertFalse(my_line3.has_intersection(my_line9))
        self.assertFalse(my_line3.has_intersection(my_line10))
        self.assertFalse(my_line3.has_intersection(my_line11))
        self.assertFalse(my_line3.has_intersection(my_line12))

        # Line 4 intersection
        self.assertTrue(my_line4.has_intersection(my_line5))
        self.assertTrue(my_line4.has_intersection(my_line6))
        self.assertTrue(my_line4.has_intersection(my_line7))
        self.assertTrue(my_line4.has_intersection(my_line8))
        self.assertFalse(my_line4.has_intersection(my_line9))
        self.assertFalse(my_line4.has_intersection(my_line10))
        self.assertFalse(my_line4.has_intersection(my_line11))
        self.assertFalse(my_line4.has_intersection(my_line12))


        # Line 5 intersection
        self.assertFalse(my_line5.has_intersection(my_line6))
        self.assertFalse(my_line5.has_intersection(my_line7))
        self.assertFalse(my_line5.has_intersection(my_line8))
        self.assertTrue(my_line5.has_intersection(my_line9))
        self.assertFalse(my_line5.has_intersection(my_line10))
        self.assertFalse(my_line5.has_intersection(my_line11))
        self.assertFalse(my_line5.has_intersection(my_line12))

        # Line 6 intersection
        self.assertTrue(my_line6.has_intersection(my_line7))
        self.assertTrue(my_line6.has_intersection(my_line8))
        self.assertTrue(my_line6.has_intersection(my_line9))
        self.assertTrue(my_line6.has_intersection(my_line10))
        self.assertTrue(my_line6.has_intersection(my_line11))
        self.assertFalse(my_line6.has_intersection(my_line12))

        #Line 7-8 intersection
        self.assertTrue(my_line7.has_intersection(my_line8))
        self.assertTrue(my_line8.has_intersection(my_line7))
        self.assertTrue(my_line7.has_intersection(my_line9))
        self.assertTrue(my_line7.has_intersection(my_line10))
        self.assertTrue(my_line8.has_intersection(my_line11))
        self.assertFalse(my_line7.has_intersection(my_line12))

        #line 9 intersection
        self.assertTrue(my_line9.has_intersection(my_line10))
        self.assertFalse(my_line9.has_intersection(my_line11))
        self.assertFalse(my_line9.has_intersection(my_line12))

        #line 10 intersection
        self.assertFalse(my_line10.has_intersection(my_line3))
        self.assertFalse(my_line10.has_intersection(my_line5))
        self.assertTrue(my_line10.has_intersection(my_line7))
        self.assertTrue(my_line10.has_intersection(my_line8))
        self.assertTrue(my_line10.has_intersection(my_line10))
        self.assertFalse(my_line10.has_intersection(my_line11))
        self.assertFalse(my_line10.has_intersection(my_line12))

        #line 11 intersection  
        self.assertTrue(my_line11.has_intersection(my_line12))


        #special set for testing error machine problem
        my_line1 = self.def_line([1.0, 0], [0.8, 2 / 3])
        my_line2 = self.def_line([0.8, 02 / 3], [1.0, 1])

        self.assertFalse(my_line1.has_intersection(my_line2))


    def test_domainintersection(self):
        """Test domain intersection is set correctly"""

        #def a set of line
        my_line1 = self.def_line([0, 0], [1, 1])         #diagonal
        my_line2 = self.def_line([0.5, 0.5], [0.9, 0.9]) # part of the diagonal
        my_line3 = self.def_line([0.1, 0.1], [0.4, 0.4]) # other part of the diagonal
        my_line4 = self.def_line([0, 0.5], [0.5, 1])     # parallel to the diagonal
        my_line5 = self.def_line([0.0, 0.0], [0.0, 1.0]) # y axis 
        my_line6 = self.def_line([0, 1], [1, 0])         # second diagonal
        my_line7 = self.def_line([0, 1], [0.6, 0.4])     # part of the second 
        my_line8 = self.def_line([0.6, 0.4], [0, 1])     # same part but inverse order
        my_line9 = self.def_line([0, 0.5], [0.9, 1])     # other

        #with line1 ->return line 2 domain
        self.assertEquals(my_line1.domain_intersection(my_line1), (0, 1))
        self.assertEquals(my_line1.domain_intersection(my_line2), (0.5, 0.9))
        self.assertEquals(my_line1.domain_intersection(my_line3), (0.1, 0.4))
        self.assertEquals(my_line1.domain_intersection(my_line4), (0.0, 0.5))
        self.assertEquals(my_line1.domain_intersection(my_line5), (0.0, 0.0))
        self.assertEquals(my_line1.domain_intersection(my_line6), (0.0, 1.0))
        self.assertEquals(my_line1.domain_intersection(my_line7), (0, 0.6))
        self.assertEquals(my_line1.domain_intersection(my_line8), (0, 0.6))
        self.assertEquals(my_line1.domain_intersection(my_line9), (0, 0.9))

        #with line 5 =>(0,0) at max
        self.assertEquals(my_line5.domain_intersection(my_line2), (None, None))
        self.assertEquals(my_line5.domain_intersection(my_line3), (None, None))
        self.assertEquals(my_line5.domain_intersection(my_line4), (0.0, 0.0))
        self.assertEquals(my_line5.domain_intersection(my_line5), (0.0, 0.0))
        self.assertEquals(my_line5.domain_intersection(my_line6), (0.0, 0.0))
        self.assertEquals(my_line5.domain_intersection(my_line7), (0, 0.0))
        self.assertEquals(my_line5.domain_intersection(my_line8), (0, 0.0))
        self.assertEquals(my_line5.domain_intersection(my_line9), (0, 0.0))

    def test_get_length(self):
        """Test if we can compute the length of a line."""
 
        my_line1 = self.def_line([0.1, 0.1], [0.4, 0.1]) #horizontal
        my_line2 = self.def_line([0.1, 0.1], [0.4, 0.5]) #normal
        my_line3 = self.def_line([0, 0.5], [0, 1])       

        self.assertAlmostEqual(my_line1.get_length(),0.3)
        self.assertAlmostEqual(my_line2.get_length(),0.5)
        self.assertAlmostEqual(my_line3.get_length(),0.5)

    def test_hasordinate(self):
        """Test if we can recover the ordinate at any position"""

        my_line1 = self.def_line([0.1, 0.1], [0.4, 0.1]) #horizontal
        my_line3 = self.def_line([0.1, 0.1], [0.4, 0.4]) #normal
        my_line4 = self.def_line([0, 0.5], [0.5, 1])

        #returns correct value
        self.assertEquals(my_line1.has_ordinate(0.2), 0.1)
        self.assertEquals(my_line1.has_ordinate(0.1), 0.1)
        self.assertEquals(my_line3.has_ordinate(0.2), 0.2)
        self.assertEquals(my_line3.has_ordinate(0.1), 0.1)
        self.assertEquals(my_line4.has_ordinate(0.5), 1)

    def test_hasordinate_wronginput(self):
        """Test has_ordinate on incorrext input"""

        my_line1 = self.def_line([0.1, 0.1], [0.4, 0.2]) #random
        my_line2 = self.def_line([0.1, 0.1], [0.1, 0.4]) #vertical 

        #fail if asked outside range
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line1.has_ordinate, -2)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line1.has_ordinate, 1.2)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line1.has_ordinate, 0.05)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line1.has_ordinate, 0.5)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, -2)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, 1.2)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, 0.05)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, 0.5)

        #fails for vertical line
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, 0.1)

        #fails if not real value
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, 'a')
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, [0, 0.2])
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_ordinate, my_line1)


    def test_has_ordinate_failure(self):
        """Test error raising if no vertex before position related operation"""

        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          self.my_line.has_ordinate, 0.5)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          self.my_line.has_intersection, self.my_line)

        #check intersection if one is valid
        my_line2 = self.def_line([0.1, 0.1], [0.4, 0.2]) #random
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          my_line2.has_intersection, self.my_line)
        self.assertRaises(drawing.FeynmanLine.FeynmanLineError, \
                          self.my_line.has_intersection, my_line2)

#===============================================================================
# TestVertex
#===============================================================================
class TestVertexPoint(unittest.TestCase):
    """The TestCase class for testing VertexPoint"""

    def setUp(self):
        """basic building of the class to test"""

        self.line1 = drawing.FeynmanLine(11)
        self.line2 = drawing.FeynmanLine(11)
        self.line3 = drawing.FeynmanLine(11)
        self.line4 = drawing.FeynmanLine(11)
        self.myleglist = base_objects.LegList([base_objects.Leg({'id':3,
                                      'number':5,
                                      'state':True,
                                      'from_group':False})] * 10)
        self.mydict = {'id':3,
                      'legs':self.myleglist}
        self.vertex = base_objects.Vertex(self.mydict)

    def test_building(self):
        """Test the correct creation of FeynmanVertex object"""

        my_vertex = drawing.VertexPoint(self.vertex)
        # Test the File has the correct link with basic object
        self.assertTrue(isinstance(my_vertex, base_objects.Vertex))
        self.assertTrue(isinstance(my_vertex, drawing.VertexPoint))

        # Test fail if not Vertex Input in data
        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          drawing.VertexPoint, {'data':''})

        # Ensure that my_vertex and self.vertex and 100% different
        self.assertFalse(my_vertex is self.vertex)
        my_vertex['value'] = 2
        self.assertRaises(base_objects.PhysicsObject.PhysicsObjectError,
                          self.vertex.__getitem__, 'value')
        self.assertTrue('value' in my_vertex.keys())
        self.assertFalse('value' in self.vertex.keys())

        # Check that we have new attributes
        self.assertTrue(hasattr(my_vertex, 'line'))
        self.assertTrue('id' in my_vertex.keys())
        self.assertTrue(hasattr(my_vertex, 'pos_x'))
        self.assertTrue(hasattr(my_vertex, 'pos_x'))

        # Check that we recreate a vertex from the same vertex they are 
        #different.
        my_vertex2 = drawing.VertexPoint(self.vertex)
        self.assertFalse(my_vertex2 is self.vertex)
        self.assertFalse(my_vertex2 is my_vertex)

        # Check that adding a line acts only on one vertex.
        my_vertex.add_line(self.line1)
        self.assertFalse(self.line1 in my_vertex2.line)



    def test_def_position(self):
        """Test assignment of a position to a vertex"""

        my_vertex = drawing.VertexPoint(self.vertex)
        my_vertex.def_position(0.1, 0.3)
        self.assertEqual(my_vertex.pos_x, 0.1)
        self.assertEqual(my_vertex.pos_y, 0.3)
        #check border are corectly define (no error raises
        my_vertex.def_position(0, 0.3)
        my_vertex.def_position(0, 0)
        my_vertex.def_position(0, 1)
        my_vertex.def_position(1, 0)
        my_vertex.def_position(1, 0.3)
        my_vertex.def_position(1, 1)
        my_vertex.def_position(0.3, 0)
        my_vertex.def_position(0.3, 1)

        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          my_vertex.def_position, 1.4, 0.2)
        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          my_vertex.def_position, -1.0, 0.2)
        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          my_vertex.def_position, 0.4, 1.2)
        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          my_vertex.def_position, 0, -0.2)

    def test_redef_position(self):
        """Test if redefine vertex position is fine"""
        # Check that lambda function linked to Line are correctly remove
        #Note: This lambda function is not use anymore

        my_vertex = drawing.VertexPoint(self.vertex)
        my_vertex.def_position(0.1, 0.3)
        my_vertex2 = drawing.VertexPoint(self.vertex)
        my_vertex2.def_position(0.4, 0.6)
        self.line1.def_begin_point(my_vertex)
        self.line1.def_end_point(my_vertex2)
        self.assertAlmostEquals(self.line1.has_ordinate(0.2), 0.4)
        my_vertex2.def_position(0.3, 0.6)
        self.assertFalse(hasattr(self, "ordinate_fct"))
        #self.assertRaises(self.line1.ordinate_fct,0)
        self.assertAlmostEquals
        (self.line1.has_ordinate(0.2), 0.45)

    def test_add_line(self):
        """Test if wa can safely add a line to a Vertex"""

        my_vertex = drawing.VertexPoint(self.vertex)
        my_vertex.add_line(self.line1)

        self.assertTrue(self.line1 in my_vertex.line)
        my_vertex.add_line(self.line1)
        self.assertEquals(my_vertex.line.count(self.line1), 1)

        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                                                    my_vertex.add_line, 'data')

    def test_remove_line(self):
        """Test that line can be safely remove"""

        my_vertex = drawing.VertexPoint(self.vertex)
        my_vertex.line = [self.line1]
        my_vertex.remove_line(self.line1)
        self.assertFalse(self.line1 in my_vertex.line)

        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          my_vertex.remove_line, self.line1)
        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                                                    my_vertex.add_line, 'data')


    def test_def_level(self):
        """Test the level assignment """

        my_vertex = drawing.VertexPoint(self.vertex)
        my_vertex.def_level(3)
        self.assertEquals(my_vertex.level, 3)

        self.assertRaises(drawing.VertexPoint.VertexPointError, \
                          my_vertex.def_level, '3')

    def test_isexternal(self):
        """Test if can distinguish the vertex type"""

        vertex = base_objects.Vertex({'id':0, 'legs':base_objects.LegList([])})
        vertexpoint = drawing.VertexPoint(vertex)
        leg1 = base_objects.Leg({'id':22, 'number':1, 'state':False,
                            'from_group':False})
        line1 = drawing.FeynmanLine(22, leg1)
        line1.def_begin_point(vertexpoint)

        self.assertTrue(vertexpoint.is_external())

    def test_fuse_vertex(self):
        """Test if it's possible to fuse two vertex"""

        # Test diagram gg>gg via a S-channel
        leg1 = base_objects.Leg({'id':22, 'number':1, 'state':False,
                            'from_group':False})
        leg2 = base_objects.Leg({'id':22, 'number':2, 'state':False,
                            'from_group':False})
        leg3 = base_objects.Leg({'id':22, 'number':3, 'state':True,
                            'from_group':False})
        leg4 = base_objects.Leg({'id':22, 'number':4, 'state':True,
                            'from_group':False})

        #intermediate particle +vertex associate
        leg_s = base_objects.Leg({'id':22, 'number':1, 'state':True,
                        'from_group':True})
        vertex1 = base_objects.Vertex({'id':1, \
                        'legs':base_objects.LegList([leg1, leg2, leg_s])})


        vertex2 = base_objects.Vertex({'id':2, \
                        'legs':base_objects.LegList([leg_s, leg3, leg4])})

        #pass in Drawing object
        vertex1 = drawing.VertexPoint(vertex1)
        vertex2 = drawing.VertexPoint(vertex2)
        line1 = drawing.FeynmanLine(22, leg1)
        line2 = drawing.FeynmanLine(22, leg2)
        line3 = drawing.FeynmanLine(22, leg3)
        line4 = drawing.FeynmanLine(22, leg4)
        line_s = drawing.FeynmanLine(22, leg_s)

        #link object
        line1.def_end_point(vertex1)
        line2.def_end_point(vertex1)
        line_s.def_begin_point(vertex1)
        line_s.def_end_point(vertex2)
        line3.def_begin_point(vertex2)
        line4.def_begin_point(vertex2)

        #fuse the two vertex
        vertex1.fuse_vertex(vertex2, line_s)

        #check that vertex1.line is correctly modify
        self.assertEqual(len(vertex1.line), 4)
        self.assertEqual(len([l for l in vertex1.line if l is line1]), 1)
        self.assertEqual(len([l for l in vertex1.line if l is line2]), 1)
        self.assertEqual(len([l for l in vertex1.line if l is line3]), 1)
        self.assertEqual(len([l for l in vertex1.line if l is line4]), 1)
        self.assertEqual(len([l for l in vertex1.line if l is line_s]), 0)

        #check that line3-line4 begin vertex are correctly modify
        self.assertTrue(vertex1 is line3.start)
        self.assertTrue(vertex1 is line4.start)
        self.assertTrue(vertex1 is line1.end)
        self.assertTrue(vertex1 is line2.end)


#===============================================================================
# TestVertex
#===============================================================================
class TestFeynmanDiagram(unittest.TestCase):
    """Test the object which compute the position of the vertex/line 
        for a given Diagram object
    """

    #test diagram gg>gg via a T-channel
    leg1 = base_objects.Leg({'id':22, 'number':1, 'state':False,
                            'from_group':False})
    leg2 = base_objects.Leg({'id':22, 'number':2, 'state':False,
                            'from_group':False})
    leg3 = base_objects.Leg({'id':22, 'number':3, 'state':True,
                            'from_group':False})
    leg4 = base_objects.Leg({'id':22, 'number':4, 'state':True,
                            'from_group':False})

    #intermediate particle +vertex associate
    leg_t1 = base_objects.Leg({'id':22, 'number':1, 'state':False,
                        'from_group':True})
    vertex1 = base_objects.Vertex({'id':1, \
                        'legs':base_objects.LegList([leg1, leg3, leg_t1])})

    leg_t2 = base_objects.Leg({'id':22, 'number':2, 'state':False,
                        'from_group':True})
    vertex2 = base_objects.Vertex({'id':2, \
                        'legs':base_objects.LegList([leg2, leg4, leg_t2])})

    vertex3 = base_objects.Vertex({'id':0, \
                        'legs':base_objects.LegList([leg_t1, leg_t2])})

    vertexlist = base_objects.VertexList([vertex1, vertex2, vertex3])
    t_diagram_dict = {'vertices':vertexlist}

    #test diagram gg>gg via a S-channel
    leg1 = base_objects.Leg({'id':22, 'number':1, 'state':False,
                            'from_group':False})
    leg2 = base_objects.Leg({'id':22, 'number':2, 'state':False,
                            'from_group':False})
    leg3 = base_objects.Leg({'id':22, 'number':3, 'state':True,
                            'from_group':False})
    leg4 = base_objects.Leg({'id':22, 'number':4, 'state':True,
                            'from_group':False})

    #intermediate particle +vertex associate
    leg_s = base_objects.Leg({'id':22, 'number':1, 'state':True,
                        'from_group':True})
    vertex1 = base_objects.Vertex({'id':1, \
                        'legs':base_objects.LegList([leg1, leg2, leg_s])})

    leg_temp = base_objects.Leg({'id':22, 'number':1, 'state':True,
                            'from_group':False})

    vertex2 = base_objects.Vertex({'id':2, \
                        'legs':base_objects.LegList([leg_s, leg3, leg_temp])})

    vertex3 = base_objects.Vertex({'id':0, \
                        'legs':base_objects.LegList([leg_temp, leg4])})

    vertexlist = base_objects.VertexList([vertex1, vertex2, vertex3])
    s_diagram_dict = {'vertices':vertexlist}


    # Recover some diagram causing crashes or having some interesting feature
    #in order to ensure that those problem will not appear again. 
    #Those diagrams were keep in a pickle format"""
    filehandler = open(os.path.join(_file_path, \
                                    '../input_files/test_draw.obj'), 'r')
    store_diagram = pickle.load(filehandler)



    def setUp(self):
        """Basic building of the object needed to build the test"""

        opt=drawing.DrawOption({'external':1,'horizontal':1,'max_size':0})
        # gg>g(g>uux)g (via a T channel)  
        mix_diagram = self.store_diagram['g g > g g u u~'][18]
        self.mix_drawing = drawing.FeynmanDiagram(mix_diagram, _model, opt)

        # gg>gg (via a T channel)
        t_diagram = self.store_diagram['g g > g g'][2]
        #t_diagram = base_objects.Diagram(self.t_diagram_dict)
        self.t_drawing = drawing.FeynmanDiagram(t_diagram, _model, opt)

        # gg>gg (via a S channel)
        s_diagram = self.store_diagram['g g > g g'][1]
        #s_diagram = base_objects.Diagram(self.s_diagram_dict)
        self.s_drawing = drawing.FeynmanDiagram(s_diagram, _model, opt)

    def test_load_diagram(self):
        """ Test update of a diagram to a drawing class """

        # check len of output
        self.mix_drawing.load_diagram()
        self.assertEqual(len(self.mix_drawing.vertexList), 10)
        self.assertEqual(len(self.mix_drawing.lineList), 9)

        self.t_drawing.load_diagram()
        self.assertEqual(len(self.t_drawing.vertexList), 6)
        self.assertEqual(len(self.t_drawing.lineList), 5)

        self.s_drawing.load_diagram()
        self.assertEqual(len(self.s_drawing.vertexList), 6)
        self.assertEqual(len(self.s_drawing.lineList), 5)

        #check type of object
        for obj in self.mix_drawing.vertexList:
            self.assertTrue(isinstance(obj, drawing.VertexPoint))
        for obj in self.mix_drawing.lineList:
            self.assertTrue(isinstance(obj, drawing.FeynmanLine))

        #check that the load correctly assign the model to the Line
        for line in self.mix_drawing.lineList:
            self.assertTrue(hasattr(line, 'model'))
            
    def test_dealing_with_last_line(self):
        """ check that we deal correctly with format coming from decaychains"""
        
        diagram = self.store_diagram['e- e+ > t t~, t > w+ b'][0]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        #call the function
        diagram.load_diagram()        
        self.assertEqual(len(diagram.lineList), 7)
        

    @staticmethod
    def vertex_identification(vertex):
        """return a integer which acts like an id"""

        tag = 0
        for i, line in enumerate(vertex.line):
            tag += (10 ** i) * line.get('number')
        return tag


    def test_line_ordering_in_load(self):
        """Test the default orientation of the line after the load process"""

        self.mix_drawing.load_diagram()
        self.mix_drawing.define_level()
        self.mix_drawing.find_initial_vertex_position()
        begin_tag = [1, 131, 131, 2, 242, 521, 565, 565, 521]
        end_tag = [131, 3, 521, 242, 4, 242, 5, 6, 565]
        for i, line in enumerate(self.mix_drawing.lineList):
            self.assertEquals(self.vertex_identification(line.start), \
                                                                   begin_tag[i])
            self.assertEquals(self.vertex_identification(line.end), \
                                                                   end_tag[i])


        diagram = self.store_diagram['g g > g g g g'][26]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()
        tag = [(1, 131), (131, 3), (131, 251), (2, 242), (242, 4), (262, 242), (251, 5),
             (262, 6), (251, 262)]

        for i, line in enumerate(diagram.lineList):
            self.assertEquals(self.vertex_identification(line.start), \
                                                                   tag[i][0])
            self.assertEquals(self.vertex_identification(line.end), \
                                                                   tag[i][1])

    def test_define_level(self):
        """ Test level assignment """

        self.mix_drawing.load_diagram()

        self.mix_drawing.define_level()

        #order: initial-external-vertex in diagram order                                 
        level_solution = [1, 1, 2, 1, 0, 2, 0, 2, 3, 3]
        number_of_line = [3, 3, 3, 3, 1, 1, 1, 1, 1, 1]
        # the ordering is not important but we test it anyway in order 
        # to ensure that we don't have any wrong permutation
        self.assertEquals(self.mix_drawing.max_level, 3)
        for i in range(0, 10):
            self.assertEquals(self.mix_drawing.vertexList[i].level, \
                                                            level_solution[i])
            self.assertEquals(len(self.mix_drawing.vertexList[i].line), \
                                                            number_of_line[i])

        self.s_drawing.load_diagram()
        self.s_drawing.define_level()

        #order: initial-external-vertex in diagram order                                 
        level_solution = [1, 2, 0, 0, 3, 3]

        for i in range(0, 6):
            self.assertEquals(self.s_drawing.vertexList[i].level, \
                                                            level_solution[i])
        self.assertEquals(self.s_drawing.max_level, 3)

        self.t_drawing.load_diagram()
        self.t_drawing.define_level()

        #order: initial-external-vertex in diagram order                                 
        level_solution = [1, 1, 0, 2, 0, 2]
        self.assertEquals(self.t_drawing.max_level, 2)
        for i in range(0, 6):
            self.assertEquals(self.t_drawing.vertexList[i].level, \
                                                            level_solution[i])


    def test_find_vertex_at_level(self):
        """Test correct evolution from one level to the next one. 
            Check in the same time the position assign
            on a ordered list of vertex."""

        self.mix_drawing.load_diagram()
        self.mix_drawing.define_level()

        #define by hand level 0:
        vertexlist_l0 = [vertex for vertex in self.mix_drawing.vertexList if\
                                                         vertex.level == 0 ]
        vertexlist_l0.reverse()

        #define by hand level 1:
        sol_l1 = [vertex for vertex in self.mix_drawing.vertexList if\
                                                         vertex.level == 1 ]
        #wrong order
        sol_l1[1], sol_l1[2] = sol_l1[2], sol_l1[1]

        #ask to find level 1 from level 0
        vertexlist_l1 = self.mix_drawing.find_t_channel_vertex()
        self.assertEquals(len(vertexlist_l1), len(sol_l1))
        for i in range(0, len(sol_l1)):
            self.assertEquals(vertexlist_l1[i], sol_l1[i])

        #redo this step but add the position to those vertex
        self.mix_drawing.find_vertex_position_tchannel()

        sol = [[1 / 3, 1 / 6], [1 / 3, 1 / 2], [1 / 3, 5 / 6]]
        for i in range(0, len(vertexlist_l1)):
            vertex = vertexlist_l1[i]

            self.assertAlmostEquals(vertex.pos_x, sol[i][0])
            self.assertAlmostEquals(vertex.pos_y, sol[i][1])

        vertexlist_l2 = self.mix_drawing.find_vertex_at_level(vertexlist_l1)
        self.assertEquals(len(vertexlist_l2), 3)

        #ask to update of level 2 +check that wa can assign position
        self.mix_drawing.find_vertex_position_at_level(vertexlist_l1, 2, auto=0)

        #check position
        vertexlist = [vertex for vertex in self.mix_drawing.vertexList if\
                                                         vertex.level == 2 ]
        sol = [[2 / 3, 0.5], [2 / 3, 0], [2 / 3, 1]]
        ext = [False, True, True]
        for i in range(0, len(vertexlist)):
            vertex = vertexlist[i]

            self.assertEquals(vertex.pos_x, sol[i][0])
            self.assertEquals(vertex.pos_y, sol[i][1])
            self.assertEquals(vertex.is_external(), ext[i]) #more a test of the \
                # order and of is_external

    def test_find_t_channel_vertex(self):
        """Test that the routines finding T-vertex in correct order"""

        diagram = self.store_diagram['g g > g g g g'][26]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.load_diagram()
        diagram.define_level()
        level0 = [vertex for vertex in diagram.vertexList if vertex.level == 0]
        level1 = [vertex for vertex in diagram.vertexList if vertex.level == 1]

        #sanity check
        self.assertEquals(len(diagram.vertexList), 10)
        self.assertEquals(len(level1), 4)
        #test the routine
        level0.reverse()
        t_vertex = diagram.find_t_channel_vertex()

        for vertex in t_vertex:
            self.assertTrue(vertex.level, 1)
            self.assertFalse(vertex in level0)

        self.assertEquals(len(t_vertex), 4)
        level1.sort()
        t_vertex.sort()
        self.assertEquals(level1, t_vertex)


    def test_find_initial_vertex_position(self):
        """Test if find the correct position for vertex"""

        self.mix_drawing.load_diagram()
        self.mix_drawing.define_level()
        self.mix_drawing.find_initial_vertex_position()

        level = [1  , 1  , 2  , 1  , 0  , 2  , 0  , 2  , 3  , 3 ]
        x_position = [1 / 3, 1 / 3, 2 / 3, 1 / 3, 0.0, 2 / 3, 0.0, 2 / 3, 1.0, 1.0]
        y_position = [1 / 6, 5 / 6, 1 / 2, 1 / 2, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0]


        for i in range(0, 10):
            self.assertEquals(self.mix_drawing.vertexList[i].level, \
                              level[i])
            self.assertAlmostEquals(self.mix_drawing.vertexList[i].pos_x, \
                              x_position[i])
            self.assertAlmostEquals(self.mix_drawing.vertexList[i].pos_y, \
                              y_position[i])

    def test_creation_from_cmd(self):
        """Test basic diagram comming from (old) cmd works"""

        diagram = self.store_diagram['u d~ > c s~'][0]
        diagram = drawing.FeynmanDiagram(diagram, _model)

        diagram.load_diagram()
        diagram.define_level()
        level_solution = [1, 2, 0, 0, 3, 3]
        for i in range(0, 6):
            self.assertEquals(diagram.vertexList[i].level, \
                              level_solution[i])
        diagram.find_initial_vertex_position()
        level_solution = [1, 2, 0, 0, 3, 3]
        x_position = [1 / 3, 2 / 3, 0, 0, 1, 1]
        y_position = [1 / 2, 1 / 2, 0, 1, 0, 1]
        self.assertEquals(len(diagram.vertexList), 6)
        for i in range(0, 6):
            self.assertEquals(diagram.vertexList[i].level, \
                              level_solution[i])
            self.assertAlmostEquals(diagram.vertexList[i].pos_x, \
                              x_position[i])
            self.assertAlmostEquals(diagram.vertexList[i].pos_y, \
                              y_position[i])
        for line in diagram.lineList:
            self.assertNotEquals(line.start, None)
            self.assertNotEquals(line.end, None)


        diagram = self.store_diagram['g g > g g g g g g'][73]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()

        nb_at_zero = 0
        for vertex in diagram.vertexList:
            if vertex.pos_x == 0  and vertex.pos_y == 0:
                nb_at_zero += 1
        self.assertEqual(nb_at_zero, 1)


    def test_one_initial_state_particle(self):
        """Test if we can create diagram for one particle in initial state."""

        diagram = self.store_diagram['mu- > vm e- ve~'][0]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()

        # Check that all line are defined
        nb_at_zero = 0
        for vertex in diagram.vertexList:
            if vertex.pos_x == 0  and vertex.pos_y == 0:
                nb_at_zero += 1
        self.assertEqual(nb_at_zero, 0)

        # Check that we didn't have T-channel
        nb_at_level_one = 0
        for vertex in diagram.vertexList:
            if vertex.level == 1:
                nb_at_level_one += 1
        self.assertEqual(nb_at_level_one, 1)

        # Check that no line cross another
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['mu- > vm e- ve~'][0]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()


        #check that all line are defined
        nb_at_zero = 0
        for vertex in diagram.vertexList:
            if vertex.pos_x == 0  and vertex.pos_y == 0:
                nb_at_zero += 1
        self.assertEqual(nb_at_zero, 0)


        # Check that we didn't have T-channel
        nb_at_level_one = 0
        for vertex in diagram.vertexList:
            if vertex.level == 1:
                nb_at_level_one += 1
        self.assertEqual(nb_at_level_one, 1)

        # Check that no line cross another
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['d > d d g d~ QED=0'][0]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        
        #check that all line are defined
        nb_at_zero = 0
        for vertex in diagram.vertexList:
            if vertex.pos_x == 0  and vertex.pos_y == 0:
                nb_at_zero += 1
        self.assertEqual(nb_at_zero, 0)


        # Check that we didn't have T-channel
        nb_at_level_one = 0
        for vertex in diagram.vertexList:
            if vertex.level == 1:
                nb_at_level_one += 1
        self.assertEqual(nb_at_level_one, 1)

        # Check that no line cross another
        self.assertFalse(diagram._debug_has_intersection())


    def test_notion_of_egality(self):
        """Test if not failing on wrongly equal leg"""

        global _file_path

        #_cmd.do_generate('g g > g g')

        #test the S-channel
        #diagram = _cmd.curr_amp['diagrams'][1]
        diagram = self.store_diagram['g g > g g'][1]

        diagram = drawing.FeynmanDiagram(diagram, _model)

        diagram.load_diagram()
        diagram.define_level()
        level_solution = [1, 2, 0, 0, 3, 3]
        for i in range(0, 6):
            self.assertEquals(diagram.vertexList[i].level, \
                              level_solution[i])
        diagram.find_initial_vertex_position()
        x_position = [1 / 3, 2 / 3, 0, 0, 1, 1]
        y_position = [1 / 2, 1 / 2, 0, 1, 0, 1]
        self.assertEquals(len(diagram.vertexList), 6)
        for i in range(0, 6):
            self.assertEquals(diagram.vertexList[i].level, \
                              level_solution[i])
            self.assertAlmostEquals(diagram.vertexList[i].pos_x, \
                              x_position[i])
            self.assertAlmostEquals(diagram.vertexList[i].pos_y, \
                              y_position[i])
        for line in diagram.lineList:
            self.assertNotEquals(line.start, None)
            self.assertNotEquals(line.end, None)

        #test the T-channel
        diagram = self.store_diagram['g g > g g'][2]
        diagram = drawing.FeynmanDiagram(diagram, _model)

        diagram.load_diagram()
        diagram.define_level()
        level_solution = [1, 1, 0, 2, 0, 2]
        for i in range(0, 6):
            self.assertEquals(diagram.vertexList[i].level, \
                              level_solution[i])
        diagram.find_initial_vertex_position()

        x_position = [1 / 2, 1 / 2, 0, 1, 0, 1]
        y_position = [1 / 4, 3 / 4, 0, 0, 1, 1]
        self.assertEquals(len(diagram.vertexList), 6)
        for i in range(0, 6):
            self.assertEquals(diagram.vertexList[i].level, \
                              level_solution[i])
            self.assertAlmostEquals(diagram.vertexList[i].pos_x, \
                              x_position[i])
            self.assertAlmostEquals(diagram.vertexList[i].pos_y, \
                              y_position[i])
        for line in diagram.lineList:
            self.assertNotEquals(line.start, None)
            self.assertNotEquals(line.end, None)

    def test_fermion_flow(self):
        """Test Fermion-flow is working in T-channel"""

        # Load diagram with one fermion flow
        diagram = self.store_diagram['mu+ mu- > w+ w- a'][7]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        t_lines = [line for line in diagram.lineList if line.start.level == 1
                                                and line.end.level == 1]

        for line in t_lines:
            if line.is_fermion():
                self.assertTrue(line.start.pos_y > line.end.pos_y)

        # Load diagram with two fermion flow
        diagram = self.store_diagram['mu+ mu- > w+ w- a'][6]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        t_lines = [line for line in diagram.lineList if line.start.level == 1
                                                and line.end.level == 1]

        for line in t_lines:
            if line.is_fermion():
                self.assertTrue(line.start.pos_y > line.end.pos_y)

        # One fermion flow but in opposite direction
        diagram = self.store_diagram['g g > g g u u~'][100]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        t_lines = [line for line in diagram.lineList if line.start.level == 1
                                                and line.end.level == 1]

        for line in t_lines:
            if line.is_fermion():
                self.assertTrue(line.start.pos_y > line.end.pos_y)
                
        # Two fermion in opposite direction
        diagram = self.store_diagram['u u > Z u u g'][26]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        t_lines = [line for line in diagram.lineList if line.start.level == 1
                                                and line.end.level == 1]
        
        for line in t_lines:
            if line.is_fermion():
                self.assertTrue(line.start.pos_y > line.end.pos_y)
                
        
        # Two fermion in opposite direction
        diagram = self.store_diagram['u~ u~ > Z u~ u~ g'][26]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        t_lines = [line for line in diagram.lineList if line.start.level == 1
                                                and line.end.level == 1]
        
        for line in t_lines:
            if line.is_fermion():
                self.assertTrue(line.start.pos_y < line.end.pos_y)           

    def test_diagram_equality(self):
        """Test if the diagram equalities work"""
        
        diagram_list = []
        for i in range(8):
            diagram = self.store_diagram['t h > t g W+ W-'][i]
            diagram = drawing.FeynmanDiagram(diagram, _model)
            diagram.main()
            diagram_list.append(diagram)
            
        for i in range(8):
            for j in range(i,8):
                if i == j:
                    self.assertTrue(diagram_list[i] == diagram_list[j])
                else:
                    self.assertFalse(diagram_list[i] == diagram_list[j])
                    
                    
        diagram_list = []
        for i in range(2):
            diagram = self.store_diagram['g g > g g g'][i]
            diagram = drawing.FeynmanDiagram(diagram, _model)
            diagram.main()
            diagram_list.append(diagram)
            
        for i in range(2):
            for j in range(i,2):
                if i == j:
                    self.assertTrue(diagram_list[i] == diagram_list[j])
                else:
                    self.assertFalse(diagram_list[i] == diagram_list[j])

    def test_no_cutting_line(self):
        """Test that the output diagram doesn't intersection between line."""

        diagram = self.store_diagram['g g > g g g g g g'][73]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g g g g g'][2556]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g u u~'][18]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g u u~'][100]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g g g'][0]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())
        self.assertEqual(len(diagram.lineList),8)

        diagram = self.store_diagram['g g > g g g g'][0]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g g g'][26]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g g g'][92]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g g g'][93]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['g g > g g g g'][192]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['mu+ mu- > w+ w- a'][6]
        diagram = drawing.FeynmanDiagram(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        diagram = self.store_diagram['mu+ mu- > w+ w- a'][7]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.main()
        self.assertFalse(diagram._debug_has_intersection())

        for i in range(7):
            diagram = self.store_diagram['t h > t g W+ W-'][i]
            diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
            diagram.main()
            self.assertFalse(diagram._debug_has_intersection())

            diagram = self.store_diagram['t h > t g W+ W-'][i]
            diagram = drawing.FeynmanDiagram(diagram, _model)
            diagram.main()
            self.assertFalse(diagram._debug_has_intersection())
        
    def test_non_integer_external(self):
        """Test that the an non integer value for external works normally."""
        
        #T-channel in one level
        diagram = self.store_diagram['u~ u~ > e+ e- u~ u~ g'][1]
        option = drawing.DrawOption({'external':1.5})
        diagram = drawing.FeynmanDiagram(diagram, _model,opt=option)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()
        diagram.adjust_position()
        
        #check that all line end at y=1
        for line in diagram.lineList:
            if line.is_external() and line.get('number') > 2:
                self.assertEquals(line.end.pos_x,1)

        #T-chanel (3 T-vertex and the central decay in 2 level decay)
        diagram = self.store_diagram['u~ u~ > e+ e- u~ u~ g'][8]
        option = drawing.DrawOption({'external':1.5, 'max_size':0})
        diagram = drawing.FeynmanDiagram(diagram, _model,opt=option)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()
        diagram.adjust_position()
        for line in diagram.lineList:
            if line.is_external() and line.get('number') in [5,7]:
                dist=(line.end.pos_x-line.start.pos_x)*diagram.max_level
                self.assertEquals(dist,1.5)
        
        
        
        
        
    def test_horizontal_mode(self):
        """Test that the horizontal mode works correctly."""

        # For all diagram, first test that only initial state particle have
        #x=0 coordinate

        # Simply standard verification in this case.
        diagram = self.store_diagram['g g > g g g'][0]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()

        vertex_list = [vertex for vertex in diagram.vertexList if \
                                                              vertex.level != 0 ]
        for vertex in vertex_list:
            self.assertFalse(vertex.pos_x == 0)

        # Simply standard verification in this case.
        diagram = self.store_diagram['g g > g g g g'][192]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()

        vertex_list = [vertex for vertex in diagram.vertexList if \
                                                              vertex.level != 0 ]
        for vertex in vertex_list:
            self.assertFalse(vertex.pos_x == 0)

        # Standard verification + test position of external particles on border
        diagram = self.store_diagram['g g > g g g g'][93]
        opt = drawing.DrawOption({'external':1,'max_size':0})
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model, opt)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()

        vertex_list = [vertex for vertex in diagram.vertexList if \
                                                              vertex.level != 0 ]
        for vertex in vertex_list:
            self.assertFalse(vertex.pos_x == 0)

        # Check if the position of the external line on the below order works 
        vertex_at_x_0 = [vertex for vertex in vertex_list if vertex.pos_y == 0]
        self.assertEquals(len(vertex_at_x_0), 2)

        # Standard verification + test external should finish on a border
        diagram = self.store_diagram['g g > g g g g'][92]
        diagram = drawing.FeynmanDiagramHorizontal(diagram, _model)
        diagram.load_diagram()
        diagram.define_level()
        diagram.find_initial_vertex_position()

        vertex_list = [vertex for vertex in diagram.vertexList if \
                                                              vertex.level != 0 ]
        for vertex in vertex_list:
            self.assertFalse(vertex.pos_x == 0)
            x = vertex.pos_x
            y = vertex.pos_y
            if vertex.is_external():
                self.assertEquals((x - 1) * (y) * (y - 1), 0)
            else:
                self.assertNotEquals((x - 1) * (y) * (y - 1), 0)


#===============================================================================
# TestDrawingEPS
#===============================================================================
class TestDrawingOption(unittest.TestCase):
    """Sanity check for all combination of option. This check on a small sample
    of diagram that no line have zero lenght and that we don't have any line 
    crossing for any combination of option."""

    # Made a set of diagram available here
    store_diagram = TestFeynmanDiagram.store_diagram
    
    def schedular(self, diagram):
        """Test that the DrawingEPS returns valid result"""
        
        horizontal_list = [True, False]
        external_list = [0,1,1.5]
        contract_unpropa_list =[True, False]
        max_size_list = [0,1.8]
        
        opt = drawing.DrawOption()
        for horizontal in horizontal_list:
            opt.set('horizontal', horizontal)
            for external in external_list:
                opt.set('external',external)
                for contract_unpropa in contract_unpropa_list:
                    opt.set('contract_non_propagating',contract_unpropa)
                    for max_size in max_size_list:
                        opt.set('max_size',max_size)
                        
                        plot = draw_eps.EpsDiagramDrawer(diagram, \
                                        '__testdiag__.eps', model=_model, \
                                         amplitude='')
                        plot.draw(opt)
                        self.assertFalse(\
                                    plot.diagram._debug_has_intersection())
                        for line in plot.diagram.lineList:
                            self.assertNotAlmostEquals(line.get_length(), 0)
                            
    def test_option_6g(self):
        """Test that gg>6g is fine with all options"""
        diagram = self.store_diagram['g g > g g g g g g'][73]
        self.schedular(diagram)
        
    def test_option_6g_second(self):
        """Test that gg>6g is fine with all options"""
        diagram = self.store_diagram['g g > g g g g g g'][2556]
        self.schedular(diagram)   
        
    def test_option_multi_type(self):
        """Test that t h > t g W+ W-  is fine with all options"""
        diagram = self.store_diagram['t h > t g W+ W-'][0] 
        self.schedular(diagram)        
          
#===============================================================================
# TestDrawingS_EPS
#===============================================================================
class TestDrawingS_EPS(unittest.TestCase):
    """ Class testing if we can create the files in the EPS mode for a set
        of diagrams.
    
    This test the following two points:
    1) can we create the output file?
    2) can we convert him in pdf? (Imagemagick is needed for this)
        checking that the file is valid."""

    # Made a set of diagram available here
    store_diagram = TestFeynmanDiagram.store_diagram


    def setUp(self):
        """Charge a diagram to draw"""

        self.diagram = base_objects.DiagramList()
        for i in range(7):
            self.diagram.append(self.store_diagram['t h > t g W+ W-'][i])

        self.plot = draw_eps.MultiEpsDiagramDrawer(self.diagram, '__testdiag__.eps', \
                                          model=_model, amplitude='')
        
        
    def output_is_valid(self, position, pdf_check=True):
        """Test if the output files exist. 
        Additionally if pdf_check is on True
        check if we can convert the output file in pdf. Finally delete files."""

        # Check if exist
        self.assertTrue(os.path.isfile(position))

        # Check if the file is valid
        if pdf_check:
            filename, ext = os.path.splitext('position')
            os.system('convert ' + position + ' ' + filename + '.pdf')

            # Try is use to ensure that no file are left on disk
            try:
                self.assertTrue(os.path.isfile(filename + '.pdf'))
            except:
                os.remove(position)
                raise
            os.remove(filename + '.pdf')
        os.remove(position)
        return
    
    def test_schedular(self):
        """Test the multidiagram drawing"""
        
        opt = drawing.DrawOption()
        self.setUp()
        self.plot.draw(opt=opt)
        self.output_is_valid('__testdiag__.eps')


if __name__ == '__main__':

    # For debugging it's interesting to store problematic diagram in one file.
    #Those one are generated with cmd and store in files with pickle module.

    process_diag = {}
    process_diag['mu- > vm e- ve~'] = [0]
    process_diag['d > d d g d~ QED=0'] = [0]
    process_diag['u d~ > c s~'] = [0]
    process_diag['g g > g g'] = [1, 2]
    process_diag['g g > g g g'] = [0, 1]
    process_diag['g g > g g u u~'] = [18, 100]
    process_diag['g g > g g g g'] = [0, 26, 92, 93, 192]
    process_diag['g g > g g g g g g'] = [73, 2556]
    process_diag['mu+ mu- > w+ w- a'] = [6, 7]
    process_diag['t h > t g W+ W-'] = [0, 1, 2, 3, 4, 5, 6, 7]
    process_diag['u u > Z u u g'] = [26]
    process_diag['u~ u~ > Z u~ u~ g'] = [26]
    process_diag['u~ u~ > e+ e- u~ u~ g'] = [1,8]

    from madgraph.interface.cmd_interface import MadGraphCmd
    cmd = MadGraphCmd()
    cmd.do_import('v4 ' + os.path.join(_file_path, \
                                        '../input_files/v4_sm_particles.dat'))
    cmd.do_import('v4 ' + os.path.join(_file_path, \
                                    '../input_files/v4_sm_interactions.dat'))

    # Create the diagrams
    diag_content = {}
    for gen_line, pos_list in process_diag.items():
        print gen_line, ':',
        cmd.do_generate(gen_line)
        diag_content[gen_line] = {}
        for pos in pos_list:
            diag_content[gen_line][pos] =cmd._MadGraphCmd__curr_amps[0]['diagrams'][pos]

    # Store the diagrams  
    file_test_diagram = open(os.path.join(_file_path , \
                                    '../input_files/test_draw.obj'), 'w')
    pickle.dump(diag_content, file_test_diagram)
    print 'done'






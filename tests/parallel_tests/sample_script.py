#! /usr/bin/env python
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

"""A sample script running a comparison between different ME generators using
objects and routines defined in me_comparator. To define your own test case, 
simply modify this script. Support for new ME generator is achieved through
inheritance of the MERunner class.
"""

import logging
import logging.config
import pydoc
import os
import sys

#Look for MG5/MG4 path
mg5_path = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-3])
print mg5_path
sys.path.append(mg5_path)

import me_comparator
from madgraph import MG4DIR
mg4_path = MG4DIR



if '__main__' == __name__: 
    # Get full logging info
    logging.config.fileConfig(os.path.join(mg5_path, 'tests', '.mg5_logging.conf'))
    logging.root.setLevel(logging.INFO)
    logging.getLogger('madgraph').setLevel(logging.INFO)
    logging.getLogger('cmdprint').setLevel(logging.INFO)
    logging.getLogger('tutorial').setLevel(logging.ERROR)
        
    logging.basicConfig(level=logging.INFO)
#    my_proc_list = me_comparator.create_proc_list_enhanced(
##        ['w+', 'w-', 'z'],
##        initial=2, final_1=2)
    my_proc_list = ['e- x1+ > e- h1 x1+','e- x1+ > e- h2 x1+','e- x1+ > e- h3 x1+',
                    'e+ x1+ > e+ h1 x1+','e+ x1+ > e+ h2 x1+','e+ x1+ > e+ h3 x1+']
    my_proc_list += ['el+ h2 > el+ w+ w-', 'w+ w- > ta1+ ta1-']
    my_proc_list += ['u u~ > u u~ g']
                   
    my_proc_list += me_comparator.create_proc_list(['g', 'go'], initial=2,
                                                  final=3)
    #my_proc_list = me_comparator.create_proc_list(['g', 'h', 'h3'], initial=2,
    #                                               final=4)
    

    # Create a MERunner object for MG4
    my_mg4 = me_comparator.MG4Runner()
    my_mg4.setup(mg4_path)

    # Create a MERunner object for MG5
    my_mg5 = me_comparator.MG5Runner()
    my_mg5.setup(mg5_path, mg4_path)

    # Create a MERunner object for UFO-ALOHA-MG5
    my_mg5_ufo = me_comparator.MG5_UFO_Runner()
    my_mg5_ufo.setup(mg5_path, mg4_path)

    # Create a MERunner object for C++
    #my_mg5_cpp = me_comparator.MG5_CPP_Runner()
    #my_mg5_cpp.setup(mg5_path, mg4_path)

    # Create and setup a comparator
    my_comp = me_comparator.MEComparator()
    my_comp.set_me_runners(my_mg4, my_mg5, my_mg5_ufo)

    # Run the actual comparison
    my_comp.run_comparison(my_proc_list,
                           model='mssm',
                           orders={'QED':4, 'QCD':4}, energy=2000)

    # Do some cleanup
    #my_comp.cleanup()
    filename='mssm_results2.log'

    # Print the output
    my_comp.output_result(filename=filename)
    pydoc.pager(file(filename,'r').read())

    # Print a list of non zero processes
    #print my_comp.get_non_zero_processes()


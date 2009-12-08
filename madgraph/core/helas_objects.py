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

import copy
import logging
import re
import itertools

import madgraph.core.base_objects as base_objects
import madgraph.core.diagram_generation as diagram_generation

"""Definitions of objects used to generate Helas calls (language-independent):
HelasWavefunction, HelasAmplitude, HelasDiagram for the generation of
wavefunctions and amplitudes;
HelasParticle, HelasInteraction, HelasModel are language-independent
base classes for the language-specific classes found in the
iolibs directory"""

#===============================================================================
# 
#===============================================================================

#===============================================================================
# HelasWavefunction
#===============================================================================
class HelasWavefunction(base_objects.PhysicsObject):
    """HelasWavefunction object, has the information necessary for
    writing a call to a HELAS wavefunction routine: the PDG number,
    all relevant particle information, a list of mother wavefunctions,
    interaction id, all relevant interaction information, fermion flow
    state, wavefunction number
    """

    def default_setup(self):
        """Default values for all properties"""

        # Properties related to the particle propagator
        self['pdg_code'] = 0
        self['name'] = 'none'
        self['antiname'] = 'none'
        self['spin'] = 1
        self['color'] = 1
        self['mass'] = 'zero'
        self['width'] = 'zero'
        self['is_part'] = True
        self['self_antipart'] = False
        # Properties related to the interaction generating the propagator
        self['interaction_id'] = 0
        self['inter_color'] = []
        self['lorentz'] = []
        self['couplings'] = { (0, 0):'none'}
        self['conjugate_couplings'] = { (0, 0):'none'}
        self['pdg_codes'] = []
        self['conjugate_pdg_codes'] = []
        # Properties relating to the leg/vertex
        self['state'] = 'incoming'
        self['mothers'] = HelasWavefunctionList()
        self['number_external'] = 0
        self['number'] = 0
        self['fermionflow'] = 1
        
    # Customized constructor
    def __init__(self, *arguments):
        """Allow generating a HelasWavefunction from a Leg
        """

        if len(arguments) > 2:
            if isinstance(arguments[0], base_objects.Leg) and \
                   isinstance(arguments[1], int) and \
                   isinstance(arguments[2], base_objects.Model):
                super(HelasWavefunction, self).__init__()
                leg = arguments[0]
                interaction_id = arguments[1]
                model = arguments[2]
                self.set('pdg_code', leg.get('id'), model)
                self.set('number_external', leg.get('number'))
                self.set('number', leg.get('number'))
                self.set('state', leg.get('state'))
                # Set fermion flow state. Initial particle and final
                # antiparticle are incoming, and vice versa for
                # outgoing
                if self.get('spin') % 2 == 0:
                    if leg.get('state') == 'initial' and \
                           self.get('is_part') or \
                           leg.get('state') == 'final' and \
                           not self.get('is_part'):
                        self.set('state', 'incoming')
                    else:
                        self.set('state', 'outgoing')
                # For boson, set state to initial/final
                # If initial state, flip PDG code (if has antipart)
                # since all bosons should be treated as outgoing
                #else:
                #    if leg.get('state') == 'initial':
                #        self.set('is_part',not self.get('is_part'))
                #        if not self.get('self_antipart'):
                #            self.set('pdg_code', -self.get('pdg_code'))
                self.set('interaction_id', interaction_id, model)
        elif arguments:
            super(HelasWavefunction, self).__init__(arguments[0])
            # Set couplings separately, since it needs to be set after
            # color and lorentz
            if 'couplings' in arguments[0].keys():
                self.set('couplings', arguments[0]['couplings'])
            if 'conjugate_couplings' in arguments[0].keys():
                self.set('conjugate_couplings', arguments[0]['conjugate_couplings'])
        else:
            super(HelasWavefunction, self).__init__()
   
    def filter(self, name, value):
        """Filter for valid wavefunction property values."""

        if name == 'pdg_code':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                      "%s is not a valid pdg_code for wavefunction" % \
                      str(value)

        if name in ['name', 'antiname']:
            # Must start with a letter, followed by letters,  digits,
            # - and + only
            p = re.compile('\A[a-zA-Z]+[\w]*[\-\+]*~?\Z')
            if not p.match(value):
                raise self.PhysicsObjectError, \
                        "%s is not a valid particle name" % value

        if name is 'spin':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                    "Spin %s is not an integer" % repr(value)
            if value < 1 or value > 5:
                raise self.PhysicsObjectError, \
                   "Spin %i is smaller than one" % value

        if name is 'color':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                    "Color %s is not an integer" % repr(value)
            if value not in [1, 3, 6, 8]:
                raise self.PhysicsObjectError, \
                   "Color %i is not valid" % value

        if name in ['mass', 'width']:
            # Must start with a letter, followed by letters, digits or _
            p = re.compile('\A[a-zA-Z]+[\w\_]*\Z')
            if not p.match(value):
                raise self.PhysicsObjectError, \
                        "%s is not a valid name for mass/width variable" % \
                        value

        if name in ['is_part', 'self_antipart']:
            if not isinstance(value, bool):
                raise self.PhysicsObjectError, \
                    "%s tag %s is not a boolean" % (name, repr(value))

        if name == 'interaction_id':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                        "%s is not a valid integer for wavefunction interaction id" % str(value)

        if name in ['inter_color', 'lorentz']:
            #Should be a list of strings
            if not isinstance(value, list):
                raise self.PhysicsObjectError, \
                        "%s is not a valid list of strings" % str(value)
            for mystr in value:
                if not isinstance(mystr, str):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid string" % str(mystr)

        if name in ['couplings', 'conjugate_couplings']:
            #Should be a dictionary of strings with (i,j) keys
            if not isinstance(value, dict):
                raise self.PhysicsObjectError, \
                        "%s is not a valid dictionary for couplings" % \
                                                                str(value)

            if len(value) != len(self['inter_color']) * len(self['lorentz']):
                raise self.PhysicsObjectError, \
                        "Dictionary " + str(value) + \
                        " for couplings has not the right number of entry"

            for key in value.keys():
                if not isinstance(key, tuple):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid tuple" % str(key)
                if len(key) != 2:
                    raise self.PhysicsObjectError, \
                        "%s is not a valid tuple with 2 elements" % str(key)
                if not isinstance(key[0], int) or not isinstance(key[1], int):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid tuple of integer" % str(key)
                if key[0] < 0 or key[1] < 0 or \
                   key[0] >= len(self['inter_color']) or key[1] >= \
                                                    len(self['lorentz']):
                    raise self.PhysicsObjectError, \
                        "%s is not a tuple with valid range" % str(key)
                if not isinstance(value[key], str):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid string" % str(mystr)

        if name in ['pdg_codes', 'conjugate_pdg_codes']:
            #Should be a list of integers
            if not isinstance(value, list):
                raise self.PhysicsObjectError, \
                        "%s is not a valid list of integers" % str(value)
            for mystr in value:
                if not isinstance(mystr, int):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid integer" % str(mystr)

        if name == 'state':
            if not isinstance(value, str):
                raise self.PhysicsObjectError, \
                        "%s is not a valid string for wavefunction state" % \
                                                                    str(value)
            if value not in ['incoming', 'outgoing',
                             'intermediate', 'initial', 'final']:
                raise self.PhysicsObjectError, \
                        "%s is not a valid wavefunction state (incoming|outgoing|intermediate)" % \
                                                                    str(value)
        if name == 'fermionflow':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                        "%s is not a valid integer for wavefunction number" % str(value)
            if not value in [-1,0,1]:
                raise self.PhysicsObjectError, \
                        "%s is not a valid fermionflow (must be -1, 0 or 1)" % str(value)                

        if name in ['number_external', 'number']:
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                        "%s is not a valid integer for wavefunction number" % str(value)

        if name == 'mothers':
            if not isinstance(value, HelasWavefunctionList):
                raise self.PhysicsObjectError, \
                      "%s is not a valid list of mothers for wavefunction" % \
                      str(value)

        return True

    # Enhanced set function, where we can append a model

    def set(self, *arguments):
        """When setting interaction_id, if model is given (in tuple),
        set all other interaction properties. When setting pdg_code,
        if model is given, set all other particle properties."""

        if len(arguments) < 2:
            raise self.PhysicsObjectError, \
                  "Too few arguments for set"

        name = arguments[0]
        value = arguments[1]
        
        if len(arguments) > 2 and \
               isinstance(value, int) and \
               isinstance(arguments[2], base_objects.Model):
            if name == 'interaction_id':
                self.set('interaction_id', value)
                if value > 0:
                    inter = arguments[2].get('interaction_dict')[value]
                    self.set('inter_color', inter.get('color'))
                    self.set('lorentz', inter.get('lorentz'))
                    self.set('couplings', inter.get('couplings'))
                    self.set('pdg_codes',sorted([\
                        part.get_pdg_code() for part in \
                        inter.get('particles')]))
                    if not inter.get('conjugate_interaction'):
                        raise self.PhysicsObjectError,\
                              "Interaction %d has no conjugate_interaction" % \
                              repr(inter.get('id'))
                    conj_inter = arguments[2].get('interaction_dict')[\
                        inter.get('conjugate_interaction')]
                    self.set('conjugate_couplings',
                             conj_inter.get('couplings'))
                    self.set('conjugate_pdg_codes',sorted([\
                        part.get_pdg_code() for part in \
                        conj_inter.get('particles')]))
                return True
            elif name == 'pdg_code':
                self.set('pdg_code', value)
                part = arguments[2].get('particle_dict')[value]
                self.set('name', part.get('name'))
                self.set('antiname', part.get('antiname'))
                self.set('spin', part.get('spin'))
                self.set('color', part.get('color'))
                self.set('mass', part.get('mass'))
                self.set('width', part.get('width'))
                self.set('is_part', part.get('is_part'))
                self.set('self_antipart', part.get('self_antipart'))
                return True
            else:
                raise self.PhysicsObjectError, \
                      "%s not allowed name for 3-argument set", name
        else:
            return super(HelasWavefunction, self).set(name, value)

    def get_sorted_keys(self):
        """Return particle property names as a nicely sorted list."""

        return ['pdg_code', 'name', 'antiname', 'spin', 'color',
                'mass', 'width', 'is_part', 'self_antipart',
                'interaction_id', 'inter_color', 'lorentz',
                'couplings', 'conjugate_couplings',
                'state', 'number_external', 'number', 'fermionflow', 'mothers']

    # Helper functions

    def set_state_and_particle(self, model):
        """Set incoming/outgoing state according to mother states and
        Lorentz structure of the interaction, and set PDG code
        according to the particles in the interaction"""

        if not isinstance(model, base_objects.Model):
            raise self.PhysicsObjectError, \
                  "%s is not a valid model for call to set_state_and_particle" \
                  % repr(model)
        # Start by setting the state of the wavefunction
        if self.get('spin') % 2 == 1:
            # For boson, set state to intermediate
            self.set('state', 'intermediate')
        else:
            # For fermion, set state to same as other fermion (in the right way)
            mother_fermions = filter(lambda wf: wf.get('spin') % 2 == 0,
                                     self.get('mothers'))
            if len(filter(lambda wf: wf.get_with_flow('state') == 'incoming',
                          self.get('mothers'))) > \
                          len(filter(lambda wf: \
                                     wf.get_with_flow('state') == 'outgoing',
                          self.get('mothers'))):
                # If more incoming than outgoing mothers,
                # Pick one with incoming state as mother and set flow
                # Note that this needs to be done more properly if we have
                # 4-fermion vertices
                mother = filter(lambda wf: \
                                wf.get_with_flow('state') == 'incoming',
                                self.get('mothers'))[0]
            else:
                # If more outgoing than incoming mothers,
                # Pick one with outgoing state as mother and set flow
                mother = filter(lambda wf: \
                                wf.get_with_flow('state') == 'outgoing',
                                self.get('mothers'))[0]
            self.set('state', mother.get('state'))
            self.set('fermionflow', mother.get('fermionflow'))

        # We want the particle created here to go into the next
        # vertex, so we need to flip identity for incoming
        # antiparticle and outgoing particle.
        if not self.get('self_antipart') and \
               (self.get('state') == 'incoming' and not self.get('is_part') \
                or self.get('state') == 'outgoing' and self.get('is_part')):
            self.set('pdg_code', -self.get('pdg_code'), model)

        # For a boson, flip code (since going into next vertex)
        #if not self.get('self_antipart') and \
        #       self.get('spin') % 2 == 1:
        #    self.set('pdg_code', -self.get('pdg_code'), model)

        return True
        
    def check_and_fix_fermion_flow(self,
                                   wavefunctions,
                                   diagram_wavefunctions,
                                   external_wavefunctions):
        """Check for clashing fermion flow (N(incoming) !=
        N(outgoing)) in mothers
        """

        #return self.get('mothers').check_and_fix_fermion_flow(\
        #                           wavefunctions,
        #                           diagram_wavefunctions,
        #                           external_wavefunctions,
        #                           self.get_with_flow('state'),
        #                           self.get_outgoing_pdg_code())

        # Clash is defined by whether the mothers have N(incoming) !=
        # N(outgoing) after this state has been subtracted, OR
        # the pdg codes for the interaction don't work with flow

        mother_states = [ wf.get_with_flow('state') for wf in \
                          self.get('mothers') ]

        if self.get_with_flow('state') in mother_states:
            mother_states.remove(self.get_with_flow('state'))

        Nincoming = len(filter(lambda state: state == 'incoming',
                               mother_states))
        Noutgoing = len(filter(lambda state: state == 'outgoing',
                               mother_states))

        pdg_codes = [wf.get_pdg_code_outgoing() for wf in \
                     self.get('mothers')]
        pdg_codes.append(self.get_pdg_code_incoming())
        pdg_codes.sort()

        if Nincoming == Noutgoing and \
               pdg_codes == self.get_with_flow('pdg_codes'):
            print 'Ok! ', pdg_codes,\
                  self.get_with_flow('pdg_codes')

            return self

        print 'Need flip wf: ', Nincoming, Noutgoing, pdg_codes,\
              self.get_with_flow('pdg_codes'), self.get('pdg_code'), \
              self.get_pdg_code_incoming()

        # Start by checking if the problem is this particle
        if Nincoming == Noutgoing and \
           pdg_codes == self.get_with_flow('conjugate_pdg_codes'):
            if not self.get('spin') % 2 == 0:
                raise self.PhysicsObjectError, \
                      "Error: Need to flip fermion flow of boson"
            new_wf = self.flip_flow(wavefunctions,
                                    diagram_wavefunctions,
                                    external_wavefunctions)
            pdg_codes = [wf.get_pdg_code_outgoing() for wf in \
                         new_wf.get('mothers')]
            pdg_codes.append(new_wf.get('pdg_code'))
            pdg_codes.sort()

            if not pdg_codes == new_wf.get_with_flow('pdg_codes'):
                raise self.PhysicsObjectError,\
                      "Error: Flipped flow did not do it: %s != %s" %\
                      (repr(pdg_codes), repr(new_wf.get_with_flow('pdg_codes')))
            return new_wf

        if self.get_pdg_code_incoming() not in self.get_with_flow('pdg_codes'):
            raise self.PhysicsObjectError,\
                  "Error: Self-code not in pdg codes!"
        
        # Check if the pdg codes are ok:
        if pdg_codes != self.get_with_flow('pdg_codes'):        

            reduced_pdg_codes = copy.copy(pdg_codes)        

            # Remove boson codes
            for wf in filter(lambda wf: wf.get('spin') % 2 == 1,self.get('mothers')):
                reduced_pdg_codes.remove(wf.get_pdg_code_outgoing())
            if self.get('spin') % 2 == 1:
                reduced_pdg_codes.remove(self.get_pdg_code_incoming())

            # Fermion mothers
            fermion_mothers = filter(lambda wf: wf.get('spin') % 2 == 0,
                                self.get('mothers'))
        
            # Find the erraneous code
            for mother in fermion_mothers:
                if mother.get_pdg_code_outgoing() in reduced_pdg_codes:
                    reduced_pdg_codes.remove(mother.get_pdg_code_outgoing())
                else:
                    # This mother needs to get the fermion flow code flipped
                    new_mother = mother.flip_flow(wavefunctions,
                                     diagram_wavefunctions,
                                     external_wavefunctions)
                    # Replace old mother with new mother
                    self.get('mothers')[self.get(mothers).index(mother)] = new_mother
                    reduced_pdg_codes.remove(new_mother.get_pdg_code_outgoing())
            if reduced_pdg_codes:
                raise self.PhysicsObjectError, \
                      "Problem with bosonic mothers!"

        mother_states = [ wf.get_with_flow('state') for wf in \
                          self.get('mothers') ]

        if self.get_with_flow('state') in mother_states:
            mother_states.remove(my_state)

        Nincoming = len(filter(lambda state: state == 'incoming',
                               mother_states))
        Noutgoing = len(filter(lambda state: state == 'outgoing',
                               mother_states))

        while Nincoming != Noutgoing:
            # Flip flow of first mother with wrong flow.
            if Nincoming > Noutgoing:
                flow_mothers = filter(lambda wf: \
                                          wf.get('spin') % 2 == 0 and \
                                          wf.get_with_flow('state') == 'incoming',
                                          self.get('mothers'))
            else:
                flow_mothers = filter(lambda wf: \
                                          wf.get('spin') % 2 == 0 and \
                                          wf.get_with_flow('state') == 'outgoing',
                                          self.get('mothers'))
            new_mother = flow_mothers[0].flip_flow(wavefunctions,
                                          diagram_wavefunctions,
                                          external_wavefunctions)

            # Replace old mother with new mother
            self.get('mothers')[self.get('mothers').index(\
                flow_mothers[0])] = new_mother

            mother_states = [ wf.get_with_flow('state') for wf in \
                              self.get('mothers') ]
            
            if self.get_with_flow('state') in mother_states:
                mother_states.remove(my_state)
                
            Nincoming = len(filter(lambda state: state == 'incoming',
                                       mother_states))
            Noutgoing = len(filter(lambda state: state == 'outgoing',
                                       mother_states))
            print 'pdg_codes: ',pdg_codes 
            print 'self.pdg_codes: ',self.get_with_flow('pdg_codes')
            print 'fermionflow: ',self.get('fermionflow')
            print 'Nincoming: ',Nincoming, ' Noutgoing: ',Noutgoing

        return self
            
    def check_majorana_and_flip_flow(self, found_majorana,
                                     wavefunctions,
                                     diagram_wavefunctions,
                                     external_wavefunctions):
        """Recursive function. Check for Majorana fermion. If found,
        continue down to external leg, then flip all the fermion flows
        on the way back up.
        """

        if not found_majorana:
            found_majorana = self.get('self_antipart')

        new_wf = self
        flip_flow = False
        #flip_sign = False
        
        # Stop recursion at the external leg
        mothers = copy.copy(self.get('mothers'))
        if not mothers:
            flip_flow = found_majorana
        else:
            # Follow fermion flow up through tree
            fermion_mother = filter(lambda wf: wf.get('spin') % 2 == 0 and
                                     wf.get_with_flow('state') == \
                                     self.get_with_flow('state'),
                                     mothers)

            if len(fermion_mother) > 1:
                raise self.PhysicsObjectError,\
                      "6-fermion vertices not yet implemented"
            if len(fermion_mother) == 0:
                raise self.PhysicsObjectError,\
                      "Previous unresolved fermion flow in mother chain"
            
            # Perform recursion by calling on mother
            new_mother = fermion_mother[0].check_majorana_and_flip_flow(\
                found_majorana,
                wavefunctions,
                diagram_wavefunctions,
                external_wavefunctions)

            # If mother is Majorana and has different fermion flow, it means
            # that we should from now on in the chain flip the particle id
            # and flow state
            # Otherwise, if mother has different fermion flow, flip flow
            flip_flow = new_mother.get('fermionflow') != self.get('fermionflow')
            #flip_flow = new_mother.get('fermionflow') != self.get('fermionflow') \
            #            and not new_mother.get('self_antipart')
            #flip_sign = new_mother.get('fermionflow') != self.get('fermionflow') \
            #            and new_mother.get('self_antipart') or \
            #            new_mother.get('state') != self.get('state')
                        
            # Replace old mother with new mother
            mothers[mothers.index(fermion_mother[0])] = new_mother
                
        # Flip sign if needed
        if flip_flow: #or flip_sign:
            if self in wavefunctions:
                # Need to create a new copy
                new_wf = copy.copy(self)
                # Wavefunction number is given by: number of external
                # wavefunctions + number of non-external wavefunctions
                # in wavefunctions and diagram_wavefunctions
                number = len(external_wavefunctions) + 1
                number = number + len(filter(lambda wf: \
                                             wf not in external_wavefunctions.values(),
                                         wavefunctions))
                number = number + len(filter(lambda wf: \
                                             wf not in external_wavefunctions.values(),
                                         diagram_wavefunctions))
                new_wf.set('number',number)
                new_wf.set('mothers',mothers)                
                if new_wf not in wavefunctions:
                    diagram_wavefunctions.append(new_wf)

            # Now flip flow or sign
            if flip_flow:
                new_wf.set('fermionflow', -new_wf.get('fermionflow'))

            #if flip_sign:
            #    new_wf.set('state', filter(lambda state: \
            #                               state != self.get('state'),
            #                               ['incoming', 'outgoing'])[0])
            #    if not new_wf.get('self_antipart'):
            #        new_wf.set('pdg_code', -new_wf.get('pdg_code'))

        # Return the new (or old) wavefunction
        return new_wf

    def flip_flow(self,
                  wavefunctions,
                  diagram_wavefunctions,
                  external_wavefunctions):
        """Recursive function. Trace fermion flow down to external
        leg, then flip all the fermion flows on the way back up.
        """

        print "flip_flow called for ", self.get('pdg_code')

        new_wf = self

        # Stop recursion at the external leg
        mothers = copy.copy(self.get('mothers'))
        if mothers:
            # Follow fermion flow up through tree
            fermion_mother = filter(lambda wf: wf.get('spin') % 2 == 0 and
                                     wf.get_with_flow('state') == \
                                     self.get_with_flow('state'),
                                     mothers)

            if len(fermion_mother) > 1:
                raise self.PhysicsObjectError,\
                      "6-fermion vertices not yet implemented"
            if len(fermion_mother) == 0:
                raise self.PhysicsObjectError,\
                      "Previous unresolved fermion flow in mother chain"
            
            # Perform recursion by calling on mother
            new_mother = fermion_mother[0].flip_flow(\
                wavefunctions,
                diagram_wavefunctions,
                external_wavefunctions)

            # Replace old mother with new mother
            mothers[mothers.index(fermion_mother[0])] = new_mother
                
        # Flip fermion flow
        if self in wavefunctions:
            # Need to create a new copy
            new_wf = copy.copy(self)
            # Wavefunction number is given by: number of external
            # wavefunctions + number of non-external wavefunctions
            # in wavefunctions and diagram_wavefunctions
            number = len(external_wavefunctions) + 1
            number = number + len(filter(lambda wf: \
                                         wf not in external_wavefunctions.values(),
                                         wavefunctions))
            number = number + len(filter(lambda wf: \
                                         wf not in external_wavefunctions.values(),
                                         diagram_wavefunctions))
            new_wf.set('number',number)
            new_wf.set('mothers',mothers)                
            # Now flip flow
            new_wf.set('fermionflow', -new_wf.get('fermionflow'))
            if new_wf not in wavefunctions:
                diagram_wavefunctions.append(new_wf)
            else:
                new_wf = wavefunctions[wavefunctions.index(new_wf)]
        else:
            new_wf.set('mothers',mothers)
            # Flip flow
            new_wf.set('fermionflow', -new_wf.get('fermionflow'))
            if new_wf in wavefunctions:
                new_wf = wavefunctions[wavefunctions.index(new_wf)]
                diagram_wavefunctions.remove(new_wf)

        print "Flipped flow of ",new_wf

        # Return the new (or old) wavefunction
        return new_wf

    def needs_hermitian_conjugate(self):
        """Returns true if there is a fermion flow clash, i.e.,
        there is an odd number of negative fermion flows"""
        
        if self.get('mothers'):
            return self.get('fermionflow')*\
                   reduce(lambda x, y: x * y,
                          [ wf.get('fermionflow') for wf in \
                            self.get('mothers') ], 1) < 0

#            # Easiest case: Not flipped fermionflow or no Majorana
#            # mother with flipped fermionflow, return False
#            if self.get('fermionflow') > 0 or \
#               not self.get('self_antipart') and not \
#               filter(lambda wf: wf.get('fermionflow') < 0 and \
#                      wf.get('self_antipart'), self.get('mothers')):
#                print "False"
#                return False
#            # Easy case 1: If we have a Majorana parent which is an
#            # external particle
#            if len(filter(lambda wf: wf.get('fermionflow') < 0 and \
#                          wf.get('self_antipart') and not wf.get('mothers'),
#                          self.get('mothers'))) == 1:
#                print "True"
#                return True
#            # Easy case 2: If we have a Majorana parent which is not an
#            # external particle, that should be the conjugate
#            if filter(lambda wf: wf.get('fermionflow') < 0 and \
#                      wf.get('self_antipart') and \
#                      wf.get('state') == self.get('state'),
#                      self.get('mothers')):
#                print "False 2"
#                return False
#            # Now it gets more complicated - if this is a Majorana
#            # particle without a Majorana parent, we need to parse
#            # through the parents to make sure there is no other
#            # Majorana particle, which would already have given a
#            # conjugate
#            mothers = filter(lambda wf: wf.get('fermionflow') < 0 and \
#                             wf.get('state') == self.get('state'),
#                             self.get('mothers'))
#            if len(mothers) > 1:
#                raise self.PhysicsObjectError,\
#                      "Too many negative fermionflow mothers, not yet implemented"
#            got_herm_conj = False
#            while mothers:
#                mother = mothers[0]
#                print "mother: ",mother.get('number'),mother.get('pdg_code')
#                got_herm_conj = got_herm_conj or \
#                                mother.get('self_antipart')
#                mothers = filter(lambda wf: wf.get('fermionflow') < 0 and \
#                             wf.get('state') == self.get('state'),
#                             mother.get('mothers'))
#                if len(mothers) > 1:
#                    raise self.PhysicsObjectError,\
#                          "Too many negative fermionflow mothers, not yet implemented"
#                print not got_herm_conj
#            return not got_herm_conj
        else:
            return False

    def get_with_flow(self, name):
        """Generate the is_part and state needed for writing out
        wavefunctions, taking into account the fermion flow"""

        if self.get('fermionflow') > 0:
            # Just return (spin, state)
            return self.get(name)
        
        # If fermionflow is -1, need to flip state
        if name == 'is_part':
            return 1 - self.get('is_part')
        if name == 'state':
            return filter(lambda state: state != self.get('state'),
                          ['incoming', 'outgoing'])[0]
        #if name == 'pdg_code':
        #    if self.get('self_antipart'):
        #        return self.get('pdg_code')
        #    else:
        #        return -self.get('pdg_code')
        #if name == 'couplings':
        #    return self.get('conjugate_couplings')
        #if name == 'conjugate_couplings':
        #    return self.get('couplings')
        #if name == 'pdg_codes':
        #    return self.get('conjugate_pdg_codes')
        #if name == 'conjugate_pdg_codes':
        #    return self.get('pdg_codes')
        return self.get(name)

    def get_pdg_code_outgoing(self):
        """Generate the corresponding pdg_code for an outgoing particle,
        taking into account fermion flow, assuming the particle being final"""

        if self.get('self_antipart'):
            return self.get('pdg_code')

        if self.get('state') not in ['incoming', 'outgoing']:
            # This is a boson
            return self.get('pdg_code')

        if (self.get('state') == 'incoming' and self.get('is_part') \
                or self.get('state') == 'outgoing' and not self.get('is_part')):
            return -self.get('pdg_code')
        else:
            return self.get('pdg_code')

    def get_pdg_code_incoming(self):
        """Generate the corresponding pdg_code for an outgoing particle,
        taking into account fermion flow, assuming the particle being initial"""

        if self.get('self_antipart'):
            return self.get('pdg_code')

        if self.get('state') not in ['incoming', 'outgoing']:
            # This is a boson
            return -self.get('pdg_code')

        if (self.get('state') == 'outgoing' and self.get('is_part') \
                or self.get('state') == 'incoming' and not self.get('is_part')):
            return -self.get('pdg_code')
        else:
            return self.get('pdg_code')

    def get_spin_state_number(self):

        state_number = {'incoming': -1, 'outgoing': 1,
                        'intermediate': 1, 'initial': 1, 'final': 1}
        return self.get('fermionflow')* \
               state_number[self.get('state')]* \
               self.get('spin')

    def get_coupling_conjugate(self):
        """Special get for couplings: Returns conjugate coupling if this is
        a conjugate wavefunction, i.e., if any fermionflow is negative"""

        if self.get('fermionflow') < 0 or \
           filter(lambda wf: wf.get('fermionflow') < 0, self.get('mothers')):
            return self.get('conjugate_couplings')
        else:
            return self.get('couplings')

    def get_call_key(self):
        """Generate the (spin, state) tuple used as key for the helas call
        dictionaries in HelasModel"""

        res = []
        for mother in self.get('mothers'):
            res.append(mother.get_spin_state_number())

        # Sort according to spin and flow direction
        res.sort()

        res.append(self.get_spin_state_number())
        
        # Check if we need to append a charge conjugation flag
        if self.needs_hermitian_conjugate():
            res.append('C')

        return tuple(res)

    # Overloaded operators
    
    def __eq__(self, other):
        """Overloading the equality operator, to make comparison easy
        when checking if wavefunction is already written, or when
        checking for identical processes. Note that the number for
        this wavefunction, the pdg code, and the interaction id are
        irrelevant, while the numbers for the mothers are important.
        """

        if not isinstance(other,HelasWavefunction):
            return False

        # Check relevant directly defined properties
        if self['spin'] != other['spin'] or \
           self['color'] != other['color'] or \
           self['mass'] != other['mass'] or \
           self['width'] != other['width'] or \
           self['is_part'] != other['is_part'] or \
           self['self_antipart'] != other['self_antipart'] or \
           self['inter_color'] != other['inter_color'] or \
           self['lorentz'] != other['lorentz'] or \
           self['number_external'] != other['number_external'] or \
           self['couplings'] != other['couplings'] or \
           self['fermionflow'] != other['fermionflow'] or \
           self['state'] != other['state']:
            return False

        # Check that mothers have the same numbers (only relevant info)
        return [ mother.get('number') for mother in self['mothers'] ] == \
               [ mother.get('number') for mother in other['mothers'] ]
    

    def __ne__(self, other):
        """Overloading the nonequality operator, to make comparison easy"""
        return not self.__eq__(other)

#===============================================================================
# HelasWavefunctionList
#===============================================================================
class HelasWavefunctionList(base_objects.PhysicsObjectList):
    """List of HelasWavefunction objects
    """

    def is_valid_element(self, obj):
        """Test if object obj is a valid HelasWavefunction for the list."""
        
        return isinstance(obj, HelasWavefunction)

    # Helper function
    def check_and_fix_fermion_flow(self,
                                   wavefunctions,
                                   diagram_wavefunctions,
                                   external_wavefunctions,
                                   my_state):
        """Check for clashing fermion flow (N(incoming) !=
        N(outgoing)). If found, we need to trace back through the
        mother structure (only looking at fermions), until we find a
        Majorana fermion.  Set fermionflow = -1 for this wavefunction,
        as well as all other fermions along this line all the way from
        the initial clash to the external fermion, and consider an
        incoming particle with fermionflow -1 as outgoing (and vice
        versa). Continue until we have N(incoming) = N(outgoing).
        """
        # Clash is defined by whether the mothers have N(incoming) !=
        # N(outgoing) after this state has been subtracted
        mother_states = [ wf.get_with_flow('state') for wf in \
                          self ]
        if my_state in mother_states:
            mother_states.remove(my_state)

        Nincoming = len(filter(lambda state: state == 'incoming',
                               mother_states))
        Noutgoing = len(filter(lambda state: state == 'outgoing',
                               mother_states))

        if Nincoming == Noutgoing:
            return True

        fermion_mothers = filter(lambda wf: wf.get('spin') % 2 == 0,
                                 self)
        for mother in fermion_mothers:
            if Nincoming > Noutgoing and \
               mother.get_with_flow('state') == 'outgoing' or \
               Nincoming < Noutgoing and \
               mother.get_with_flow('state') == 'incoming' or \
               Nincoming == Noutgoing:
                # This is not a problematic leg
                continue

            # Call recursive function to check for Majorana fermions
            # and flip fermionflow if found
            found_majorana = False

            new_mother = mother.check_majorana_and_flip_flow(found_majorana,
                                                wavefunctions,
                                                diagram_wavefunctions,
                                                external_wavefunctions) 
            # Replace old mother with new mother
            self[self.index(mother)] = new_mother

            # Update counters
            mother_states = [ wf.get_with_flow('state') for wf in \
                             self ]
            if my_state in mother_states:
                mother_states.remove(my_state)

            Nincoming = len(filter(lambda state: state == 'incoming',
                                       mother_states))
            Noutgoing = len(filter(lambda state: state == 'outgoing',
                                       mother_states))
            
        if Nincoming != Noutgoing:
            raise self.PhysicsObjectListError, \
                  "Failed to fix fermion flow, %d != %d" % \
                  (Nincoming, Noutgoing)

        return True

    

#===============================================================================
# HelasAmplitude
#===============================================================================
class HelasAmplitude(base_objects.PhysicsObject):
    """HelasAmplitude object, has the information necessary for
    writing a call to a HELAS amplitude routine:a list of mother wavefunctions,
    interaction id, amplitude number
    """

    def default_setup(self):
        """Default values for all properties"""

        # Properties related to the interaction generating the propagator
        self['interaction_id'] = 0
        self['inter_color'] = []
        self['lorentz'] = []
        self['couplings'] = { (0, 0):'none'}
        self['conjugate_couplings'] = { (0, 0):'none'}
        self['pdg_codes'] = []
        self['conjugate_pdg_codes'] = []
        # Properties relating to the vertex
        self['number'] = 0
        self['mothers'] = HelasWavefunctionList()
        
    # Customized constructor
    def __init__(self, *arguments):
        """Allow generating a HelasAmplitude from a Vertex
        """

        if len(arguments) > 1:
            if isinstance(arguments[0],base_objects.Vertex) and \
               isinstance(arguments[1],base_objects.Model):
                super(HelasAmplitude, self).__init__()
                self.set('interaction_id',
                         arguments[0].get('id'), arguments[1])
        elif arguments:
            super(HelasAmplitude, self).__init__(arguments[0])
            # Set couplings separately, since it needs to be set after
            # color and lorentz
            if 'couplings' in arguments[0].keys():
                self.set('couplings', arguments[0]['couplings'])
            if 'conjugate_couplings' in arguments[0].keys():
                self.set('conjugate_couplings', arguments[0]['conjugate_couplings'])
        else:
            super(HelasAmplitude, self).__init__()
   
    def filter(self, name, value):
        """Filter for valid property values."""

        if name == 'interaction_id':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                        "%s is not a valid integer for wavefunction interaction id" % str(value)

        if name in ['inter_color', 'lorentz']:
            #Should be a list of strings
            if not isinstance(value, list):
                raise self.PhysicsObjectError, \
                        "%s is not a valid list of strings" % str(value)
            for mystr in value:
                if not isinstance(mystr, str):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid string" % str(mystr)

        if name in ['couplings', 'conjugate_couplings']:
            #Should be a dictionary of strings with (i,j) keys
            if not isinstance(value, dict):
                raise self.PhysicsObjectError, \
                        "%s is not a valid dictionary for couplings" % \
                                                                str(value)

            if len(value) != len(self['inter_color']) * len(self['lorentz']):
                raise self.PhysicsObjectError, \
                        "Dictionary " + str(value) + \
                        " for couplings has not the right number of entry"

            for key in value.keys():
                if not isinstance(key, tuple):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid tuple" % str(key)
                if len(key) != 2:
                    raise self.PhysicsObjectError, \
                        "%s is not a valid tuple with 2 elements" % str(key)
                if not isinstance(key[0], int) or not isinstance(key[1], int):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid tuple of integer" % str(key)
                if key[0] < 0 or key[1] < 0 or \
                   key[0] >= len(self['inter_color']) or key[1] >= \
                                                    len(self['lorentz']):
                    raise self.PhysicsObjectError, \
                        "%s is not a tuple with valid range" % str(key)
                if not isinstance(value[key], str):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid string" % str(mystr)

        if name == 'number':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                        "%s is not a valid integer for amplitude number" % str(value)

        if name in ['pdg_codes', 'conjugate_pdg_codes']:
            #Should be a list of integers
            if not isinstance(value, list):
                raise self.PhysicsObjectError, \
                        "%s is not a valid list of integers" % str(value)
            for mystr in value:
                if not isinstance(mystr, int):
                    raise self.PhysicsObjectError, \
                        "%s is not a valid integer" % str(mystr)

        if name == 'mothers':
            if not isinstance(value, HelasWavefunctionList):
                raise self.PhysicsObjectError, \
                      "%s is not a valid list of mothers for amplitude" % \
                      str(value)

        return True

    # Enhanced set function, where we can append a model

    def set(self, *arguments):
        """When setting interaction_id, if model is given (in tuple),
        set all other interaction properties. When setting pdg_code,
        if model is given, set all other particle properties."""

        if len(arguments) < 2:
            raise self.PhysicsObjectError, \
                  "Too few arguments for set"

        name = arguments[0]
        value = arguments[1]
        
        if len(arguments) > 2 and \
               isinstance(value, int) and \
               isinstance(arguments[2], base_objects.Model):
            if name == 'interaction_id':
                self.set('interaction_id', value)
                if value > 0:
                    inter = arguments[2].get('interaction_dict')[value]
                    self.set('inter_color', inter.get('color'))
                    self.set('lorentz', inter.get('lorentz'))
                    self.set('couplings', inter.get('couplings'))
                    self.set('pdg_codes',sorted([\
                        part.get_pdg_code() for part in \
                        inter.get('particles')]))
                    if not inter.get('conjugate_interaction'):
                        raise self.PhysicsObjectError,\
                              "Interaction %d has no conjugate_interaction" % \
                              repr(inter.get('id'))
                    conj_inter = arguments[2].get('interaction_dict')[\
                        inter.get('conjugate_interaction')]
                    self.set('conjugate_couplings',
                             conj_inter.get('couplings'))
                    self.set('conjugate_pdg_codes',sorted([\
                        part.get_pdg_code() for part in \
                        conj_inter.get('particles')]))
                return True
            else:
                raise self.PhysicsObjectError, \
                      "%s not allowed name for 3-argument set", name
        else:
            return super(HelasAmplitude, self).set(name, value)

    def get_sorted_keys(self):
        """Return particle property names as a nicely sorted list."""

        return ['interaction_id', 'inter_color', 'lorentz', 'couplings', 
                'conjugate_couplings', 'pdg_codes', 'conjugate_pdg_codes',
                'number', 'mothers']


    # Helper functions

    def check_and_fix_fermion_flow(self,
                                   wavefunctions,
                                   diagram_wavefunctions,
                                   external_wavefunctions):
        """Check for clashing fermion flow (N(incoming) !=
        N(outgoing)) in mothers
        """

        #return self.get('mothers').check_and_fix_fermion_flow(\
        #                           wavefunctions,
        #                           diagram_wavefunctions,
        #                           external_wavefunctions,
        #                           'nostate')

        # Clash is defined by whether the mothers have N(incoming) !=
        # N(outgoing) after this state has been subtracted, OR
        # the pdg codes for the interaction don't work with flow

        mother_states = [ wf.get_with_flow('state') for wf in \
                          self.get('mothers') ]

        Nincoming = len(filter(lambda state: state == 'incoming',
                               mother_states))
        Noutgoing = len(filter(lambda state: state == 'outgoing',
                               mother_states))

        pdg_codes = sorted([wf.get_pdg_code_outgoing() for wf in \
                     self.get('mothers')])

        if Nincoming == Noutgoing and \
               pdg_codes == self.get('pdg_codes'):
            return True

        print 'Need flip amp: ', Nincoming, Noutgoing, pdg_codes,\
              self.get('pdg_codes')

        # Start by checking if the pdg codes are ok:
        if pdg_codes != self.get_pdg_codes_conjugate():        

            reduced_pdg_codes = copy.copy(pdg_codes)        

            # Remove boson codes
            for wf in filter(lambda wf: wf.get('spin') % 2 == 1,self.get('mothers')):
                reduced_pdg_codes.remove(wf.get_pdg_code_outgoing())

            # Fermion mothers
            fermion_mothers = filter(lambda wf: wf.get('spin') % 2 == 0,
                                self.get('mothers'))
        
            # Find the erraneous code
            for mother in fermion_mothers:
                if mother.get_pdg_code_outgoing() in reduced_pdg_codes:
                    reduced_pdg_codes.remove(mother.get_pdg_code_outgoing())
                else:
                    # This mother needs to get the fermion flow code flipped
                    new_mother = mother.flip_flow(wavefunctions,
                                     diagram_wavefunctions,
                                     external_wavefunctions)
                    # Replace old mother with new mother
                    self[self.index(mother)] = new_mother
                    reduced_pdg_codes.remove(new_mother.get_pdg_code_outgoing())
            if reduced_pdg_codes:
                raise self.PhysicsObjectError, \
                      "Problem with bosonic mothers!"

        mother_states = [ wf.get_with_flow('state') for wf in \
                          self.get('mothers') ]

        Nincoming = len(filter(lambda state: state == 'incoming',
                               mother_states))
        Noutgoing = len(filter(lambda state: state == 'outgoing',
                               mother_states))

        print 'Nincoming = ',Nincoming, ' Noutgoing = ',Noutgoing
        print 'pdg_codes = ', sorted([wf.get_pdg_code_outgoing() for wf in \
                     self.get('mothers')])
        print 'should be: ',self.get('pdg_codes')
        print 'for: ',self

        while Nincoming != Noutgoing:
            # The problem is in pure Majorana states. Flip flow of
            # first Majorana mother with wrong flow.
            if Nincoming > Noutgoing:
                majorana_mothers = filter(lambda wf: wf.get('self_antipart') and \
                                          wf.get('spin') % 2 == 0 and \
                                          wf.get_with_flow('state') == 'incoming',
                                          self.get('mothers'))
            else:
                majorana_mothers = filter(lambda wf: wf.get('self_antipart') and \
                                          wf.get('spin') % 2 == 0 and \
                                          wf.get_with_flow('state') == 'outgoing',
                                          self.get('mothers'))
            new_mother = majorana_mothers[0].flip_flow(wavefunctions,
                                          diagram_wavefunctions,
                                          external_wavefunctions)

            # Replace old mother with new mother
            self.get('mothers')[self.get('mothers').index(\
                majorana_mothers[0])] = new_mother

            mother_states = [ wf.get_with_flow('state') for wf in \
                              self.get('mothers') ]
            
            Nincoming = len(filter(lambda state: state == 'incoming',
                                   mother_states))
            Noutgoing = len(filter(lambda state: state == 'outgoing',
                                   mother_states))
            
    def needs_hermitian_conjugate(self):
        """Returns true if there is a fermion flow clash, i.e.,
        there is an odd number of negative fermion flows"""

        return filter(lambda wf: wf.get('fermionflow') < 0,
                      self.get('mothers'))

#        # Only if we have a Majorana parent which is an
#        # external particle, return true
#        if len(filter(lambda wf: wf.get('fermionflow') < 0 and \
#                      wf.get('self_antipart') and not wf.get('mothers'),
#                      self.get('mothers'))) == 1:
#            return True
#        else:
#            return False

#        return reduce(lambda x, y: x * y,
#                      [ wf.get('fermionflow') for wf in \
#                        self.get('mothers') ], 1) < 0                      

    def get_coupling_conjugate(self):
        """Special get for couplings: Returns conjugate coupling if this is
        a conjugate wavefunction, i.e., if any fermionflow is negative"""

        #if sorted([wf.get_pdg_code_incoming() for wf in \
        #           self.get('mothers')]) == self.get('pdg_codes'):
        #    return self.get('couplings')
        #elif sorted([wf.get_pdg_code_incoming() for wf in \
        #           self.get('mothers')]) == self.get('conjugate_pdg_codes'):
        #    return self.get('conjugate_couplings')
        #else:
        #    raise self.PhysicsObjectError, \
        #          "PDG codes %s do not correspond to either pdg_codes %s or conjugate %s" % \
        #          (repr(sorted([wf.get_pdg_code_incoming() for wf in \
        #                        self.get('mothers')])),
        #           repr(self.get('pdg_codes')),
        #           repr(self.get('conjugate_pdg_codes')))

        if self.needs_hermitian_conjugate():
            return self.get('conjugate_couplings')
        else:
            return self.get('couplings')


    def get_pdg_codes_conjugate(self):
        """Special get for pdg_codes: Returns conjugate pdg_codes if this is
        a conjugate wavefunction, as determined by the bosonic mothers"""

        if self.needs_hermitian_conjugate():
            return self.get('conjugate_pdg_codes')
        else:
            return self.get('pdg_codes')

        # Use bosonic pdg codes to determine between pdg_codes and
        # conjugate_pdg_codes
        #bosonic_pdg_codes = [wf.get_pdg_code_incoming() for wf in \
        # self.get('mothers')]
        #
        #reduced_bosonic_pdg_codes = copy.copy(bosonic_pdg_codes)
        #reduced_pdg_codes = copy.copy(self.get('pdg_codes'))
        #for code in bosonic_pdg_codes:
        #    if code in reduced_pdg_codes:
        #        reduced_bosonic_pdg_codes.remove(code)
        #        reduced_pdg_codes.remove(code)
        #if not reduced_bosonic_pdg_codes:
        #    return self.get('pdg_codes')
        #
        #reduced_bosonic_pdg_codes = copy.copy(bosonic_pdg_codes)
        #reduced_pdg_codes = copy.copy(self.get('conjugate_pdg_codes'))
        #for code in bosonic_pdg_codes:
        #    if code in reduced_pdg_codes:
        #        reduced_bosonic_pdg_codes.remove(code)
        #        reduced_pdg_codes.remove(code)
        #if not reduced_bosonic_pdg_codes:
        #    return self.get('conjugate_pdg_codes')
        #
        #raise self.PhysicsObjectError, \
        #      "Mother bosons correspond to neither pdg_codes nor conjugate_pdg_codes"

    def get_call_key(self):
        """Generate the (spin, state) tuples used as key for the helas call
        dictionaries in HelasModel"""

        res = []
        for mother in self.get('mothers'):
            res.append(mother.get_spin_state_number())

        # Sort according to spin and flow direction
        res.sort()

        # Check if we need to append a charge conjugation flag
        if self.needs_hermitian_conjugate():
            res.append('C')

        return tuple(res)

    # Comparison between different amplitudes, to allow check for
    # identical processes. Note that we are then not interested in
    # interaction id, but in all other properties.
    def __eq__(self, other):
        """Comparison between different amplitudes, to allow check for
        identical processes.
        """
        
        if not isinstance(other,HelasAmplitude):
            return False

        # Check relevant directly defined properties
        if self['inter_color'] != other['inter_color'] or \
           self['lorentz'] != other['lorentz'] or \
           self['couplings'] != other['couplings'] or \
           self['number'] != other['number']:
            return False

        # Check that mothers have the same numbers (only relevant info)
        return [ mother.get('number') for mother in self['mothers'] ] == \
               [ mother.get('number') for mother in other['mothers'] ]

    def __ne__(self, other):
        """Overloading the nonequality operator, to make comparison easy"""
        return not self.__eq__(other)

#===============================================================================
# HelasAmplitudeList
#===============================================================================
class HelasAmplitudeList(base_objects.PhysicsObjectList):
    """List of HelasAmplitude objects
    """

    def is_valid_element(self, obj):
        """Test if object obj is a valid HelasAmplitude for the list."""
        
        return isinstance(obj, HelasAmplitude)


#===============================================================================
# HelasDiagram
#===============================================================================
class HelasDiagram(base_objects.PhysicsObject):
    """HelasDiagram: list of vertices (ordered)
    """

    def default_setup(self):
        """Default values for all properties"""

        self['wavefunctions'] = HelasWavefunctionList()
        self['amplitude'] = HelasAmplitude()
        self['fermionfactor'] = 1

    def filter(self, name, value):
        """Filter for valid diagram property values."""

        if name == 'wavefunctions':
            if not isinstance(value, HelasWavefunctionList):
                raise self.PhysicsObjectError, \
                        "%s is not a valid HelasWavefunctionList object" % str(value)
        if name == 'amplitude':
            if not isinstance(value, HelasAmplitude):
                raise self.PhysicsObjectError, \
                        "%s is not a valid HelasAmplitude object" % str(value)

        if name == 'fermionfactor':
            if not isinstance(value, int):
                raise self.PhysicsObjectError, \
                        "%s is not a valid integer for fermionfactor" % str(value)
            if not value in [-1,1]:
                raise self.PhysicsObjectError, \
                        "%s is not a valid fermion factor (must be -1 or 1)" % str(value)                

        return True

    def get_sorted_keys(self):
        """Return particle property names as a nicely sorted list."""

        return ['wavefunctions', 'amplitude', 'fermionfactor']
    
#===============================================================================
# HelasDiagramList
#===============================================================================
class HelasDiagramList(base_objects.PhysicsObjectList):
    """List of HelasDiagram objects
    """

    def is_valid_element(self, obj):
        """Test if object obj is a valid HelasDiagram for the list."""

        return isinstance(obj, HelasDiagram)
    
#===============================================================================
# HelasMatrixElement
#===============================================================================
class HelasMatrixElement(base_objects.PhysicsObject):
    """HelasMatrixElement: list of HelasDiagrams (ordered)
    """

    def default_setup(self):
        """Default values for all properties"""

        self['diagrams'] = HelasDiagramList()

    def filter(self, name, value):
        """Filter for valid diagram property values."""

        if name == 'diagrams':
            if not isinstance(value, HelasDiagramList):
                raise self.PhysicsObjectError, \
                        "%s is not a valid HelasDiagramList object" % str(value)
        return True

    def get_sorted_keys(self):
        """Return particle property names as a nicely sorted list."""

        return ['diagrams']
    
    # Customized constructor
    def __init__(self, *arguments):
        """Constructor for the HelasMatrixElement. In particular allows
        generating a HelasMatrixElement from a DiagramList, with
        automatic generation of the necessary wavefunctions
        """

        if arguments:
            if isinstance(arguments[0],diagram_generation.Amplitude):
                super(HelasMatrixElement, self).__init__()
                amplitude = arguments[0]
                optimization = 1
                if len(arguments) > 1 and isinstance(arguments[1],int):
                    optimization = arguments[1]

                self.generate_helas_diagrams(amplitude, optimization)
                self.calculate_fermion_factors(amplitude)
            else:
                super(HelasMatrixElement, self).__init__(arguments[0])
        else:
            super(HelasMatrixElement, self).__init__()
   
    def generate_helas_diagrams(self, amplitude, optimization = 1):
        """Starting from a list of Diagrams from the diagram
        generation, generate the corresponding HelasDiagrams, i.e.,
        the wave functions, amplitudes and fermionfactors. Choose
        between default optimization (= 1) or no optimization (= 0,
        for GPU).
        """

        if not isinstance(amplitude, diagram_generation.Amplitude) or \
               not isinstance(optimization,int):
            raise self.PhysicsObjectError,\
                  "Missing or erraneous arguments for generate_helas_diagrams"
        diagram_list = amplitude.get('diagrams')
        process = amplitude.get('process')
        model = process.get('model')
        if not diagram_list:
            return

        # wavefunctions has all the previously defined wavefunctions
        wavefunctions = []

        # Generate wavefunctions for the external particles
        external_wavefunctions = dict([(leg.get('number'),
                                        HelasWavefunction(leg, 0, model)) \
                                       for leg in process.get('legs')])

        incoming_numbers = [ leg.get('number') for leg in filter(lambda leg: \
                                  leg.get('state') == 'initial',
                                  process.get('legs')) ]

        # Now go through the diagrams, looking for undefined wavefunctions

        helas_diagrams = HelasDiagramList()

        for diagram in diagram_list:

            print "New diagram"

            # Dictionary from leg number to wave function, keeps track
            # of the present position in the tree
            number_to_wavefunctions = {}

            # Initialize wavefunctions for this diagram
            diagram_wavefunctions = HelasWavefunctionList()
            
            vertices = copy.copy(diagram.get('vertices'))

            # Single out last vertex, since this will give amplitude
            lastvx = vertices.pop()

            # Check if last vertex is indentity vertex
            if lastvx.get('id') == 0:
                # Need to "glue together" last and next-to-last
                # vertext, by replacing the (incoming) last leg of the
                # next-to-last vertex with the (outgoing) leg in the
                # last vertex
                nexttolastvertex = vertices.pop()
                legs = nexttolastvertex.get('legs')
                ntlnumber = legs[len(legs)-1].get('number')
                lastleg = filter(lambda leg: leg.get('number') != ntlnumber,
                                 lastvx.get('legs'))[0]
                # Replace the last leg of nexttolastvertex
                legs[len(legs)-1] = lastleg
                lastvx = nexttolastvertex
                # Sort the legs, to get right order of wave functions
                lastvx.get('legs').sort(lambda leg1, leg2: \
                                    leg1.get('number')-leg2.get('number'))

            # If wavefunction from incoming particles, flip pdg code
            # (both for s- and t-channel particle)
            #lastleg = lastvx.get('legs')[len(lastvx.get('legs')) - 1]
            #if lastleg.get('number') in incoming_numbers:
            #    part = model.get('particle_dict')[lastleg.get('id')]
            #    lastleg.set('id', part.get_anti_pdg_code())

            # Go through all vertices except the last and create
            # wavefunctions
            for vertex in vertices:
                legs = copy.copy(vertex.get('legs'))
                last_leg = legs.pop()
                # Generate list of mothers from legs
                mothers = self.getmothers(legs, number_to_wavefunctions,
                                          external_wavefunctions,
                                          wavefunctions,
                                          diagram_wavefunctions)
                # Now generate new wavefunction for the last leg
                wf = HelasWavefunction(last_leg, vertex.get('id'), model)
                wf.set('mothers', mothers)
                # Need to set incoming/outgoing and
                # particle/antiparticle according to the fermion flow
                # of mothers
                wf.set_state_and_particle(model)
                # Need to check for clashing fermion flow due to
                # Majorana fermions, and modify if necessary
                wf = wf.check_and_fix_fermion_flow(wavefunctions,
                                                       diagram_wavefunctions,
                                                       external_wavefunctions)
                # Wavefunction number is given by: number of external
                # wavefunctions + number of non-external wavefunctions
                # in wavefunctions and diagram_wavefunctions
                if not wf in diagram_wavefunctions:
                    number = len(external_wavefunctions) + 1
                    number = number + len(filter(lambda wf: \
                                                 wf not in external_wavefunctions.values(),
                                                 wavefunctions))
                    number = number + len(filter(lambda wf: \
                                                 wf not in external_wavefunctions.values(),
                                                 diagram_wavefunctions))
                    wf.set('number',number)
                    # Store wavefunction
                    if wf in wavefunctions:
                        wf = wavefunctions[wavefunctions.index(wf)]
                    else:
                        diagram_wavefunctions.append(wf)
                    number_to_wavefunctions[last_leg.get('number')] = wf

            # Find mothers for the amplitude
            legs = lastvx.get('legs')
            mothers = self.getmothers(legs, number_to_wavefunctions,
                                      external_wavefunctions,
                                      wavefunctions,
                                      diagram_wavefunctions)
                
            # Now generate a HelasAmplitude from the last vertex.
            amp = HelasAmplitude(lastvx, model)
            amp.set('mothers', mothers)
            amp.set('number', diagram_list.index(diagram) + 1)

            # Need to check for clashing fermion flow due to
            # Majorana fermions, and modify if necessary
            amp.check_and_fix_fermion_flow(wavefunctions,
                                           diagram_wavefunctions,
                                           external_wavefunctions)

            # Sort the wavefunctions according to number
            diagram_wavefunctions.sort(lambda wf1, wf2: \
                                       wf1.get('number')-wf2.get('number'))

            # Generate HelasDiagram
            helas_diagrams.append(HelasDiagram({ \
                'wavefunctions': diagram_wavefunctions,
                'amplitude': amp
                }))

            if optimization:
                wavefunctions.extend(diagram_wavefunctions)

        self.set('diagrams',helas_diagrams)

    def calculate_fermion_factors(self, amplitude):
        """Starting from a list of Diagrams from the
        diagram generation, generate the corresponding HelasDiagrams,
        i.e., the wave functions, amplitudes and fermionfactors
        """


    # Helper methods

    def getmothers(self, legs, number_to_wavefunctions,
                   external_wavefunctions, wavefunctions,
                   diagram_wavefunctions):
        """Generate list of mothers from number_to_wavefunctions and
        external_wavefunctions"""
        
        mothers = HelasWavefunctionList()

        for leg in legs:
            if not leg.get('number') in number_to_wavefunctions:
                # This is an external leg, pick from external_wavefunctions
                wf = external_wavefunctions[leg.get('number')]
                number_to_wavefunctions[leg.get('number')] = wf
                if not wf in wavefunctions:
                    diagram_wavefunctions.append(wf)
            else:
                # The mother is an existing wavefunction
                wf = number_to_wavefunctions[leg.get('number')]
            mothers.append(wf)

        return mothers

#===============================================================================
# HelasModel
#===============================================================================
class HelasModel(base_objects.PhysicsObject):
    """Language independent base class for writing Helas calls. The
    calls are stored in two dictionaries, wavefunctions and
    amplitudes, with entries being a mapping from a set of spin and
    incoming/outgoing states to a function which writes the
    corresponding wavefunction call."""

    def default_setup(self):

        self['name'] = ""
        self['wavefunctions'] = {}
        self['amplitudes'] = {}

    def filter(self, name, value):
        """Filter for model property values"""

        if name == 'name':
            if not isinstance(value, str):
                raise self.PhysicsObjectError, \
                    "Object of type %s is not a string" % \
                                                            type(value)

        if name == 'wavefunctions':
            # Should be a dictionary of functions returning strings, 
            # with keys (spins, flow state)
            if not isinstance(value, dict):
                raise self.PhysicsObjectError, \
                        "%s is not a valid dictionary for wavefunction" % \
                                                                str(value)

            for key in value.keys():
                self.add_wavefunction(key, value[key])

        if name == 'amplitudes':
            # Should be a dictionary of functions returning strings, 
            # with keys (spins, flow state)
            if not isinstance(value, dict):
                raise self.PhysicsObjectError, \
                        "%s is not a valid dictionary for amplitude" % \
                                                                str(value)

            for key in value.keys():
                add_amplitude(key, value[key])

        return True

    def get_sorted_keys(self):
        """Return process property names as a nicely sorted list."""

        return ['name', 'wavefunctions', 'amplitudes']

    def get_matrix_element_calls(self, matrix_element):
        """Return a list of strings, corresponding to the Helas calls
        for the matrix element"""

        if not isinstance(matrix_element, HelasMatrixElement):
            raise self.PhysicsObjectError, \
                  "%s not valid argument for get_matrix_element_calls" % \
                  repr(matrix_element)

        res = []
        for diagram in matrix_element.get('diagrams'):
            res.extend([ self.get_wavefunction_call(wf) for \
                         wf in diagram.get('wavefunctions') ])
            res.append(self.get_amplitude_call(diagram.get('amplitude')))

        return res

    def get_wavefunction_call(self, wavefunction):
        """Return the function for writing the wavefunction
        corresponding to the key"""

        if wavefunction.get_call_key() in self.get("wavefunctions").keys():
            return self["wavefunctions"][wavefunction.get_call_key()](wavefunction)
        else:
            return ""

    def get_amplitude_call(self, amplitude):
        """Return the function for writing the amplitude
        corresponding to the key"""

        if amplitude.get_call_key() in self.get("amplitudes").keys():
            return self["amplitudes"][amplitude.get_call_key()](amplitude)
        else:
            return ""

    def add_wavefunction(self, key, function):
        """Set the function for writing the wavefunction
        corresponding to the key"""


        if not isinstance(key, tuple):
            raise self.PhysicsObjectError, \
                  "%s is not a valid tuple for wavefunction key" % \
                  str(key)

        if not callable(function):
            raise self.PhysicsObjectError, \
                  "%s is not a valid function for wavefunction string" % \
                  str(function)

        self.get('wavefunctions')[key] = function
        return True
        
    def add_amplitude(self, key, function):
        """Set the function for writing the amplitude
        corresponding to the key"""


        if not isinstance(key, tuple):
            raise self.PhysicsObjectError, \
                  "%s is not a valid tuple for amplitude key" % \
                  str(key)

        if not callable(function):
            raise self.PhysicsObjectError, \
                  "%s is not a valid function for amplitude string" % \
                  str(function)

        self.get('amplitudes')[key] = function
        return True
        
    # Customized constructor
    def __init__(self, argument = {}):
        """Allow generating a HelasModel from a Model
        """

        if isinstance(argument,base_objects.Model):
            super(HelasModel, self).__init__()
            self.set('name',argument.get('name'))
        else:
            super(HelasModel, self).__init__(argument)


#===============================================================================
# HelasFortranModel
#===============================================================================
class HelasFortranModel(HelasModel):
    """The class for writing Helas calls in Fortran, starting from
    HelasWavefunctions and HelasAmplitudes."""

    mother_dict = {1: 'S', 2: 'O', -2: 'I', 3: 'V', 5: 'T'}
    self_dict = {1: 'H', 2: 'F', -2: 'F', 3: 'J', 5: 'U'}
    sort_wf = {'O': 0, 'I': 1, 'S': 2, 'T': 3, 'V': 4}
    sort_amp = {'S': 1, 'V': 2, 'T': 0, 'O': 3, 'I': 4}

    def default_setup(self):

        super(HelasFortranModel, self).default_setup()

        # Add special fortran Helas calls, which are not automatically
        # generated

    def get_wavefunction_call(self, wavefunction):
        """Return the function for writing the wavefunction
        corresponding to the key"""

        val = super(HelasFortranModel, self).get_wavefunction_call(wavefunction)

        if val:
            return val

        # If function not already existing, try to generate it.

        if len(wavefunction.get('mothers')) > 3:
            raise self.PhysicsObjectError,\
                  """Automatic generation of Fortran wavefunctions not
                  implemented for > 3 mothers"""

        self.generate_helas_call(wavefunction)
        return super(HelasFortranModel, self).get_wavefunction_call(wavefunction)

    def get_amplitude_call(self, amplitude):
        """Return the function for writing the amplitude
        corresponding to the key"""

        val = super(HelasFortranModel, self).get_amplitude_call(amplitude)

        if val:
            return val

        # If function not already existing, try to generate it.

        if len(amplitude.get('mothers')) > 4:
            raise self.PhysicsObjectError,\
                  """Automatic generation of Fortran amplitudes not
                  implemented for > 4 mothers"""

        self.generate_helas_call(amplitude)
        return super(HelasFortranModel, self).get_amplitude_call(amplitude)

    def generate_helas_call(self, argument):
            
        if not isinstance(argument, HelasWavefunction) and \
           not isinstance(argument, HelasAmplitude):
            raise self.PhysicsObjectError, \
                  "get_helas_call must be called with wavefunction or amplitude"

        call = "      CALL "

        call_function = None
            
        if isinstance(argument, HelasWavefunction) and \
               not argument.get('mothers'):
            # String is just IXXXXX, OXXXXX, VXXXXX or SXXXXX
            call = call + HelasFortranModel.mother_dict[\
                argument.get_spin_state_number()]
            # Fill out with X up to 6 positions
            call = call + 'X' * (17 - len(call))
            call = call + "(P(0,%d),"
            if argument.get('spin') != 1:
                # For non-scalars, need mass and helicity
                call = call + "%s,NHEL(%d),"
            call = call + "%d*IC(%d),W(1,%d))"
            if argument.get('spin') == 1:
                call_function = lambda wf: call % \
                                (wf.get('number_external'),
                                 # For boson, need initial/final here
                                 (-1)**(wf.get('state') == 'initial'),
                                 wf.get('number_external'),
                                 wf.get('number'))
            elif argument.get('spin') % 2 == 1:
                call_function = lambda wf: call % \
                                (wf.get('number_external'),
                                 wf.get('mass'),
                                 wf.get('number_external'),
                                 # For boson, need initial/final here
                                 (-1)**(wf.get('state')=='initial'),
                                 wf.get('number_external'),
                                 wf.get('number'))
            else:
                call_function = lambda wf: call % \
                                (wf.get('number_external'),
                                 wf.get('mass'),
                                 wf.get('number_external'),
                                 # For fermions, need particle/antiparticle
                                 -(-1)**wf.get_with_flow('is_part'),
                                 wf.get('number_external'),
                                 wf.get('number'))
        else:
            # String is FOVXXX, FIVXXX, JIOXXX etc.
            if isinstance(argument, HelasWavefunction):
                call = call + \
                       HelasFortranModel.self_dict[\
                argument.get_spin_state_number()]

            mother_letters = HelasFortranModel.sorted_letters(argument)

            call = call +''.join(mother_letters)
            # IMPLEMENT Add C and other addition (for HEFT etc) if needed
            # Check if we need to append a charge conjugation flag
            if argument.needs_hermitian_conjugate():
                call = call + 'C'


            # Fill out with X up to 6 positions
            call = call + 'X' * (17 - len(call)) + '('
            # Wavefunctions
            call = call + "W(1,%d)," * len(argument.get('mothers'))
            # Couplings
            call = call + "%s,"

            # IMPLEMENT Here we need to add extra coupling for certain
            # 4-vertices

            if isinstance(argument, HelasWavefunction):
                # Mass and width
                call = call + "%s,%s,"
                # New wavefunction
                call = call + "W(1,%d))"
            else:
                # Amplitude
                call = call + "AMP(%d))"                

            if isinstance(argument,HelasWavefunction):
                # Create call for wavefunction
                if len(argument.get('mothers')) == 2:
                    call_function = lambda wf: call % \
                                    (HelasFortranModel.sorted_mothers(wf)[0].get('number'),
                                     HelasFortranModel.sorted_mothers(wf)[1].get('number'),
                                     #wf.get_coupling_conjugate().values()[0],
                                     wf.get_with_flow('couplings').values()[0],
                                     wf.get('mass'),
                                     wf.get('width'),
                                     wf.get('number'))
                else:
                    call_function = lambda wf: call % \
                                    (HelasFortranModel.sorted_mothers(wf)[0].get('number'),
                                     HelasFortranModel.sorted_mothers(wf)[1].get('number'),
                                     HelasFortranModel.sorted_mothers(wf)[2].get('number'),
                                     #wf.get_coupling_conjugate().values()[0],
                                     wf.get_with_flow('couplings').values()[0],
                                     wf.get('mass'),
                                     wf.get('width'),
                                     wf.get('number'))
            else:
                # Create call for amplitude
                if len(argument.get('mothers')) == 3:
                    call_function = lambda amp: call % \
                                    (HelasFortranModel.sorted_mothers(amp)[0].get('number'),
                                     HelasFortranModel.sorted_mothers(amp)[1].get('number'),
                                     HelasFortranModel.sorted_mothers(amp)[2].get('number'),
                                     #amp.get_coupling_conjugate().values()[0],
                                     amp.get('couplings').values()[0],
                                     amp.get('number'))
                else:
                    call_function = lambda amp: call % \
                                    (HelasFortranModel.sorted_mothers(amp)[0].get('number'),
                                     HelasFortranModel.sorted_mothers(amp)[1].get('number'),
                                     HelasFortranModel.sorted_mothers(amp)[2].get('number'),
                                     HelasFortranModel.sorted_mothers(amp)[3].get('number'),
                                     #amp.get_coupling_conjugate().values()[0],
                                     amp.get('couplings').values()[0],
                                     amp.get('number'))                    
                
        if isinstance(argument,HelasWavefunction):
            self.add_wavefunction(argument.get_call_key(),call_function)
        else:
            self.add_amplitude(argument.get_call_key(),call_function)
            
    # Static helper functions

    @staticmethod
    def sorted_mothers(arg):
        """Gives a list of mother wavefunctions sorted according to
        1. the spin order needed in the Fortran Helas calls and
        2. the number for the external leg"""

        if isinstance(arg, HelasWavefunction) or \
           isinstance(arg, HelasAmplitude):
            return sorted(arg.get('mothers'),
                          lambda wf1, wf2: \
                          HelasFortranModel.sort_amp[\
                HelasFortranModel.mother_dict[wf2.get_spin_state_number()]]\
                          - HelasFortranModel.sort_amp[\
                HelasFortranModel.mother_dict[wf1.get_spin_state_number()]]\
                          or wf1.get('number_external') - \
                          wf2.get('number_external'))
    
    @staticmethod
    def sorted_letters(arg):
        """Gives a list of letters sorted according to
        the order of letters in the Fortran Helas calls"""

        if isinstance(arg, HelasWavefunction):
            return sorted([HelasFortranModel.mother_dict[\
            wf.get_spin_state_number()] for wf in arg.get('mothers')],
                          lambda l1, l2: \
                          HelasFortranModel.sort_wf[l2] - \
                          HelasFortranModel.sort_wf[l1])

        if isinstance(arg, HelasAmplitude):
            return sorted([HelasFortranModel.mother_dict[\
            wf.get_spin_state_number()] for wf in arg.get('mothers')],
                          lambda l1, l2: \
                          HelasFortranModel.sort_amp[l2] - \
                          HelasFortranModel.sort_amp[l1])
    

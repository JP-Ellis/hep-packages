################################################################################
#
# Copyright (c) 2010 The MadGraph Development team and Contributors
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
import models.model_reader as model_reader
import madgraph.core.base_objects as base_objects


class ParamCardWriterError(Exception):
    """ a error class for this file """

class ParamCardWriter(object):
    """ A class for writting an update param_card for a given model """

    header = \
    "######################################################################\n" + \
    "## PARAM_CARD AUTOMATICALY GENERATED BY MG5 FOLLOWING UFO MODEL   ####\n" + \
    "######################################################################\n" + \
    "##                                                                  ##\n" + \
    "##  Width set on Auto will be computed following the information    ##\n" + \
    "##        present in the decay.py files of the model. By default,   ##\n" + \
    "##        this is only 1->2 decay modes.                            ##\n" + \
    "##                                                                  ##\n" + \
    "######################################################################\n"
    
    sm_pdg = [1,2,3,4,5,6,11,12,13,13,14,15,16,21,22,23,24,25]
    qnumber_str ="""Block QNUMBERS %(pdg)d  # %(name)s 
        1 %(charge)d  # 3 times electric charge
        2 %(spin)d  # number of spin states (2S+1)
        3 %(color)d  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 %(antipart)d  # Particle/Antiparticle distinction (0=own anti)\n"""


    def __init__(self, model, filepath=None):
        """ model is a valid MG5 model, filepath is the path were to write the
        param_card.dat """

        # Compute the value of all dependant parameter
        if isinstance(model, model_reader.ModelReader):
            self.model = model
        else:
            self.model = model_reader.ModelReader(model)
            self.model.set_parameters_and_couplings()


        # Organize the data
        self.external = self.model['parameters'][('external',)]
        self.param_dict = self.create_param_dict()
        self.define_not_dep_param()
    
        if filepath:
            self.define_output_file(filepath)
            self.write_card()
    
    
    def create_param_dict(self):
        """ return {'name': parameterObject}"""
        
        out = {}
        for key, params in self.model['parameters'].items():
            for param in params:
                out[param.name] = param
                
        if 'ZERO' not in out.keys():
            zero = base_objects.ModelVariable('ZERO', '0', 'real')
            out['ZERO'] = zero
        return out

    
    def define_not_dep_param(self):
        """define self.dep_mass and self.dep_width in case that they are 
        requested in the param_card.dat"""
        
        all_particles = self.model['particles']
        
        # 
        self.dep_mass, self.dep_width = [] , []
        self.duplicate_mass, self.duplicate_width =[], [] 

        def_param = [] 
        # one loop for the mass
        for p in all_particles:
            mass = self.param_dict[p["mass"]]
            if mass in def_param:
                self.duplicate_mass.append((p, mass))
                continue
            elif p["mass"] != 'ZERO':
                def_param.append(mass)
            if p['mass'] not in self.external:
                self.dep_mass.append((p, mass))

        # one loop for the width
        def_param = [] 
        for p in all_particles:
            width = self.param_dict[p["width"]]
            if width in def_param:
                self.duplicate_width.append((p, width))
                continue
            else:
                if p["width"] != 'ZERO':
                    def_param.append(width)
            if p['width'] not in self.external:
                self.dep_width.append((p, width))

        
        
    @staticmethod
    def order_param(obj1, obj2):
        """ order parameter of a given block """
        
        if obj1.lhablock == obj2.lhablock:
            pass
        elif obj1.lhablock == 'DECAY':
            return 1
        elif obj2.lhablock == 'DECAY':
            return -1
        elif obj1.lhablock < obj2.lhablock:
            return -1
        elif obj1.lhablock != obj2.lhablock:
            return 1
        
        maxlen = min([len(obj1.lhacode), len(obj2.lhacode)])

        for i in range(maxlen):
            if obj1.lhacode[i] < obj2.lhacode[i]:
                return -1
            elif obj1.lhacode[i] > obj2.lhacode[i]:
                return 1
            
        #identical up to the first finish
        if len(obj1.lhacode) > len(obj2.lhacode):
            return 1
        elif  len(obj1.lhacode) == len(obj2.lhacode):
            return 0
        else:
            return -1

    def define_output_file(self, path, mode='w'):
        """ initialize the file"""
        
        if isinstance(path, str):
            self.fsock = open(path, mode)
        else:
            self.fsock = path # prebuild file/IOstring
        
        self.fsock.write(self.header)

    def write_card(self, path=None):
        """schedular for writing a card"""
  
        if path:
            self.define_input_file(path)
  
        # order the parameter in a smart way
        self.external.sort(self.order_param)
        
        cur_lhablock = ''
        for param in self.external:
            #check if we change of lhablock
            if cur_lhablock != param.lhablock: 
                # check if some dependent param should be written
                self.write_dep_param_block(cur_lhablock)
                cur_lhablock = param.lhablock
                # write the header of the new block
                self.write_block(cur_lhablock)
            #write the parameter
            self.write_param(param, cur_lhablock)
        self.write_dep_param_block(cur_lhablock)
        self.write_qnumber()
        
    def write_block(self, name):
        """ write a comment for a block"""
        
        self.fsock.writelines(
        """\n###################################""" + \
        """\n## INFORMATION FOR %s""" % name.upper() +\
        """\n###################################\n"""
         )
        if name!='DECAY':
            self.fsock.write("""Block %s \n""" % name.lower())
            
    def write_param(self, param, lhablock):
        """ write the line corresponding to a given parameter """
    
        if hasattr(param, 'info'):
            info = param.info
        else:
            info = param.name
    
        if param.value.imag != 0:
            raise ParamCardWriterError, 'All External Parameter should be real'
    

        # avoid to keep special value used to avoid restriction
        if param.value == 9.999999e-1:
            param.value = 1
        elif param.value == 0.000001e-99:
            param.value = 0
    
    
        lhacode=' '.join(['%3s' % key for key in param.lhacode])
        if lhablock != 'DECAY':
            text = """  %s %e # %s \n""" % (lhacode, param.value.real, info) 
        else:
            text = '''DECAY %s %e # %s \n''' % (lhacode, param.value.real, info)
        self.fsock.write(text)             
      
        
    def write_dep_param_block(self, lhablock):
        """writing the requested LHA parameter"""

        if lhablock == 'MASS':
            data = self.dep_mass 
            prefix = " "
        elif lhablock == 'DECAY':
            data = self.dep_width
            prefix = "DECAY "
        else:
            return
        
        text = ""
        def sort(el1, el2):
            (p1,n) =el1
            (p2,n) = el2
            if (p1["pdg_code"] -p2["pdg_code"]) > 0:
                return 1
            else:
                return -1 
        
        data.sort(sort)
        for part, param in data:
            if self.model['parameter_dict'][param.name].imag:
                raise ParamCardWriterError, 'All Mass/Width Parameter should be real'
            value = complex(self.model['parameter_dict'][param.name]).real
            text += """%s %s %f # %s : %s \n""" %(prefix, part["pdg_code"], 
                        value, part["name"], param.expr)  
        
        # Add duplicate parameter
        if lhablock == 'MASS':
            data = self.duplicate_mass 
            name = 'mass'
        elif lhablock == 'DECAY':
            data = self.duplicate_width
            name = 'width'
    
        for part, param in data:
            if self.model['parameter_dict'][param.name].imag:
                raise ParamCardWriterError, 'All Mass/Width Parameter should be real'
            value = complex(self.model['parameter_dict'][param.name]).real
            text += """%s %s %f # %s : %s \n""" %(prefix, part["pdg_code"], 
                        value, part["name"], part[name])
            
        if not text:
            return
         
        pretext = "##  Not dependent paramater.\n"
        pretext += "## Those values should be edited following the \n"
        pretext += "## analytical expression. MG5 ignore those values \n"
        pretext += "## but they are important for interfacing the output of MG5\n"
        pretext += "## to external program such as Pythia.\n"
        self.fsock.write(pretext + text)                
        
    
    def write_qnumber(self):
        """ write qnumber """
        
        def is_anti(logical):
            if logical:
                return 0
            else:
                return 1
        

        text = "" 
        for part in self.model['particles']:
            if part["pdg_code"] in self.sm_pdg or part["pdg_code"] < 0:
                continue
            text += self.qnumber_str % {'pdg': part["pdg_code"],
                                 'name': part["name"],
                                 'charge': 3 * part["charge"],
                                 'spin': part["spin"],
                                 'color': part["color"],
                                 'antipart': is_anti(part['self_antipart'])}

        if text:
            pretext="""#===========================================================\n"""
            pretext += """# QUANTUM NUMBERS OF NEW STATE(S) (NON SM PDG CODE)\n"""
            pretext += """#===========================================================\n\n"""
        
            self.fsock.write(pretext + text)
        
        
            
            
            
            
        
            
if '__main__' == __name__:
    ParamCardWriter('./param_card.dat', generic=True)
    print 'write ./param_card.dat'
    

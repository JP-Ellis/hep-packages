
__date__ = "19 December 2010"
__author__ = 'olivier.mattelaer@uclouvain.be'

class ParamCardWriter(object):
    
    header = \
    """######################################################################\n""" + \
    """## PARAM_CARD AUTOMATICALY GENERATED BY THE UFO  #####################\n""" + \
    """######################################################################\n"""   
    
    def __init__(self, filename, list_of_parameters=None):
        """write a valid param_card.dat"""
        
        if not list_of_parameters:
            from parameters import all_parameters
            list_of_parameters = [param for param in all_parameters if \
                                                       param.nature=='external']
        
        self.fsock = open(filename, 'w')
        self.fsock.write(self.header)
        
        self.write_card(list_of_parameters)
    
    
    def write_card(self, all_ext_param):
        """ """
        
      
        
        # list all lhablock
        all_lhablock = set([param.lhablock for param in all_ext_param])
        
        # ordonate lhablock alphabeticaly
        list(all_lhablock).sort()
        
        for lhablock in all_lhablock:
            self.write_block(lhablock)
            [self.write_param(param, lhablock) for param in all_ext_param if \
                                                     param.lhablock == lhablock]
    def write_block(self, name):
        """ write a comment for a block"""
        
        self.fsock.writelines(
        """\n###################################""" + \
        """\n## INFORMATION FOR %s""" % name.upper() +\
        """\n###################################\n"""
         )
        if name!='DECAY':
            self.fsock.write("""Block %s \n""" % name)

    def write_param(self, param, lhablock):
        
        lhacode=' '.join(['%3s' % key for key in param.lhacode])
        if lhablock != 'DECAY':
            text = """  %s %e # %s \n""" % (lhacode, param.value.real, param.name ) 
        else:
            text = '''DECAY %s %e \n''' % (lhacode, param.value.real)
        self.fsock.write(text) 
            
            
if '__main__' == __name__:
    ParamCardWriter('./param_card.dat')
    print 'done'
    

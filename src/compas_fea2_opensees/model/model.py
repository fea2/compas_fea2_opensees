from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Model
from compas_fea2.model import SolidSection

class OpenseesModel(Model):
    """ OpenSees implementation of the :class::`Model`.

    For detailed information about OpenSees and its API visti: https://opensees.github.io/OpenSeesDocumentation/user/interpreters.html

    Warning
    -------
    Work in Progress!

    """
    __doc__ += Model.__doc__


    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(OpenseesModel, self).__init__(name=name, description=description, author=author, **kwargs)

    def jobdata(self):
        return """#
model Basic -ndm 3 -ndf 3
#
#==================================================================
# Materials
#==================================================================
#
{}
#
#==================================================================
# Sections
#==================================================================
#
{}
#
#==================================================================
# Parts
#==================================================================
#
{}
#
#
#------------------------------------------------------------------
# Initial conditions
#------------------------------------------------------------------
#
#    tag   DX   DY   RZ   MX   MY   MZ
{}
#
#
#------------------------------------------------------------------
# Connectors
#------------------------------------------------------------------
#
{}
#
#""".format(
    '\n'.join([material.jobdata() for material in self.materials]),
    '\n'.join([section.jobdata() for section in self.sections if not isinstance(section, SolidSection)]),
    '\n'.join([part.jobdata() for part in self.parts]),
    '\n'.join([bc.jobdata(nodes) for bc, nodes in self.bcs.items()]),
    '\n'.join([connector.jobdata() for connector in self.connectors]),

)

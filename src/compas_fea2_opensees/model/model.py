from compas_fea2.model import Model
from compas_fea2.model import SolidSection
from compas_fea2.model import TrussSection


class OpenseesModel(Model):
    """OpenSees implementation of the :class::`Model`.

    For detailed information about OpenSees and its API visti: https://opensees.github.io/OpenSeesDocumentation/user/interpreters.html

    Warning
    -------
    Work in Progress!

    """

    __doc__ += Model.__doc__

    def __init__(self, description=None, author=None, **kwargs):
        super(OpenseesModel, self).__init__(description=description, author=author, **kwargs)

    def jobdata(self):
        return """#
# By default, models in compas_fea2 are defined in 3D.
model Basic -ndm 3
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
            "\n".join([material.jobdata() for material in sorted(self.materials, key=lambda x: x.key)]),
            "\n".join([section.jobdata() for section in sorted(self.sections, key=lambda x: x.key) if not isinstance(section, (SolidSection, TrussSection))]),
            "\n".join([part.jobdata() for part in sorted(self.parts, key=lambda x: x.key)]),
            "\n".join([bc.jobdata(nodes) for bc, nodes in self.bcs.items()]),
            "\n".join([connector.jobdata() for connector in sorted(self.connectors, key=lambda x: x.key)]),
        )

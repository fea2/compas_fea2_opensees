from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import DeformablePart


class OpenseesPart(DeformablePart):
    """OpenSees implementation of :class:`compas_fea2.model.DeformablePart`.

    Note
    ----
    Models with multiple parts are not currently supported in Opensees.
    """

    __doc__ += DeformablePart.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    ndm : int
        Dimensionality of the model. Can be from 1, 2, or 3, by default
        3 (3d model).
    ndof : int
        number of degree of freedom at the nodes. It can be 1, 3 or 6, by default
        6.

    """

    def __init__(self, ndm=None, ndf=None, **kwargs):
        super(OpenseesPart, self).__init__(**kwargs)
        self._ndm = ndm or 3
        self._ndf = ndf or {1: 1, 2: 3, 3: 6}[self._ndm]

    @property
    def ndm(self):
        """The ndm property."""
        return self._ndm

    @ndm.setter
    def ndm(self, value):
        value = int(value)
        if value < 1 or value > 3:
            raise ValueError("The model dimension can be either 1,2 or 3.")
        self._ndm = value

    @property
    def ndf(self):
        return self._ndf

    @ndf.setter
    def ndf(self, value):
        value = int(value)
        if value not in (1, 3, 6):
            raise ValueError("The number of degree of freedom can be either 1,3 or 6.")
        self._ndf = value

    # =========================================================================
    #                       Generate input file data
    # =========================================================================
    def jobdata(self):
        return """#
#------------------------------------------------------------------
# Part {}
#------------------------------------------------------------------
model Basic -ndm {} -ndf {}
#
# Nodes
#------------------------------------------------------------------
#
#    tag        X       Y       Z       mx      my      mz
{}
#
# Elements
#------------------------------------------------------------------
#
{}
#
#""".format(
            self.name,
            self._ndm,
            self._ndf,
            "\n".join([node.jobdata() for node in sorted(self.nodes, key=lambda x: x.key)]),
            "\n".join([element.jobdata() for element in sorted(self.elements, key=lambda x: x.key)]),
        )

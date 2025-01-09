from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import GeneralDisplacement

dofs = ["x", "y", "z", "xx", "yy", "zz"]


class OpenseesGeneralDisplacement(GeneralDisplacement):
    """OpenSees implementation of :class:`compas_fea2.problem.PointLoad`.\n"""

    __doc__ += GeneralDisplacement.__doc__

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes="global", **kwargs):
        super(OpenseesGeneralDisplacement, self).__init__(x, y, z, xx, yy, zz, axes, **kwargs)
        raise NotImplementedError

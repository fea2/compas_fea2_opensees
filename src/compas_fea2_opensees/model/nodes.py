
from compas_fea2.model import Node


class OpenseesNode(Node):
    """Opensees implementation of the :class:`Node`. \n"""

    __doc__ += Node.__doc__

    def __init__(self, xyz, mass=None, **kwargs):
        super(OpenseesNode, self).__init__(xyz=xyz, mass=mass, **kwargs)

    def jobdata(self):
        # FIXME: the approximation on the floating point is not correct because it depends on the units
        x, y, z = self.xyz
        coordinates = "{0}{1}{2}{3:>15.8f}{2}{4:>15.8f}{2}{5:>15.8f}".format("node ", self.key, " ", x, y, z)
        if any(self.mass):
            mass = " -mass " + " ".join(["{:>15.8f}".format(m) for m in self.mass])
        else:
            mass = ""
        return coordinates + mass

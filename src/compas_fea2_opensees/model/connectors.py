from compas_fea2.model import RigidLinkConnector
from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthContactConnector
from compas_fea2.model import ZeroLengthSpringConnector


class OpenseesRigidLinkConnector(RigidLinkConnector):
    """Opensees implementation of :class:`compas_fea2.model.connectors.RigidLinkConnector`.\n"""

    __doc__ += RigidLinkConnector.__doc__

    def __init__(self, nodes, dofs="beam", **kwargs):
        super(OpenseesRigidLinkConnector, self).__init__(nodes, dofs, **kwargs)

    def jobdata(self):
        cNode = self.nodes[0].key
        rNode = self.nodes[1].key
        if self.dofs == "beam":
            return f"rigidLink beam {rNode} {cNode}"
        elif self.dofs == "bar":
            return f"rigidLink bar {rNode} {cNode}"
        else:
            if not any([dof in list(range(1, min([self.nodes[0].part.ndf, self.nodes[1].part.ndf]) + 1)) for dof in self.dofs]):
                raise ValueError("Invalid DOF")
            return f"equalDOF {rNode} {cNode} {' '.join([str(dof) for dof in self.dofs])}"


class OpenseesSpringConnector(SpringConnector):
    def __init__(self, master, slave, **kwargs):
        super(OpenseesSpringConnector, self).__init__(master, slave, tol=None, **kwargs)
        raise NotImplementedError


class OpenseesZeroLengthSpringConnector(ZeroLengthSpringConnector):
    """Opensees implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, section, directions, yielding=None, failure=None, implementation=None, **kwargs):
        super(OpenseesZeroLengthSpringConnector, self).__init__(nodes, section, directions, yielding, failure, **kwargs)
        self._implementation = implementation

    @property
    def implementation(self):
        return self._implementation

    def jobdata(self):
        try:
            return getattr(self, "_" + self.implementation)()
        except AttributeError:
            raise ValueError("{} is not a valid implementation.".format(self._implementation))


class OpenseesZeroLengthContactConnector(ZeroLengthContactConnector):
    """Opensees implementation of :class:`compas_fea2.model.connectors.ZeroLengthContactConnector`.\n"""

    __doc__ += ZeroLengthContactConnector.__doc__

    def __init__(self, nodes, direction, Kn, Kt, mu, implementation=None, **kwargs):
        super(OpenseesZeroLengthContactConnector, self).__init__(nodes, direction, Kn, Kt, mu, **kwargs)
        self._implementation = implementation
        self._c = kwargs.get("c", 0.0)

    @property
    def implementation(self):
        if not self._implementation:
            return "Contact3D"
        else:
            return self._implementation

    def jobdata(self):
        try:
            return getattr(self, "_" + self.implementation)()
        except AttributeError:
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    def _Contact3D(self):
        eleTag = self.key + len(sorted(self.model.elements, key=lambda x: x.key))
        cNode = self.nodes[0].key
        rNode = self.nodes[1].key
        return f"element zeroLengthContact3D {eleTag} {cNode} {rNode} {self.Kn} {self.Kt} {self.mu} {self._c} {self.direction}"

    def _ASDimplex(self):
        eleTag = self.key + len(sorted(self.model.elements, key=lambda x: x.key))
        cNode = self.nodes[0].key
        rNode = self.nodes[1].key
        return f"element zeroLengthContactASDimplex {eleTag} {cNode} {rNode} {self.Kn} {self.Kt} {self.mu} -orient {' '.join([str(i) for i in self.direction])}"

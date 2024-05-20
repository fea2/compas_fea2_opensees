from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthSpringConnector


class OpenseesSpringConnector(SpringConnector):
    def __init__(self, master, slave, name=None, **kwargs):
        super(OpenseesSpringConnector, self).__init__(master, slave, tol=None, name=name, **kwargs)
        raise NotImplementedError


class OpenseesZeroLengthSpringConnector(ZeroLengthSpringConnector):
    """Opensees implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, section, directions, yielding=None, failure=None, **kwargs):
        super(OpenseesZeroLengthSpringConnector, self).__init__(nodes, section, directions, yielding, failure, **kwargs)

    def jobdata(self):
        return f"element zeroLength {self.input_key+len(self.model.parts)*10000000} {self.nodes[0].input_key} {self.nodes[1].input_key} -mat 0 -dir 1 2 3"

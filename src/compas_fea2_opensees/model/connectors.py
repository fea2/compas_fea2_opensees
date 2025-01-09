from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_fea2
from compas_fea2.model import SpringConnector
from compas_fea2.model import ZeroLengthSpringConnector
from compas_fea2.model import RigidLinkConnector


class OpenseesSpringConnector(SpringConnector):
    def __init__(self, master, slave, **kwargs):
        super(OpenseesSpringConnector, self).__init__(master, slave, tol=None, **kwargs)
        raise NotImplementedError


class OpenseesZeroLengthSpringConnector(ZeroLengthSpringConnector):
    """Opensees implementation of :class:`compas_fea2.model.connectors.ZeroLengthSpringConnector`.\n"""

    __doc__ += ZeroLengthSpringConnector.__doc__

    def __init__(self, nodes, section, directions, yielding=None, failure=None, **kwargs):
        super(OpenseesZeroLengthSpringConnector, self).__init__(nodes, section, directions, yielding, failure, **kwargs)

    def jobdata(self):
        
        # return f"element zeroLengthND {self.input_key+len(self.model.elements)} {self.nodes[0].input_key} {self.nodes[1].input_key} 1000 0 1 2 3"
        # return f"rigidLink bar {self.nodes[0].input_key} {self.nodes[1].input_key}"
        # return f"equalDOF {self.nodes[0].input_key} {self.nodes[1].input_key} 1 2 3"
#         return f"""
# set Kn 1.0e10
# set Kt 100.0
# set mu 0.5
# element zeroLengthContactASDimplex {self.input_key+len(self.model.elements)} {self.nodes[0].input_key} {self.nodes[1].input_key}   $Kn $Kt $mu -orient 0 0 1
# #"""
        eleTag = self.input_key+len(sorted(self.model.elements, key=lambda x: x.input_key))
        cNode = self.nodes[0].input_key
        rNode = self.nodes[1].input_key
        Kn = 1e10
        Kt = 1e10
        mu = 0.8
        c = 0.1
        direction = 3
        # return f"element zeroLength {eleTag} {cNode} {rNode} -mat 0 -dir 3" # -orient 1 0 0 0 1 0"
        
        # Somehow working
        return f"element zeroLengthContact3D {eleTag} {cNode} {rNode} {Kn} {Kt} {mu} {c} {direction}"
        
        
class OpenseesRigidLinkConnector(RigidLinkConnector):
    """Opensees implementation of :class:`compas_fea2.model.connectors.RigidLinkConnector`.\n"""

    __doc__ += RigidLinkConnector.__doc__

    def __init__(self, nodes, dofs='beam', **kwargs):
        super(OpenseesRigidLinkConnector, self).__init__(nodes, dofs, **kwargs)

    def jobdata(self):
        cNode = self.nodes[0].input_key
        rNode = self.nodes[1].input_key
        if self.dofs == 'beam':
            return f"rigidLink beam {rNode} {cNode}"
        elif self.dofs == 'bar':
            return f"rigidLink bar {rNode} {cNode}"
        else:
            if not any([dof in list(range(1, min([self.nodes[0].part.ndf, self.nodes[1].part.ndf])+1)) for dof in self.dofs]):
                raise ValueError("Invalid DOF") 
            return f"equalDOF {rNode} {cNode} {' '.join([str(dof) for dof in self.dofs])}"
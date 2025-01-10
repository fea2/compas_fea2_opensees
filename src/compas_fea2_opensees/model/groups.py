from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import ElementsGroup
from compas_fea2.model import NodesGroup
from compas_fea2.model.groups import FacesGroup
from compas_fea2.model.groups import PartsGroup


class OpenseesNodesGroup(NodesGroup):
    """"""

    __doc__ += NodesGroup.__doc__

    def __init__(self, nodes, **kwargs):
        super(OpenseesNodesGroup, self).__init__(nodes=nodes, **kwargs)

    def jobdata(self):
        return f"region {self.input_key} -nodeOnly {' '.join([str(node.input_key) for node in self.nodes])}"


class OpenseesElementsGroup(ElementsGroup):
    """"""

    __doc__ += ElementsGroup.__doc__

    def __init__(self, elements, **kwargs):
        super(OpenseesElementsGroup, self).__init__(elements=elements, **kwargs)

    def jobdata(self):
        return f"region {self.input_key} -eleOnly {' '.join([str(element.input_key) for element in self.elements])}"


class OpenseesFacesGroup(FacesGroup):
    """Opensees implementation of the :class:`compas_fea2.model.FacesGroup`.\n"""

    __doc__ += FacesGroup.__doc__

    def __init__(self, *, part, element_face, **kwargs):
        super(FacesGroup, self).__init__(part=part, element_face=element_face, **kwargs)

    def jobdata(self):
        raise NotImplementedError


class OpenseesPartsGroup(PartsGroup):
    """Opensees implementation of the :class:`compas_fea2.model.PartsGroup`.\n"""

    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, **kwargs):
        super(OpenseesPartsGroup, self).__init__(parts=parts, **kwargs)

    def jobdata(self):
        raise NotImplementedError

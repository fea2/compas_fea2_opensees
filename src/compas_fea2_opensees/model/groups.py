
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
        return f"region {self.key} -nodeOnly {' '.join([str(node.key) for node in self.nodes])}"


class OpenseesElementsGroup(ElementsGroup):
    """"""

    __doc__ += ElementsGroup.__doc__

    def __init__(self, elements, **kwargs):
        super(OpenseesElementsGroup, self).__init__(elements=elements, **kwargs)

    def jobdata(self):
        return f"region {self.key} -eleOnly {' '.join([str(element.key) for element in self.elements])}"


class OpenseesFacesGroup(FacesGroup):
    """Opensees implementation of the :class:`compas_fea2.model.FacesGroup`.\n"""

    __doc__ += FacesGroup.__doc__

    def __init__(self, faces, **kwargs):
        super(FacesGroup, self).__init__(faces, **kwargs)

    def jobdata(self):
        raise NotImplementedError


class OpenseesPartsGroup(PartsGroup):
    """Opensees implementation of the :class:`compas_fea2.model.PartsGroup`.\n"""

    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, **kwargs):
        super(OpenseesPartsGroup, self).__init__(parts=parts, **kwargs)

    def jobdata(self):
        raise NotImplementedError

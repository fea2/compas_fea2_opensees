from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import ConcentratedLoad
from compas_fea2.problem import PressureLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import TributaryLoad
from compas_fea2.problem import PrestressLoad
from compas_fea2.problem import HarmonicPointLoad
from compas_fea2.problem import HarmonicPressureLoad

from typing import Iterable


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


class OpenseesConcentratedLoad(ConcentratedLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.PointLoad`.\n
    """
    __doc__ += ConcentratedLoad.__doc__

    def __init__(self, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global', name=None, **kwargs):
        super(OpenseesConcentratedLoad, self).__init__(x=x, y=y, z=z, xx=xx, yy=yy, zz=zz, axes=axes, name=name, **kwargs)

    def jobdata(self, node):
        return '\tload {} {}'.format(node.input_key, ' '.join([str(self.components[dof] or 0.0) for dof in dofs[:node.part.ndf]]))


class OpenseesPressureLoad(PressureLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.AreaLoad`.\n
    """
    __doc__ += PressureLoad.__doc__

    def __init__(self, elements, x, y, z, axes, name=None, **kwargs):
        super(OpenseesPressureLoad, self).__init__(elements, x, y, z, axes, name=name, **kwargs)
        raise NotImplementedError


class OpenseesGravityLoad(GravityLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.GravityLoad`.\n
    """
    __doc__ += GravityLoad.__doc__

    def __init__(self, g=9.81, x=0., y=0., z=-1., name=None, **kwargs):
        super(OpenseesGravityLoad, self).__init__(g, x, y, z, name=name, **kwargs)

    # def jobdata(self, distribution):
    #     if not distribution:
    #         distribution=self.model.parts
    #     if not isinstance(distribution, Iterable):
    #         distribution = [distribution]
    #     jobdata = []
    #     for part in distribution:
    #         for element in part.elements:
    #             sw_node = [element.volume*self.g*element.section.material.density/len(element.nodes)*c for c in [self.x, self.y, self.z]]+[0.]*(part.ndm-3) #TODO check if ndm or ndof
    #             for n in element.nodes:
    #                 jobdata.append('\tload {} {}'.format(n.key, ' '.join([str(c) for c in sw_node])))
    #     return '\n'.join(jobdata)


class OpenseesPrestressLoad(PrestressLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.PrestressLoad`.\n
    """
    __doc__ += PrestressLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesPrestressLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class OpenseesTributaryLoad(TributaryLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.TributaryLoad`.\n
    """
    __doc__ += TributaryLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesTributaryLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError
        # for v in self.model.discretized_boudary_mesh.vertices():
        #     n = self.model.find_node_by_location(self.model.discretized_boudary_mesh.vertex_coordinates(v))
        #     gravity_load = GravityLoad(g, x, y, z)
        #     tributary_area = self.model.discretized_boudary_mesh.vertex_area(v)
        #     tributary_volume = tributary_area

class OpenseesHarmonicPointLoad(HarmonicPointLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.HarmonicPointLoad`.\n
    """
    __doc__ += HarmonicPointLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesHarmonicPointLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError


class OpenseesHarmonicPressureLoad(HarmonicPressureLoad):
    """OpenSees implementation of :class:`compas_fea2.problem.HarmonicPressureLoad`.\n
    """
    __doc__ += HarmonicPressureLoad.__doc__

    def __init__(self, components, axes='global', name=None, **kwargs):
        super(OpenseesHarmonicPressureLoad, self).__init__(components, axes, name, **kwargs)
        raise NotImplementedError

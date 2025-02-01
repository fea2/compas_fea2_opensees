from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Steel

# ==============================================================================
# non-linear metal
# ==============================================================================


class OpenseesSteel(Steel):
    """"""

    __doc__ += Steel.__doc__

    def __init__(self, *, fy, fu, eu, E, v, density, **kwargs):
        super(OpenseesSteel, self).__init__(fy=fy, fu=fu, eu=eu, E=E, v=v, density=density, **kwargs)
        self._EshE = (self.fu - self.fy) / self.ep

    @property
    def EshE(self):
        return self._EshE

    def jobdata(self):
        lines = ["uniaxialMaterial Steel01 {0} {1} {2} {3}".format(self.input_key, self.fy, self.E, self.EshE)]
        lines.append("nDMaterial ElasticIsotropic {} {} {} {}".format(self.input_key + 1000, self.E, self.v, self.density))
        return "\n".join(lines)

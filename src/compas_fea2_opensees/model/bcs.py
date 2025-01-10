from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import ClampBCXX
from compas_fea2.model import ClampBCYY
from compas_fea2.model import ClampBCZZ
from compas_fea2.model import FixedBC
from compas_fea2.model import FixedBCX
from compas_fea2.model import FixedBCY
from compas_fea2.model import FixedBCZ
from compas_fea2.model import GeneralBC
from compas_fea2.model import PinnedBC
from compas_fea2.model import RollerBCX
from compas_fea2.model import RollerBCXY
from compas_fea2.model import RollerBCXZ
from compas_fea2.model import RollerBCY
from compas_fea2.model import RollerBCYZ
from compas_fea2.model import RollerBCZ

dofs = ["x", "y", "z", "xx", "yy", "zz"]


def _jobdata(bc, nodes):
    return "\n".join(["fix {} {}".format(node.input_key, " ".join([str(int(getattr(bc, dof))) for dof in dofs[: node.part.ndf]])) for node in nodes])


class OpenseesGeneralBC(GeneralBC):
    """OpenSees implementation of :class:`compas_fea2.model.GeneralBC`.\n"""

    __doc__ += GeneralBC.__doc__

    def __init__(self, **kwargs):
        super(OpenseesGeneralBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesFixedBC(FixedBC):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBC`.\n"""

    __doc__ += FixedBC.__doc__

    def __init__(self, **kwargs):
        super(OpenseesFixedBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesFixedBCX(FixedBCX):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCX`.\n"""

    __doc__ += FixedBCX.__doc__

    def __init__(self, **kwargs):
        super(OpenseesFixedBCX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesFixedBCY(FixedBCY):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCY`.\n"""

    __doc__ += FixedBCY.__doc__

    def __init__(self, **kwargs):
        super(OpenseesFixedBCY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesFixedBCZ(FixedBCZ):
    """OpenSees implementation of :class:`compas_fea2.model.FixedBCZ`.\n"""

    __doc__ += FixedBCZ.__doc__

    def __init__(self, **kwargs):
        super(OpenseesFixedBCZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesPinnedBC(PinnedBC):
    """OpenSees implementation of :class:`compas_fea2.model.PinnedBC`.\n"""

    __doc__ += PinnedBC.__doc__

    def __init__(self, **kwargs):
        super(OpenseesPinnedBC, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesClampBCXX(ClampBCXX):
    """OpenSees implementation of :class:`compas_fea2.model.ClampBCXX`.\n"""

    __doc__ += ClampBCXX.__doc__

    def __init__(self, **kwargs):
        super(OpenseesClampBCXX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesClampBCYY(ClampBCYY):
    """OpenSees implementation of :class:`compas_fea2.model.ClampBCYY`.\n"""

    __doc__ += ClampBCYY.__doc__

    def __init__(self, **kwargs):
        super(OpenseesClampBCYY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesClampBCZZ(ClampBCZZ):
    """OpenSees implementation of :class:`ClampBCZZ`.\n"""

    __doc__ += ClampBCZZ.__doc__

    def __init__(self, **kwargs):
        super(OpenseesClampBCZZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesRollerBCX(RollerBCX):
    """OpenSees implementation of :class:`RollerBCX`.\n"""

    __doc__ += RollerBCX.__doc__

    def __init__(self, **kwargs):
        super(OpenseesRollerBCX, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesRollerBCY(RollerBCY):
    """OpenSees implementation of :class:`RollerBCY`.\n"""

    __doc__ += RollerBCY.__doc__

    def __init__(self, **kwargs):
        super(OpenseesRollerBCY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesRollerBCZ(RollerBCZ):
    """OpenSees implementation of :class:`RollerBCZ`.\n"""

    __doc__ += RollerBCZ.__doc__

    def __init__(self, **kwargs):
        super(OpenseesRollerBCZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesRollerBCXY(RollerBCXY):
    """OpenSees implementation of :class:`RollerBCXY`.\n"""

    __doc__ += RollerBCXY.__doc__

    def __init__(self, **kwargs):
        super(OpenseesRollerBCXY, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesRollerBCYZ(RollerBCYZ):
    """OpenSees implementation of :class:`RollerBCYZ`.\n"""

    __doc__ += RollerBCYZ.__doc__

    def __init__(self, **kwargs):
        super(OpenseesRollerBCYZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)


class OpenseesRollerBCXZ(RollerBCXZ):
    """OpenSees implementation of :class:`RollerBCXZ`.\n"""

    __doc__ += RollerBCXZ.__doc__

    def __init__(self, **kwargs):
        super(OpenseesRollerBCXZ, self).__init__(**kwargs)

    def jobdata(self, nodes):
        return _jobdata(self, nodes)

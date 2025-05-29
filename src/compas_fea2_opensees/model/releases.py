
from compas_fea2.model.releases import BeamEndPinRelease


class OpenseesBeamEndPinRelease(BeamEndPinRelease):
    def __init__(self, m1=False, m2=False, t=False, **kwargs):
        super(OpenseesBeamEndPinRelease, self).__init__(m1=m1, m2=m2, t=t, **kwargs)
        raise NotImplementedError

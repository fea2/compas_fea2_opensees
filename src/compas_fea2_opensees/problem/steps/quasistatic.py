
from compas_fea2.problem import DirectCyclicStep
from compas_fea2.problem import QuasiStaticStep


class OpenseesQuasiStaticStep(QuasiStaticStep):
    def __init__(self, **kwargs):
        super(OpenseesQuasiStaticStep, self).__init__(**kwargs)
        raise NotImplementedError


class OpenseesDirectCyclicStep(DirectCyclicStep):
    def __init__(self, **kwargs):
        super(OpenseesDirectCyclicStep, self).__init__(**kwargs)
        raise NotImplementedError

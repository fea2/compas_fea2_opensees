
from compas_fea2.problem import DynamicStep


class OpenseesDynamicStep(DynamicStep):
    def __init__(self, **kwargs):
        super(OpenseesDynamicStep, self).__init__(**kwargs)
        raise NotImplementedError

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem import DynamicStep


class OpenseesDynamicStep(DynamicStep):
    def __init__(self, **kwargs):
        super(OpenseesDynamicStep, self).__init__(**kwargs)
        raise NotImplementedError

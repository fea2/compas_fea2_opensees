from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.results import Result, DisplacementResult, StressResult
from compas_fea2.results import NodeFieldResults, ElementFieldResults

class OpenseesResult(Result):

    def __init__(self, location, name=None, *args, **kwargs):
        super(OpenseesResult, self).__init__(location, name=name, *args, **kwargs)


class OpenseesDisplacementResult(DisplacementResult):

    def __init__(self, location, u1, u2, u3, name=None, *args, **kwargs):
        super(OpenseesDisplacementResult, self).__init__(location, u1, u2, u3, name=name, *args, **kwargs)


class OpenseesStressResult(StressResult):

    def __init__(self, location, local_stress_tensor, name=None, *args, **kwargs):
        super(OpenseesStressResult, self).__init__(location, local_stress_tensor, name=name, *args, **kwargs)


class OpenseesNodeFieldResults(NodeFieldResults):
    def __init__(self, field_name,step, name=None, *args, **kwargs):
        super(OpenseesNodeFieldResults, self).__init__(field_name, step, name, *args, **kwargs)

class OpenseesElementFieldResults(ElementFieldResults):
    def __init__(self, field_name,step, name=None, *args, **kwargs):
        super(OpenseesElementFieldResults, self).__init__(field_name, step, name, *args, **kwargs)


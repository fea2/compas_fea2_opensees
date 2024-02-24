from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.results import Result, DisplacementResult, StressResult
from compas_fea2.results import DisplacementFieldResults, ElementFieldResults

class OpenseesResult(Result):

    def __init__(self, location, name=None, *args, **kwargs):
        super(OpenseesResult, self).__init__(location, name=name, *args, **kwargs)


class OpenseesDisplacementResult(DisplacementResult):

    def __init__(self, location, u1=0., u2=0., u3=0., name=None, *args, **kwargs):
        super(OpenseesDisplacementResult, self).__init__(location, u1, u2, u3, name=name, *args, **kwargs)


class OpenseesStressResult(StressResult):

    def __init__(self, location, local_stress_tensor, name=None, *args, **kwargs):
        super(OpenseesStressResult, self).__init__(location, local_stress_tensor, name=name, *args, **kwargs)


class OpenseesDisplacementFieldResults(DisplacementFieldResults):
    def __init__(self, name=None, *args, **kwargs):
        super(OpenseesDisplacementFieldResults, self).__init__(name=name, *args, **kwargs)

class OpenseesElementFieldResults(ElementFieldResults):
    def __init__(self, field_name,step, name=None, *args, **kwargs):
        super(OpenseesElementFieldResults, self).__init__(field_name, step, name, *args, **kwargs)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
from pathlib import Path
from time import time
from subprocess import Popen
from subprocess import PIPE

from compas_fea2.results import Results, StepResults, NodeFieldResults

class OpenseesResults(Results):

    def __init__(self, location, components, invariants, name=None, *kwargs):
        super(OpenseesResults, self).__init__(location, components, invariants, name=name, *kwargs)

class OpenseesStepResults(StepResults):
    def __init__(self, step, model, name=None):
        super(OpenseesStepResults, self).__init__(step, model, name)

class OpenseesNodeFieldResults(NodeFieldResults):
    def __init__(self, field_name,step, name=None, *args, **kwargs):
        super(OpenseesNodeFieldResults, self).__init__(field_name, step, name, *args, **kwargs)


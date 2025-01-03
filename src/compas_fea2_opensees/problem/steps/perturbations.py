from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import ModalAnalysis
from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ComplexEigenValue
from compas_fea2.problem.steps import LinearStaticPerturbation
from compas_fea2.problem.steps import StedyStateDynamic
from compas_fea2.problem.steps import SubstructureGeneration


class OpenseesModalAnalysis(ModalAnalysis):
    """"""
    __doc__ += ModalAnalysis.__doc__

    def __init__(self, modes=1, name=None, **kwargs):
        super(OpenseesModalAnalysis, self).__init__(modes, name=name, **kwargs)
        self.modes = modes

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
recorder Node -file eigenvalues.out -nodeRange 1 10 -dof 1 2 3 eigen {self.modes}
eigen {self.modes}
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(self.name)


class OpenseesComplexEigenValue(ComplexEigenValue):
    """"""
    __doc__ += ComplexEigenValue.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesComplexEigenValue, self).__init__(name, **kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
complexEigen
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(self.name)


class OpenseesBucklingAnalysis(BucklingAnalysis):
    """"""
    __doc__ += BucklingAnalysis.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesBucklingAnalysis, self).__init__(name, **kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
buckling
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(self.name)


class OpenseesLinearStaticPerturbation(LinearStaticPerturbation):
    """"""
    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, name=None, **kwargs):
        super(OpenseesLinearStaticPerturbation, self).__init__(name=name, **kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
linearStaticPerturbation
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(self.name)


class OpenseesStedyStateDynamic(StedyStateDynamic):
    """"""
    __doc__ += StedyStateDynamic.__doc__

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
steadyStateDynamic
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(self.name)


class OpenseesSubstructureGeneration(SubstructureGeneration):
    """"""
    __doc__ += SubstructureGeneration.__doc__

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
substructureGeneration
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(self.name)

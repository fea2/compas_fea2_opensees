from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ComplexEigenValue
from compas_fea2.problem.steps import LinearStaticPerturbation
from compas_fea2.problem.steps import ModalAnalysis
from compas_fea2.problem.steps import StedyStateDynamic
from compas_fea2.problem.steps import SubstructureGeneration


class OpenseesModalAnalysis(ModalAnalysis):
    """Perform a modal analysis using OpenSees.
    Check the OpenSees documentation for more information:
    https://opensees.github.io/OpenSeesDocumentation/user/manual/analysis/eigen.html#eigen

    Additional Parameters
    ---------------------
    solver : str, optional
        Solver to use, by default -genBandArpack. Either optons are: "genBandArpack", "symmBandLapack", "fullGenLapack"

    Explanation
    -----------
    After set eigenValues [eigen $numModes], OpenSees internally stores
    the eigenvectors for each DOF in each node.
    nodeEigenvector <nodeTag> <mode> returns a list of the displacement
    eigenvector components (one for each DOF, 6 in 3D).
    For a typical 3D beam element, you have 6 DOFs per node:
    [u_x,\\, u_y,\\, u_z,\\, \\theta_x,\\, \\theta_y,\\, \\theta_z].

    By default, OpenSees normalizes the mode shapes to unit values
    (or such that the sum of squares of the DOFs equals 1, depending on the solver).
    If you need a different normalization or if you want to scale them for visualization,
    you can apply a factor when printing or post-processing these values.
    """

    __doc__ += ModalAnalysis.__doc__

    def __init__(
        self,
        *,
        modes=1,
        solver="genBandArpack",
        **kwargs,
    ):
        super(OpenseesModalAnalysis, self).__init__(modes, **kwargs)
        self.solver = solver

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
# - Analysis Parameters
#   -------------------
{self._generate_analysis_section()}
#
# - Output Results
#   --------------
{self._generate_output_section()}
#
"""

    def _generate_header_section(self):
        return f"""#
# STEP {self.name}
#
# Define the number of modes to compute
set numModes {self.modes}
#"""

    def _generate_analysis_section(self):
        return """
# Compute eigenvalues (lambda) for the first 'numModes' modes
set eigenValues [eigen $numModes]
record
"""

    def _generate_output_section(self):
        return f"""
set eigenFile [open "eigenvalues.out" "w"]

puts "------------------------------------------------------------------"
puts "Modal Analysis Results:"
puts "  Mode :   Lambda        Omega (rad/s)    Freq (Hz)   Period (s)"
puts "------------------------------------------------------------------"

for {{set iMode 1}} {{$iMode <= $numModes}} {{incr iMode}} {{
    # lambda = eigenvalue
    set lambda   [lindex $eigenValues [expr $iMode-1]]
    set omega    [expr sqrt($lambda)]            ;# rad/s
    set freqHz   [expr $omega/(2.0*3.14159265359)]
    set Period   [expr 1.0/$freqHz]
    puts "   $iMode   :   $lambda   $omega   $freqHz  $Period"
    puts $eigenFile "$iMode $lambda $omega $freqHz $Period"
}}
puts "Modal analysis results have been exported to eigen.out"
close $eigenFile
#
set nNodes {len(self.model.nodes)}

# Open a file for all eigenvectors
set shapeFile [open "eigenvectors.out" "w"]

for {{set iMode 1}} {{$iMode <= $numModes}} {{incr iMode}} {{
    for {{set iNode 0}} {{$iNode < $nNodes}} {{incr iNode}} {{
        puts $shapeFile [format "%d %d %s" $iMode $iNode [nodeEigenvector $iNode $iMode]]
    }}
}}
close $shapeFile


modalProperties -print -file "ModalReport.out" -unorm
"""


class OpenseesComplexEigenValue(ComplexEigenValue):
    """"""

    __doc__ += ComplexEigenValue.__doc__

    def __init__(self, **kwargs):
        super(OpenseesComplexEigenValue, self).__init__(**kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
complexEigen
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(
            self.name
        )


class OpenseesBucklingAnalysis(BucklingAnalysis):
    """"""

    __doc__ += BucklingAnalysis.__doc__

    def __init__(self, **kwargs):
        super(OpenseesBucklingAnalysis, self).__init__(**kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
buckling
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(
            self.name
        )


class OpenseesLinearStaticPerturbation(LinearStaticPerturbation):
    """"""

    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, **kwargs):
        super(OpenseesLinearStaticPerturbation, self).__init__(**kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
linearStaticPerturbation
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(
            self.name
        )


class OpenseesStedyStateDynamic(StedyStateDynamic):
    """"""

    __doc__ += StedyStateDynamic.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
steadyStateDynamic
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(
            self.name
        )


class OpenseesSubstructureGeneration(SubstructureGeneration):
    """"""

    __doc__ += SubstructureGeneration.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
substructureGeneration
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#""".format(
            self.name
        )

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
    """

    Explanation
    -----------
    After set eigenValues [eigen $numModes], OpenSees internally stores
    the eigenvectors for each DOF in each node.
    nodeEigenvector <nodeTag> <mode> returns a list of the displacement
    eigenvector components (one for each DOF, 6 in 3D).
    For a typical 3D beam element, you have 6 DOFs per node:
    [u_x,\, u_y,\, u_z,\, \theta_x,\, \theta_y,\, \theta_z].

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
        max_increments=1,
        initial_inc_size=1,
        min_inc_size=0.00001,
        constraint="Plain",
        numberer="RCM",
        system="BandGeneral",
        test="NormUnbalance 1.0e-12 100",
        integrator="NewmarkExplicit 0",  # "Newmark 0.5 0.25",
        analysis="Transient",
        time=1,
        algorithm="Linear",
        **kwargs,
    ):
        super(OpenseesModalAnalysis, self).__init__(modes, **kwargs)
        self.max_increments = max_increments
        self.initial_inc_size = initial_inc_size
        self.min_inc_size = min_inc_size
        self.constraint = constraint
        self.numberer = numberer
        self.system = system
        self.test = test
        self.integrator = integrator
        self.analysis = analysis
        self.time = (time,)
        self.algorithm = algorithm

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
        return f"""# Define a simple system/analysis setup for the eigenvalue solver
system {self.system}
constraints {self.constraint}
numberer {self.numberer}
test {self.test}
algorithm {self.algorithm}
integrator {self.integrator}
analysis {self.analysis}

# Compute eigenvalues (lambda) for the first 'numModes' modes
set eigenValues [eigen $numModes]
record 

puts "Eigenvalues found: $eigenValues"

puts "------------------------------------------------------------"
puts "Modal Analysis Results:"
puts "  Mode :   Lambda        Omega (rad/s)    Freq (Hz)"
puts "------------------------------------------------------------"

for {{set iMode 1}} {{$iMode <= $numModes}} {{incr iMode}} {{
    # lambda = eigenvalue
    set lambda   [lindex $eigenValues [expr $iMode-1]]
    set omega    [expr sqrt($lambda)]            ;# rad/s
    set freqHz   [expr $omega/(2.0*3.14159265359)]
    puts "   $iMode   :   $lambda   $omega   $freqHz"
}}

puts "------------------------------------------------------------"

#"""

    def _generate_output_section(self):
        massMatrix = [f"[lindex $massMatrix {i}]" for i in range(6)]
        return f"""# Write the modal shapes to a file

recoreder -file modal_shapes_all_nodes.out 
    
set nNodes {len(self.model.nodes)}

# Open a file for all eigenvectors
set shapeFile [open "modal_shapes_all_nodes.out" "w"]

# Save all eigenvectors at once using OpenSees output
puts $shapeFile "---------------------------------------------------"
puts $shapeFile "Modal Shapes for All Nodes and All Modes"
puts $shapeFile "---------------------------------------------------"

puts $shapeFile "Eigenvalues: $eigenValues"

# Use batch-style processing for eigenvectors
for {{set iMode 1}} {{$iMode <= $numModes}} {{incr iMode}} {{
    puts $shapeFile "\nMode $iMode:"
    
    # Add a custom 'print nodeEigenvector' script
    for {{set iNode 0}} {{$iNode < $nNodes}} {{incr iNode}} {{
        puts $shapeFile [format "Node %d : %s" $iNode [nodeEigenvector $iNode $iMode]]
    }}
}}
close $shapeFile


# set modalMassFile [open "modal_mass_6dof.out" w]
# puts $modalMassFile "Mode   Modal Mass"

# for {{set mode 1}} {{$mode <= $nNodes}} {{incr mode}} {{
#     set modalMass 0.0

#     for {{set node 1}} {{$node <= $nNodes}} {{incr node}} {{
#         # Get eigenvector (modal shape) for the node and mode
#         set eigenvector [nodeEigenvector $node $mode]

#         # Get nodal mass matrix (6x6)
#         set massMatrix [mass $node]

#         # Extract eigenvector components
#         set ux [lindex $eigenvector 0]
#         set uy [lindex $eigenvector 1]
#         set uz [lindex $eigenvector 2]
#         set rx [lindex $eigenvector 3]
#         set ry [lindex $eigenvector 4]
#         set rz [lindex $eigenvector 5]

#         # Compute contribution to modal mass
#         set nodeMass [expr \
#             $massMatrix(0,0)*$ux*$ux + $massMatrix(1,1)*$uy*$uy + $massMatrix(2,2)*$uz*$uz + \
#             $massMatrix(3,3)*$rx*$rx + $massMatrix(4,4)*$ry*$ry + $massMatrix(5,5)*$rz*$rz]
#         set modalMass [expr $modalMass + $nodeMass]
#     }}

#     # Output modal mass for the current mode
#     puts $modalMassFile "$mode   $modalMass"
# }}

# close $modalMassFile
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

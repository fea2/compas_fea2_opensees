from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import AccelerationFieldOutput
from compas_fea2.problem.outputs import DisplacementFieldOutput
from compas_fea2.problem.outputs import ReactionFieldOutput
from compas_fea2.problem.outputs import Stress2DFieldOutput
from compas_fea2.problem.outputs import VelocityFieldOutput
from compas_fea2.problem.outputs import SectionForcesFieldOutput
from compas_fea2.problem.outputs import HistoryOutput


def tcl_export_node_results(field_name, function_name):
    return f"""
set {field_name}File [open "{field_name}.out" "w"]
set allNodes [getNodeTags]
foreach nodeTag $allNodes {{
    set {field_name} [{function_name} $nodeTag]
    puts ${field_name}File "$nodeTag ${field_name}"
}}
close ${field_name}File
"""


class OpenseesDisplacementFieldOutput(DisplacementFieldOutput):
    """"""

    __doc__ += DisplacementFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesDisplacementFieldOutput, self).__init__(**kwargs)

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeDisp")


class OpenseesAccelerationFieldOutput(AccelerationFieldOutput):
    """"""

    __doc__ += AccelerationFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesAccelerationFieldOutput, self).__init__(**kwargs)

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeAccel")


class OpenseesVelocityFieldOutput(VelocityFieldOutput):
    """"""

    __doc__ += VelocityFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesVelocityFieldOutput, self).__init__(**kwargs)

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeVel")


class OpenseesReactionFieldOutput(ReactionFieldOutput):
    """"""

    __doc__ += ReactionFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesReactionFieldOutput, self).__init__(**kwargs)

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeReaction")


class OpenseesStress2DFieldOutput(Stress2DFieldOutput):
    """"""

    __doc__ += Stress2DFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesStress2DFieldOutput, self).__init__(**kwargs)

    def jobdata(self):
        return f"""
# ---------------------------------------------
# Custom Element Stress Export Script
# ---------------------------------------------
set stressFile [open "{self.field_name}.out" "w"]
set allElements [getEleTags]
foreach eleTag $allElements {{
    set eleStresses [eleResponse $eleTag "stresses"]
    puts $stressFile "$eleTag $eleStresses"
}}
close $stressFile
puts "Element stresses have been exported to {self.field_name}.out"

# ---------------------------------------------
# Custom Element Strain Export Script
# ---------------------------------------------
set strainFile [open "{self.field_name}_str.out" "w"]
set allElements [getEleTags]
foreach eleTag $allElements {{
    set eleDeformation [eleResponse $eleTag "deformation"]
    puts $strainFile "$eleTag $eleDeformation"
}}
close $strainFile
puts "Element strains have been exported to {self.field_name}_str.out"

# ---------------------------------------------
# Custom Element Strain Export Script
# ---------------------------------------------
set deformationFile [open "{self.field_name}_def.out" "w"]
set allElements [getEleTags]
foreach eleTag $allElements {{
    set eleDeformation [eleResponse $eleTag "deformation"]
    puts $deformationFile "$eleTag $eleDeformation"
}}
close $deformationFile
puts "Element deformations have been exported to {self.field_name}_def.out"
"""


class OpenseesSectionForcesFieldOutput(SectionForcesFieldOutput):
    """"""

    __doc__ += SectionForcesFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesSectionForcesFieldOutput, self).__init__(**kwargs)

    def jobdata(self):
        return f"""
# ---------------------------------------------
# Custom Element Section Force Export Script
# ---------------------------------------------
# Open a file to write the section forces
set sectionForceFile [open "{self.field_name}.out" "w"]

# Get all element tags in the model
set allElements [getEleTags]

# Loop through each element and extract section forces
foreach eleTag $allElements {{

    set secForces [eleResponse $eleTag "force"]

    # Write the element tag, section number, and forces to the file
    puts $sectionForceFile "$eleTag $secForces"
    }}

# Close the file
close $sectionForceFile

# Print a message indicating the export is complete
puts "Section forces have been exported to {self.field_name}.out"
"""


class OpenseesHistoryOutput(HistoryOutput):
    """"""

    __doc__ += HistoryOutput.__doc__

    def __init__(self):
        super(OpenseesHistoryOutput, self).__init__()
        raise NotImplementedError

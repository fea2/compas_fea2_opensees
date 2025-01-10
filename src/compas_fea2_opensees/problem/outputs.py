from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import AccelerationFieldOutput
from compas_fea2.problem.outputs import DisplacementFieldOutput
from compas_fea2.problem.outputs import FieldOutput
from compas_fea2.problem.outputs import HistoryOutput
from compas_fea2.problem.outputs import ReactionFieldOutput
from compas_fea2.problem.outputs import Stress2DFieldOutput
from compas_fea2.problem.outputs import VelocityFieldOutput


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
        return f"""
# ---------------------------------------------
# Custom Displacement Export Script
# ---------------------------------------------
set dispFile [open "{self.field_name}.out" "w"]
set allNodes [getNodeTags]
foreach nodeTag $allNodes {{
    set disp [nodeDisp $nodeTag]
    puts $dispFile "$nodeTag $disp"
}}
close $dispFile
puts "Displacements have been exported to {self.field_name}.out"
"""


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
"""


class OpenseesFieldOutput(FieldOutput):
    """"""

    __doc__ += FieldOutput.__doc__

    def __init__(self, node_outputs=None, element_outputs=None, **kwargs):
        super(OpenseesFieldOutput, self).__init__(node_outputs=node_outputs, element_outputs=element_outputs, contact_outputs=None, **kwargs)


class OpenseesHistoryOutput(HistoryOutput):
    """"""

    __doc__ += HistoryOutput.__doc__

    def __init__(self):
        super(OpenseesHistoryOutput, self).__init__()
        raise NotImplementedError

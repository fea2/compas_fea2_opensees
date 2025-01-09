from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import (
    FieldOutput, 
    HistoryOutput, 
    DisplacementFieldOutput,
    ReactionFieldOutput,
    Stress2DFieldOutput,
    )

class OpenseesDisplacementFieldOutput(DisplacementFieldOutput):
    """"""
    __doc__ += DisplacementFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesDisplacementFieldOutput, self).__init__(**kwargs)
    
    def jobdata(self):
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

class OpenseesReactionFieldOutput(ReactionFieldOutput):
    """"""
    __doc__ += ReactionFieldOutput.__doc__

    def __init__(self, **kwargs):
        super(OpenseesReactionFieldOutput, self).__init__(**kwargs)
    
    def jobdata(self):
        return f"""
# ---------------------------------------------
# Custom Reaction Export Script
# ---------------------------------------------
set reactFile [open "{self.field_name}.out" "w"]
set allNodes [getNodeTags]
foreach nodeTag $allNodes {{
    set react [nodeReaction $nodeTag]
    puts $reactFile "$nodeTag $react"
}}
close $reactFile
puts "Reactions have been exported to {self.field_name}.out"
"""

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
        super(OpenseesFieldOutput, self).__init__(node_outputs=node_outputs,
                                                  element_outputs=element_outputs,
                                                  contact_outputs=None,
                                                **kwargs)

class OpenseesHistoryOutput(HistoryOutput):
    """"""
    __doc__ += HistoryOutput.__doc__

    def __init__(self):
        super(OpenseesHistoryOutput, self).__init__()
        raise NotImplementedError

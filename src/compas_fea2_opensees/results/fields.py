from compas_fea2.results.fields import DisplacementFieldResults
from compas_fea2.results.fields import ReactionFieldResults
from compas_fea2.results.fields import SectionForcesFieldResults
from compas_fea2.results.fields import StressFieldResults
from compas_fea2.results.fields import ContactForcesFieldResults


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


class OpenseesDisplacementFieldResults(DisplacementFieldResults):
    def __init__(self, step, *args, **kwargs):
        super().__init__(step, *args, **kwargs)
        self.input_name = "U"
        self.output_type = "node"

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeDisp")


# class OpenseesAccelerationFieldResults(AccelerationFieldResults):
#     def __init__(self, step, *args, **kwargs):
#         super().__init__(step, *args, **kwargs)
#         self.input_name = "A"
#         self.output_type = "node"

#     def jobdata(self):
#         return tcl_export_node_results(self.field_name, "nodeAccel")


# class OpenseesVelocityFieldResults(VelocityFieldResults):
#     def __init__(self, step, *args, **kwargs):
#         super().__init__(step, *args, **kwargs)
#         self.input_name = "V"
#         self.output_type = "node"

#     def jobdata(self):
#         return tcl_export_node_results(self.field_name, "nodeVel")


class OpenseesReactionFieldResults(ReactionFieldResults):
    def __init__(self, step, *args, **kwargs):
        super().__init__(step, *args, **kwargs)
        self.input_name = "RF"
        self.output_type = "node"

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeReaction")


class OpenseesSectionForcesFieldResults(SectionForcesFieldResults):
    def __init__(self, step, *args, **kwargs):
        super().__init__(step, *args, **kwargs)
        self.input_name = "SF"
        self.output_type = "element"

    def jobdata(self):
        return "SF"


class OpenseesStressFieldResults(StressFieldResults):
    def __init__(self, step, *args, **kwargs):
        super().__init__(step, *args, **kwargs)
        self.input_name = "S"
        self.output_type = "element"

    def jobdata(self):
        return "S"


class OpenseesContactFieldResults(ContactForcesFieldResults):
    def __init__(self, step, *args, **kwargs):
        super().__init__(step, *args, **kwargs)
        self.input_name = "CFORCE"
        self.output_type = "element"

    def jobdata(self):
        return NotImplementedError(
            "Opensees does not support contact forces field results in the same way as other fields. "
            "You may need to implement a custom method to extract contact forces."
        )

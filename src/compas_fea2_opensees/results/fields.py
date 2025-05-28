import os

from compas_fea2.results import DisplacementFieldResults
from compas_fea2.results import ReactionFieldResults
from compas_fea2.results import SectionForcesFieldResults
from compas_fea2.results import StressFieldResults


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


def _extract_results(obj):
    """
    Read the .csv results file and convert it to a dictionary.

    Parameters
    ----------
    database_path : path
        Path to the folder where the sqlite database will be created
    database_name : str
        Name of the database
    field_output : :class:`compas_fea2.problem.FieldOutput`
        FieldOutput object containing the nodes and/or element outputs to extract.
    """
    
    import numpy as np
    from compas_fea2.results.database import ResultsDatabase
    

    results = []
    with open(os.path.join(obj.problem.path, f"{obj.field_name}.out"), "r") as f:
        # remove the first line of names of columns
        lines = f.readlines()[0:]
        for line in lines:
            columns = line.split()
            input_key = int(columns[0])  # Convert the first column to int
            member = getattr(obj.model, obj.results_func)(input_key)[0]
            values = list(map(lambda x: round(float(x), 6), columns[1:]))
            if not values:
                continue

            # NOTE: OpenSees outputs the stresses at the integration points, so we need to average them to get the element stresses
            if obj.field_name == "s2d":
                num_integration_points = 4
                num_columns = len(values) // num_integration_points
                reshaped_data = np.array(values).reshape((num_integration_points, num_columns))
                averages = np.mean(reshaped_data, axis=0)
                values = averages.tolist()
                # NOTE: The OpenSees output is generalised stress, so we need to convert it to True stress
                t = member.section.t
                true_stresses = {
                    "sigma_11": values[0] / t,
                    "sigma_22": values[1] / t,
                    "tau_12": values[2] / t,
                    "sigma_b11": 6 * values[3] / t**2,
                    "sigma_b22": 6 * values[4] / t**2,
                    "sigma_b12": 6 * values[5] / t**2,
                    "tau_q1": values[6] / (t * 5 / 6),  # Assuming shear area = 5/6 * t
                    "tau_q2": values[7] / (t * 5 / 6),
                }
                values = list(true_stresses.values())

            if len(values) < len(obj.components_names):
                values = values + [0.0] * (len(obj.components_names) - len(values))
            elif len(values) > len(obj.components_names):
                values = values[: len(obj.components_names)]
            else:
                values = values

            results.append([member.key] + [obj.step.name, member.part.name] + values)

    ResultsDatabase.sqlite(obj.problem).create_table_for_output_class(obj, results)


class OpenseesDisplacementFieldResults(DisplacementFieldResults):
    """"""

    __doc__ += DisplacementFieldResults.__doc__

    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeDisp")

    def extract_results(self):
        _extract_results(self)


class OpenseesReactionFieldResults(ReactionFieldResults):
    """"""

    __doc__ += ReactionFieldResults.__doc__

    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

    def jobdata(self):
        return tcl_export_node_results(self.field_name, "nodeReaction")

    def extract_results(self):
        _extract_results(self)


class OpenseesSectionForcesFieldResults(SectionForcesFieldResults):
    """"""

    __doc__ += ReactionFieldResults.__doc__

    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

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

    def extract_results(self):
        _extract_results(self)


class OpenseesStressFieldResults(StressFieldResults):
    def __init__(self, step, **kwargs):
        super().__init__(step, **kwargs)

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

    def extract_results(self):
        _extract_results(self)

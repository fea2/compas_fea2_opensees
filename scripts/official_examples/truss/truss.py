"""
Example: 2D 3-element truss in compas_fea2
Replicating the OpenSees example with:
 - 4 nodes
 - 3 truss elements
 - Elastic material
 - Single nodal load
 - Static analysis
"""

# =============================================================================
# 1. Imports
# =============================================================================
import os

import compas_fea2
from compas_fea2.model import Model, Part
from compas_fea2.model import Node
from compas_fea2.model import TrussSection
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import TrussElement
from compas_fea2.problem import Problem
from compas_fea2.problem import (
    LoadCombination,
    DisplacementFieldOutput,
    AccelerationFieldOutput,
    ReactionFieldOutput,
)

from compas_fea2_opensees import TEMP

# Set the backend implementation
compas_fea2.set_backend("compas_fea2_opensees")

# =============================================================================
# 2. Create the Model
# =============================================================================
model = Model(name="Basic_Truss_Example")
prt = Part(name="Truss", ndf=2, ndm=2)
model.add_part(prt)

# =============================================================================
# 3. Define Nodes (2D => z = 0)
#    Node numbering matches the original OpenSees script
# =============================================================================
n1 = Node(name="N1", xyz=(0.0, 0.0, 0.0))
n2 = Node(name="N2", xyz=(144.0, 0.0, 0.0))
n3 = Node(name="N3", xyz=(168.0, 0.0, 0.0))
n4 = Node(name="N4", xyz=(72.0, 96.0, 0.0))
prt.add_nodes([n1, n2, n3, n4])

# =============================================================================
# 4. Material & Sections
#    - Equivalent to "uniaxialMaterial Elastic 1 3000" in OpenSees
#    - Using a simple isotropic or deformable material with E=3000
# =============================================================================
material = ElasticIsotropic(name="Mat_E3000", E=3000.0, v=0.3, density=1.0)  # example
section_10 = TrussSection(name="TrussSec_A10", A=10.0, material=material)
section_5 = TrussSection(name="TrussSec_A5", A=5.0, material=material)

# =============================================================================
# 5. Define Truss Elements
#    - Each "element truss" from OpenSees becomes a TrussElement
# =============================================================================
# element Truss 1 1 4 10.0 1
elem_1 = TrussElement(name="E1", nodes=[n1, n4], section=section_10)
# element Truss 2 2 4 5.0 1
elem_2 = TrussElement(name="E2", nodes=[n2, n4], section=section_5)
# element Truss 3 3 4 5.0 1
elem_3 = TrussElement(name="E3", nodes=[n3, n4], section=section_5)
prt.add_elements([elem_1, elem_2, elem_3])

# =============================================================================
# 6. Boundary Conditions
#    - "pin 1 1 1" => x,y restraints
#    - compas_fea2 is 3D, so also fix z to keep node from out-of-plane movement
# =============================================================================
model.add_pin_bc(nodes=[n1, n2, n3])

# =============================================================================
# 7. Analysis Steps
#    - Single linear static step, similar to "analyze 1"
# =============================================================================
prb = Problem("point_load")
step = prb.add_static_step(name="StaticStep")

# =============================================================================
# 8. Loading
#    - "load 4 100 -50" => 100 kip in x, -50 kip in y
#    - in compas_fea2 this is a node pattern
# =============================================================================
step.add_node_pattern(name="Load_N4", nodes=[n4], x=100.0, y=-50.0, z=0.0, load_case="LL")
step.combination = LoadCombination.SLS()
# step.add_output(FieldOutput(node_outputs=['U']))
step.add_output(DisplacementFieldOutput())
step.add_output(ReactionFieldOutput())
step.add_output(AccelerationFieldOutput())

# =============================================================================
# 9. Run the Analysis (OpenSees example)
# =============================================================================
model.add_problem(prb)
prb.analyse_and_extract(problems=[prb], path=os.path.join(TEMP, prb.name), verbose=True)

# =============================================================================
# 10. Post-processing & Outputs
#     - compas_fea2 automatically stores results in the Model's results structure.
#     - You can print or export nodal displacements, element forces, etc.
# =============================================================================
disp = prb.displacement_field
react = prb.reaction_field
print(disp.get_results(members=[n4], steps=[step])[step][0].vector)

assert round(disp.get_results(members=[n4], steps=[step])[step][0].vector.x, 3) == 0.530
assert round(disp.get_results(members=[n4], steps=[step])[step][0].vector.y, 3) == -0.178
print("Results match OpenSees example!")

# Show results
# prb.show_displacements(step, show_bcs=0.1)
prb.show_reactions(step, show_bcs=0.1)
# prb.show_deformed(scale_results=100, show_original=0.2, show_bcs=0.01)

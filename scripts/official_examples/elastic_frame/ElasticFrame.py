from compas_fea2.model import Model, Part, Node, BeamElement, ElasticIsotropic, GenericBeamSection
from compas_fea2.problem import Problem, ModalAnalysis
from compas_fea2_opensees import TEMP
import os
import compas_fea2

# Set the backend implementation
compas_fea2.set_backend("compas_fea2_opensees")

# Variables
g = 386.4
ft = 12.0
Load1 = 1185.0
Load2 = 1185.0
Load3 = 970.0

# set floor masses
m1 = Load1 / (4 * g)  # 4 nodes per floor
m2 = Load2 / (4 * g)
m3 = Load3 / (4 * g)

# set floor distributed loads
w1 = Load1 / (90 * ft)  # frame 90 ft long
w2 = Load2 / (90 * ft)
w3 = Load3 / (90 * ft)

# Initialize the model
mdl = Model(name="ElasticFrame")
prt = mdl.add_part(Part(name="ElasticFrame-1"))
prt.ndm = 2
prt.ndf = 3

# Define material properties (Steel)
steel = ElasticIsotropic(name="Steel", E=29000.0, v=0.3, density=0.0)

# Define cross-sectional properties
section_col_small = GenericBeamSection(name="W14X257", A=75.6, Ixx=3400.0, Iyy=0, Ixy=0, Avx=0, Avy=0, J=0, g0=0, gw=0, material=steel)
section_col_large = GenericBeamSection(name="W14X311", A=91.4, Ixx=4330.0, Iyy=0, Ixy=0, Avx=0, Avy=0, J=0, g0=0, gw=0, material=steel)
section_beam1 = GenericBeamSection(name="W33X118", A=34.7, Ixx=5900.0, Iyy=0, Ixy=0, Avx=0, Avy=0, J=0, g0=0, gw=0, material=steel)
section_beam2 = GenericBeamSection(name="W30X116", A=34.2, Ixx=4930.0, Iyy=0, Ixy=0, Avx=0, Avy=0, J=0, g0=0, gw=0, material=steel)
section_beam3 = GenericBeamSection(name="W24X68", A=20.1, Ixx=1830.0, Iyy=0, Ixy=0, Avx=0, Avy=0, J=0, g0=0, gw=0, material=steel)

# Create nodes
nodes_data = {
    1: [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
    2: [(360.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
    3: [(720.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
    4: [(1080.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
    5: [(0.0, 162.0, 0.0), (m1, m1, 0.0)],
    6: [(360.0, 162.0, 0.0), (m1, m1, 0.0)],
    7: [(720.0, 162.0, 0.0), (m1, m1, 0.0)],
    8: [(1080.0, 162.0, 0.0), (m1, m1, 0.0)],
    9: [(0.0, 324.0, 0.0), (m2, m2, 0.0)],
    10: [(360.0, 324.0, 0.0), (m2, m2, 0.0)],
    11: [(720.0, 324.0, 0.0), (m2, m2, 0.0)],
    12: [(1080.0, 324.0, 0.0), (m2, m2, 0.0)],
    13: [(0.0, 486.0, 0.0), (m3, m3, 0.0)],
    14: [(360.0, 486.0, 0.0), (m3, m3, 0.0)],
    15: [(720.0, 486.0, 0.0), (m3, m3, 0.0)],
    16: [(1080.0, 486.0, 0.0), (m3, m3, 0.0)],
}

for nid, data in nodes_data.items():
    prt.add_node(Node(name=nid, xyz=data[0], mass=data[1]))

# Apply boundary conditions (fixed supports at base nodes)
for nid in [1, 2, 3, 4]:
    n = prt.find_node_by_key(nid - 1)
    mdl.add_pin_bc(n)

# Define elements
columns_info = [
    (1, 1, 5, section_col_small),
    (2, 5, 9, section_col_small),
    (3, 9, 13, section_col_small),
    (4, 2, 6, section_col_large),
    (5, 6, 10, section_col_large),
    (6, 10, 14, section_col_large),
    (7, 3, 7, section_col_large),
    (8, 7, 11, section_col_large),
    (9, 11, 15, section_col_large),
    (10, 4, 8, section_col_small),
    (11, 8, 12, section_col_small),
    (12, 12, 16, section_col_small),
]

beams_info = [
    (13, 5, 6, section_beam1),
    (14, 6, 7, section_beam1),
    (15, 7, 8, section_beam1),
    (16, 9, 10, section_beam2),
    (17, 10, 11, section_beam2),
    (18, 11, 12, section_beam2),
    (19, 13, 14, section_beam3),
    (20, 14, 15, section_beam3),
    (21, 15, 16, section_beam3),
]

for eid, n1, n2, section in columns_info + beams_info:
    n1 = prt.find_node_by_key(n1 - 1)
    n2 = prt.find_node_by_key(n2 - 1)
    prt.add_element(BeamElement(nodes=[n1, n2], section=section, frame=[0, 0, 1]))

# mdl.show(show_bcs=0.03)

prb = mdl.add_problem(Problem(name="ModalAnalysis"))
stp = prb.add_step(ModalAnalysis(modes=5))

prb.analyse_and_extract(problems=[prb], path=os.path.join(TEMP, prb.name), verbose=True)

prb.show_mode_shape(step=stp, mode=1, scale_results=100)

T1 = 1.0255648890522602
T2 = 0.349763251359163
T3 = 0.1918511027003436
T4 = 0.15622827787433158
T5 = 0.13070968403144037

"""Runs the analysis through the OpenSees solver.

Parameters
----------
path : str, :class:`pathlib.Path`
    Path to the analysis folder. A new folder with the name
    of the problem will be created at this location for all the required
    analysis files.
exe : str, optional
    Location of the OpenSees executable, by default ``C:/OpenSees3.2.0/bin/OpenSees.exe``.
verbose : bool, optional
    Decide wether print or not the output from the solver, by default ``False``.

Returns
-------
None

"""

import os
from compas_fea2.utilities._utils import launch_process

print("\nBegin the analysis...")

file_path = "/Users/francesco/code/fea2/compas_fea2_opensees/scripts/tcl"
file_name = "modal_analysis_beam"
filepath = os.path.join(file_path, file_name + ".tcl")
filepath = (
    "/Users/francesco/code/fea2/compas_fea2_opensees/temp/ModalAnalysis/ElasticFrame/ModalAnalysis/ModalAnalysis.tcl"
)

verbose = True
exe = "/Applications/OpenSees3.7.0/bin/OpenSees"

cmd = 'cd "{}" && "{}" "{}"'.format(file_path, exe, filepath)
for line in launch_process(cmd_args=cmd, cwd=file_path, verbose=verbose):
    line = line.strip().decode()

    if verbose:
        print(line)
print("Analysis completed!")


# File path where the Node displacement data is saved
# results_file = os.path.join(file_path, "Node_Disp.out")
# import matplotlib.pyplot as plt


# # Initialize lists to hold displacement data
# displacement_x = []
# displacement_y = []
# displacement_z = []

# # Read the Node displacement results from the file
# with open(results_file, 'r') as file:
#     for line in file:
#         values = line.split()
#         if len(values) == 3:
#             # Read the x, y, and z displacements
#             x_disp = float(values[0])
#             y_disp = float(values[1])
#             z_disp = float(values[2])
#             displacement_x.append(x_disp)
#             displacement_y.append(y_disp)
#             displacement_z.append(z_disp)

# # Plot the displacements
# plt.figure(figsize=(10, 6))

# plt.plot(range(len(displacement_x)), displacement_x, label='X Displacement', marker='o')
# plt.plot(range(len(displacement_y)), displacement_y, label='Y Displacement', marker='o')
# plt.plot(range(len(displacement_z)), displacement_z, label='Z Displacement', marker='o')

# # Add titles and labels
# plt.title('Node Displacement over Time')
# plt.xlabel('Time Step')
# plt.ylabel('Displacement (meters)')
# plt.legend()
# plt.grid(True)

# # Show the plot
# plt.show()

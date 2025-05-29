import os
import numpy as np


from compas_fea2.problem import Problem
from compas_fea2.utilities._utils import launch_process
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import with_spinner

import compas_fea2_opensees
from compas_fea2.results.database import SQLiteResultsDatabase


class OpenseesProblem(Problem):
    """OpenSees implementation of the :class:`Problem`.\n"""

    __doc__ += Problem.__doc__

    def __init__(self, description=None, **kwargs):
        super(OpenseesProblem, self).__init__(description=description, **kwargs)

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    # @timer(message="Analysis completed in")
    @with_spinner("Analysis in progress")
    def analyse(self, path, exe=None, erase_data=False, verbose=False, *args, **kwargs):
        """Runs the analysis through the OpenSees solver.

        Parameters
        ----------
        path : str or pathlib.Path
            Path to the analysis folder. A new folder with the name
            of the problem will be created at this location for all the required
            analysis files.
        exe : str, optional
            Location of the OpenSees executable, by default ``C:/OpenSees3.2.0/bin/OpenSees.exe``.
        verbose : bool, optional
            Decide whether to print the output from the solver, by default ``False``.

        Returns
        -------
        None
        """
        self._check_analysis_path(path, erase_data=erase_data)
        self.model.assign_keys(start=self.model._key)
        self.write_input_file()
        filepath = os.path.join(self.path, self.name + ".tcl")

        exe = exe or compas_fea2_opensees.EXE
        if not os.path.exists(exe):
            raise ValueError(f"backend not found at {exe}")

        cmd = 'cd "{}" && "{}" "{}"'.format(self.path, exe, filepath)
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=verbose):
            line = line.strip()
            if "error" in line.split(" "):
                raise Exception("ERROR! - Analysis failed to converge!\nSet VERBOSE=True to check the error.")
        print("Analysis completed!")

    def analyse_and_extract(self, path, exe=None, erase_data=False, verbose=False, *args, **kwargs):
        """Runs the analysis through the OpenSees solver and extract the results
        from the native format into a SQLite database. The Model is also saved as
        .cfm file.

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
        self.model.assign_keys(start=self.model._key)
        self.analyse(path=path, exe=exe, erase_data=erase_data, verbose=verbose, *args, **kwargs)
        self.extract_results(database_path=path, database_name=self.name, field_output=None)
        return self.extract_results()

    # =============================================================================
    #                               Job data
    # =============================================================================

    @timer(message="Problem generated in ")
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return "\n".join([step.jobdata() for step in self._steps_order])

    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # ==========================================================================
    # Extract results
    # ==========================================================================
    @timer(message="Data extracted from OpenSees .out files in")
    def extract_results(self, database_path=None, database_name=None, field_output=None):
        """Extract data from the Abaqus .odb file and store into a SQLite database.

        Parameters
        ----------
        fields : list
            Output fields to extract, by default 'None'. If `None` all available
            fields will be extracted, which might require considerable time.

        Returns
        -------
        None

        """
        print("Extracting data from Opensees .out files...")

        rdb = self.rdb
        model = self.model
        for step in self.steps:
            if isinstance(step, compas_fea2_opensees.OpenseesModalAnalysis):
                problem_path = step.problem.path
                model = step.model

                eigenvalues = []
                with open(os.path.join(problem_path, "eigenvalues.out"), "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        eigenvalues.append(line.split())

                eigenvectors = []
                with open(os.path.join(problem_path, "eigenvectors.out"), "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        eigenvectors.append(line.split())

                cursor = rdb.connection.cursor()

                # Create table for eigenvalues
                cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS eigenvalues (
                    id INTEGER PRIMARY KEY,
                    step TEXT,
                    mode INTEGER,
                    lambda REAL,
                    omega REAL,
                    freq REAL,
                    period REAL
                    )
                """
                )

                # Insert eigenvalues into the database
                for eigenvalue in eigenvalues:
                    cursor.execute(
                        """
                    INSERT INTO eigenvalues (step, mode, lambda, omega, freq, period)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        [step.name] + eigenvalue,
                    )
                rdb.connection.commit()

                for i, eigenvector in enumerate(eigenvectors):
                    if len(eigenvector) < 8:
                        eigenvector = eigenvector + [0.0] * (8 - len(eigenvector))
                    node = model.find_node_by_key(int(eigenvector[1]))[0]
                    eigenvectors[i] = [eigenvector[0], step.name, node.part.name, node.key] + eigenvector[2:]

                # Create table for modal shapes
                cursor.execute(
                    f"""
                CREATE TABLE IF NOT EXISTS eigenvectors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mode INTEGER,
                    step TEXT,
                    part TEXT,
                    key INTEGER,
                    {",\n".join([f"{c} REAL" for c in ['x', 'y', 'z', 'xx', 'yy', 'zz']])}
                    )
                """
                )
                # Insert modal shape data into the database
                for eigenvector in eigenvectors:
                    cursor.execute(
                        f"""
                    INSERT INTO eigenvectors (mode, step, part, key, {", ".join([c for c in ['x', 'y', 'z', 'xx', 'yy', 'zz']])})
                    VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?)
                    """,
                        eigenvector,
                    )

                rdb.connection.commit()

                print(f"Modal shapes and eigenvalues successfully saved to {problem_path}")

            else:
                for field_output in step.field_outputs:

                    field_name = field_output.field_name
                    problem_path = field_output.problem.path

                    results = []
                    with open(os.path.join(problem_path, f"{field_name}.out"), "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            columns = line.split()

                            key = int(columns[0])  # Convert the first column to int
                            member = getattr(model, field_output.results_func)(key)[0]

                            values = list(map(lambda x: round(float(x), 6), columns[1:]))
                            if not values:
                                continue

                            # NOTE: OpenSees outputs the stresses at the integration points,
                            # so we need to average them to get the element stresses
                            if field_name == "s2d":
                                num_integration_points = 4
                                num_columns = len(values) // num_integration_points
                                reshaped_data = np.array(values).reshape((num_integration_points, num_columns))
                                averages = np.mean(reshaped_data, axis=0)
                                values = averages.tolist()
                                # NOTE: The OpenSees output is generalised stress,
                                # so we need to convert it to True stress
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

                            if len(values) < len(field_output.components_names):
                                values = values + [0.0] * (len(field_output.components_names) - len(values))
                            elif len(values) > len(field_output.components_names):
                                values = values[: len(field_output.components_names)]
                            else:
                                values = values

                            results.append([member.key] + [step.name, member.part.name] + values)

                    rdb.create_table_for_output_class(field_output, results)

            print("Results extraction completed!")

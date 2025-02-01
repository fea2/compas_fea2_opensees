from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sqlite3

from compas_fea2.problem import Problem
from compas_fea2.utilities._utils import launch_process
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import with_spinner

import compas_fea2_opensees


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
        self.write_input_file()
        filepath = os.path.join(self.path, self.name + ".tcl")

        exe = exe or compas_fea2_opensees.EXE
        if not os.path.exists(exe):
            raise ValueError(f"backend not found at {exe}")

        cmd = 'cd "{}" && "{}" "{}"'.format(self.path, exe, filepath)
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=verbose):
            line = line.strip().decode()
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
        if kwargs.get("save", False):
            self.model.to_cfm(self.model.path.joinpath(f"{self.model.name}.cfm"))
        return self.convert_results_to_sqlite()

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
    def convert_results_to_sqlite(self, database_path=None, database_name=None, field_output=None):
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
        from ..results.results_to_sql import process_modal_shapes
        from ..results.results_to_sql import read_results_file

        # FIXME use the ResultsDatabase class
        connection = sqlite3.connect(self.path_db)

        for step in self.steps:
            if isinstance(step, compas_fea2_opensees.OpenseesModalAnalysis):
                process_modal_shapes(connection, step)
            else:
                for field_output in step.field_outputs:
                    read_results_file(connection, field_output)

        connection.close()
        print("Results extraction completed!")

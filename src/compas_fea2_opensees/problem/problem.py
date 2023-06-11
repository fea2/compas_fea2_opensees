from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from pathlib import Path
from compas_fea2.problem import Problem
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process

from ..job.input_file import OpenseesInputFile


class OpenseesProblem(Problem):
    """OpenSees implementation of the :class:`Problem`.\n
    """
    __doc__ += Problem.__doc__

    def __init__(self, name=None, description=None, **kwargs):
        super(OpenseesProblem, self).__init__(name=name, description=description, **kwargs)
        # FIXME move these to the Steps
        self.tolerance = None
        self.iterations = None
        self.increments = None  # self.increments =1./increments
    # =========================================================================
    #                           Optimisation methods
    # =========================================================================

    # =========================================================================
    #                         Analysis methods
    # =========================================================================

    @timer(message='Analysis completed in')
    def analyse(self, path, exe='C:/OpenSees3.2.0/bin/OpenSees.exe', verbose=False, *args, **kwargs):
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
        print('\nBegin the analysis...')
        self._check_analysis_path(path)
        print(self.path, self.model.path)
        self.write_input_file()
        filepath=os.path.join(self.path, self.name+'.tcl')
        cmd = 'cd {} && {} {}'.format(self.path, exe, filepath)
        for line in launch_process(cmd_args=cmd, cwd=self.path, verbose=verbose):
            print(line)

    def analyse_and_extract(self, path, exe='C:/OpenSees3.2.0/bin/OpenSees.exe', verbose=False, *args, **kwargs):
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
        self.analyse(path=path, exe=exe, verbose=verbose, *args, **kwargs)
        self.model.to_cfm(self.model.path.joinpath(f'{self.model.name}.cfm'))
        return self.convert_results_to_sqlite()
    # =============================================================================
    #                               Job data
    # =============================================================================

    @timer(message='Problem generated in ')
    def jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return '\n'.join([step.jobdata() for step in self._steps_order])
        """recorder Node -file Node3.out -time -node 3 -dof 1 2 disp
recorder Element -file Element1.out -time -ele 1 force

pattern Plain 1 Linear {chr(123)}
    load 2 0.0 -2000.0 0.0 0.0 0.0 0.0
{chr(125)}

constraints Transformation
numberer RCM
system BandGeneral
test NormDispIncr 1.0e-6 6
algorithm Newton
integrator LoadControl 0.1

analysis Static

analyze 10
loadConst -time 0.0
        """

    # ==========================================================================
    # Extract results
    # ==========================================================================
    @timer(message='Data extracted from OpenSees .out files in')
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
        print('\nExtracting data from Opensees .out files...')
        database_path = database_path or self.path
        database_name = database_name or self.name
        from ..results.results_to_sql import read_results_file #, create_database

        for step in self.steps:
            for field_output in step.field_outputs:
                read_results_file(database_path, database_name, field_output)
        # create_database(results)
        # return Path(database_path).joinpath('{}-results.db'.format(database_name))

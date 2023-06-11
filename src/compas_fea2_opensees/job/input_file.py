import os.path
from datetime import datetime
from compas_fea2.job import InputFile
from compas_fea2.job import ParametersFile


class OpenseesInputFile(InputFile):
    """Input file object for standard analysis.

    Parameters
    ----------
    problem : obj
        Problem object.

    Attributes
    ----------
    name : str
        Input file name.
    job_name : str
        Name of the Opensees job. This is the same as the input file name.
    data : str
        Final input file text data that will be written in the .tcl file.
    """

    def __init__(self, name=None, **kwargs):
        super(OpenseesInputFile, self).__init__(name=name, **kwargs)
        self._extension = 'tcl'

    def jobdata(self):
        """Generate the content of the input fileself from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Return
        ------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""# ------------------------
# {self.problem.model.name}
# ------------------------
#
# {self.problem.model.description}
#
# Units: kips, in, sec CHANGE
#
# Author:None CHANGE
# Date: {now}
# Generated by: compas_fea2
#
#------------------------------------------------------------------
#------------------------------------------------------------------
# MODEL
#------------------------------------------------------------------
#------------------------------------------------------------------
#
#{self.problem.model.jobdata()}
#
#
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# PROBLEM
# -----------------------------------------------------------------
# -----------------------------------------------------------------
#
#{self.problem.jobdata()}
"""


class OpenseesParametersFile(ParametersFile):
    """"""

    def __init__(self, name=None, **kwargs):
        super(OpenseesParametersFile, self).__init__(name, **kwargs)
        self._extension = 'par'
        raise NotImplementedError

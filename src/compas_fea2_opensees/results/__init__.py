"""
********************************************************************************
abaqus.results
********************************************************************************

.. currentmodule:: compas_fea2.backends.abaqus.problem

Results
=======
.. autosummary::
    :toctree: generated/

    Results

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .results_to_sql import read_results_file


__all__ = [
    "read_results_file",
]

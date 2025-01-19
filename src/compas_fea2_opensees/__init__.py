"""
********************************************************************************
Opensees
********************************************************************************

reference for OpenSees commands:
https://opensees.github.io/OpenSeesDocumentation/user/userManual.html


.. currentmodule:: compas_fea2_opensees


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os
from dotenv import load_dotenv

from pydoc import ErrorDuringImport
import compas_fea2


# Models
from compas_fea2.model import Model
from compas_fea2.model import DeformablePart
from compas_fea2.model import Node

# Elements
from compas_fea2.model.elements import (
    MassElement,
    LinkElement,
    BeamElement,
    TrussElement,
    MembraneElement,
    ShellElement,
    _Element3D,
    TetrahedronElement,
)

# Sections
from compas_fea2.model.sections import (
    AngleSection,
    BeamSection,
    GenericBeamSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    MassSection,
    PipeSection,
    RectangularSection,
    SpringSection,
    StrutSection,
    TieSection,
    TrapezoidalSection,
    TrussSection,
    MembraneSection,
    ShellSection,
    SolidSection,
)

# Materials
from compas_fea2.model.materials.material import (
    ElasticIsotropic,
    ElasticOrthotropic,
    ElasticPlastic,
    Stiff,
    UserMaterial,
)
from compas_fea2.model.materials.concrete import (
    Concrete,
    ConcreteDamagedPlasticity,
    ConcreteSmearedCrack,
)
from compas_fea2.model.materials.steel import (
    Steel,
)

# Groups
from compas_fea2.model.groups import (
    NodesGroup,
    ElementsGroup,
    FacesGroup,
)

# Constraints
from compas_fea2.model.constraints import (
    TieConstraint,
)

# Connectors
from compas_fea2.model.connectors import (
    RigidLinkConnector,
    SpringConnector,
    ZeroLengthSpringConnector,
    ZeroLengthContactConnector,
)

# Releases
from compas_fea2.model.releases import (
    BeamEndPinRelease,
)

# Boundary Conditions
from compas_fea2.model.bcs import (
    FixedBC,
    FixedBCX,
    FixedBCY,
    FixedBCZ,
    ClampBCXX,
    ClampBCYY,
    ClampBCZZ,
    PinnedBC,
    RollerBCX,
    RollerBCXY,
    RollerBCXZ,
    RollerBCY,
    RollerBCYZ,
    RollerBCZ,
)

# Problem
from compas_fea2.problem import Problem

# Steps
from compas_fea2.problem.steps import (
    ModalAnalysis,
    ComplexEigenValue,
    StaticStep,
    LinearStaticPerturbation,
    BucklingAnalysis,
    DynamicStep,
    QuasiStaticStep,
    DirectCyclicStep,
)

# Loads
from compas_fea2.problem.loads import (
    ConcentratedLoad,
    PressureLoad,
    TributaryLoad,
    PrestressLoad,
    GravityLoad,
    HarmonicPointLoad,
    HarmonicPressureLoad,
)

# Displacements
from compas_fea2.problem.displacements import (
    GeneralDisplacement,
)

# Displacements
from compas_fea2.problem.combinations import (
    LoadCombination,
)

# Outputs
from compas_fea2.problem.outputs import (
    DisplacementFieldOutput,
    AccelerationFieldOutput,
    VelocityFieldOutput,
    ReactionFieldOutput,
    Stress2DFieldOutput,
    SectionForcesFieldOutput,
    HistoryOutput,
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)

# =========================================================================
#                           OPENSEES CLASSES
# =========================================================================

try:
    # Opensees Models
    from .model import OpenseesModel
    from .model import OpenseesPart
    from .model import OpenseesNode

    # Opensees Elements
    from .model.elements import (
        OpenseesMassElement,
        OpenseesLinkElement,
        OpenseesBeamElement,
        OpenseesTrussElement,
        OpenseesMembraneElement,
        OpenseesShellElement,
        _OpenseesElement3D,
        OpenseesTetrahedronElement,
    )

    # Opensees Sections
    from .model.sections import (
        OpenseesAngleSection,
        OpenseesBeamSection,
        OpenseesGenericBeamSection,
        OpenseesBoxSection,
        OpenseesCircularSection,
        OpenseesHexSection,
        OpenseesISection,
        OpenseesMassSection,
        OpenseesPipeSection,
        OpenseesRectangularSection,
        OpenseesSpringSection,
        OpenseesStrutSection,
        OpenseesTieSection,
        OpenseesTrapezoidalSection,
        OpenseesTrussSection,
        OpenseesMembraneSection,
        OpenseesShellSection,
        OpenseesSolidSection,
    )

    # Opensees Materials
    from .model.materials.material import (
        OpenseesElasticIsotropic,
        OpenseesElasticOrthotropic,
        OpenseesElasticPlastic,
        OpenseesStiff,
        OpenseesUserMaterial,
    )
    from .model.materials.concrete import (
        OpenseesConcrete,
        OpenseesConcreteDamagedPlasticity,
        OpenseesConcreteSmearedCrack,
    )
    from .model.materials.steel import (
        OpenseesSteel,
    )

    # Opensees Groups
    from .model.groups import (
        OpenseesNodesGroup,
        OpenseesElementsGroup,
        OpenseesFacesGroup,
    )

    # Opensees Constraints
    from .model.constraints import (
        OpenseesTieConstraint,
    )

    # Opensees Connectors
    from .model.connectors import (
        OpenseesRigidLinkConnector,
        OpenseesSpringConnector,
        OpenseesZeroLengthSpringConnector,
        OpenseesZeroLengthContactConnector,
    )

    # Opensees release
    from .model.releases import (
        OpenseesBeamEndPinRelease,
    )

    # Opensees Boundary Conditions
    from .model.bcs import (
        OpenseesFixedBC,
        OpenseesFixedBCX,
        OpenseesFixedBCY,
        OpenseesFixedBCZ,
        OpenseesClampBCXX,
        OpenseesClampBCYY,
        OpenseesClampBCZZ,
        OpenseesPinnedBC,
        OpenseesRollerBCX,
        OpenseesRollerBCXY,
        OpenseesRollerBCXZ,
        OpenseesRollerBCY,
        OpenseesRollerBCYZ,
        OpenseesRollerBCZ,
    )

    # Opensees Problem
    from .problem import OpenseesProblem

    # Opensees Steps
    from .problem.steps import (
        OpenseesModalAnalysis,
        OpenseesComplexEigenValue,
        OpenseesStaticStep,
        OpenseesLinearStaticPerturbation,
        OpenseesBucklingAnalysis,
        OpenseesDynamicStep,
        OpenseesQuasiStaticStep,
        OpenseesDirectCyclicStep,
    )

    # Opensees Loads
    from .problem.loads import (
        OpenseesConcentratedLoad,
        OpenseesPressureLoad,
        OpenseesTributaryLoad,
        OpenseesPrestressLoad,
        OpenseesGravityLoad,
        OpenseesHarmonicPointLoad,
        OpenseesHarmonicPressureLoad,
    )

    # Opensees Displacements
    from .problem.displacements import (
        OpenseesGeneralDisplacement,
    )

    # Opensees Displacements
    from .problem.combinations import (
        OpenseesLoadCombination,
    )

    # Opensees outputs
    from .problem.outputs import (
        OpenseesDisplacementFieldOutput,
        OpenseesAccelerationFieldOutput,
        OpenseesVelocityFieldOutput,
        OpenseesReactionFieldOutput,
        OpenseesStress2DFieldOutput,
        OpenseesSectionForcesFieldOutput,
        OpenseesHistoryOutput,
    )

    # Opensees Input File
    from .job import (
        OpenseesInputFile,
        OpenseesParametersFile,
    )

    # build the plugin registry
    def _register_backend():
        backend = compas_fea2.BACKENDS["compas_fea2_opensees"]

        backend[Model] = OpenseesModel
        backend[DeformablePart] = OpenseesPart
        backend[Node] = OpenseesNode

        backend[MassElement] = OpenseesMassElement
        backend[LinkElement] = OpenseesLinkElement
        backend[BeamElement] = OpenseesBeamElement
        backend[TrussElement] = OpenseesTrussElement
        backend[MembraneElement] = OpenseesMembraneElement
        backend[ShellElement] = OpenseesShellElement
        backend[_Element3D] = _OpenseesElement3D
        backend[TetrahedronElement] = OpenseesTetrahedronElement

        backend[AngleSection] = OpenseesAngleSection
        backend[BeamSection] = OpenseesBeamSection
        backend[GenericBeamSection] = OpenseesGenericBeamSection
        backend[BoxSection] = OpenseesBoxSection
        backend[CircularSection] = OpenseesCircularSection
        backend[HexSection] = OpenseesHexSection
        backend[ISection] = OpenseesISection
        backend[MassSection] = OpenseesMassSection
        backend[MembraneSection] = OpenseesMembraneSection
        backend[PipeSection] = OpenseesPipeSection
        backend[RectangularSection] = OpenseesRectangularSection
        backend[ShellSection] = OpenseesShellSection
        backend[SolidSection] = OpenseesSolidSection
        backend[SpringSection] = OpenseesSpringSection
        backend[StrutSection] = OpenseesStrutSection
        backend[TieSection] = OpenseesTieSection
        backend[TrapezoidalSection] = OpenseesTrapezoidalSection
        backend[TrussSection] = OpenseesTrussSection

        backend[ElasticIsotropic] = OpenseesElasticIsotropic
        backend[ElasticOrthotropic] = OpenseesElasticOrthotropic
        backend[ElasticPlastic] = OpenseesElasticPlastic
        backend[Stiff] = OpenseesStiff
        backend[UserMaterial] = OpenseesUserMaterial
        backend[Concrete] = OpenseesConcrete
        backend[ConcreteDamagedPlasticity] = OpenseesConcreteDamagedPlasticity
        backend[ConcreteSmearedCrack] = OpenseesConcreteSmearedCrack
        backend[Steel] = OpenseesSteel

        backend[NodesGroup] = OpenseesNodesGroup
        backend[ElementsGroup] = OpenseesElementsGroup
        backend[FacesGroup] = OpenseesFacesGroup

        backend[TieConstraint] = OpenseesTieConstraint

        backend[RigidLinkConnector] = OpenseesRigidLinkConnector
        backend[SpringConnector] = OpenseesSpringConnector
        backend[ZeroLengthSpringConnector] = OpenseesZeroLengthSpringConnector
        backend[ZeroLengthContactConnector] = OpenseesZeroLengthContactConnector

        backend[BeamEndPinRelease] = OpenseesBeamEndPinRelease

        backend[FixedBC] = OpenseesFixedBC
        backend[FixedBCX] = OpenseesFixedBCX
        backend[FixedBCY] = OpenseesFixedBCY
        backend[FixedBCZ] = OpenseesFixedBCZ
        backend[ClampBCXX] = OpenseesClampBCXX
        backend[ClampBCYY] = OpenseesClampBCYY
        backend[ClampBCZZ] = OpenseesClampBCZZ
        backend[PinnedBC] = OpenseesPinnedBC
        backend[RollerBCX] = OpenseesRollerBCX
        backend[RollerBCXY] = OpenseesRollerBCXY
        backend[RollerBCXZ] = OpenseesRollerBCXZ
        backend[RollerBCY] = OpenseesRollerBCY
        backend[RollerBCYZ] = OpenseesRollerBCYZ
        backend[RollerBCZ] = OpenseesRollerBCZ

        backend[Problem] = OpenseesProblem

        backend[ModalAnalysis] = OpenseesModalAnalysis
        backend[ComplexEigenValue, StaticStep] = OpenseesComplexEigenValue
        backend[StaticStep] = OpenseesStaticStep
        backend[LinearStaticPerturbation] = OpenseesLinearStaticPerturbation
        backend[BucklingAnalysis] = OpenseesBucklingAnalysis
        backend[DynamicStep] = OpenseesDynamicStep
        backend[QuasiStaticStep] = OpenseesQuasiStaticStep
        backend[DirectCyclicStep] = OpenseesDirectCyclicStep

        backend[GravityLoad] = OpenseesGravityLoad
        backend[ConcentratedLoad] = OpenseesConcentratedLoad
        backend[PressureLoad] = OpenseesPressureLoad
        backend[TributaryLoad] = OpenseesTributaryLoad
        backend[PrestressLoad] = OpenseesPrestressLoad
        backend[HarmonicPointLoad] = OpenseesHarmonicPointLoad
        backend[HarmonicPressureLoad] = OpenseesHarmonicPressureLoad

        backend[GeneralDisplacement] = OpenseesGeneralDisplacement

        backend[LoadCombination] = OpenseesLoadCombination

        backend[DisplacementFieldOutput] = OpenseesDisplacementFieldOutput
        backend[AccelerationFieldOutput] = OpenseesAccelerationFieldOutput
        backend[VelocityFieldOutput] = OpenseesVelocityFieldOutput
        backend[ReactionFieldOutput] = OpenseesReactionFieldOutput
        backend[Stress2DFieldOutput] = OpenseesStress2DFieldOutput
        backend[SectionForcesFieldOutput] = OpenseesSectionForcesFieldOutput

        backend[HistoryOutput] = OpenseesHistoryOutput

        backend[InputFile] = OpenseesInputFile
        backend[ParametersFile] = OpenseesParametersFile

        print("Opensees implementations registered...")

except ImportError:
    raise ErrorDuringImport()


def init_fea2_opensees(exe):
    """Create a default environment file if it doesn't exist and loads its variables.

    Parameters
    ----------
    verbose : bool, optional
        Be verbose when printing output, by default False
    point_overlap : bool, optional
        Allow two nodes to be at the same location, by default True
    global_tolerance : int, optional
        Tolerance for the model, by default 1
    precision : str, optional
        Values approximation, by default '3f'

    """

    env_path = os.path.abspath(os.path.join(HERE, ".env"))
    with open(env_path, "x") as f:
        f.write(
            "\n".join(
                [
                    "EXE={}".format(exe),
                ]
            )
        )
    load_dotenv(env_path)


__author__ = ["Francesco Ranaudo"]
__copyright__ = "Francesco Ranaudo"
__license__ = "MIT License"
__email__ = "ranaudo@arch.ethz.ch"
__version__ = "0.2.0"

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

if not load_dotenv():
    from sys import platform

    if platform == "linux" or platform == "linux2":
        # linux
        exe = "OpenSees"
    elif platform == "darwin":
        # OS X
        exe = "/Applications/OpenSees3.7.0/bin/OpenSees"
    elif platform == "win32":
        # Windows
        exe = "C:/OpenSees3.7.0/bin/OpenSees.exe"
    else:
        raise ValueError("you must specify the location of the solver.")
    init_fea2_opensees(exe)

EXE = os.getenv("EXE")

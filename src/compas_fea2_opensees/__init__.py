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

import os
from dotenv import load_dotenv

__author__ = ["Francesco Ranaudo"]
__copyright__ = "Francesco Ranaudo"
__license__ = "MIT License"
__email__ = "francesco.ranaudo@gmail.com"
__version__ = "0.1.0"

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

from pydoc import ErrorDuringImport
import compas_fea2


# Models
from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import RigidPart
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
    SpringSection,
    ConnectorSection,
    AngleSection,
    BeamSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    MassSection,
    PipeSection,
    RectangularSection,
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
    TieMPC,
    BeamMPC,
)

# Connectors
from compas_fea2.model.connectors import (
    LinearConnector,
    RigidLinkConnector,
    SpringConnector,
    ZeroLengthSpringConnector,
    ZeroLengthContactConnector,
    # GroundSpringConnector,
)

# Releases
from compas_fea2.model.releases import (
    BeamEndPinRelease,
)

# Boundary Conditions
from compas_fea2.model.bcs import (
    GeneralBC,
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

# Initial Conditions
from compas_fea2.model.ics import (
    InitialTemperatureField,
    InitialStressField,
)

# # Interactions
# from compas_fea2.model.interactions import (
#     HardContactFrictionPenalty,
#     HardContactNoFriction,
#     HardContactRough,
#     LinearContactFrictionPenalty,
# )

# # Interfaces
# from compas_fea2.model.interfaces import Interface

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
    # EdgeLoad,
    # FaceLoad,
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

# Results
from compas_fea2.results import (
    DisplacementFieldResults,
    ReactionFieldResults,
    StressFieldResults,
    SectionForcesFieldResults,
    ContactForcesFieldResults,
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)

# =========================================================================
#                           Opensees CLASSES
# =========================================================================

try:
    # Opensees Models
    from .model import OpenseesModel
    from .model import OpenseesPart
    # from .model import OpenseesRigidPart
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
        OpenseesSpringSection,
        # OpenseesConnectorSection,
        OpenseesAngleSection,
        OpenseesBeamSection,
        OpenseesBoxSection,
        OpenseesCircularSection,
        OpenseesHexSection,
        OpenseesISection,
        OpenseesMassSection,
        OpenseesPipeSection,
        OpenseesRectangularSection,
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
        # OpenseesBeamMPC,
        # OpenseesTieMPC,
    )

    # Opensees Connectors
    from .model.connectors import (
        # OpenseesLinearConnector,
        OpenseesSpringConnector,
        OpenseesZeroLengthSpringConnector,
        OpenseesRigidLinkConnector,
        OpenseesZeroLengthContactConnector,
        # OpenseesGroundSpringConnector,
    )

    # Opensees release
    from .model.releases import (
        OpenseesBeamEndPinRelease,
    )

    # Opensees Boundary Conditions
    from .model.bcs import (
        OpenseesGeneralBC,
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

    # # Initial Conditions
    # from .model.ics import (
    #     OpenseesInitialTemperatureField,
    #     OpenseesInitialStressField,
    # )

    # # Interactions
    # from .model.interactions import (
    #     OpenseesHardContactFrictionPenalty,
    #     OpenseesHardContactRough,
    #     OpenseesLinearContactFrictionPenalty,
    #     OpenseesHardContactNoFriction,
    # )

    # # Opensees Interfaces
    # from .model.interfaces import OpenseesInterface

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

    # Opensees Results
    from .results import (
        OpenseesStressFieldResults,
        OpenseesDisplacementFieldResults,
        OpenseesReactionFieldResults,
        OpenseesContactFieldResults,
        OpenseesSectionForcesFieldResults,
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
        backend[Part] = OpenseesPart
        # backend[RigidPart] = OpenseesRigidPart
        backend[Node] = OpenseesNode

        backend[MassElement] = OpenseesMassElement
        backend[LinkElement] = OpenseesLinkElement
        backend[BeamElement] = OpenseesBeamElement
        backend[TrussElement] = OpenseesTrussElement
        backend[MembraneElement] = OpenseesMembraneElement
        backend[ShellElement] = OpenseesShellElement
        backend[_Element3D] = _OpenseesElement3D
        backend[TetrahedronElement] = OpenseesTetrahedronElement

        backend[SpringSection] = OpenseesSpringSection
        # backend[ConnectorSection] = OpenseesConnectorSection
        backend[AngleSection] = OpenseesAngleSection
        backend[BeamSection] = OpenseesBeamSection
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
        # backend[TieMPC] = OpenseesTieMPC
        # backend[BeamMPC] = OpenseesBeamMPC

        backend[SpringConnector] = OpenseesSpringConnector
        # backend[LinearConnector] = OpenseesLinearConnector
        backend[ZeroLengthSpringConnector] = OpenseesZeroLengthSpringConnector
        backend[RigidLinkConnector] = OpenseesRigidLinkConnector
        backend[ZeroLengthContactConnector] = OpenseesZeroLengthContactConnector
        # backend[GroundSpringConnector] = OpenseesGroundSpringConnector

        backend[BeamEndPinRelease] = OpenseesBeamEndPinRelease

        backend[GeneralBC] = OpenseesGeneralBC
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

        # backend[InitialStressField] = OpenseesInitialStressField
        # backend[InitialTemperatureField] = OpenseesInitialTemperatureField

        # backend[HardContactFrictionPenalty] = OpenseesHardContactFrictionPenalty
        # backend[HardContactRough] = OpenseesHardContactRough
        # backend[LinearContactFrictionPenalty] = OpenseesLinearContactFrictionPenalty
        # backend[HardContactNoFriction] = OpenseesHardContactNoFriction

        # backend[Interface] = OpenseesInterface

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
        backend[TributaryLoad] = OpenseesTributaryLoad
        backend[PrestressLoad] = OpenseesPrestressLoad
        backend[HarmonicPointLoad] = OpenseesHarmonicPointLoad
        backend[HarmonicPressureLoad] = OpenseesHarmonicPressureLoad

        backend[GeneralDisplacement] = OpenseesGeneralDisplacement

        backend[StressFieldResults] = OpenseesStressFieldResults
        backend[DisplacementFieldResults] = OpenseesDisplacementFieldResults
        backend[ReactionFieldResults] = OpenseesReactionFieldResults
        backend[ContactForcesFieldResults] = OpenseesContactFieldResults
        backend[SectionForcesFieldResults] = OpenseesSectionForcesFieldResults

        backend[InputFile] = OpenseesInputFile
        backend[ParametersFile] = OpenseesParametersFile

        print("Opensees implementations registered...")

except:
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


if not load_dotenv():

    from sys import platform

    if platform == "linux" or platform == "linux2":
        # linux
        raise NotImplementedError()
    elif platform == "darwin":
        # OS X
        # raise SystemError("Opensees is not available on Mac")
        exe = '/Applications/OpenSees3.5.0/bin/OpenSees'
    elif platform == "win32":
        # Windows
        raise NotImplementedError()
    else:
        raise ValueError("you must specify the location of the solver.")
    init_fea2_opensees(exe)

EXE = os.getenv("EXE")

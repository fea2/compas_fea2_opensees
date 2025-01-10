********************************************************************************
model
********************************************************************************

.. currentmodule:: compas_fea2_opensees.model

Model
=====

.. autosummary::
    :toctree: generated/

    OpenseesModel

Parts
=====

.. autosummary::
    :toctree: generated/

    OpenseesPart

Nodes
=====

.. autosummary::
    :toctree: generated/

    OpenseesNode


Elements
========

.. autosummary::
    :toctree: generated/

    OpenseesMassElement
    OpenseesLinkElement
    OpenseesBeamElement
    OpenseesTrussElement
    OpenseesMembraneElement
    OpenseesShellElement
    _OpenseesElement3D


Releases
========

.. autosummary::
    :toctree: generated/

    OpenseesBeamEndPinRelease

Constraints
===========

.. autosummary::
    :toctree: generated/

    OpenseesTieConstraint

Connectors
==========

.. autosummary::
    :toctree: generated/

    OpenseesRigidLinkConnector
    OpenseesSpringConnector
    OpenseesZeroLengthSpringConnector
    OpenseesZeroLengthContactConnector


Materials
=========

.. autosummary::
    :toctree: generated/

    OpenseesElasticIsotropic
    OpenseesElasticOrthotropic
    OpenseesElasticPlastic
    OpenseesStiff
    OpenseesUserMaterial
    OpenseesSteel
    OpenseesConcrete
    OpenseesConcreteDamagedPlasticity
    OpenseesConcreteSmearedCrack
 

Sections
========

.. autosummary::
    :toctree: generated/

    OpenseesBeamSection
    OpenseesAngleSection
    OpenseesBoxSection
    OpenseesCircularSection
    OpenseesHexSection
    OpenseesISection
    OpenseesMassSection
    OpenseesPipeSection
    OpenseesRectangularSection
    OpenseesSpringSection
    OpenseesStrutSection
    OpenseesTieSection
    OpenseesTrapezoidalSection
    OpenseesTrussSection
    OpenseesMembraneSection
    OpenseesShellSection
    OpenseesSolidSection


Boundary Conditions
===================

.. autosummary::
    :toctree: generated/

    OpenseesFixedBC
    OpenseesFixedBCX
    OpenseesFixedBCY
    OpenseesFixedBCZ
    OpenseesClampBCXX
    OpenseesClampBCYY
    OpenseesClampBCZZ
    OpenseesPinnedBC
    OpenseesRollerBCX
    OpenseesRollerBCXY
    OpenseesRollerBCXZ
    OpenseesRollerBCY
    OpenseesRollerBCYZ
    OpenseesRollerBCZ

Initial Conditions
==================

.. autosummary::
    :toctree: generated/


Groups
======

.. autosummary::
    :toctree: generated/

    OpenseesNodesGroup
    OpenseesElementsGroup
    OpenseesFacesGroup

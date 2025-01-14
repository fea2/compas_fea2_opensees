from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas_fea2.model import BeamElement
from compas_fea2.model import LinkElement
from compas_fea2.model import MassElement
from compas_fea2.model import MembraneElement
from compas_fea2.model import ShellElement
from compas_fea2.model import TetrahedronElement
from compas_fea2.model import TrussElement
from compas_fea2.model import _Element3D


# ==============================================================================
# 0D elements
# ==============================================================================
class OpenseesMassElement(MassElement):
    """"""

    __doc__ += MassElement.__doc__

    def __init__(self, *, node, section, **kwargs):
        super(OpenseesMassElement, self).__init__(nodes=[node], section=section, **kwargs)
        raise NotImplementedError


class OpenseesLinkElement(LinkElement):
    """Check the documentation \n"""

    __doc__ += LinkElement.__doc__

    def __init__(self, *, nodes, **kwargs):
        super(OpenseesLinkElement, self).__init__(nodes=nodes, **kwargs)

    def jobdata(self):
        return "".join(
            (
                f"element twoNodeLink {self.input_key} {self.nodes[0].key} {self.nodes[-1].key} "
                f"-mat {self.section.material.key} {self.section.material.key} {self.section.material.key} "
                f"-dir 1 2 3 4 5 6"
            )
        )


# ==============================================================================
# 1D elements
# ==============================================================================
class OpenseesBeamElement(BeamElement):
    """OpenSees implementation of :class:`compas_fea2.model.BeamElement`.\n"""

    __doc__ += BeamElement.__doc__

    def __init__(self, nodes, section, implementation="elasticBeamColumn", frame=[0.0, 0.0, -1.0], **kwargs):
        if not implementation:
            implementation = "elasticBeamColumn"
        super(OpenseesBeamElement, self).__init__(nodes=nodes, section=section, frame=frame, implementation=implementation, **kwargs)

        try:
            self._job_data = getattr(self, "_" + implementation)
        except AttributeError:
            raise ValueError("{} is not a valid implementation model".format(implementation))

    def jobdata(self):
        return "\n".join(
            [
                # f"geomTransf Linear {self.input_key}",
                "geomTransf Corotational {} {}".format(self.input_key, " ".join([str(i) for i in self.frame.zaxis])),
                self._job_data(),
            ]
        )

    def _elasticBeamColumn(self):
        """Construct an elasticBeamColumn element object.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/gradientInelasticBeamColumn.html>`_
        """
        if self.part.ndm == 2:
            return "element elasticBeamColumn {} {} {} {} {} {}".format(
                self.input_key,
                " ".join(str(node.input_key) for node in self.nodes),
                self.section.A,
                self.section.material.E,
                self.section.Ixx,
                self.input_key,
            )
        else:
            return "element {} {} {} {} {} {} {} {} {} {}".format(
                self._implementation,
                self.input_key,
                " ".join(str(node.input_key) for node in self.nodes),
                self.section.A,
                self.section.material.E,
                self.section.material.G,
                self.section.J,
                self.section.Ixx,
                self.section.Iyy,
                self.input_key,
            )

    def _inelasticBeamColum(self):
        raise NotImplementedError("Currently under development")
        return (
            "element  {} {} {} $numIntgrPts $endSecTag1 $intSecTag $endSecTag2 $lambda1 $lambda2 $lc $transfTag <-integration integrType> <-iter $maxIter $minTol $maxTol>".format(
                self._implementation, self.input_key, " ".join(node.input_key for node in self.nodes)
            )
        )


class OpenseesTrussElement(TrussElement):
    """A 1D element that resists axial loads."""

    __doc__ += TrussElement.__doc__

    def __init__(self, nodes, section, **kwargs):
        super(OpenseesTrussElement, self).__init__(nodes=nodes, section=section, **kwargs)

    def jobdata(self):
        return f"element Truss {self.input_key} {self.nodes[0].input_key} {self.nodes[1].input_key} {self.section.A} {self.section.material.input_key}"


# ==============================================================================
# 2D elements
# ==============================================================================


class OpenseesShellElement(ShellElement):
    """OpenSees implementation of a :class:`ShellElemnt`."""

    __doc__ += ShellElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    Notes
    -----
    The element's frame is set to have one axis parallel to the segment connecting the first
    and the second node and the third axis peperdicular to the plane of the element.

    """
    # TODO maybe move mat_behavior to the material or section

    def __init__(self, nodes, section, implementation=None, mat_behaviour="PlaneStress", **kwargs):
        self._mat_behaviour = mat_behaviour
        super(OpenseesShellElement, self).__init__(nodes=nodes, section=section, implementation=implementation, **kwargs)
        if not self.implementation:
            if len(nodes) == 3:
                self._implementation = "shelldkgt"  # 'Tri31'
            elif len(nodes) == 4:
                self._implementation = "shellMITC4"
            else:
                raise NotImplementedError("An element with {} nodes is not supported".format(len(nodes)))

    @property
    def mat_behaviour(self):
        return self._mat_behaviour

    def jobdata(self):
        try:
            return getattr(self, "_" + self._implementation.lower())()
        except AttributeError:
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    def _tri31(self):
        """Construct a Tri31 element objec.

        For more information about this element in OpenSees check
        `here <https://opensees.berkeley.edu/wiki/index.php/Tri31_Element>`_

        Note
        ----
        The optional arguments are not implemented.
        """
        return "element tri31 {} {} {} {} {}".format(
            self.input_key,
            " ".join(str(node.input_key) for node in self.nodes),
            self.section.t,
            self._mat_behaviour,
            self.section.material.input_key + 1000,
        )

    def _shelldkgt(self):
        """Construct a ShellDKGT element object, which is a triangular shell
        element based on the theory of generalized conforming element.

        For more information about this element in OpenSees check
        `here <https://opensees.berkeley.edu/wiki/index.php/ShellDKGT>`_

        Note
        ----
        The optional arguments are not implemented.
        """
        self._frame = Frame.from_points(self.nodes[0].xyz, self.nodes[1].xyz, self.nodes[2].xyz)
        self._results_format = ("S11", "S22", "S12", "M11", "M22", "M12")
        return "element ShellDKGT {} {} {}".format(self.input_key, " ".join(str(node.input_key) for node in self.nodes), self.section.input_key)

    def _shelldkgq(self):
        """Construct a ShellDKGQ element object, which is a quadrilateral shell element based on the theory of generalized conforming element.

        For more information about this element in OpenSees check
        `here <https://opensees.berkeley.edu/wiki/index.php/ShellDKGQ>`_

        Note
        ----
        The optional arguments are not implemented.
        """
        self._frame = Frame.from_points(self.nodes[0].xyz, self.nodes[1].xyz, self.nodes[2].xyz)
        self._results_format = ("S11", "S22", "S12", "M11", "M22", "M12")
        return "element ShellDKGQ {} {} {}".format(self.input_key, " ".join(str(node.input_key) for node in self.nodes), self.section.input_key)

    def _shellmitc4(self):
        """Construct a ShellMITC4 element object, which uses a bilinear
        isoparametric formulation in combination with a modified shear
        interpolation to improve thin-plate bending performance.
        """
        self._frame = Frame.from_points(self.nodes[0].xyz, self.nodes[1].xyz, self.nodes[2].xyz)
        self._results_format = ("S11", "S22", "S12", "M11", "M22", "M12")
        return "element ShellMITC4 {} {} {}".format(self.input_key, " ".join(str(node.input_key) for node in self.nodes), self.section.input_key)

    def _asdshellq4(self):
        """Construct an ASDShellQ4 element object.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/ASDShellQ4.html>`_
        """
        self._frame = Frame.from_points(self.nodes[0].xyz, self.nodes[1].xyz, self.nodes[2].xyz)
        self._results_format = ("S11", "S22", "S12", "M11", "M22", "M12")
        return "element ASDShellQ4 {} {}  {}".format(self.input_key, " ".join(str(node.input_key) for node in self.nodes), self.section.input_key)

    def _fournodequad(self):
        """Construct a FourNodeQuad element object which uses a bilinear isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/Quad.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        self._frame = Frame.from_points(self.nodes[0].xyz, self.nodes[1].xyz, self.nodes[2].xyz)
        self._results_format = ("S11", "S22", "S12", "M11", "M22", "M12")
        return "element quad {} {} {} {}".format(
            self.input_key,
            " ".join(str(node.input_key) for node in self.nodes),
            self.section.t,
            self.mat_behaviour,
        )

    def _sspquad(self):
        """Construct a SSPquad (SSP –> Stabilized Single Point) element.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SSPquad.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        self._frame = Frame.from_points(self.nodes[0].xyz, self.nodes[1].xyz, self.nodes[2].xyz)
        self._results_format = ("S11", "S22", "S12", "M11", "M22", "M12")
        return "element SSPquad {} {} {} {}".format(
            self.input_key,
            " ".join(node.input_key for node in self.nodes),
            self.section.material.input_key,
            self.section.material.input_key,
        )


class OpenseesMembraneElement(MembraneElement):
    """"""

    __doc__ += MembraneElement.__doc__

    def __init__(self, nodes, section, **kwargs):
        super(OpenseesMembraneElement, self).__init__(nodes=nodes, section=section, **kwargs)
        raise NotImplementedError


# ==============================================================================
# 3D elements
# ==============================================================================


class _OpenseesElement3D(_Element3D):
    """"""

    __doc__ += _Element3D.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    mat_behaviour : str
        String representing material behavior. It can be either “PlaneStrain” or “PlaneStress.”

    """

    def __init__(self, nodes, section, implementation="stdBrick", **kwargs):
        super(_OpenseesElement3D, self).__init__(nodes=nodes, section=section, implementation=implementation, **kwargs)

    def _get_implementation(self):
        try:
            return getattr(self, "_" + self._type.lower())
        except AttributeError:
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    def jobdata(self):
        return "element {}  {}  {}".format(
            self.input_key,
            self._implementation,
            " ".join(node.input_key for node in self.nodes),
        )

    # TODO complete implementations: for now it is all done in jobdata
    def _stdbrick(self):
        """Construct an eight-node brick element object, which uses the standard isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/stdBrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return

    def _bbarbrick(self):
        """Construct an eight-node mixed volume/pressure brick element object, which uses a trilinear isoparametric formulation.

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/bbarBrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """
        return

    def _sspbrick(self):
        """Construct an eight-node ssp brick element. The SSPbrick element is an
        eight-node hexahedral element using physically stabilized single-point
        integration (SSP –> Stabilized Single Point).

        For more information about this element in OpenSees check
        `here <https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/SSPbrick.html>`_

        Note
        ----
        The optional arguments are not implemented.

        """

        return


# TODO double inheritance from _OpenseesElement3D
class OpenseesTetrahedronElement(TetrahedronElement):
    """Opensees implementation of :class:`TetrahedronElement`

    Note
    ----
    For more information check here:

        - https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/FourNodeTetrahedron.html
        - https://opensees.github.io/OpenSeesDocumentation/user/manual/model/elements/TenNodeTetrahedron.html#tennodetetrahedron

    """

    __doc__ += TetrahedronElement.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    reduced : bool, optional
        Reduce the integration points, by default ``False``.
    hybrid : bool, optional
        Use hybrid formulation, by default ``False``.
    optional : str, optional
        String with additional optional parameters, by default `None`.
    implementation : str, optional
        Name of the implementation model to be used, by default `None`. This can
        be used alternatively to the `type`, `reduced`, `optional` and `warping parameters
        to directly define the model to be used. If both are specified, the
        `implementation` overwrites the others.

    """

    def __init__(self, nodes, section=None, implementation="FourNode", **kwargs):
        super(OpenseesTetrahedronElement, self).__init__(nodes=nodes, section=section, implementation=implementation, **kwargs)
        if len(self._nodes) not in [4]:
            raise ValueError("A solid element with {} nodes cannot be created.".format(len(nodes)))

    def jobdata(self):
        try:
            return getattr(self, "_" + self.implementation)()
        except AttributeError:
            raise ValueError("{} is not a valid implementation.".format(self._implementation))

    def _FourNode(self):
        return f"element FourNodeTetrahedron {self.input_key} {' '.join(str(n.input_key) for n in self.nodes)} {self.section.material.input_key+1000}"

    def _TenNode(self):
        raise NotImplementedError

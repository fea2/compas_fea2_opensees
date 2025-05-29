
from compas_fea2.problem.steps import StaticRiksStep
from compas_fea2.problem.steps import StaticStep


class OpenseesStaticStep(StaticStep):
    """
    Opensees implementation of the :class:`LinearStaticStep`.

    Opensees Parameters
    -------------------
    max_increments : int, optional
        Maximum number of increments (default is 1).
    initial_inc_size : float, optional
        Initial increment size (default is 1).
    min_inc_size : float, optional
        Minimum increment size (default is 0.00001).
    constraint : str, optional
        Constraint handler (default is "Transformation").
        Possible values:
        - "Transformation": Suitable for most problems, handles constraints by transforming the system of equations.
        - "Plain": Simple constraint handler, suitable for small problems.
        - "Lagrange": Uses Lagrange multipliers, suitable for problems with multiple constraints.
        - "Penalty": Uses penalty method, suitable for problems where constraints need to be enforced strictly.
    numberer : str, optional
        Numberer (default is "RCM").
        Possible values:
        - "RCM": Reverse Cuthill-McKee, suitable for reducing bandwidth of the system matrix.
        - "Plain": Simple numberer, suitable for small problems.
    system : str, optional
        System of equations solver (default is "BandGeneral").
        Possible values:
        - "BandGeneral": General band solver, suitable for most problems.
        - "ProfileSPD": Profile solver for symmetric positive definite matrices, suitable for specific problems.
        - "SuperLU": Direct solver using SuperLU, suitable for large sparse systems.
        - "UmfPack": Direct solver using UMFPACK, suitable for large sparse systems.
    test : str, optional
        Convergence test (default is "NormDispIncr 1.0e-6, 10").
        Possible values:
        - "NormDispIncr": Checks norm of displacement increments, suitable for most problems.
        - "NormUnbalance": Checks norm of unbalanced forces, suitable for problems with force convergence criteria.
        - "NormDispAndUnbalance": Checks both displacement increments and unbalanced forces, suitable for strict convergence criteria.
    integrator : str, optional
        Integrator (default is "LoadControl").
        Possible values:
        - "LoadControl": Suitable for load-controlled problems.
        - "DisplacementControl": Suitable for displacement-controlled problems.
        - "ArcLength": Suitable for problems with snap-through or snap-back behavior.
    analysis : str, optional
        Analysis type (default is "Static").
        Possible values:
        - "Static": Suitable for static analysis.
        - "Transient": Suitable for transient analysis.
    time : float, optional
        Total time of the step (default is 1).
    nlgeom : bool, optional
        Nonlinear geometry flag (default is False).
    modify : bool, optional
        Modify flag (default is True).
    algorithm : str, optional
        Solution algorithm (default is "Newton").
        Possible values:
        - "Newton": Standard Newton-Raphson method, suitable for most problems.
        - "ModifiedNewton": Modified Newton-Raphson method, suitable for problems with convergence issues.
        - "BFGS": Broyden-Fletcher-Goldfarb-Shanno method, suitable for large-scale optimization problems.
        - "KrylovNewton": Krylov-Newton method, suitable for large sparse systems.
        - "SecantNewton": Secant-Newton method, suitable for problems with non-smooth behavior.
        - "PeriodicNewton": Periodic Newton-Raphson method, suitable for periodic problems.
    name : str, optional
        Name of the step.
    """

    __doc__ += StaticStep.__doc__

    def __init__(
        self,
        *,
        max_increments=1,
        initial_inc_size=1,
        min_inc_size=0.00001,
        constraint="Transformation",
        numberer="RCM",
        system="BandGeneral",
        test="NormDispIncr 1.0e-6 10",
        integrator="LoadControl",
        analysis="Static",
        time=1,
        nlgeom=False,
        modify=True,
        algorithm="Newton",
        **kwargs,
    ):
        super(OpenseesStaticStep, self).__init__(max_increments=max_increments, 
                                                 initial_inc_size=initial_inc_size, 
                                                 max_inc_size=min_inc_size, 
                                                 time=time, nlgeom=nlgeom, modify=modify, **kwargs)
        self.constraint = constraint
        self.algorithm = algorithm
        self.numberer = numberer
        self.system = system
        self.test = test
        self.integrator = integrator
        self.analysis = analysis

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
# - Displacements
#   -------------
{self._generate_displacements_section()}
#
# - Loads
#   -----
{self._generate_loads_section()}
#
# - Predefined Fields
#   -----------------
{self._generate_fields_section()}
#
#
# - Analysis Parameters
#   -------------------
#
constraints {self.constraint}
numberer {self.numberer}
system {self.system}
test {self.test}
algorithm {self.algorithm}
integrator {self.integrator} {self.time}
analysis {self.analysis}

# create a dummy Recorder for the reactions (Limitation of OpenSees)
recorder Node -file dummy.out -node 0 -dof 1 reaction
recorder Element -xml stress.xml -eleRange 1 1 stresses
recorder Element -xml strain.xml -eleRange 1 1 strains
recorder Element -xml deformation.xml -eleRange 1 1 deformations


analyze {self.max_increments}
loadConst -time 0.0
#
# - Output Results
#   --------------
{self._generate_output_section()}
#
"""

    def _generate_header_section(self):
        return f"""#
# STEP {self.name}
#
timeSeries Constant {self.problem._steps_order.index(self)} -factor 1.0
#"""

    def _generate_displacements_section(self):
        return "#"
        return "\n".join([pattern.load.jobdata(pattern.distribution) for pattern in self.displacements]) or "#"

    def _generate_loads_section(self):
        
        factor = 1
        index = 0
        loads = "\n".join([load.jobdata(node) for node, load in self.combination.node_load])

        return f"pattern Plain {index} {index} -fact {factor} {{\n{loads}\n}}" if loads else "#"
        
        # data = []
        # for node, load in self.combination.node_load:
        #     data.append(load.jobdata(node))
        # return "\n".join(data) or "#"

    def _generate_fields_section(self):
        return "#"

    def _generate_output_section(self):
        data_section = ["#"]
        if self._field_outputs:
            for foutput in self._field_outputs:
                data_section.append(foutput.jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs:
                data_section.append(houtput.jobdata())
        return "\n".join(data_section)


class OpenseesStaticRiksStep(StaticRiksStep):
    """
    Opensees implementation of the :class:`StaticRiksStep`.

    Parameters
    ----------
    max_increments : int, optional
        Maximum number of increments (default is 100).
    initial_inc_size : float, optional
        Initial increment size (default is 1).
    min_inc_size : float, optional
        Minimum increment size (default is 0.00001).
    ArcLength : list, optional
        Arc length control parameters [s, dU, JdU] (default is [1.0e-2, 1.0e-4, 10]).
        - s: Arc length step size, suitable for controlling the step size in arc length method.
        - dU: Displacement increment, suitable for controlling the displacement increment in arc length method.
        - JdU: Number of iterations, suitable for controlling the number of iterations in arc length method.
    time : float, optional
        Total time of the step (default is 1).
    nlgeom : bool, optional
        Nonlinear geometry flag (default is False).
    modify : bool, optional
        Modify flag (default is True).
    name : str, optional
        Name of the step.
    """

    def __init__(
        self,
        max_increments=100,
        initial_inc_size=1,
        min_inc_size=0.00001,
        ArcLength=[1.0e-2, 1.0e-4, 10],
        time=1,
        nlgeom=False,
        modify=True,
        name=None,
        **kwargs,
    ):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        self.ArcLength = ArcLength

    def jobdata(self):
        return f"""#
{self._generate_header_section()}
# - Displacements
#   -------------
{self._generate_displacements_section()}
#
# - Loads
#   -----
{self._generate_loads_section()}
#
# - Predefined Fields
#   -----------------
{self._generate_fields_section()}
#
# - Output Requests
#   ---------------
{self._generate_output_section()}
#
# - Analysis Parameters
#   -------------------
#
constraints Transformation
numberer RCM
system BandGeneral
test NormDispIncr {self.ArcLength[0]} {self.ArcLength[1]} {self.ArcLength[2]}
algorithm Newton
integrator ArcLength {self.ArcLength[0]}

analysis Static

analyze {self.max_increments}
loadConst -time 0.0
"""

    def _generate_header_section(self):
        return """#
# STEP {0}
#
#
# timeSeries Constant {1} -factor 1.0
#""".format(
            self.name, self.problem._steps_order.index(self)
        )

    def _generate_displacements_section(self):
        return "\n".join([pattern.load.jobdata(pattern.distribution) for pattern in self.displacements]) or "#"

    def _generate_loads_section(self):
        return self.combination.jobdata()

    def _generate_fields_section(self):
        return "#"

    def _generate_output_section(self):
        data_section = ["#"]
        if self._field_outputs:
            for foutput in self._field_outputs:
                data_section.append(foutput.jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs:
                data_section.append(houtput.jobdata())
        return "\n".join(data_section)

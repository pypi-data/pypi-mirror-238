"""Long double precision"""
from __future__ import annotations
import _alpaqa_d.longdouble
import typing
import _alpaqa_d

__all__ = [
    "ALMParams",
    "ALMSolver",
    "AndersonAccel",
    "AndersonDirection",
    "Box",
    "BoxConstrProblem",
    "ControlProblem",
    "ControlProblemWithCounters",
    "InnerOCPSolver",
    "InnerSolveOptions",
    "InnerSolver",
    "LBFGS",
    "LBFGSDirection",
    "LipschitzEstimateParams",
    "NewtonTRDirection",
    "NewtonTRDirectionParams",
    "NoopDirection",
    "OCPEvaluator",
    "PANOCDirection",
    "PANOCOCPParams",
    "PANOCOCPProgressInfo",
    "PANOCOCPSolver",
    "PANOCParams",
    "PANOCProgressInfo",
    "PANOCSolver",
    "PANTRDirection",
    "PANTRParams",
    "PANTRProgressInfo",
    "PANTRSolver",
    "Problem",
    "ProblemWithCounters",
    "SteihaugCGParams",
    "StructuredLBFGSDirection",
    "StructuredNewtonDirection",
    "UnconstrProblem",
    "ZeroFPRParams",
    "ZeroFPRProgressInfo",
    "ZeroFPRSolver",
    "functions",
    "problem_with_counters",
    "provided_functions",
    "prox",
    "prox_step"
]


class ALMParams():
    """
    C++ documentation: :cpp:class:`alpaqa::ALMParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def dual_tolerance(self) -> object:
        """
        :type: object
        """
    @dual_tolerance.setter
    def dual_tolerance(self, arg1: handle) -> None:
        pass
    @property
    def initial_penalty(self) -> object:
        """
        :type: object
        """
    @initial_penalty.setter
    def initial_penalty(self, arg1: handle) -> None:
        pass
    @property
    def initial_penalty_factor(self) -> object:
        """
        :type: object
        """
    @initial_penalty_factor.setter
    def initial_penalty_factor(self, arg1: handle) -> None:
        pass
    @property
    def initial_tolerance(self) -> object:
        """
        :type: object
        """
    @initial_tolerance.setter
    def initial_tolerance(self, arg1: handle) -> None:
        pass
    @property
    def max_iter(self) -> object:
        """
        :type: object
        """
    @max_iter.setter
    def max_iter(self, arg1: handle) -> None:
        pass
    @property
    def max_multiplier(self) -> object:
        """
        :type: object
        """
    @max_multiplier.setter
    def max_multiplier(self, arg1: handle) -> None:
        pass
    @property
    def max_penalty(self) -> object:
        """
        :type: object
        """
    @max_penalty.setter
    def max_penalty(self, arg1: handle) -> None:
        pass
    @property
    def max_time(self) -> object:
        """
        :type: object
        """
    @max_time.setter
    def max_time(self, arg1: handle) -> None:
        pass
    @property
    def min_penalty(self) -> object:
        """
        :type: object
        """
    @min_penalty.setter
    def min_penalty(self, arg1: handle) -> None:
        pass
    @property
    def penalty_update_factor(self) -> object:
        """
        :type: object
        """
    @penalty_update_factor.setter
    def penalty_update_factor(self, arg1: handle) -> None:
        pass
    @property
    def print_interval(self) -> object:
        """
        :type: object
        """
    @print_interval.setter
    def print_interval(self, arg1: handle) -> None:
        pass
    @property
    def print_precision(self) -> object:
        """
        :type: object
        """
    @print_precision.setter
    def print_precision(self, arg1: handle) -> None:
        pass
    @property
    def rel_penalty_increase_threshold(self) -> object:
        """
        :type: object
        """
    @rel_penalty_increase_threshold.setter
    def rel_penalty_increase_threshold(self, arg1: handle) -> None:
        pass
    @property
    def single_penalty_factor(self) -> object:
        """
        :type: object
        """
    @single_penalty_factor.setter
    def single_penalty_factor(self, arg1: handle) -> None:
        pass
    @property
    def tolerance(self) -> object:
        """
        :type: object
        """
    @tolerance.setter
    def tolerance(self, arg1: handle) -> None:
        pass
    @property
    def tolerance_update_factor(self) -> object:
        """
        :type: object
        """
    @tolerance_update_factor.setter
    def tolerance_update_factor(self, arg1: handle) -> None:
        pass
    pass
class ALMSolver():
    """
    Main augmented Lagrangian solver.

    C++ documentation: :cpp:class:`alpaqa::ALMSolver`
    """
    def __call__(self, problem: typing.Union[Problem, ControlProblem], x: typing.Optional[numpy.ndarray] = None, y: typing.Optional[numpy.ndarray] = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple: 
        """
        Solve.

        :param problem: Problem to solve.
        :param x: Initial guess for decision variables :math:`x`

        :param y: Initial guess for Lagrange multipliers :math:`y`
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa._alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`x`
                 * Lagrange multipliers :math:`y` at the solution
                 * Statistics
        """
    def __copy__(self) -> ALMSolver: ...
    def __deepcopy__(self, memo: dict) -> ALMSolver: ...
    @typing.overload
    def __init__(self, other: ALMSolver) -> None: 
        """
        Create a copy

        Build an ALM solver using Structured PANOC as inner solver.

        Build an ALM solver using the given inner solver.

        Build an ALM solver using the given inner solver.

        Build an ALM solver using the given inner solver.

        Build an ALM solver using the given inner solver.
        """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, inner_solver: InnerSolver) -> None: ...
    @typing.overload
    def __init__(self, inner_solver: InnerOCPSolver) -> None: ...
    @typing.overload
    def __init__(self, alm_params: typing.Union[ALMParams, dict], inner_solver: InnerSolver) -> None: ...
    @typing.overload
    def __init__(self, alm_params: typing.Union[ALMParams, dict], inner_solver: InnerOCPSolver) -> None: ...
    def __str__(self) -> str: ...
    def stop(self) -> None: ...
    @property
    def inner_solver(self) -> object:
        """
        :type: object
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def params(self) -> object:
        """
        :type: object
        """
    pass
class AndersonAccel():
    """
    C++ documentation :cpp:class:`alpaqa::AndersonAccel`
    """
    class Params():
        """
        C++ documentation :cpp:class:`alpaqa::AndersonAccelParams`
        """
        @typing.overload
        def __init__(self, params: dict) -> None: ...
        @typing.overload
        def __init__(self, **kwargs) -> None: ...
        def to_dict(self) -> dict: ...
        @property
        def memory(self) -> object:
            """
            :type: object
            """
        @memory.setter
        def memory(self, arg1: handle) -> None:
            pass
        @property
        def min_div_fac(self) -> object:
            """
            :type: object
            """
        @min_div_fac.setter
        def min_div_fac(self, arg1: handle) -> None:
            pass
        pass
    @typing.overload
    def __init__(self, params: typing.Union[AndersonAccel.Params, dict]) -> None: ...
    @typing.overload
    def __init__(self, params: typing.Union[AndersonAccel.Params, dict], n: int) -> None: ...
    def __str__(self) -> str: ...
    @typing.overload
    def compute(self, g_k: numpy.ndarray, r_k: numpy.ndarray, x_k_aa: numpy.ndarray) -> None: ...
    @typing.overload
    def compute(self, g_k: numpy.ndarray, r_k: numpy.ndarray) -> numpy.ndarray: ...
    def initialize(self, g_0: numpy.ndarray, r_0: numpy.ndarray) -> None: ...
    def reset(self) -> None: ...
    def resize(self, n: int) -> None: ...
    @property
    def Q(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def R(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def current_history(self) -> int:
        """
        :type: int
        """
    @property
    def history(self) -> int:
        """
        :type: int
        """
    @property
    def n(self) -> int:
        """
        :type: int
        """
    @property
    def params(self) -> AndersonAccel.Params:
        """
        :type: AndersonAccel.Params
        """
    pass
class AndersonDirection():
    """
    C++ documentation: :cpp:class:`alpaqa::AndersonDirection`
    """
    class DirectionParams():
        """
        C++ documentation: :cpp:class:`alpaqa::AndersonDirection::DirectionParams`
        """
        @typing.overload
        def __init__(self, params: dict) -> None: ...
        @typing.overload
        def __init__(self, **kwargs) -> None: ...
        def to_dict(self) -> dict: ...
        @property
        def rescale_on_step_size_changes(self) -> object:
            """
            :type: object
            """
        @rescale_on_step_size_changes.setter
        def rescale_on_step_size_changes(self, arg1: handle) -> None:
            pass
        pass
    def __init__(self, anderson_params: typing.Union[AndersonAccel.Params, dict] = {}, direction_params: typing.Union[AndersonDirection.DirectionParams, dict] = {}) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> typing.Tuple[AndersonAccel.Params, AndersonDirection.DirectionParams]:
        """
        :type: typing.Tuple[AndersonAccel.Params, AndersonDirection.DirectionParams]
        """
    pass
class Box():
    """
    C++ documentation: :cpp:class:`alpaqa::Box`
    """
    def __copy__(self) -> Box: ...
    def __deepcopy__(self, memo: dict) -> Box: ...
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self, other: Box) -> None: 
        """
        Create a copy

        Create an :math:`n`-dimensional box at with bounds at :math:`\pm\infty` (no constraints).

        Create a box with the given bounds.
        """
    @typing.overload
    def __init__(self, n: int) -> None: ...
    @typing.overload
    def __init__(self, *, lower: numpy.ndarray, upper: numpy.ndarray) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @property
    def lowerbound(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @lowerbound.setter
    def lowerbound(self, arg1: numpy.ndarray) -> None:
        pass
    @property
    def upperbound(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @upperbound.setter
    def upperbound(self, arg1: numpy.ndarray) -> None:
        pass
    pass
class BoxConstrProblem():
    """
    C++ documentation: :cpp:class:`alpaqa::BoxConstrProblem`
    """
    def __copy__(self) -> BoxConstrProblem: ...
    def __deepcopy__(self, memo: dict) -> BoxConstrProblem: ...
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self, other: BoxConstrProblem) -> None: 
        """
        Create a copy

        :param n: Number of unknowns
        :param m: Number of constraints
        """
    @typing.overload
    def __init__(self, n: int, m: int) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray, J: numpy.ndarray) -> int: ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray) -> numpy.ndarray: ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray, e: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray) -> numpy.ndarray: ...
    def eval_proj_multipliers(self, y: numpy.ndarray, M: float) -> None: ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray, x_hat: numpy.ndarray, p: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray) -> typing.Tuple[numpy.ndarray, numpy.ndarray, float]: ...
    def get_box_C(self) -> Box: ...
    def get_box_D(self) -> Box: ...
    def resize(self, n: int, m: int) -> None: ...
    @property
    def C(self) -> Box:
        """
        Box constraints on :math:`x`

        :type: Box
        """
    @C.setter
    def C(self, arg0: Box) -> None:
        """
        Box constraints on :math:`x`
        """
    @property
    def D(self) -> Box:
        """
        Box constraints on :math:`g(x)`

        :type: Box
        """
    @D.setter
    def D(self, arg0: Box) -> None:
        """
        Box constraints on :math:`g(x)`
        """
    @property
    def l1_reg(self) -> numpy.ndarray:
        """
        :math:`\ell_1` regularization on :math:`x`

        :type: numpy.ndarray
        """
    @l1_reg.setter
    def l1_reg(self, arg0: numpy.ndarray) -> None:
        """
        :math:`\ell_1` regularization on :math:`x`
        """
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`

        :type: int
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`

        :type: int
        """
    @property
    def penalty_alm_split(self) -> int:
        """
        Index between quadratic penalty and augmented Lagrangian constraints

        :type: int
        """
    @penalty_alm_split.setter
    def penalty_alm_split(self, arg0: int) -> None:
        """
        Index between quadratic penalty and augmented Lagrangian constraints
        """
    pass
class ControlProblem():
    """
    C++ documentation: :cpp:class:`alpaqa::TypeErasedControlProblem`
    """
    def __copy__(self) -> ControlProblem: ...
    def __deepcopy__(self, memo: dict) -> ControlProblem: ...
    def __init__(self, other: ControlProblem) -> None: 
        """
        Create a copy
        """
    pass
class ControlProblemWithCounters():
    @property
    def evaluations(self) -> _alpaqa_d.OCPEvalCounter:
        """
        :type: _alpaqa_d.OCPEvalCounter
        """
    @property
    def problem(self) -> ControlProblem:
        """
        :type: ControlProblem
        """
    pass
class InnerOCPSolver():
    def __copy__(self) -> InnerOCPSolver: ...
    def __deepcopy__(self, memo: dict) -> InnerOCPSolver: ...
    @typing.overload
    def __init__(self, other: InnerOCPSolver) -> None: 
        """
        Create a copy

        Explicit conversion.
        """
    @typing.overload
    def __init__(self, inner_solver: PANOCOCPSolver) -> None: ...
    def __str__(self) -> str: ...
    def stop(self) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
class InnerSolveOptions():
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def always_overwrite_results(self) -> object:
        """
        :type: object
        """
    @always_overwrite_results.setter
    def always_overwrite_results(self, arg1: handle) -> None:
        pass
    @property
    def max_time(self) -> object:
        """
        :type: object
        """
    @max_time.setter
    def max_time(self, arg1: handle) -> None:
        pass
    @property
    def tolerance(self) -> object:
        """
        :type: object
        """
    @tolerance.setter
    def tolerance(self, arg1: handle) -> None:
        pass
    pass
class InnerSolver():
    def __copy__(self) -> InnerSolver: ...
    def __deepcopy__(self, memo: dict) -> InnerSolver: ...
    @typing.overload
    def __init__(self, other: InnerSolver) -> None: 
        """
        Create a copy

        Explicit conversion.

        Explicit conversion.

        Explicit conversion.
        """
    @typing.overload
    def __init__(self, inner_solver: PANOCSolver) -> None: ...
    @typing.overload
    def __init__(self, inner_solver: ZeroFPRSolver) -> None: ...
    @typing.overload
    def __init__(self, inner_solver: PANTRSolver) -> None: ...
    def __str__(self) -> str: ...
    def stop(self) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
class LBFGS():
    """
    C++ documentation :cpp:class:`alpaqa::LBFGS`
    """
    class Params():
        """
        C++ documentation :cpp:class:`alpaqa::LBFGSParams`
        """
        class CBFGS():
            """
            C++ documentation :cpp:class:`alpaqa::CBFGSParams`
            """
            @typing.overload
            def __init__(self, params: dict) -> None: ...
            @typing.overload
            def __init__(self, **kwargs) -> None: ...
            def to_dict(self) -> dict: ...
            @property
            def α(self) -> object:
                """
                :type: object
                """
            @α.setter
            def α(self, arg1: handle) -> None:
                pass
            @property
            def ϵ(self) -> object:
                """
                :type: object
                """
            @ϵ.setter
            def ϵ(self, arg1: handle) -> None:
                pass
            pass
        @typing.overload
        def __init__(self, params: dict) -> None: ...
        @typing.overload
        def __init__(self, **kwargs) -> None: ...
        def to_dict(self) -> dict: ...
        @property
        def cbfgs(self) -> object:
            """
            :type: object
            """
        @cbfgs.setter
        def cbfgs(self, arg1: handle) -> None:
            pass
        @property
        def force_pos_def(self) -> object:
            """
            :type: object
            """
        @force_pos_def.setter
        def force_pos_def(self, arg1: handle) -> None:
            pass
        @property
        def memory(self) -> object:
            """
            :type: object
            """
        @memory.setter
        def memory(self, arg1: handle) -> None:
            pass
        @property
        def min_abs_s(self) -> object:
            """
            :type: object
            """
        @min_abs_s.setter
        def min_abs_s(self, arg1: handle) -> None:
            pass
        @property
        def min_div_fac(self) -> object:
            """
            :type: object
            """
        @min_div_fac.setter
        def min_div_fac(self, arg1: handle) -> None:
            pass
        @property
        def stepsize(self) -> object:
            """
            :type: object
            """
        @stepsize.setter
        def stepsize(self, arg1: handle) -> None:
            pass
        pass
    class Sign():
        """
        C++ documentation :cpp:enum:`alpaqa::LBFGS::Sign`

        Members:

          Positive

          Negative
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: object) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        @property
        def name(self) -> str:
            """
            :type: str
            """
        @property
        def value(self) -> int:
            """
            :type: int
            """
        Negative: _alpaqa_d.longdouble.LBFGS.Sign # value = <Sign.Negative: 1>
        Positive: _alpaqa_d.longdouble.LBFGS.Sign # value = <Sign.Positive: 0>
        __members__: dict # value = {'Positive': <Sign.Positive: 0>, 'Negative': <Sign.Negative: 1>}
        pass
    @typing.overload
    def __init__(self, params: typing.Union[LBFGS.Params, dict]) -> None: ...
    @typing.overload
    def __init__(self, params: typing.Union[LBFGS.Params, dict], n: int) -> None: ...
    def __str__(self) -> str: ...
    def apply(self, q: numpy.ndarray, γ: float) -> bool: ...
    def apply_masked(self, q: numpy.ndarray, γ: float, J: typing.List[int]) -> bool: ...
    def current_history(self) -> int: ...
    def reset(self) -> None: ...
    def resize(self, n: int) -> None: ...
    def s(self, i: int) -> numpy.ndarray: ...
    def scale_y(self, factor: float) -> None: ...
    def update(self, xk: numpy.ndarray, xkp1: numpy.ndarray, pk: numpy.ndarray, pkp1: numpy.ndarray, sign: LBFGS.Sign = Sign.Positive, forced: bool = False) -> bool: ...
    def update_sy(self, sk: numpy.ndarray, yk: numpy.ndarray, pkp1Tpkp1: float, forced: bool = False) -> bool: ...
    @staticmethod
    def update_valid(params: LBFGS.Params, yᵀs: float, sᵀs: float, pᵀp: float) -> bool: ...
    def y(self, i: int) -> numpy.ndarray: ...
    def α(self, i: int) -> float: ...
    def ρ(self, i: int) -> float: ...
    @property
    def n(self) -> int:
        """
        :type: int
        """
    @property
    def params(self) -> LBFGS.Params:
        """
        :type: LBFGS.Params
        """
    Negative: _alpaqa_d.longdouble.LBFGS.Sign # value = <Sign.Negative: 1>
    Positive: _alpaqa_d.longdouble.LBFGS.Sign # value = <Sign.Positive: 0>
    pass
class LBFGSDirection():
    """
    C++ documentation: :cpp:class:`alpaqa::LBFGSDirection`
    """
    class DirectionParams():
        """
        C++ documentation: :cpp:class:`alpaqa::LBFGSDirection::DirectionParams`
        """
        @typing.overload
        def __init__(self, params: dict) -> None: ...
        @typing.overload
        def __init__(self, **kwargs) -> None: ...
        def to_dict(self) -> dict: ...
        @property
        def rescale_on_step_size_changes(self) -> object:
            """
            :type: object
            """
        @rescale_on_step_size_changes.setter
        def rescale_on_step_size_changes(self, arg1: handle) -> None:
            pass
        pass
    def __init__(self, lbfgs_params: typing.Union[LBFGS.Params, dict] = {}, direction_params: typing.Union[LBFGSDirection.DirectionParams, dict] = {}) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> typing.Tuple[LBFGS.Params, LBFGSDirection.DirectionParams]:
        """
        :type: typing.Tuple[LBFGS.Params, LBFGSDirection.DirectionParams]
        """
    pass
class LipschitzEstimateParams():
    """
    C++ documentation: :cpp:class:`alpaqa::LipschitzEstimateParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def L_0(self) -> object:
        """
        :type: object
        """
    @L_0.setter
    def L_0(self, arg1: handle) -> None:
        pass
    @property
    def Lγ_factor(self) -> object:
        """
        :type: object
        """
    @Lγ_factor.setter
    def Lγ_factor(self, arg1: handle) -> None:
        pass
    @property
    def δ(self) -> object:
        """
        :type: object
        """
    @δ.setter
    def δ(self, arg1: handle) -> None:
        pass
    @property
    def ε(self) -> object:
        """
        :type: object
        """
    @ε.setter
    def ε(self, arg1: handle) -> None:
        pass
    pass
class NewtonTRDirection():
    """
    C++ documentation: :cpp:class:`alpaqa::NewtonTRDirection`
    """
    def __init__(self, accelerator_params: typing.Union[SteihaugCGParams, dict] = {}, direction_params: typing.Union[NewtonTRDirectionParams, dict] = {}) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> typing.Tuple[SteihaugCGParams, NewtonTRDirectionParams]:
        """
        :type: typing.Tuple[SteihaugCGParams, NewtonTRDirectionParams]
        """
    pass
class NewtonTRDirectionParams():
    """
    C++ documentation: :cpp:class:`alpaqa::NewtonTRDirectionParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def finite_diff(self) -> object:
        """
        :type: object
        """
    @finite_diff.setter
    def finite_diff(self, arg1: handle) -> None:
        pass
    @property
    def finite_diff_stepsize(self) -> object:
        """
        :type: object
        """
    @finite_diff_stepsize.setter
    def finite_diff_stepsize(self, arg1: handle) -> None:
        pass
    @property
    def hessian_vec_factor(self) -> object:
        """
        :type: object
        """
    @hessian_vec_factor.setter
    def hessian_vec_factor(self, arg1: handle) -> None:
        pass
    pass
class NoopDirection():
    """
    C++ documentation: :cpp:class:`alpaqa::NoopDirection`
    """
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    AcceleratorParams = None
    DirectionParams = None
    params = None
    pass
class OCPEvaluator():
    def Qk(self, k: int, u: numpy.ndarray, y: typing.Optional[numpy.ndarray] = None, μ: typing.Optional[numpy.ndarray] = None) -> numpy.ndarray: ...
    def Rk(self, k: int, u: numpy.ndarray, mask: numpy.ndarray) -> numpy.ndarray: ...
    def Sk(self, k: int, u: numpy.ndarray, mask: numpy.ndarray) -> numpy.ndarray: ...
    def __init__(self, problem: ControlProblem) -> None: ...
    def forward_backward(self, u: numpy.ndarray, y: typing.Optional[numpy.ndarray] = None, μ: typing.Optional[numpy.ndarray] = None) -> typing.Tuple[float, numpy.ndarray]: 
        """
        :return: * Cost
                 * Gradient
        """
    def lqr_factor_solve(self, u: numpy.ndarray, γ: float, y: typing.Optional[numpy.ndarray] = None, μ: typing.Optional[numpy.ndarray] = None) -> numpy.ndarray: ...
    def lqr_factor_solve_QRS(self, u: numpy.ndarray, γ: float, Q: list, R: list, S: list, y: typing.Optional[numpy.ndarray] = None, μ: typing.Optional[numpy.ndarray] = None, masked: bool = True) -> numpy.ndarray: ...
    pass
class PANOCDirection():
    @typing.overload
    def __init__(self, direction: NoopDirection) -> None: 
        """
        Explicit conversion.

        Explicit conversion.

        Explicit conversion.

        Explicit conversion.

        Explicit conversion.

        Explicit conversion from a custom Python class.
        """
    @typing.overload
    def __init__(self, direction: LBFGSDirection) -> None: ...
    @typing.overload
    def __init__(self, direction: StructuredLBFGSDirection) -> None: ...
    @typing.overload
    def __init__(self, direction: StructuredNewtonDirection) -> None: ...
    @typing.overload
    def __init__(self, direction: AndersonDirection) -> None: ...
    @typing.overload
    def __init__(self, direction: object) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> object:
        """
        :type: object
        """
    pass
class PANOCOCPParams():
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCOCPParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def L_max(self) -> object:
        """
        :type: object
        """
    @L_max.setter
    def L_max(self, arg1: handle) -> None:
        pass
    @property
    def L_max_inc(self) -> object:
        """
        :type: object
        """
    @L_max_inc.setter
    def L_max_inc(self, arg1: handle) -> None:
        pass
    @property
    def L_min(self) -> object:
        """
        :type: object
        """
    @L_min.setter
    def L_min(self, arg1: handle) -> None:
        pass
    @property
    def Lipschitz(self) -> object:
        """
        :type: object
        """
    @Lipschitz.setter
    def Lipschitz(self, arg1: handle) -> None:
        pass
    @property
    def disable_acceleration(self) -> object:
        """
        :type: object
        """
    @disable_acceleration.setter
    def disable_acceleration(self, arg1: handle) -> None:
        pass
    @property
    def gn_interval(self) -> object:
        """
        :type: object
        """
    @gn_interval.setter
    def gn_interval(self, arg1: handle) -> None:
        pass
    @property
    def gn_sticky(self) -> object:
        """
        :type: object
        """
    @gn_sticky.setter
    def gn_sticky(self, arg1: handle) -> None:
        pass
    @property
    def lbfgs_params(self) -> object:
        """
        :type: object
        """
    @lbfgs_params.setter
    def lbfgs_params(self, arg1: handle) -> None:
        pass
    @property
    def linesearch_strictness_factor(self) -> object:
        """
        :type: object
        """
    @linesearch_strictness_factor.setter
    def linesearch_strictness_factor(self, arg1: handle) -> None:
        pass
    @property
    def linesearch_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @linesearch_tolerance_factor.setter
    def linesearch_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def lqr_factor_cholesky(self) -> object:
        """
        :type: object
        """
    @lqr_factor_cholesky.setter
    def lqr_factor_cholesky(self, arg1: handle) -> None:
        pass
    @property
    def max_iter(self) -> object:
        """
        :type: object
        """
    @max_iter.setter
    def max_iter(self, arg1: handle) -> None:
        pass
    @property
    def max_no_progress(self) -> object:
        """
        :type: object
        """
    @max_no_progress.setter
    def max_no_progress(self, arg1: handle) -> None:
        pass
    @property
    def max_time(self) -> object:
        """
        :type: object
        """
    @max_time.setter
    def max_time(self, arg1: handle) -> None:
        pass
    @property
    def min_linesearch_coefficient(self) -> object:
        """
        :type: object
        """
    @min_linesearch_coefficient.setter
    def min_linesearch_coefficient(self, arg1: handle) -> None:
        pass
    @property
    def print_interval(self) -> object:
        """
        :type: object
        """
    @print_interval.setter
    def print_interval(self, arg1: handle) -> None:
        pass
    @property
    def print_precision(self) -> object:
        """
        :type: object
        """
    @print_precision.setter
    def print_precision(self, arg1: handle) -> None:
        pass
    @property
    def quadratic_upperbound_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @quadratic_upperbound_tolerance_factor.setter
    def quadratic_upperbound_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def reset_lbfgs_on_gn_step(self) -> object:
        """
        :type: object
        """
    @reset_lbfgs_on_gn_step.setter
    def reset_lbfgs_on_gn_step(self, arg1: handle) -> None:
        pass
    @property
    def stop_crit(self) -> object:
        """
        :type: object
        """
    @stop_crit.setter
    def stop_crit(self, arg1: handle) -> None:
        pass
    pass
class PANOCOCPProgressInfo():
    """
    Data passed to the PANOC progress callback.

    C++ documentation: :cpp:class:`alpaqa::PANOCOCPProgressInfo`
    """
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`

        :type: float
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\left\|p\right\| / \gamma`

        :type: float
        """
    @property
    def gn(self) -> bool:
        """
        Was :math:`q` a Gauss-Newton or L-BFGS step?

        :type: bool
        """
    @property
    def grad_ψ(self) -> numpy.ndarray:
        """
        Gradient of objective :math:`\nabla\psi(u)`

        :type: numpy.ndarray
        """
    @property
    def k(self) -> int:
        """
        Iteration

        :type: int
        """
    @property
    def lqr_min_rcond(self) -> float:
        """
        Minimum reciprocal condition number encountered in LQR factorization

        :type: float
        """
    @property
    def nJ(self) -> int:
        """
        Number of inactive constraints :math:`\#\mathcal J`

        :type: int
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\left\|p\right\|^2`

        :type: float
        """
    @property
    def p(self) -> numpy.ndarray:
        """
        Projected gradient step :math:`p`

        :type: numpy.ndarray
        """
    @property
    def params(self) -> PANOCOCPParams:
        """
        Solver parameters

        :type: PANOCOCPParams
        """
    @property
    def problem(self) -> ControlProblem:
        """
        Problem being solved

        :type: ControlProblem
        """
    @property
    def q(self) -> numpy.ndarray:
        """
        Previous accelerated step :math:`q`

        :type: numpy.ndarray
        """
    @property
    def status(self) -> _alpaqa_d.SolverStatus:
        """
        Current solver status

        :type: _alpaqa_d.SolverStatus
        """
    @property
    def u(self) -> numpy.ndarray:
        """
        Inputs

        :type: numpy.ndarray
        """
    @property
    def u_hat(self) -> numpy.ndarray:
        """
        Inputs after projected gradient step

        :type: numpy.ndarray
        """
    @property
    def x(self) -> numpy.ndarray:
        """
        States

        :type: numpy.ndarray
        """
    @property
    def x_hat(self) -> numpy.ndarray:
        """
        States after projected gradient step

        :type: numpy.ndarray
        """
    @property
    def xu(self) -> numpy.ndarray:
        """
        States :math:`x` and inputs :math:`u`

        :type: numpy.ndarray
        """
    @property
    def xu_hat(self) -> numpy.ndarray:
        """
        Variables after projected gradient step :math:`\hat u`

        :type: numpy.ndarray
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\gamma`

        :type: float
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\varepsilon_k`

        :type: float
        """
    @property
    def τ(self) -> float:
        """
        Line search parameter :math:`\tau`

        :type: float
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\varphi_\gamma(u)`

        :type: float
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\psi(u)`

        :type: float
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\psi(\hat u)`

        :type: float
        """
    pass
class PANOCOCPSolver():
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCOCPSolver`
    """
    def __call__(self, problem: ControlProblem, opts: InnerSolveOptions = {}, x: typing.Optional[numpy.ndarray] = None, y: typing.Optional[numpy.ndarray] = None, Σ: typing.Optional[numpy.ndarray] = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple: 
        """
        Solve.

        :param problem: Problem to solve
        :param opts: Options
        :param u: Initial guess
        :param y: Lagrange multipliers
        :param Σ: Penalty factors
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa._alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`u`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> PANOCOCPSolver: ...
    def __deepcopy__(self, memo: dict) -> PANOCOCPSolver: ...
    @typing.overload
    def __init__(self, other: PANOCOCPSolver) -> None: 
        """
        Create a copy

        Create a PANOC solver.
        """
    @typing.overload
    def __init__(self, panoc_params: typing.Union[PANOCOCPParams, dict]) -> None: ...
    def __str__(self) -> str: ...
    def set_progress_callback(self, callback: typing.Callable[[PANOCOCPProgressInfo], None]) -> PANOCOCPSolver: 
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
class PANOCParams():
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def L_max(self) -> object:
        """
        :type: object
        """
    @L_max.setter
    def L_max(self, arg1: handle) -> None:
        pass
    @property
    def L_min(self) -> object:
        """
        :type: object
        """
    @L_min.setter
    def L_min(self, arg1: handle) -> None:
        pass
    @property
    def Lipschitz(self) -> object:
        """
        :type: object
        """
    @Lipschitz.setter
    def Lipschitz(self, arg1: handle) -> None:
        pass
    @property
    def eager_gradient_eval(self) -> object:
        """
        :type: object
        """
    @eager_gradient_eval.setter
    def eager_gradient_eval(self, arg1: handle) -> None:
        pass
    @property
    def force_linesearch(self) -> object:
        """
        :type: object
        """
    @force_linesearch.setter
    def force_linesearch(self, arg1: handle) -> None:
        pass
    @property
    def linesearch_strictness_factor(self) -> object:
        """
        :type: object
        """
    @linesearch_strictness_factor.setter
    def linesearch_strictness_factor(self, arg1: handle) -> None:
        pass
    @property
    def linesearch_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @linesearch_tolerance_factor.setter
    def linesearch_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def max_iter(self) -> object:
        """
        :type: object
        """
    @max_iter.setter
    def max_iter(self, arg1: handle) -> None:
        pass
    @property
    def max_no_progress(self) -> object:
        """
        :type: object
        """
    @max_no_progress.setter
    def max_no_progress(self, arg1: handle) -> None:
        pass
    @property
    def max_time(self) -> object:
        """
        :type: object
        """
    @max_time.setter
    def max_time(self, arg1: handle) -> None:
        pass
    @property
    def min_linesearch_coefficient(self) -> object:
        """
        :type: object
        """
    @min_linesearch_coefficient.setter
    def min_linesearch_coefficient(self, arg1: handle) -> None:
        pass
    @property
    def print_interval(self) -> object:
        """
        :type: object
        """
    @print_interval.setter
    def print_interval(self, arg1: handle) -> None:
        pass
    @property
    def print_precision(self) -> object:
        """
        :type: object
        """
    @print_precision.setter
    def print_precision(self, arg1: handle) -> None:
        pass
    @property
    def quadratic_upperbound_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @quadratic_upperbound_tolerance_factor.setter
    def quadratic_upperbound_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def recompute_last_prox_step_after_stepsize_change(self) -> object:
        """
        :type: object
        """
    @recompute_last_prox_step_after_stepsize_change.setter
    def recompute_last_prox_step_after_stepsize_change(self, arg1: handle) -> None:
        pass
    @property
    def stop_crit(self) -> object:
        """
        :type: object
        """
    @stop_crit.setter
    def stop_crit(self, arg1: handle) -> None:
        pass
    @property
    def update_direction_in_candidate(self) -> object:
        """
        :type: object
        """
    @update_direction_in_candidate.setter
    def update_direction_in_candidate(self, arg1: handle) -> None:
        pass
    pass
class PANOCProgressInfo():
    """
    Data passed to the PANOC progress callback.

    C++ documentation: :cpp:class:`alpaqa::PANOCProgressInfo`
    """
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`

        :type: float
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\left\|p\right\| / \gamma`

        :type: float
        """
    @property
    def grad_ψ(self) -> numpy.ndarray:
        """
        Gradient of objective :math:`\nabla\psi(x)`

        :type: numpy.ndarray
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray:
        """
        Gradient of objective at x̂ :math:`\nabla\psi(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def k(self) -> int:
        """
        Iteration

        :type: int
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\left\|p\right\|^2`

        :type: float
        """
    @property
    def p(self) -> numpy.ndarray:
        """
        Projected gradient step :math:`p`

        :type: numpy.ndarray
        """
    @property
    def params(self) -> PANOCParams:
        """
        Solver parameters

        :type: PANOCParams
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved

        :type: Problem
        """
    @property
    def q(self) -> numpy.ndarray:
        """
        Previous quasi-Newton step :math:`\nabla\psi(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def status(self) -> _alpaqa_d.SolverStatus:
        """
        Current solver status

        :type: _alpaqa_d.SolverStatus
        """
    @property
    def x(self) -> numpy.ndarray:
        """
        Decision variable :math:`x`

        :type: numpy.ndarray
        """
    @property
    def x_hat(self) -> numpy.ndarray:
        """
        Decision variable after projected gradient step :math:`\hat x`

        :type: numpy.ndarray
        """
    @property
    def y(self) -> numpy.ndarray:
        """
        Lagrange multipliers :math:`y`

        :type: numpy.ndarray
        """
    @property
    def y_hat(self) -> numpy.ndarray:
        """
        Candidate updated multipliers at x̂ :math:`\hat y(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def Σ(self) -> numpy.ndarray:
        """
        Penalty factor :math:`\Sigma`

        :type: numpy.ndarray
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\gamma`

        :type: float
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\varepsilon_k`

        :type: float
        """
    @property
    def τ(self) -> float:
        """
        Previous line search parameter :math:`\tau`

        :type: float
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\varphi_\gamma(x)`

        :type: float
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\psi(x)`

        :type: float
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\psi(\hat x)`

        :type: float
        """
    pass
class PANOCSolver():
    """
    C++ documentation: :cpp:class:`alpaqa::PANOCSolver`
    """
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: typing.Optional[numpy.ndarray] = None, y: typing.Optional[numpy.ndarray] = None, Σ: typing.Optional[numpy.ndarray] = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple: 
        """
        Solve.

        :param problem: Problem to solve
        :param opts: Options
        :param u: Initial guess
        :param y: Lagrange multipliers
        :param Σ: Penalty factors
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa._alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`u`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> PANOCSolver: ...
    def __deepcopy__(self, memo: dict) -> PANOCSolver: ...
    @typing.overload
    def __init__(self, other: PANOCSolver) -> None: 
        """
        Create a copy

        Create a PANOC solver using structured L-BFGS directions.

        Create a PANOC solver using a custom direction.
        """
    @typing.overload
    def __init__(self, panoc_params: typing.Union[PANOCParams, dict] = {}, lbfgs_params: typing.Union[LBFGS.Params, dict] = {}, direction_params: typing.Union[StructuredLBFGSDirection.DirectionParams, dict] = {}) -> None: ...
    @typing.overload
    def __init__(self, panoc_params: typing.Union[PANOCParams, dict], direction: PANOCDirection) -> None: ...
    def __str__(self) -> str: ...
    def set_progress_callback(self, callback: typing.Callable[[PANOCProgressInfo], None]) -> PANOCSolver: 
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None: ...
    @property
    def direction(self) -> PANOCDirection:
        """
        :type: PANOCDirection
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
class PANTRDirection():
    @typing.overload
    def __init__(self, direction: NewtonTRDirection) -> None: 
        """
        Explicit conversion.

        Explicit conversion from a custom Python class.
        """
    @typing.overload
    def __init__(self, direction: object) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> object:
        """
        :type: object
        """
    pass
class PANTRParams():
    """
    C++ documentation: :cpp:class:`alpaqa::PANTRParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def L_max(self) -> object:
        """
        :type: object
        """
    @L_max.setter
    def L_max(self, arg1: handle) -> None:
        pass
    @property
    def L_min(self) -> object:
        """
        :type: object
        """
    @L_min.setter
    def L_min(self, arg1: handle) -> None:
        pass
    @property
    def Lipschitz(self) -> object:
        """
        :type: object
        """
    @Lipschitz.setter
    def Lipschitz(self, arg1: handle) -> None:
        pass
    @property
    def TR_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @TR_tolerance_factor.setter
    def TR_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def compute_ratio_using_new_stepsize(self) -> object:
        """
        :type: object
        """
    @compute_ratio_using_new_stepsize.setter
    def compute_ratio_using_new_stepsize(self, arg1: handle) -> None:
        pass
    @property
    def disable_acceleration(self) -> object:
        """
        :type: object
        """
    @disable_acceleration.setter
    def disable_acceleration(self, arg1: handle) -> None:
        pass
    @property
    def initial_radius(self) -> object:
        """
        :type: object
        """
    @initial_radius.setter
    def initial_radius(self, arg1: handle) -> None:
        pass
    @property
    def max_iter(self) -> object:
        """
        :type: object
        """
    @max_iter.setter
    def max_iter(self, arg1: handle) -> None:
        pass
    @property
    def max_no_progress(self) -> object:
        """
        :type: object
        """
    @max_no_progress.setter
    def max_no_progress(self, arg1: handle) -> None:
        pass
    @property
    def max_time(self) -> object:
        """
        :type: object
        """
    @max_time.setter
    def max_time(self, arg1: handle) -> None:
        pass
    @property
    def min_radius(self) -> object:
        """
        :type: object
        """
    @min_radius.setter
    def min_radius(self, arg1: handle) -> None:
        pass
    @property
    def print_interval(self) -> object:
        """
        :type: object
        """
    @print_interval.setter
    def print_interval(self, arg1: handle) -> None:
        pass
    @property
    def print_precision(self) -> object:
        """
        :type: object
        """
    @print_precision.setter
    def print_precision(self, arg1: handle) -> None:
        pass
    @property
    def quadratic_upperbound_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @quadratic_upperbound_tolerance_factor.setter
    def quadratic_upperbound_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def radius_factor_acceptable(self) -> object:
        """
        :type: object
        """
    @radius_factor_acceptable.setter
    def radius_factor_acceptable(self, arg1: handle) -> None:
        pass
    @property
    def radius_factor_good(self) -> object:
        """
        :type: object
        """
    @radius_factor_good.setter
    def radius_factor_good(self, arg1: handle) -> None:
        pass
    @property
    def radius_factor_rejected(self) -> object:
        """
        :type: object
        """
    @radius_factor_rejected.setter
    def radius_factor_rejected(self, arg1: handle) -> None:
        pass
    @property
    def ratio_approx_fbe_quadratic_model(self) -> object:
        """
        :type: object
        """
    @ratio_approx_fbe_quadratic_model.setter
    def ratio_approx_fbe_quadratic_model(self, arg1: handle) -> None:
        pass
    @property
    def ratio_threshold_acceptable(self) -> object:
        """
        :type: object
        """
    @ratio_threshold_acceptable.setter
    def ratio_threshold_acceptable(self, arg1: handle) -> None:
        pass
    @property
    def ratio_threshold_good(self) -> object:
        """
        :type: object
        """
    @ratio_threshold_good.setter
    def ratio_threshold_good(self, arg1: handle) -> None:
        pass
    @property
    def recompute_last_prox_step_after_direction_reset(self) -> object:
        """
        :type: object
        """
    @recompute_last_prox_step_after_direction_reset.setter
    def recompute_last_prox_step_after_direction_reset(self, arg1: handle) -> None:
        pass
    @property
    def stop_crit(self) -> object:
        """
        :type: object
        """
    @stop_crit.setter
    def stop_crit(self, arg1: handle) -> None:
        pass
    @property
    def update_direction_on_prox_step(self) -> object:
        """
        :type: object
        """
    @update_direction_on_prox_step.setter
    def update_direction_on_prox_step(self, arg1: handle) -> None:
        pass
    pass
class PANTRProgressInfo():
    """
    Data passed to the PANTR progress callback.

    C++ documentation: :cpp:class:`alpaqa::PANTRProgressInfo`
    """
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`

        :type: float
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\left\|p\right\| / \gamma`

        :type: float
        """
    @property
    def grad_ψ(self) -> numpy.ndarray:
        """
        Gradient of objective :math:`\nabla\psi(x)`

        :type: numpy.ndarray
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray:
        """
        Gradient of objective at x̂ :math:`\nabla\psi(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def k(self) -> int:
        """
        Iteration

        :type: int
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\left\|p\right\|^2`

        :type: float
        """
    @property
    def p(self) -> numpy.ndarray:
        """
        Projected gradient step :math:`p`

        :type: numpy.ndarray
        """
    @property
    def params(self) -> PANTRParams:
        """
        Solver parameters

        :type: PANTRParams
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved

        :type: Problem
        """
    @property
    def q(self) -> numpy.ndarray:
        """
        Previous quasi-Newton step :math:`\nabla\psi(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def status(self) -> _alpaqa_d.SolverStatus:
        """
        Current solver status

        :type: _alpaqa_d.SolverStatus
        """
    @property
    def x(self) -> numpy.ndarray:
        """
        Decision variable :math:`x`

        :type: numpy.ndarray
        """
    @property
    def x_hat(self) -> numpy.ndarray:
        """
        Decision variable after projected gradient step :math:`\hat x`

        :type: numpy.ndarray
        """
    @property
    def y(self) -> numpy.ndarray:
        """
        Lagrange multipliers :math:`y`

        :type: numpy.ndarray
        """
    @property
    def y_hat(self) -> numpy.ndarray:
        """
        Candidate updated multipliers at x̂ :math:`\hat y(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def Δ(self) -> float:
        """
        Previous trust radius :math:`\Delta`

        :type: float
        """
    @property
    def Σ(self) -> numpy.ndarray:
        """
        Penalty factor :math:`\Sigma`

        :type: numpy.ndarray
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\gamma`

        :type: float
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\varepsilon_k`

        :type: float
        """
    @property
    def ρ(self) -> float:
        """
        Previous decrease ratio :math:`\rho`

        :type: float
        """
    @property
    def τ(self) -> float:
        """
        :type: float
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\varphi_\gamma(x)`

        :type: float
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\psi(x)`

        :type: float
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\psi(\hat x)`

        :type: float
        """
    pass
class PANTRSolver():
    """
    C++ documentation: :cpp:class:`alpaqa::PANTRSolver`
    """
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: typing.Optional[numpy.ndarray] = None, y: typing.Optional[numpy.ndarray] = None, Σ: typing.Optional[numpy.ndarray] = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple: 
        """
        Solve.

        :param problem: Problem to solve
        :param opts: Options
        :param u: Initial guess
        :param y: Lagrange multipliers
        :param Σ: Penalty factors
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa._alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`u`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> PANTRSolver: ...
    def __deepcopy__(self, memo: dict) -> PANTRSolver: ...
    @typing.overload
    def __init__(self, other: PANTRSolver) -> None: 
        """
        Create a copy

        Create a PANTR solver using a structured Newton CG subproblem solver.

        Create a PANTR solver using a custom direction.
        """
    @typing.overload
    def __init__(self, pantr_params: typing.Union[PANTRParams, dict] = {}, steihaug_params: typing.Union[SteihaugCGParams, dict] = {}, direction_params: typing.Union[NewtonTRDirectionParams, dict] = {}) -> None: ...
    @typing.overload
    def __init__(self, pantr_params: typing.Union[PANTRParams, dict], direction: PANTRDirection) -> None: ...
    def __str__(self) -> str: ...
    def set_progress_callback(self, callback: typing.Callable[[PANTRProgressInfo], None]) -> PANTRSolver: 
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None: ...
    @property
    def direction(self) -> PANTRDirection:
        """
        :type: PANTRDirection
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
class Problem():
    """
    C++ documentation: :cpp:class:`alpaqa::TypeErasedProblem`
    """
    def __copy__(self) -> Problem: ...
    def __deepcopy__(self, memo: dict) -> Problem: ...
    @typing.overload
    def __init__(self, other: Problem) -> None: 
        """
        Create a copy

        Explicit conversion from a custom Python class.
        """
    @typing.overload
    def __init__(self, problem: object) -> None: ...
    def check(self) -> None: ...
    def eval_f(self, x: numpy.ndarray) -> float: ...
    def eval_f_g(self, x: numpy.ndarray, g: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray, grad_fx: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_f_grad_f(self, x: numpy.ndarray) -> tuple: ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray, gx: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_g(self, x: numpy.ndarray) -> numpy.ndarray: ...
    def eval_grad_L(self, x: numpy.ndarray, y: numpy.ndarray, grad_L: numpy.ndarray, work_n: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray, grad_fx: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_grad_f(self, x: numpy.ndarray) -> numpy.ndarray: ...
    def eval_grad_f_grad_g_prod(self, x: numpy.ndarray, y: numpy.ndarray, grad_f: numpy.ndarray, grad_gxy: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray, y: numpy.ndarray, grad_gxy: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_grad_g_prod(self, x: numpy.ndarray, y: numpy.ndarray) -> numpy.ndarray: ...
    def eval_grad_gi(self, x: numpy.ndarray, i: int, grad_gi: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray, grad_ψ: numpy.ndarray, work_n: numpy.ndarray, work_m: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_grad_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray) -> numpy.ndarray: ...
    def eval_hess_L(self, x: numpy.ndarray, y: numpy.ndarray, scale: float = 1.0) -> typing.Tuple[object, _alpaqa_d.Symmetry]: 
        """
        Returns the Hessian of the Lagrangian and its symmetry.
        """
    def eval_hess_L_prod(self, x: numpy.ndarray, y: numpy.ndarray, scale: float, v: numpy.ndarray, Hv: numpy.ndarray) -> None: ...
    def eval_hess_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray, scale: float = 1.0) -> typing.Tuple[object, _alpaqa_d.Symmetry]: 
        """
        Returns the Hessian of the augmented Lagrangian and its symmetry.
        """
    def eval_hess_ψ_prod(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray, scale: float, v: numpy.ndarray, Hv: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray, J: numpy.ndarray) -> int: ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray) -> numpy.ndarray: ...
    def eval_jac_g(self, x: numpy.ndarray) -> typing.Tuple[object, _alpaqa_d.Symmetry]: 
        """
        Returns the Jacobian of the constraints and its symmetry.
        """
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray, e: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray) -> numpy.ndarray: ...
    def eval_proj_multipliers(self, y: numpy.ndarray, M: float) -> None: ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray, x_hat: numpy.ndarray, p: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray) -> typing.Tuple[numpy.ndarray, numpy.ndarray, float]: ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray, ŷ: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray) -> typing.Tuple[float, numpy.ndarray]: ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray, grad_ψ: numpy.ndarray, work_n: numpy.ndarray, work_m: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_ψ_grad_ψ(self, x: numpy.ndarray, y: numpy.ndarray, Σ: numpy.ndarray) -> typing.Tuple[float, numpy.ndarray]: ...
    def get_box_C(self) -> Box: ...
    def get_box_D(self) -> Box: ...
    def provides_check(self) -> bool: ...
    def provides_eval_f_g(self) -> bool: ...
    def provides_eval_f_grad_f(self) -> bool: ...
    def provides_eval_grad_L(self) -> bool: ...
    def provides_eval_grad_f_grad_g_prod(self) -> bool: ...
    def provides_eval_grad_gi(self) -> bool: ...
    def provides_eval_grad_ψ(self) -> bool: ...
    def provides_eval_hess_L(self) -> bool: ...
    def provides_eval_hess_L_prod(self) -> bool: ...
    def provides_eval_hess_ψ(self) -> bool: ...
    def provides_eval_hess_ψ_prod(self) -> bool: ...
    def provides_eval_inactive_indices_res_lna(self) -> bool: ...
    def provides_eval_jac_g(self) -> bool: ...
    def provides_eval_ψ(self) -> bool: ...
    def provides_eval_ψ_grad_ψ(self) -> bool: ...
    def provides_get_box_C(self) -> bool: ...
    def provides_get_box_D(self) -> bool: ...
    def provides_get_hess_L_sparsity(self) -> bool: ...
    def provides_get_hess_ψ_sparsity(self) -> bool: ...
    def provides_get_jac_g_sparsity(self) -> bool: ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`

        :type: int
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`

        :type: int
        """
    pass
class ProblemWithCounters():
    @property
    def evaluations(self) -> _alpaqa_d.EvalCounter:
        """
        :type: _alpaqa_d.EvalCounter
        """
    @property
    def problem(self) -> Problem:
        """
        :type: Problem
        """
    pass
class SteihaugCGParams():
    """
    C++ documentation: :cpp:class:`alpaqa::SteihaugCGParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def max_iter_factor(self) -> object:
        """
        :type: object
        """
    @max_iter_factor.setter
    def max_iter_factor(self, arg1: handle) -> None:
        pass
    @property
    def tol_max(self) -> object:
        """
        :type: object
        """
    @tol_max.setter
    def tol_max(self, arg1: handle) -> None:
        pass
    @property
    def tol_scale(self) -> object:
        """
        :type: object
        """
    @tol_scale.setter
    def tol_scale(self, arg1: handle) -> None:
        pass
    @property
    def tol_scale_root(self) -> object:
        """
        :type: object
        """
    @tol_scale_root.setter
    def tol_scale_root(self, arg1: handle) -> None:
        pass
    pass
class StructuredLBFGSDirection():
    """
    C++ documentation: :cpp:class:`alpaqa::StructuredLBFGSDirection`
    """
    class DirectionParams():
        """
        C++ documentation: :cpp:class:`alpaqa::StructuredLBFGSDirection::DirectionParams`
        """
        @typing.overload
        def __init__(self, params: dict) -> None: ...
        @typing.overload
        def __init__(self, **kwargs) -> None: ...
        def to_dict(self) -> dict: ...
        @property
        def full_augmented_hessian(self) -> object:
            """
            :type: object
            """
        @full_augmented_hessian.setter
        def full_augmented_hessian(self, arg1: handle) -> None:
            pass
        @property
        def hessian_vec_factor(self) -> object:
            """
            :type: object
            """
        @hessian_vec_factor.setter
        def hessian_vec_factor(self, arg1: handle) -> None:
            pass
        @property
        def hessian_vec_finite_differences(self) -> object:
            """
            :type: object
            """
        @hessian_vec_finite_differences.setter
        def hessian_vec_finite_differences(self, arg1: handle) -> None:
            pass
        pass
    def __init__(self, lbfgs_params: typing.Union[LBFGS.Params, dict] = {}, direction_params: typing.Union[StructuredLBFGSDirection.DirectionParams, dict] = {}) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> typing.Tuple[LBFGS.Params, StructuredLBFGSDirection.DirectionParams]:
        """
        :type: typing.Tuple[LBFGS.Params, StructuredLBFGSDirection.DirectionParams]
        """
    pass
class StructuredNewtonDirection():
    """
    C++ documentation: :cpp:class:`alpaqa::StructuredNewtonDirection`
    """
    class DirectionParams():
        """
        C++ documentation: :cpp:class:`alpaqa::StructuredNewtonDirection::DirectionParams`
        """
        @typing.overload
        def __init__(self, params: dict) -> None: ...
        @typing.overload
        def __init__(self, **kwargs) -> None: ...
        def to_dict(self) -> dict: ...
        @property
        def hessian_vec_factor(self) -> object:
            """
            :type: object
            """
        @hessian_vec_factor.setter
        def hessian_vec_factor(self, arg1: handle) -> None:
            pass
        pass
    def __init__(self, direction_params: typing.Union[StructuredNewtonDirection.DirectionParams, dict] = {}) -> None: ...
    def __str__(self) -> str: ...
    @property
    def params(self) -> StructuredNewtonDirection.DirectionParams:
        """
        :type: StructuredNewtonDirection.DirectionParams
        """
    pass
class UnconstrProblem():
    """
    C++ documentation: :cpp:class:`alpaqa::UnconstrProblem`
    """
    def __copy__(self) -> UnconstrProblem: ...
    def __deepcopy__(self, memo: dict) -> UnconstrProblem: ...
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self, other: UnconstrProblem) -> None: 
        """
        Create a copy

        :param n: Number of unknowns
        """
    @typing.overload
    def __init__(self, n: int) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def eval_g(self, x: numpy.ndarray, g: numpy.ndarray) -> None: ...
    def eval_grad_g_prod(self, x: numpy.ndarray, y: numpy.ndarray, grad_gxy: numpy.ndarray) -> None: ...
    def eval_grad_gi(self, x: numpy.ndarray, i: int, grad_gi: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray, J: numpy.ndarray) -> int: ...
    @typing.overload
    def eval_inactive_indices_res_lna(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray) -> numpy.ndarray: ...
    def eval_jac_g(self, x: numpy.ndarray, J_values: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray, e: numpy.ndarray) -> None: ...
    @typing.overload
    def eval_proj_diff_g(self, z: numpy.ndarray) -> numpy.ndarray: ...
    def eval_proj_multipliers(self, y: numpy.ndarray, M: float) -> None: ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray, x_hat: numpy.ndarray, p: numpy.ndarray) -> float: ...
    @typing.overload
    def eval_prox_grad_step(self, γ: float, x: numpy.ndarray, grad_ψ: numpy.ndarray) -> typing.Tuple[numpy.ndarray, numpy.ndarray, float]: ...
    def resize(self, n: int) -> None: ...
    @property
    def m(self) -> int:
        """
        Number of general constraints, dimension of :math:`g(x)`

        :type: int
        """
    @property
    def n(self) -> int:
        """
        Number of decision variables, dimension of :math:`x`

        :type: int
        """
    pass
class ZeroFPRParams():
    """
    C++ documentation: :cpp:class:`alpaqa::ZeroFPRParams`
    """
    @typing.overload
    def __init__(self, params: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    @property
    def L_max(self) -> object:
        """
        :type: object
        """
    @L_max.setter
    def L_max(self, arg1: handle) -> None:
        pass
    @property
    def L_min(self) -> object:
        """
        :type: object
        """
    @L_min.setter
    def L_min(self, arg1: handle) -> None:
        pass
    @property
    def Lipschitz(self) -> object:
        """
        :type: object
        """
    @Lipschitz.setter
    def Lipschitz(self, arg1: handle) -> None:
        pass
    @property
    def force_linesearch(self) -> object:
        """
        :type: object
        """
    @force_linesearch.setter
    def force_linesearch(self, arg1: handle) -> None:
        pass
    @property
    def linesearch_strictness_factor(self) -> object:
        """
        :type: object
        """
    @linesearch_strictness_factor.setter
    def linesearch_strictness_factor(self, arg1: handle) -> None:
        pass
    @property
    def linesearch_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @linesearch_tolerance_factor.setter
    def linesearch_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def max_iter(self) -> object:
        """
        :type: object
        """
    @max_iter.setter
    def max_iter(self, arg1: handle) -> None:
        pass
    @property
    def max_no_progress(self) -> object:
        """
        :type: object
        """
    @max_no_progress.setter
    def max_no_progress(self, arg1: handle) -> None:
        pass
    @property
    def max_time(self) -> object:
        """
        :type: object
        """
    @max_time.setter
    def max_time(self, arg1: handle) -> None:
        pass
    @property
    def min_linesearch_coefficient(self) -> object:
        """
        :type: object
        """
    @min_linesearch_coefficient.setter
    def min_linesearch_coefficient(self, arg1: handle) -> None:
        pass
    @property
    def print_interval(self) -> object:
        """
        :type: object
        """
    @print_interval.setter
    def print_interval(self, arg1: handle) -> None:
        pass
    @property
    def print_precision(self) -> object:
        """
        :type: object
        """
    @print_precision.setter
    def print_precision(self, arg1: handle) -> None:
        pass
    @property
    def quadratic_upperbound_tolerance_factor(self) -> object:
        """
        :type: object
        """
    @quadratic_upperbound_tolerance_factor.setter
    def quadratic_upperbound_tolerance_factor(self, arg1: handle) -> None:
        pass
    @property
    def recompute_last_prox_step_after_stepsize_change(self) -> object:
        """
        :type: object
        """
    @recompute_last_prox_step_after_stepsize_change.setter
    def recompute_last_prox_step_after_stepsize_change(self, arg1: handle) -> None:
        pass
    @property
    def stop_crit(self) -> object:
        """
        :type: object
        """
    @stop_crit.setter
    def stop_crit(self, arg1: handle) -> None:
        pass
    @property
    def update_direction_from_prox_step(self) -> object:
        """
        :type: object
        """
    @update_direction_from_prox_step.setter
    def update_direction_from_prox_step(self, arg1: handle) -> None:
        pass
    @property
    def update_direction_in_candidate(self) -> object:
        """
        :type: object
        """
    @update_direction_in_candidate.setter
    def update_direction_in_candidate(self, arg1: handle) -> None:
        pass
    pass
class ZeroFPRProgressInfo():
    """
    Data passed to the ZeroFPR progress callback.

    C++ documentation: :cpp:class:`alpaqa::ZeroFPRProgressInfo`
    """
    @property
    def L(self) -> float:
        """
        Estimate of Lipschitz constant of objective :math:`L`

        :type: float
        """
    @property
    def fpr(self) -> float:
        """
        Fixed-point residual :math:`\left\|p\right\| / \gamma`

        :type: float
        """
    @property
    def grad_ψ(self) -> numpy.ndarray:
        """
        Gradient of objective :math:`\nabla\psi(x)`

        :type: numpy.ndarray
        """
    @property
    def grad_ψ_hat(self) -> numpy.ndarray:
        """
        Gradient of objective at x̂ :math:`\nabla\psi(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def k(self) -> int:
        """
        Iteration

        :type: int
        """
    @property
    def norm_sq_p(self) -> float:
        """
        :math:`\left\|p\right\|^2`

        :type: float
        """
    @property
    def p(self) -> numpy.ndarray:
        """
        Projected gradient step :math:`p`

        :type: numpy.ndarray
        """
    @property
    def params(self) -> ZeroFPRParams:
        """
        Solver parameters

        :type: ZeroFPRParams
        """
    @property
    def problem(self) -> Problem:
        """
        Problem being solved

        :type: Problem
        """
    @property
    def q(self) -> numpy.ndarray:
        """
        Previous quasi-Newton step :math:`\nabla\psi(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def status(self) -> _alpaqa_d.SolverStatus:
        """
        Current solver status

        :type: _alpaqa_d.SolverStatus
        """
    @property
    def x(self) -> numpy.ndarray:
        """
        Decision variable :math:`x`

        :type: numpy.ndarray
        """
    @property
    def x_hat(self) -> numpy.ndarray:
        """
        Decision variable after projected gradient step :math:`\hat x`

        :type: numpy.ndarray
        """
    @property
    def y(self) -> numpy.ndarray:
        """
        Lagrange multipliers :math:`y`

        :type: numpy.ndarray
        """
    @property
    def y_hat(self) -> numpy.ndarray:
        """
        Candidate updated multipliers at x̂ :math:`\hat y(\hat x)`

        :type: numpy.ndarray
        """
    @property
    def Σ(self) -> numpy.ndarray:
        """
        Penalty factor :math:`\Sigma`

        :type: numpy.ndarray
        """
    @property
    def γ(self) -> float:
        """
        Step size :math:`\gamma`

        :type: float
        """
    @property
    def ε(self) -> float:
        """
        Tolerance reached :math:`\varepsilon_k`

        :type: float
        """
    @property
    def τ(self) -> float:
        """
        Previous line search parameter :math:`\tau`

        :type: float
        """
    @property
    def φγ(self) -> float:
        """
        Forward-backward envelope :math:`\varphi_\gamma(x)`

        :type: float
        """
    @property
    def ψ(self) -> float:
        """
        Objective value :math:`\psi(x)`

        :type: float
        """
    @property
    def ψ_hat(self) -> float:
        """
        Objective at x̂ :math:`\psi(\hat x)`

        :type: float
        """
    pass
class ZeroFPRSolver():
    """
    C++ documentation: :cpp:class:`alpaqa::ZeroFPRSolver`
    """
    def __call__(self, problem: Problem, opts: InnerSolveOptions = {}, x: typing.Optional[numpy.ndarray] = None, y: typing.Optional[numpy.ndarray] = None, Σ: typing.Optional[numpy.ndarray] = None, *, asynchronous: bool = True, suppress_interrupt: bool = False) -> tuple: 
        """
        Solve.

        :param problem: Problem to solve
        :param opts: Options
        :param u: Initial guess
        :param y: Lagrange multipliers
        :param Σ: Penalty factors
        :param asynchronous: Release the GIL and run the solver on a separate thread
        :param suppress_interrupt: If the solver is interrupted by a ``KeyboardInterrupt``, don't propagate this exception back to the Python interpreter, but stop the solver early, and return a solution with the status set to :py:data:`alpaqa._alpaqa.SolverStatus.Interrupted`.
        :return: * Solution :math:`u`
                 * Updated Lagrange multipliers (only if parameter ``y`` was not ``None``)
                 * Constraint violation (only if parameter ``y`` was not ``None``)
                 * Statistics
        """
    def __copy__(self) -> ZeroFPRSolver: ...
    def __deepcopy__(self, memo: dict) -> ZeroFPRSolver: ...
    @typing.overload
    def __init__(self, other: ZeroFPRSolver) -> None: 
        """
        Create a copy

        Create a ZeroFPR solver using structured L-BFGS directions.

        Create a ZeroFPR solver using a custom direction.
        """
    @typing.overload
    def __init__(self, zerofpr_params: typing.Union[ZeroFPRParams, dict] = {}, lbfgs_params: typing.Union[LBFGS.Params, dict] = {}, direction_params: typing.Union[StructuredLBFGSDirection.DirectionParams, dict] = {}) -> None: ...
    @typing.overload
    def __init__(self, zerofpr_params: typing.Union[ZeroFPRParams, dict], direction: PANOCDirection) -> None: ...
    def __str__(self) -> str: ...
    def set_progress_callback(self, callback: typing.Callable[[ZeroFPRProgressInfo], None]) -> ZeroFPRSolver: 
        """
        Specify a callable that is invoked with some intermediate results on each iteration of the algorithm.
        """
    def stop(self) -> None: ...
    @property
    def direction(self) -> PANOCDirection:
        """
        :type: PANOCDirection
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
def problem_with_counters(problem: object) -> ProblemWithCounters:
    pass
def provided_functions(problem: Problem) -> str:
    """
    Returns a string representing the functions provided by the problem.
    """
@typing.overload
def prox(self: functions.NuclearNorm, input: numpy.ndarray, output: numpy.ndarray, γ: float = 1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`

    C++ documentation: :cpp:var:`alpaqa::prox`
    Compute the proximal mapping of ``self`` at ``in`` with step size ``γ``. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox_step`
    """
@typing.overload
def prox(self: functions.NuclearNorm, input: numpy.ndarray, γ: float = 1) -> typing.Tuple[float, numpy.ndarray]:
    pass
@typing.overload
def prox(self: functions.L1Norm, input: numpy.ndarray, output: numpy.ndarray, γ: float = 1) -> float:
    pass
@typing.overload
def prox(self: functions.L1Norm, input: numpy.ndarray, γ: float = 1) -> typing.Tuple[float, numpy.ndarray]:
    pass
@typing.overload
def prox(self: functions.L1NormElementwise, input: numpy.ndarray, output: numpy.ndarray, γ: float = 1) -> float:
    pass
@typing.overload
def prox(self: functions.L1NormElementwise, input: numpy.ndarray, γ: float = 1) -> typing.Tuple[float, numpy.ndarray]:
    pass
@typing.overload
def prox(self: Box, input: numpy.ndarray, output: numpy.ndarray, γ: float = 1) -> float:
    pass
@typing.overload
def prox(self: Box, input: numpy.ndarray, γ: float = 1) -> typing.Tuple[float, numpy.ndarray]:
    pass
@typing.overload
def prox_step(self: functions.NuclearNorm, input: numpy.ndarray, input_step: numpy.ndarray, output: numpy.ndarray, output_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> float:
    """
    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version overwrites the given output arguments.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

    C++ documentation: :cpp:var:`alpaqa::prox_step`
    Compute a generalized forward-backward step. This version returns the outputs as a tuple.

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`
    """
@typing.overload
def prox_step(self: functions.NuclearNorm, input: numpy.ndarray, input_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> typing.Tuple[float, numpy.ndarray, numpy.ndarray]:
    pass
@typing.overload
def prox_step(self: functions.L1Norm, input: numpy.ndarray, input_step: numpy.ndarray, output: numpy.ndarray, output_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> float:
    pass
@typing.overload
def prox_step(self: functions.L1Norm, input: numpy.ndarray, input_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> typing.Tuple[float, numpy.ndarray, numpy.ndarray]:
    pass
@typing.overload
def prox_step(self: functions.L1NormElementwise, input: numpy.ndarray, input_step: numpy.ndarray, output: numpy.ndarray, output_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> float:
    pass
@typing.overload
def prox_step(self: functions.L1NormElementwise, input: numpy.ndarray, input_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> typing.Tuple[float, numpy.ndarray, numpy.ndarray]:
    pass
@typing.overload
def prox_step(self: Box, input: numpy.ndarray, input_step: numpy.ndarray, output: numpy.ndarray, output_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> float:
    pass
@typing.overload
def prox_step(self: Box, input: numpy.ndarray, input_step: numpy.ndarray, γ: float = 1, γ_step: float = -1) -> typing.Tuple[float, numpy.ndarray, numpy.ndarray]:
    pass

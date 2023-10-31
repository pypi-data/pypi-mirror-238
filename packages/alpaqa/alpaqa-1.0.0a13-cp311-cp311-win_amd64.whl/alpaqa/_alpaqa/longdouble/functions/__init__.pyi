"""(Proximal) functions and operators."""
from __future__ import annotations
import _alpaqa.longdouble.functions
import typing

__all__ = [
    "L1Norm",
    "L1NormElementwise",
    "NuclearNorm"
]


class L1Norm():
    """
    C++ documentation :cpp:class:`alpaqa::functions::L1Norm`
    ℓ₁-norm regularizer (with a single scalar regularization factor).

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`
    """
    def __init__(self, λ: float = 1) -> None: ...
    @property
    def λ(self) -> float:
        """
        Regularization factor.

        :type: float
        """
    pass
class L1NormElementwise():
    """
    C++ documentation :cpp:class:`alpaqa::functions::L1NormElementwise`
    ℓ₁-norm regularizer (with element-wise regularization factors).

    .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, λ: numpy.ndarray) -> None: ...
    @property
    def λ(self) -> numpy.ndarray:
        """
        Regularization factors.

        :type: numpy.ndarray
        """
    pass
class NuclearNorm():
    """
    C++ documentation :cpp:class:`alpaqa::functions::NuclearNorm`
    """
    @typing.overload
    def __init__(self, λ: float) -> None: ...
    @typing.overload
    def __init__(self, λ: float, rows: int, cols: int) -> None: ...
    @property
    def U(self) -> numpy.ndarray:
        """
        Left singular vectors.

        :type: numpy.ndarray
        """
    @property
    def V(self) -> numpy.ndarray:
        """
        Right singular vectors.

        :type: numpy.ndarray
        """
    @property
    def singular_values(self) -> numpy.ndarray:
        """
        Vector of singular values of the last output of the prox method.

        .. seealso:: :py:func:`alpaqa._alpaqa.float64.prox`

        :type: numpy.ndarray
        """
    @property
    def singular_values_input(self) -> numpy.ndarray:
        """
        Vector of singular values of the last input of the prox method.

        :type: numpy.ndarray
        """
    @property
    def λ(self) -> float:
        """
        Regularization factor.

        :type: float
        """
    pass

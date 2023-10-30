"""Holds some common types which are used in various places."""

from typing import Any, Iterable

from torch import Tensor

Params = Iterable[Tensor] | Iterable[dict[str, Any]]

Betas2 = tuple[float, float]
State = dict[str, Any]
Nus2 = tuple[float, float]

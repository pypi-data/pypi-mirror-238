"""Defines some functions to do specific common PyTorch operations."""

from torch import Tensor


def append_dims(x: Tensor, target_dims: int) -> Tensor:
    """Appends broadcastable dimensions to a given tensor.

    Args:
        x: The input tensor, with shape ``(*)`` and some number of dimensions
            smaller than ``target_dims``
        target_dims: The target number of dimensions, which should be larger
            than the number of dimensions of ``x``

    Returns:
        A new tensor with shape ``(*, 1, ..., 1)``, with trailing ones added
        to make the tensor have ``target_dims`` dimensions.
    """
    dims_to_append = target_dims - x.dim()
    if dims_to_append < 0:
        raise ValueError(f"Input dimension {x.dim()} is larger than target dimension {target_dims}")
    return x[(...,) + (None,) * dims_to_append]

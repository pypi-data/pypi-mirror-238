"""Defines loss functions used for Diffusion models."""

import math

import torch
from torch import Tensor


def pseudo_huber_loss(
    x: Tensor,
    y: Tensor,
    dim: int = -1,
    factor: float = 0.00054,
    keepdim: bool = False,
) -> Tensor:
    """Returns the pseudo-Huber loss.

    This is taken from the Consistency Models paper.

    Args:
        x: The input tensor.
        y: The target tensor.
        dim: The dimension to compute the loss over.
        factor: The factor to use in the loss.
        keepdim: Whether to keep the dimension or not.

    Returns:
        The pseudo-Huber loss over the given dimension (i.e., that )
    """
    c = factor * math.sqrt(x.shape[dim])
    return torch.sqrt(torch.norm(x - y, p=2, dim=dim, keepdim=keepdim) ** 2 + c**2) - c

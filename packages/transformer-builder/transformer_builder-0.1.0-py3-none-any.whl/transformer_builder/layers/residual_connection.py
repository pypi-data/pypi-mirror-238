import torch
from torch import nn


class ResidualConnection(nn.Module):
    """
    Wraps a module with residual connection.

    Remembers input, adds output of the module and applies normalization.
    """

    def __init__(
        self,
        module: nn.Module,
        normalization: nn.Module,
    ):
        """
        Args:
            module: The module to apply the residual connection to.

            normalization: The normalization module to be applied to
            the sum of the initial input and the output of the module.
        """
        super().__init__()
        self.normalization = normalization
        self.module = module

    def forward(self, x: torch.Tensor, *args, **kwargs):
        _x = x
        x = self.module(x, *args, **kwargs)
        return self.normalization(x + _x)

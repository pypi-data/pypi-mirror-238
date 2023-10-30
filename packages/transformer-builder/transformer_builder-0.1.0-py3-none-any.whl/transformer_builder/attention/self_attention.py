import torch
from torch import nn
from torch.nn.functional import scaled_dot_product_attention


class SelfAttention(nn.Module):
    """
    This class implements the Self-Attention head.
    """

    def __init__(
        self,
        dropout: float = 0.0,
        casual_masking: bool = False,
        layer_before: nn.Module = nn.Identity(),
        q_architecture: nn.Module = nn.Identity(),
        k_architecture: nn.Module = nn.Identity(),
        v_architecture: nn.Module = nn.Identity(),
        layer_after: nn.Module = nn.Identity(),
        scale: float = None,
    ) -> None:
        """
        Args:
            dropout: The attention dropout.

            casual_masking: Whether to apply upper triangular masking to the input.
            Incompatible with mask passed in the forward pass

            layer_before: The layer before k, q, v.

            q_architecture: Architecture for the query.

            k_architecture: Architecture for the key.

            v_architecture: Architecture for the value.

            layer_after: Layer after the scaled dot product of the attention.

            scale: The scaling value.
            Used to scale the dot product of q and k
        """
        super().__init__()
        self.dropout = dropout
        self.casual_masking = casual_masking

        self.layer_before = layer_before
        self.q_architecture = q_architecture
        self.k_architecture = k_architecture
        self.v_architecture = v_architecture
        self.layer_after = layer_after

        self.scale = scale

    def forward(
        self,
        x: torch.Tensor,
        mask: torch.Tensor = None,
    ) -> torch.Tensor:
        """
        This method implements the forward pass of the Self-Attention.
        Args:
            x: The input tensor of shape
            (optional_batch_size, sequence_length, embedding_dim).

            mask: Mask tensor of shape
            (optional_batch_size, sequence_length, sequence_length).
            Used to mask the attention, incompatible with casual masking.

        Returns:
            Tensor: The output tensor.
        """
        x = self.layer_before(x)

        query_future = torch.jit.fork(self.q_architecture, x)
        key_future = torch.jit.fork(self.k_architecture, x)
        value_future = torch.jit.fork(self.v_architecture, x)

        query = torch.jit.wait(query_future)
        key = torch.jit.wait(key_future)
        value = torch.jit.wait(value_future)

        attention = scaled_dot_product_attention(
            query=query,
            key=key,
            value=value,
            attn_mask=mask,
            dropout_p=self.dropout,
            scale=self.scale,
            is_causal=self.casual_masking,
        )

        attention = self.layer_after(attention)

        return attention

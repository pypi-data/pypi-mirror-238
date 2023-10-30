# transformer-builder

[![License](https://img.shields.io/badge/license-BSD-blue.svg)](https://github.com/MrKekovich/transformer-builder/blob/master/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Project Status](https://img.shields.io/badge/Project%20Status-pre--alpha-blue)](https://github.com/MrKekovich/transformer-builder/)

---

> Make your own transformers with ease.

Transformers have become a popular choice for a wide range of Natural Language Processing (NLP) and deep learning tasks.
The transformer-builder package allows you to create custom transformer models with ease, providing flexibility and
modularity for your deep learning projects.

---

## Features

- Build custom transformer models with a user-friendly and flexible interface.
- Configurable encoder and decoder blocks with support for custom self-attention mechanisms.
- Encapsulated self-attention blocks that adapt to your specific use case.
- Open-source and customizable to fit your project's requirements.

---

## Installation

You can install transformer-builder using pip:

```bash
pip install transformer-builder
```

---

## Usage

Here's an example of how to use Transformer Builder to create a custom model:

```python
import torch
from torch import nn

from transformer_builder.attention import SelfAttention, MultiHeadAttention
from transformer_builder.layers import ResidualConnection

vocab_size = 16_000
embedding_dim = 512
num_heads = 8
d_head = embedding_dim // num_heads

vocab_size = 16_000
embedding_dim = 512
num_heads = 4
num_blocks = 3
d_head = embedding_dim // num_heads

blocks = [MultiHeadAttention(
    layer_before=nn.Linear(embedding_dim, embedding_dim),
    self_attention_heads=[
        SelfAttention(
            q_architecture=nn.Linear(embedding_dim, d_head),  # Default: nn.Identity
            k_architecture=nn.Linear(embedding_dim, d_head),
            v_architecture=nn.Linear(embedding_dim, d_head),
        ),
        SelfAttention(
            # This will calculate scaled dot product attention of original inputs
            # And pass the result to the linear layer
            layer_after=nn.Linear(embedding_dim, d_head),
        ),
        SelfAttention(
            layer_after=nn.Linear(embedding_dim, d_head),
        ),
        SelfAttention(
            # Now some exotic attention architecture
            layer_before=SelfAttention(),
            # The default value for self_attention_heads is single default head
            layer_after=MultiHeadAttention(
                layer_after=nn.Linear(embedding_dim, d_head),
            )
        )
    ]
)
    for _ in range(num_blocks)]

gpt = nn.Sequential(
    # nn.Embedding(vocab_size, embedding_dim), for simplicity, we will use random embeddings
    # ResidualConnection will add original input to the output of the module and apply normalization
    *[ResidualConnection(
        module=multi_head_attention,
        normalization=nn.LayerNorm(embedding_dim)
    ) for multi_head_attention in blocks],
)

gpt(torch.randn(8, embedding_dim))

```

---

## Customization

With transformer-builder, you can customize each aspect of your blocks individually,
allowing for fine-grained control over your model's architecture.
The example above demonstrates how to configure the self-attention layer,
layer normalization, and linear layers.
You can go crazy and create encoder inside decoder inside self-attention!

---

## Contributing

If you would like to contribute to this project, please follow our
[contribution guidelines](https://github.com/MrKekovich/transformer-builder/blob/master/CONTRIBUTING.md).

---

## Support and Feedback

If you have questions, encounter issues, or have feedback, please open an issue on our
[GitHub repository](https://github.com/MrKekovich/transformer-builder).

---

## Acknowledgments

This project was inspired by the need for a flexible and customizable API for creating
decoder blocks in deep learning models.

---

## Author

[MrKekovich](https://github.com/MrKekovich)

---

## License

This project is licensed under the [BSD-3-Clause](https://opensource.org/license/bsd-3-clause/) License.
See the [LICENSE](https://github.com/MrKekovich/transformer-builder/blob/master/LICENSE) file for details.

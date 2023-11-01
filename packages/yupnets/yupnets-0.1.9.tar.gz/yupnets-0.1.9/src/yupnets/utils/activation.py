import torch.nn as nn

__all__ = [
    "Activation",
]


class Activation:
    activations = [
        "ELU",
        "GELU",
        "ReLU",
        "LeakyReLU",
        "Mish",
        "Sigmoid",
        "SiLU",
        "Softplus",
        "Tanh",
    ]

    def __init__(
            self,
            activation_type: str,
    ) -> None:
        if activation_type not in self.activations:
            raise ValueError(f"Unsupported activation: {activation_type}")

        self.activation_type = activation_type
        self.activation = getattr(nn, activation_type)

    def __call__(
            self,
            inplace=True,
            **kwargs,
    ) -> nn.Module:
        if self.activation_type in ["ELU", "ReLU", "LeakyRELU", ]:
            activation = self.activation(inplace=inplace, **kwargs)

        else:
            activation = self.activation(**kwargs)

        return activation

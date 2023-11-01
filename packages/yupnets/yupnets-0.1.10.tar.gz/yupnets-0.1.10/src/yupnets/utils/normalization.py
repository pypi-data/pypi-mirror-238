import torch.nn as nn

__all__ = [
    "Normalization",
]


class Normalization:
    normalizations = [
        "BatchNorm2d",
        "GroupNorm",
        "LayerNorm",
    ]

    def __init__(
            self,
            normalization_type: str,
    ) -> None:
        if normalization_type not in self.normalizations:
            raise ValueError(f"Unsupported normalization: {normalization_type}")

        self.normalization_type = normalization_type
        self.normalization = getattr(nn, normalization_type)

    def __call__(
            self,
            channels: int,
            **kwargs,
    ) -> nn.Module:
        if self.normalization_type is "BatchNorm2d":
            normalization = self.normalization(num_features=channels, **kwargs)

        # TBD
        elif self.normalization_type is "GroupNorm":
            normalization = self.normalization(num_channels=channels, **kwargs)

        # TBD
        elif self.normalization_type is "LayerNorm":
            normalization = self.normalization(normalized_shape=channels, **kwargs)

        else:
            raise

        return normalization

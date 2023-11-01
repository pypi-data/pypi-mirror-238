from typing import Any, Optional

from . import cifar10, imagenet1k
from .utils import VisionTransformer

__all__ = [
    "nets",
    "vit_loader",
]

nets = \
    cifar10.__all__ + \
    imagenet1k.__all__


def vit_loader(
        net: Optional[str] = "vit",
        **kwargs: Any,
) -> VisionTransformer:
    if net != "vit":
        if net in cifar10.__all__:
            _kwargs = getattr(cifar10, net)

        elif net in imagenet1k.__all__:
            _kwargs = getattr(imagenet1k, net)

        else:
            raise ValueError(f"{net} not supported in VisionTransformer")

        for key, value in kwargs.items():
            _kwargs[key] = value

        return VisionTransformer(**_kwargs)

    else:
        return VisionTransformer(**kwargs)

from typing import Any, Optional

from . import cifar10, imagenet1k
from .utils import ResNet

__all__ = [
    "nets",
    "resnet_loader",
]

nets = \
    cifar10.__all__ + \
    imagenet1k.__all__


def resnet_loader(
        net: Optional[str] = "resnet",
        **kwargs: Any,
) -> ResNet:
    if net != "resnet":
        if net in cifar10.__all__:
            _kwargs = getattr(cifar10, net)

        elif net in imagenet1k.__all__:
            _kwargs = getattr(imagenet1k, net)

        else:
            raise ValueError(f"{net} not supported in ResNet")

        for key, value in kwargs.items():
            _kwargs[key] = value

        return ResNet(**_kwargs)

    else:
        return ResNet(**kwargs)

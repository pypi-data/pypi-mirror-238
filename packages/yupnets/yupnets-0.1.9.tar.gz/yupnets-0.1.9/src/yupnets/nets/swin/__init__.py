from typing import Any, Optional

from . import imagenet1k
from .utils import SwinTransformer

__all__ = [
    "nets",
    "swin_loader",
]

nets = \
    imagenet1k.__all__


def swin_loader(
        net: Optional[str] = "swin",
        **kwargs: Any,
) -> SwinTransformer:
    if net != "swin":
        if net in imagenet1k.__all__:
            _kwargs = getattr(imagenet1k, net)

        else:
            raise ValueError(f"{net} not supported in SwinTransformer")

        for key, value in kwargs.items():
            _kwargs[key] = value

        return SwinTransformer(**_kwargs)

    else:
        return SwinTransformer(**kwargs)

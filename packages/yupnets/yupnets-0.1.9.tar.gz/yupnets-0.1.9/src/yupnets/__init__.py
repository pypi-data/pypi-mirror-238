from .nets import *
from .test import *
from .utils import *
from .xray import *

__all__ = [
    # nets
    "load_net",

    # test
    "AccuracyTest",
    "CalibrationTest",
    "HessianTest3D",
    "LinearityTest",

    # utils
    "Activation",
    "BatchManager",
    "Normalization",

    # xray
    "get_layer_ids",
    "get_layer",
    "FeatureExtractor",
]


def load_net(
        net: str,
        **kwargs,
):
    if net in resnet.nets or net == "resnet":
        loader = resnet.resnet_loader

    elif net in swin.nets or net == "swin":
        loader = swin.swin_loader

    elif net in vit.nets or net == "vit":
        loader = vit.vit_loader

    else:
        raise ValueError(f"Unsupported net: {net}")

    model = loader(net=net, **kwargs)

    setattr(model, "name", net)

    return model

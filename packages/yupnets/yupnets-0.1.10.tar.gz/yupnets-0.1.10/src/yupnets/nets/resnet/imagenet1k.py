from .utils import BasicBlock, Bottleneck

__all__ = [
    "resnet18",
    "resnet34",
    "resnet50",
    "resnet101",
    "resnet152",

    "resnext50_32x4d",
    "resnext101_32x8d",
    "resnext101_64x4d",

    "wide_resnet50_2",
    "wide_resnet101_2",
]

resnet18 = {
    "block": BasicBlock,
    "planes": [64, 128, 256, 512],
    "layers": [2, 2, 2, 2],
    "num_classes": 1000,
}

resnet34 = {
    "block": BasicBlock,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 6, 3],
    "num_classes": 1000,
}

resnet50 = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 6, 3],
    "num_classes": 1000,
}

resnet101 = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 23, 3],
    "num_classes": 1000,
}

resnet152 = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 8, 36, 3],
    "num_classes": 1000,
}

resnext50_32x4d = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 6, 3],
    "num_classes": 1000,
    "groups": 32,
    "width_per_group": 4,
}

resnext101_32x8d = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 23, 3],
    "num_classes": 1000,
    "groups": 32,
    "width_per_group": 8,
}

resnext101_64x4d = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 23, 3],
    "num_classes": 1000,
    "groups": 64,
    "width_per_group": 4,
}

wide_resnet50_2 = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 6, 3],
    "num_classes": 1000,
    "width_per_group": 64 * 2,
}

wide_resnet101_2 = {
    "block": Bottleneck,
    "planes": [64, 128, 256, 512],
    "layers": [3, 4, 23, 3],
    "num_classes": 1000,
    "width_per_group": 64 * 2,
}

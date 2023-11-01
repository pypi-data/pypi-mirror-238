from .utils import BasicBlock

__all__ = [
    "resnet20",
    "resnet32",
    "resnet44",
    "resnet56",
    "resnet110",
    "resnet1202",
]

resnet20 = {
    "block": BasicBlock,
    "planes": [16, 32, 64],
    "layers": [3, 3, 3],
    "num_classes": 10,
}

resnet32 = {
    "block": BasicBlock,
    "planes": [16, 32, 64],
    "layers": [5, 5, 5],
    "num_classes": 10,
}

resnet44 = {
    "block": BasicBlock,
    "planes": [16, 32, 64],
    "layers": [7, 7, 7],
    "num_classes": 10,
}

resnet56 = {
    "block": BasicBlock,
    "planes": [16, 32, 64],
    "layers": [9, 9, 9],
    "num_classes": 10,
}

resnet110 = {
    "block": BasicBlock,
    "planes": [16, 32, 64],
    "layers": [18, 18, 18],
    "num_classes": 10,
}

resnet1202 = {
    "block": BasicBlock,
    "planes": [16, 32, 64],
    "layers": [200, 200, 200],
    "num_classes": 10,
}

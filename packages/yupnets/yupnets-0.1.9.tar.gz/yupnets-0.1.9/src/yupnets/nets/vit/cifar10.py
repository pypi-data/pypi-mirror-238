"""
Parameters are referred to from [1].

[1] Vision Transformer for Small-Size Datasets (https://arxiv.org/abs/2112.13492)
"""
__all__ = [
    "vit_b_4",
    "vit_b_8",
    "vit_l_4",
    "vit_l_8",
]

image_size = 32

vit_b_4 = {
    "image_size": image_size,
    "patch_size": 4,
    "num_layers": 12,
    "num_heads": 12,
    "hidden_dim": 192,
    "mlp_dim": 384,
    "num_classes": 10,
}

vit_b_8 = {
    "image_size": image_size,
    "patch_size": 8,
    "num_layers": 12,
    "num_heads": 12,
    "hidden_dim": 192,
    "mlp_dim": 384,
    "num_classes": 10,
}

vit_l_4 = {
    "image_size": image_size,
    "patch_size": 4,
    "num_layers": 24,
    "num_heads": 16,
    "hidden_dim": 256,
    "mlp_dim": 512,
    "num_classes": 10,
}

vit_l_8 = {
    "image_size": image_size,
    "patch_size": 8,
    "num_layers": 24,
    "num_heads": 16,
    "hidden_dim": 256,
    "mlp_dim": 512,
    "num_classes": 10,
}

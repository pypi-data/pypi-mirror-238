__all__ = [
    "vit_b_16",
    "vit_b_32",
    "vit_l_16",
    "vit_l_32",
    "vit_h_14",
]

image_size = 224

vit_b_16 = {
    "image_size": image_size,
    "patch_size": 16,
    "num_layers": 12,
    "num_heads": 12,
    "hidden_dim": 768,
    "mlp_dim": 3072,
    "num_classes": 1000,
}

vit_b_32 = {
    "image_size": image_size,
    "patch_size": 32,
    "num_layers": 12,
    "num_heads": 12,
    "hidden_dim": 768,
    "mlp_dim": 3072,
    "num_classes": 1000,
}

vit_l_16 = {
    "image_size": image_size,
    "patch_size": 16,
    "num_layers": 24,
    "num_heads": 16,
    "hidden_dim": 1024,
    "mlp_dim": 4096,
    "num_classes": 1000,
}

vit_l_32 = {
    "image_size": image_size,
    "patch_size": 32,
    "num_layers": 24,
    "num_heads": 16,
    "hidden_dim": 1024,
    "mlp_dim": 4096,
    "num_classes": 1000,
}

vit_h_14 = {
    "image_size": image_size,
    "patch_size": 14,
    "num_layers": 32,
    "num_heads": 16,
    "hidden_dim": 1280,
    "mlp_dim": 5120,
    "num_classes": 1000,
}

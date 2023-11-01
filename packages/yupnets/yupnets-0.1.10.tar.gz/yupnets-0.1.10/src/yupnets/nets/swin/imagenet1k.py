from .utils import \
    SwinTransformerBlock, PatchMerging, \
    SwinTransformerBlockV2, PatchMergingV2

__all__ = [
    "swin_t",
    "swin_s",
    "swin_b",

    "swin_v2_t",
    "swin_v2_s",
    "swin_v2_b",
]

image_size = 224

swin_t = {
    "patch_size": [4, 4],
    "embed_dim": 96,
    "depths": [2, 2, 6, 2],
    "num_heads": [3, 6, 12, 24],
    "window_size": [7, 7],
    "stochastic_depth_prob": 0.2,
    "block": SwinTransformerBlock,
    "downsample_layer": PatchMerging,
    "num_classes": 1000,
}

swin_s = {
    "patch_size": [4, 4],
    "embed_dim": 96,
    "depths": [2, 2, 18, 2],
    "num_heads": [3, 6, 12, 24],
    "window_size": [7, 7],
    "stochastic_depth_prob": 0.3,
    "block": SwinTransformerBlock,
    "downsample_layer": PatchMerging,
    "num_classes": 1000,
}

swin_b = {
    "patch_size": [4, 4],
    "embed_dim": 128,
    "depths": [2, 2, 18, 2],
    "num_heads": [4, 8, 16, 32],
    "window_size": [7, 7],
    "stochastic_depth_prob": 0.5,
    "block": SwinTransformerBlock,
    "downsample_layer": PatchMerging,
    "num_classes": 1000,
}

swin_v2_t = {
    "patch_size": [4, 4],
    "embed_dim": 96,
    "depths": [2, 2, 6, 2],
    "num_heads": [3, 6, 12, 24],
    "window_size": [8, 8],
    "stochastic_depth_prob": 0.2,
    "block": SwinTransformerBlockV2,
    "downsample_layer": PatchMergingV2,
    "num_classes": 1000,
}

swin_v2_s = {
    "patch_size": [4, 4],
    "embed_dim": 96,
    "depths": [2, 2, 18, 2],
    "num_heads": [3, 6, 12, 24],
    "window_size": [8, 8],
    "stochastic_depth_prob": 0.3,
    "block": SwinTransformerBlockV2,
    "downsample_layer": PatchMergingV2,
    "num_classes": 1000,
}

swin_v2_b = {
    "patch_size": [4, 4],
    "embed_dim": 128,
    "depths": [2, 2, 18, 2],
    "num_heads": [4, 8, 16, 32],
    "window_size": [8, 8],
    "stochastic_depth_prob": 0.5,
    "block": SwinTransformerBlockV2,
    "downsample_layer": PatchMergingV2,
    "num_classes": 1000,
}

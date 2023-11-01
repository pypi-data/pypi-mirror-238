from typing import Any, List

import torch

__all__ = [
    "get_layer_ids",
    "get_layer",
]


def get_attr(
        obj: Any,
        attrs: str,
) -> Any:
    for attr in attrs.split("."):
        try:
            obj = getattr(obj, attr)

        except AttributeError:
            raise

    return obj


def is_attention_layer(
        layer_id: str,
) -> bool:
    # ViT
    if "self_attention" in layer_id:
        return True

    # Swin
    elif "attn" in layer_id:
        return True

    else:
        return False


def get_layer_ids(
        model: torch.nn.Module,
) -> List[str]:
    names = [name for name, _ in model.named_modules() if len(name)]

    layer_ids = []

    for i in range(len(names) - 1):
        if is_attention_layer(names[i]):
            layer_ids.append(names[i])
            continue

        if names[i] in names[i + 1]:
            continue

        else:
            layer_ids.append(names[i])

    layer_ids.append(names[-1])

    return layer_ids


def get_layer(
        model: torch.nn.Module,
        layer_id: str,
) -> torch.nn.Module:
    return get_attr(model, layer_id)

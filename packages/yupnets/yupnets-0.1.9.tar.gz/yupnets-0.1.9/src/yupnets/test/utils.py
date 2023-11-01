from typing import Optional

__all__ = [
    "_desc",
]


def _desc(
        default_desc: str,
        model: Optional = None,
        dataset: Optional = None,
) -> str:
    desc = default_desc

    if hasattr(model, "name"):
        desc += f" of {model.name}"
    if hasattr(dataset, "name"):
        desc += f" on {dataset.name}"

    return desc

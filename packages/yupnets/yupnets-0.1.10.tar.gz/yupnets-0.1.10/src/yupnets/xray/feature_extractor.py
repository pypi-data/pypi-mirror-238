from typing import Callable, Dict, Union

import torch

__all__ = [
    "FeatureExtractor",
]


class FeatureExtractor(torch.nn.Module):
    def __init__(
            self,
            model: torch.nn.Module,
            penultimate_only: bool = False,
            use_cuda: bool = False,
    ) -> None:
        from .utils import get_layer_ids, get_layer
        super().__init__()

        self.model = model
        self.penultimate_only = penultimate_only
        self.use_cuda = use_cuda
        self.machine = "cuda" if use_cuda else "cpu"

        layer_ids = get_layer_ids(model)
        self.features = dict()

        self.hooks = []

        for layer_id in layer_ids:
            layer = get_layer(model, layer_id)
            layer_kind = layer.__class__.__name__

            self.hooks.append(
                layer.register_forward_hook(self.save_outputs_hook(layer_id, layer_kind))
            )

    def save_outputs_hook(
            self,
            layer_id: str,
            layer_kind: str,
    ) -> Callable:
        def fn(_, __, output):
            layer_key = f"{len(self.features)}-{layer_kind}-{layer_id}"

            if isinstance(output, tuple):
                output = [out for out in output if out is not None]
                output = torch.cat(output, dim=0)

            self.features[layer_key] = output.detach().cpu()

        return fn

    def forward(
            self,
            x: torch.Tensor,
    ) -> Union[Dict[str, torch.Tensor], torch.Tensor]:
        self.model = getattr(self.model, "cuda" if self.use_cuda else "cpu")()
        _ = self.model(x.to(self.machine))

        for hook in self.hooks:
            hook.remove()

        features = self.features

        if self.penultimate_only:
            penultimate_layer_id = list(features.keys())[-2]
            features = features[penultimate_layer_id]

        if self.use_cuda:
            torch.cuda.empty_cache()

        self.reset()

        return features

    def reset(self) -> None:
        self.__init__(
            model=self.model,
            penultimate_only=self.penultimate_only,
            use_cuda=self.use_cuda,
        )

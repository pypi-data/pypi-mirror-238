from typing import Any, Callable, Dict, List, Optional, Union

from collections import defaultdict
import torch
import tqdm

__all__ = [
    "BatchManager",
]


def merge_tensor(
        list_of_tensor: List[torch.Tensor],
) -> torch.Tensor:
    return torch.cat(list_of_tensor, dim=0)


def merge_dict(
        list_of_dict: List[Dict[Any, torch.Tensor]],
) -> Dict[Any, torch.Tensor]:
    merged_dict = defaultdict(list)

    for d in list_of_dict:  # you can list as many input dicts as you want here
        for key, value in d.items():
            merged_dict[key].append(value)

    for key, value in merged_dict.items():
        merged_dict[key] = torch.cat(value, dim=0)

    return merged_dict


def merge(batches: List, ):
    if list(set(batches)) == [None]:
        return None

    elif isinstance(batches[0], torch.Tensor):
        return merge_tensor(batches)

    elif isinstance(batches[0], Dict):
        return merge_dict(batches)

    else:
        raise ValueError(f"Unexpected type in batch: {type(batches[0])}")


class BatchManager:
    def __init__(
            self,
            func: Callable,
            batch_size: Optional[int] = None,
            verbose: bool = False,
    ) -> None:
        self.func = func
        self.batch_size = batch_size
        self.verbose = verbose

    def __call__(
            self,
            data: torch.Tensor,
    ) -> Union[
        None,
        torch.Tensor,
        Dict[Any, torch.Tensor],
    ]:
        if self.batch_size is None:
            return self.func(data)

        else:
            batches = self.split(data)

            res = []

            for batch in tqdm.tqdm(batches, disable=not self.verbose):
                res_batch = self.func(batch)
                res.append(res_batch)

            res = merge(res)

            return res

    def split(
            self,
            data: torch.Tensor,
    ) -> List[torch.Tensor]:
        batches = data.split(self.batch_size, dim=0)

        return batches

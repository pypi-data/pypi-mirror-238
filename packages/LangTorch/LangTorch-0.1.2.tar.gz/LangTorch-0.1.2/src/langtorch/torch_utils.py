from typing import Optional, Union, List, Tuple, Sequence

import torch
from torch.types import _TensorOrTensors, _size

_OptionalTensor = Optional[torch.Tensor]


def tensor_or_tensors_to_tuple(tensors: Optional[_TensorOrTensors], length: int) -> Tuple[_OptionalTensor, ...]:
    if tensors is None:
        return (None,) * length
    if isinstance(tensors, torch.Tensor):
        return (tensors,)
    return tuple(tensors)

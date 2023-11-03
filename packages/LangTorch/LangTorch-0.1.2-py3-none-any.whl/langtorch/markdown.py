from typing import Optional, Union, List, Tuple, Sequence

import langtorch.autograd
import langtorch.torch_utils
import langtorch.utils
import numpy as np
import torch
import torch.nn.functional as F
from langtorch.operations import *
from langtorch.api.call import get_embedding, chat, auth
from torch import Tensor
from torch.types import _TensorOrTensors, _size

from .tt import TextTensor, TextModule


class ExtendedTextTensor(TextTensor):
    def __new__(cls, content="", embedding: Optional[Union[torch.Tensor, List[float], np.ndarray]] = None,
                is_gradient: bool = False,
                is_param=True, metadata=None, dtype="<U", **kwargs):
        instance = super().__new__(cls, content, embedding, is_gradient, is_param, metadata, dtype, **kwargs)
        # add new attributes or alter existing ones here if needed
        return instance

    def new_method(self):
        # add new methods if needed
        return "This is a new method in ExtendedTextTensor"

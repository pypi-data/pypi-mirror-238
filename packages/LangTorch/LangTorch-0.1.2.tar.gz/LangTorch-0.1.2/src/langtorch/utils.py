from queue import Queue
from threading import Lock, Thread
from typing import Optional, Union, List, Tuple, Sequence

import numpy as np
import torch
from .torch_utils import _OptionalTensor
import langtorch
from torch.types import _TensorOrTensors, _size
import logging

def iter_subarrays(arr, dim):
    # Check that dim is a valid dimension
    if dim < 0: dim = dim + len(arr.shape)
    if dim >= len(arr.shape):
        raise ValueError(f"dim must be between -{len(arr.shape)} and {len(arr.shape) - 1}")

    # Split the array along the dim dimension
    subarrays = np.array_split(arr, arr.shape[dim], axis=dim)

    # Return an iterator over the subarrays
    return iter(subarrays)


def zeros_like(other, **kwargs):
    return langtorch.TextTensor(np.char.array(torch.zeros(other.shape), unicode=True).join("").astype(dtype="<U"), **kwargs)


def str_like(other, string, **kwargs):
    return langtorch.TextTensor(np.char.array(torch.zeros(other.shape), unicode=True).join("").astype(dtype="<U"), **kwargs) + TextTensor(string, **kwargs)


def zeros(*shape, **kwargs):
    return langtorch. TextTensor(np.char.array(torch.zeros(*shape), unicode=True).join("").astype(dtype="<U"), **kwargs)


def tensor_or_tensors_to_tuple(tensors: Optional[_TensorOrTensors], length: int) -> Tuple[_OptionalTensor, ...]:
    if tensors is None:
        return (None,) * length
    if isinstance(tensors, torch.Tensor):
        return (tensors,)
    return tuple(tensors)



def _calculate_shape(output: torch.Tensor, grad: torch.Tensor,
                     is_grads_batched: bool):
    # is_same_size ensures that both tensors are either nested or non nested
    if output.is_nested:
        if is_grads_batched:
            raise RuntimeError("Batched grads are not supported with Nested Tensor.")
        out_shape = output._nested_tensor_size()
        grad_shape = grad._nested_tensor_size()

        return out_shape, grad_shape

    reg_out_shape = output.shape
    reg_grad_shape = grad.shape if not is_grads_batched else grad.shape[1:]
    return reg_out_shape, reg_grad_shape


def make_grads(outputs: Sequence[torch.Tensor], grads: Sequence[_OptionalTensor],
               is_grads_batched: bool) -> Tuple[_OptionalTensor, ...]:
    new_grads: List[_OptionalTensor] = []
    for out, grad in zip(outputs, grads):
        if isinstance(grad, torch.Tensor):
            first_grad = grad if not is_grads_batched else grad[0]
            if not torch.is_same_size(out, first_grad):
                out_shape, grad_shape = langtorch._calculate_shape(out, first_grad, is_grads_batched)
                if is_grads_batched:
                    raise RuntimeError("If `is_grads_batched=True`, we interpret the first "
                                       "dimension of each grad_output as the batch dimension. "
                                       "The sizes of the remaining dimensions are expected to match "
                                       "the shape of corresponding output, but a mismatch "
                                       "was detected: grad_output["
                                       + str(grads.index(grad)) + "] has a shape of "
                                       + str(grad_shape) + " and output["
                                       + str(outputs.index(out)) + "] has a shape of "
                                       + str(out_shape) + ". "
                                                          "If you only want some tensors in `grad_output` to be considered "
                                                          "batched, consider using vmap.")
                else:
                    raise RuntimeError("Mismatch in shape: grad_output["
                                       + str(grads.index(grad)) + "] has a shape of "
                                       + str(grad_shape) + " and output["
                                       + str(outputs.index(out)) + "] has a shape of "
                                       + str(out_shape) + ".")
            if out.dtype.is_complex != grad.dtype.is_complex:
                raise RuntimeError("For complex Tensors, both grad_output and output"
                                   " are required to have the same dtype."
                                   " Mismatch in dtype: grad_output["
                                   + str(grads.index(grad)) + "] has a dtype of "
                                   + str(grad.dtype) + " and output["
                                   + str(outputs.index(out)) + "] has a dtype of "
                                   + str(out.dtype) + ".")
            new_grads.append(grad)
        elif grad is None:
            if out.requires_grad:
                if out.numel() != 1:
                    raise RuntimeError("grad can be implicitly created only for scalar outputs")
                new_grads.append(torch.ones_like(out, memory_format=torch.preserve_format))
            else:
                new_grads.append(None)
        else:
            raise TypeError("gradients can be either Tensors or None, but got " +
                            type(grad).__name__)
    return tuple(new_grads)

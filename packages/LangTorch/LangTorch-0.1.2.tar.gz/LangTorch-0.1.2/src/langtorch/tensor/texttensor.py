from typing import Optional, Union, List
from pyparsing import ParseException
import numpy as np
import csv
import torch
from ..text import Text
from ..utils import zeros_like
from ..api.call import get_embedding
from ..autograd import make_grads
import langtorch
from copy import deepcopy
from torch.types import _TensorOrTensors
from ..functional import AddTextTensor, MulTextTensor, PermuteTextTensor, FormatTextTensor, JoinTextTensor, \
    ReshapeTextTensor, SplitTextTensor


# Metaclass to combine _TensorMeta and the instance check override for Parameter.
class _ParameterMeta(torch._C._TensorMeta):
    # Make `isinstance(t, Parameter)` return True for custom tensor instances that have the _is_param flag.
    def __instancecheck__(self, instance):
        return super().__instancecheck__(instance) or (
                isinstance(instance, torch.Tensor) and getattr(instance, '_is_param', False))


def chararray_to_TextArray(arr, text_class = Text, shape=None, **kwargs):
    if isinstance(arr, np.ndarray):
        try:
            if all([isinstance(a, text_class) for a in arr.flat]):
                return arr
        except:
            pass

    arr = np.array(arr, dtype=object)
    text_arr = [text_class(a, **kwargs) for a in arr.flat]
    text_arr = np.array(text_arr, dtype=object).reshape(arr.shape if shape is None else shape)
    return text_arr


class TextTensor(torch.Tensor, metaclass=_ParameterMeta):
    text_class = Text # The class of a Tensor entry, replaced in subclasses. May in the future move this logic to the metaclass
    _embedding_module = None # TextTensor to Tensor with an embedding model
    _tokenizer = None  # TextTensor to Tensor with a transformer tokenizer

    @classmethod
    def input_formatter(cls, content):
        # Default implementation, to be overridden by subclasses if needed
        return content

    @classmethod
    def linter(cls, tensor):
        # Default implementation, ensures correct class of Tensor content entries
        tensor.content = chararray_to_TextArray(tensor.content, cls.text_class)
        return tensor

    @classmethod
    def _str_formatter(cls, instance):
        if len(instance.shape) == 0:
            return str(instance.item())
        string = str(np.array(instance.content, dtype=np.unicode_)).replace("\\n","\n")
        return f'{cls.__name__}({string}, requires_grad = {instance.requires_grad})'  # {super().__repr__().replace("TextTensor(","")}'

    def __new__(cls, content="", embedding: Optional[Union[torch.Tensor, List[float], np.ndarray, bool]] = None,
                metadata=None, requires_grad: bool =True, is_gradient: bool = False, is_param=True, parse = True, **kwargs):
        if metadata is None:
            metadata = dict()
        for attr in ["content", "embedding"]:
            if not attr in metadata:
                metadata[attr] = eval(attr)

        # Set content to be an object array with cls.text_class entries
        metadata["content"] = cls.to_array(metadata["content"], parse=parse)
        # Apply input formatter
        metadata["content"] = cls.input_formatter(metadata["content"])
        if embedding == True:
            metadata["embedding"] = get_embedding([str(m) for m in metadata["content"].flat])["embedding"].to_list()

        tensor = super().__new__(cls, torch.arange(metadata["content"].size, dtype=torch.float32).reshape(
            metadata["content"].shape), **kwargs)

        tensor.metadata = metadata
        tensor._is_param = is_param
        tensor._is_gradient = is_gradient
        tensor.requires_grad = requires_grad
        assert tensor._content is not None

        # Apply linter
        tensor = cls.linter(tensor)
        return tensor

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def to_array(cls, input, **kwargs):
        return input.content if isinstance(input, cls) \
            else np.array(input, dtype=object) if isinstance(input, Text) \
            else chararray_to_TextArray(input, cls.text_class, **kwargs)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = TextTensor.to_array(content)
        assert self._content is not None

    @property
    def embedding(self):
        if self._embedding is None and hasattr(self, 'metadata') and self.metadata is not None:
            print("Warning: autoembedding ON")
            self.embed()
        return self._embedding

    @embedding.setter
    def embedding(self, embedding: Union[torch.Tensor, List[float], np.ndarray, tuple]):
        if embedding is None:
            self._embedding = None
            return
        assert isinstance(embedding, torch.Tensor) or isinstance(embedding, np.ndarray) or isinstance(embedding, list)  or isinstance(embedding, list), "Value of embedding should be a Tensor, array or list"

        self._embedding = embedding if isinstance(embedding, torch.Tensor) else torch.tensor(embedding)
        try:
            self._embedding = self._embedding.reshape(*self.content.shape, -1)
        except ValueError:
            raise ValueError("The shape of the embedding does not match the size of the TextTensor")
        self._metadata["embedding"] = self._embedding

    @property
    def tokens(self):
        if not hasattr(self, "_tokens"):
            if self.tokenizer is not None:
                self._tokens = self.tokenizer(self)
            else:
                raise AttributeError("Tokens unavailable as no tokenizer has been set")
        return self._tokens

    input_ids = tokens

    @tokens.setter
    def tokens(self, tokens):
        self._tokens = tokens

    @property
    def tokenizer(self):
        return self._tokenizer


    @tokenizer.setter
    def tokenizer(self, tokenizer):
        if isinstance(tokenizer, str):
            from transformers import AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self._tokenizer = tokenizer

    def tokenize(self, tokenizer = None):
        if tokenizer is not None:
            self.tokenizer = tokenizer
        assert self.tokenizer is not None
        input_dict = tokenizer.toke



    @classmethod
    def from_df(cls, df: 'DataFrame', **kwargs) -> 'TextTensor':
        text_list = []
        if not "parse" in kwargs:
            kwargs["parse"] = False

        for row in df.values:
            # Create a Text object with (column_name, value) pairs
            text_content = [(col_name, str(value)) for col_name, value in zip(df.columns, row) if value != np.nan and str(value)!=""]
            text_obj = Text(*text_content, **kwargs)
            text_list.append(text_obj)

        # Convert the list of Text objects to a TextTensor of shape (n, 1)
        text_tensor = cls(text_list, **kwargs).reshape(-1, 1)

        return text_tensor

    def set_key(self, keys, inplace = False):
        reshaped_keys = zeros_like(self.content) + keys
        if inplace:
            result = self
        else:
            result = self.copy()

        # Apply set_key to each entry
        for index, text_entry in np.ndenumerate(result.content):
            result.content[index] = text_entry.set_key(reshaped_keys[index].item())

        return result

    def set_key_(self, keys):
        return self.set_key(keys, inplace = True)

    def add_key(self, keys):
        return self

    def copy(self):
        new_dict = deepcopy(self.metadata)
        return self.__class__(metadata = new_dict, parse = False)


    def apply(self, func):
        """Applies a function: Text -> Text to each entry of self.content"""
        # Ensure the function is callable
        if not callable(func):
            raise ValueError("Provided function is not callable.")

        # Apply the function to each entry
        for index, text_entry in np.ndenumerate(self.content):
            self.content[index] = func(text_entry)

        return self

    def inv(self):
        # Apply inverse operation on each element of the char array
        self.content = np.vectorize(lambda x: x.inv())(self.content)

    @property
    def metadata(self):
        return self._metadata


    @metadata.setter
    def metadata(self, metadata):
        if not hasattr(self, "_metadata"): self._metadata = {}
        # set core attributes
        for attr in ["content", "embedding"]:
            if attr in metadata:
                setattr(self, attr, metadata.pop(attr))

        for attr in ["content", "embedding"]:
            metadata[attr] = getattr(self, "_"+attr)

        self._metadata = metadata

    def metadata_index(self, index):
        """Pick out entries of metadata with the provided index. Usually used to transfer metadata to a sub-tensor."""

        def positive_indices(indices, shape):
            """Change negative to positive indices, e.g. -1 to len(self)-1"""
            if indices == tuple(): return tuple()
            if shape == tuple():
                raise RuntimeError(f"TextTensor is 0-dimensional. It cannot be accessed with {indices}. Use .item() instead")

            if not isinstance(indices, tuple):
                indices = (indices,)
                shape = (shape,)

            result = []
            for index, size in zip(indices, shape):
                if isinstance(index, slice):
                    start = index.start if index.start is None or index.start >= 0 else index.start + size
                    stop = index.stop if index.stop is None or index.stop >= 0 else index.stop + size
                    result.append(slice(start, stop, index.step))
                elif isinstance(index, int):
                    result.append(index if index >= 0 else index + size)
                else:
                    # Pass through for any other index types
                    result.append(index)
            return tuple(result)

        index = positive_indices(index, self.content.shape)
        index = index[0] if len(index) == 1 else index

        if len(self.content.shape) == 0: # and (index == slice(None, None, None))
            return self.metadata_apply(lambda v: v, lambda v: v, lambda v: v)

        else:
            return self.metadata_apply(lambda v: v[index], lambda v: v[index], lambda v: v)

    def metadata_apply(self, f_tensor=None, f_embedding=None, f_scalar=None, *args, **kwargs):
        """
        Apply a specified function to a copy of metadata elements of the TextTensor.

        Parameters:
        - f_tensor (function, optional): Function to be applied to tensor-shaped metadata attributes.
        - f_embedding (function, optional): Function to be applied to the 'embedding' attribute.
        - f_scalar (function, optional): Function to be applied to scalar metadata attributes.
        - *args: Variable length argument list to be passed to the functions.
        - **kwargs: Arbitrary keyword arguments to be passed to the functions.

        Returns:
        - dict: A dictionary with updated metadata attributes.
        """
        tensor_attributes, scalar_attributes = [], []
        for k, v in self._metadata.items():
            try:
                if tuple(v.shape) == tuple(self.shape):
                    tensor_attributes.append(k)
            except AttributeError:
                if k != "embedding":
                    scalar_attributes.append(k)

        metadata = self._metadata.copy()

        if f_tensor:
            for k in tensor_attributes:
                metadata[k] = f_tensor(metadata[k], *args, **kwargs)

        if f_embedding and metadata["embedding"]:
            metadata["embedding"] = f_embedding(metadata["embedding"], *args, **kwargs)

        if f_scalar:
            for k in scalar_attributes:
                metadata[k] = f_scalar(metadata[k], *args, **kwargs)

        return metadata

    def __repr__(self):
        return str(self.sum().content)

    def __str__(self):
        return self._str_formatter(self)

    def inspect(self):
        details = np.vectorize(lambda x: x.inspect())(self.content)
        return details

    def __eq__(self, other):
        return self.content == other.content if isinstance(other, TextTensor) else self.content == other

    def sum(self, dim=None):
        if len(self.shape) == 0:
            return self
        if dim is None:
            result = self
            connecting_char = [" "] + ["\n" * (i + 1) for i in range(len(self.content.shape) - 1)]
            for i, char in enumerate(connecting_char):
                result = result.join_on(char, dim=-1)
            assert len(result.shape) <= 1
        else:
            result = self.join_on("", dim=dim)
        return result

    def join_on(self, on=" ", dim=None):
        # TODO make this output Text objects
        return JoinTextTensor.apply(self, on, dim)

    def format(self, **kwargs):
        """
        Return a formatted version of self, using substitutions from kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        return FormatTextTensor.apply(self, kwargs)

    def to_list(self):
        return [TextTensor(m) for m in self.content.flat]

    def __pow__(self, power):
        if power == -1:
            self_copy = self.copy()
            self_copy.inv()
        else:
            raise ValueError("Only power of -1 is supported for inversion.")
        return self_copy


    def add__(self, other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other, parse = False) # TODO Parsing rules
            except ParseException:
                other = TextTensor(other, parse = False)
        result = self.__class__(self.content + other.content, parse = False)
        return result

    def mul__(self, other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other, parse = False) # TODO parsing rules
            except ParseException:
                other = TextTensor(other, parse = False)
        result = self.__class__(self.content * other.content, parse = False)
        return result

    def __add__(self,other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other, parse = False) # TODO parsing rules
            except ParseException:
                other = TextTensor(other, parse = False)
        return AddTextTensor.apply(self, other)

    def __mul__(self,other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other, parse = False) # TODO parsing rules
            except ParseException:
                other = TextTensor(other, parse = False)
        return MulTextTensor.apply(self, other)

    def __matmul__(self, other):
        if isinstance(other, str) or isinstance(other, np.ndarray):
            try:
                other = TextTensor(other) #To parse or not to parse?
            except ParseException:
                other = TextTensor(other, parse = False)
        result = self.__class__(self.content @ other.content, parse = False)
        return result

    def item(self):
        return next(self.content.flat)

    def items(self):
        """Get (key, value) pairs from all Text entries in tensor"""
        return np.array([{"items": tuple(t.items())} for t in self.content.flat], dtype = object).reshape(self.content.shape)

    def __getattr__(self, name):
        try:
            metadata = object.__getattribute__(self, "_metadata")
        except AttributeError:
            raise AttributeError("'TextTensor' object has no attribute 'metadata'. TextTensor was probably initialised outside of langtorch, e.g. when passing TextTensor to a torch function that expects torch.Tensor")
        if name in ["_content", "content"] or name in metadata:
            if name in metadata:
                return metadata[name]
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                return None
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            # Query np.ndarray attrs
            try:
                assert self.content is not None
                return getattr(self._content, name)
            except AttributeError:
                # Query Text attrs

                try:
                    attr = np.array(np.vectorize(lambda obj: getattr(obj, name))(self._content), dtype=object)
                    if callable(attr.flat[0]):
                        return lambda: np.vectorize(lambda x: x())(attr)
                    else:
                        return attr
                except:
                    raise AttributeError(f"Object {self}, Neither TextTensor nor Text has attribute '{name}'")

    def __getitem__(self, index):
        return self.__class__(metadata=self.metadata_index(index), parse = False)

    def __iter__(self):
        """ For unpacking using ** into transformer models"""
        yield 'input_ids', self.input_ids
        yield 'attention_mask', self.attention_mask
        if self.token_type_ids is not None:
            yield 'token_type_ids', self.token_type_ids

    def __contains__(self, item):
        return item in self.content

    @property
    def TT(self):
        from .tt import TextModule
        return TextModule(self.mT)

    @property
    def T(self):  # diff!
        return self.__class__(self.content.T, super().mT, parse = False)

    @property
    def mT(self):  # diff!
        return self.__class__(self.content.T, super().mT, parse = False)

    def embed(self, verbose = False):
        self.embedding = get_embedding([str(m) for m in self.content.flat], verbose = verbose)["embedding"].to_list()

    def apply(self, func):
        """Applies a function to each entry of self.content."""
        # Ensure the function is callable
        if not callable(func):
            raise ValueError("Provided function is not callable.")

        # Apply the function to each entry
        for index, text_entry in np.ndenumerate(self.content):
            self.content[index] = func(text_entry)

        return self

    def reshape(self, *shape):
        return ReshapeTextTensor.apply(self, shape)[0]

    def usqueeze(tensor, dim=0):
        return tensor.reshape(tensor.shape[:dim] + [1] + tensor.shape[dim:])

    def squeeze(tensor, dim=None):
        if dim is None:
            # Remove all dimensions of size 1
            return tensor.view([dim for dim in tensor.shape if dim != 1])
        else:
            # Remove only the specified dimension if it is of size 1
            if tensor.shape[dim] == 1:
                return tensor.view(tensor.shape[:dim] + tensor.shape[dim + 1:])
            else:
                return tensor

    def expand(tensor, *sizes):
        # Check if the number of dimensions of the tensor is less than the length of the target sizes
        if tensor.dim() < len(sizes):
            # Add singleton dimensions to the front of the tensor
            for _ in range(len(sizes) - tensor.dim()):
                tensor = tensor.unsqueeze(0)

        # Prepare a list to hold the expanded sizes
        expanded_sizes = []

        # Loop over the target sizes from last to first
        for tensor_size, target_size in zip(reversed(tensor.shape), reversed(sizes)):
            if tensor_size == 1:
                # If the size of the tensor in this dimension is 1, it can be expanded
                expanded_sizes.append(target_size)
            elif tensor_size != target_size:
                # If the size of the tensor in this dimension is not equal to the target size,
                # and is not 1, it cannot be expanded
                raise ValueError(f"size mismatch for dimension {len(expanded_sizes)}, {tensor_size} != {target_size}")
            else:
                # If the size of the tensor in this dimension is equal to the target size,
                # it doesn't need to be expanded
                expanded_sizes.append(tensor_size)

        # Reverse the list of expanded sizes to match the original order of dimensions
        expanded_sizes = list(reversed(expanded_sizes))

        # Use the repeat method to create a new tensor that repeats the original tensor along each dimension
        return tensor.repeat(*expanded_sizes)

    def swapaxes(self, axis1: int, axis2: int):
        # Create a list of axes in order
        axes = list(range(len(self.shape)))
        # Swap the specified axes
        axes[axis1], axes[axis2] = axes[axis2], axes[axis1]
        # Return the tensor with axes swapped
        return self.permute(axes)

    def permute(self, axes):
        return PermuteTextTensor.apply(self, axes)

    def view(self, *shape):
        return self.__class__(
            metadata=self.metadata_apply(lambda v: v.reshape(*shape), lambda v: v.reshape(*shape, v.shape[-1])),
            parse = False)

    def repeat(tensor, *sizes):
        # Ensure the number of dimensions of tensor and sizes match
        if len(tensor.shape) != len(sizes):
            raise ValueError("Number of dimensions of tensor and sizes must match")

        # Manually create a repeated tensor
        content = tensor.content
        for dim, size in enumerate(sizes):
            slices = [content] * size
            content = np.concatenate(slices, axis=dim)
        tensor = tensor.__class__(content, parse = False)
        return tensor

    def split(self, sep):
        """
        Return a new TextModule, with an additional first dimension to split everything using sep as the delimiter.

          sep
            The delimiter according which to split the bytearray.
            None (the default value) means split on ASCII whitespace characters
            (space, tab, return, newline, formfeed, vertical tab).
        """
        return SplitTextTensor.apply(self, sep)

    def format(self, **kwargs):
        """
        Return a formatted version of self, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        return FormatTextTensor.apply(self, kwargs)

    def save(self, filename, sep=','):
        """Save content to a CSV file using the csv module.

        Args:
            filename (str): The name of the CSV file.
            content (list of list of str): The content to be written to the CSV file.
            sep (str, optional): The field separator for the CSV. Defaults to ','.
        """
        with open(filename, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=sep)
            csv_writer.writerows([[str(mm) for mm in m] for m in self._content])

    def to_csv(self, filename, sep="\t"):
        """
        Save a csv with text or, if available, with embeddings (flattened shape)
        """
        if self._embedding is None:
            self.save(filename, sep=sep)  # Tab as default, because texts have a lot of commas
        else:
            try:
                with open(filename, 'w', newline='') as f:
                    for row in self._content:
                        # Join the elements in the row with commas
                        line = sep.join(row)
                        # Write the line to the file
                        f.write(line + '\n')
            except Exception as E:
                raise Exception(f"Failed to save with embeddings, {E}")

    def backward(
            tensors: _TensorOrTensors,
            grad_tensors: Optional[_TensorOrTensors] = None,
            retain_graph: Optional[bool] = None,
            create_graph: bool = False,
            grad_variables: Optional[_TensorOrTensors] = None,
            inputs: Optional[_TensorOrTensors] = None,
    ) -> None:
        r"""See. docs"""
        if torch._C._are_functorch_transforms_active():
            raise RuntimeError(
                "backward() called inside a functorch transform. This is not "
                "supported, please use functorch.grad or functorch.vjp instead "
                "or call backward() outside of functorch transforms.")

        if grad_variables is not None:
            if grad_tensors is None:
                grad_tensors = grad_variables
            else:
                raise RuntimeError("'grad_tensors' and 'grad_variables' (deprecated) "
                                   "arguments both passed to backward(). Please only "
                                   "use 'grad_tensors'.")
        if inputs is not None and len(inputs) == 0:
            raise RuntimeError("'inputs' argument to backward() cannot be empty.")

        if grad_tensors is None:
            grad_tensors = zeros_like(tensors).reshape(tensors.shape)
        elif isinstance(grad_tensors, str):
            grad_tensors = (TextTensor(grad_tensors),)

        tensors = (tensors,) if isinstance(tensors, torch.Tensor) else tuple(tensors)
        inputs = (inputs,) if isinstance(inputs, torch.Tensor) else \
            tuple(inputs) if inputs is not None else tuple()
        grad_tensors_ = langtorch.torch_utils.tensor_or_tensors_to_tuple(grad_tensors, len(tensors))
        grad_tensors_ = make_grads(tensors, grad_tensors_, is_grads_batched=False)
        if retain_graph is None:
            retain_graph = create_graph

        # The reason we repeat same the comment below is that
        # some Python versions print out the first line of a multi-line function
        # calls in the traceback and some print out the last line
        langtorch.autograd.run_backward(  # langtorch version of a C++ engine that torch uses to run the backward pass
            tensors, grad_tensors_, retain_graph, create_graph, inputs,
            allow_unreachable=True,
            accumulate_grad=True)  # langtorch version of a C++ engine that torch uses to run the backward pass


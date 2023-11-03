import time
from typing import Optional, Union, List
from ...tensor import TextTensor
import langtorch.torch_utils
import langtorch.utils
from langtorch.utils import iter_subarrays
import torch
from .embedding import get_embedding

class TextModule(torch.nn.Module):
    tensor_class = TextTensor
    def __init__(self,
                 content: Optional[Union[str, 'TextTensor']] = "",
                 activation=lambda x: x,
                 key=None,
                 memoize=False, *args, **kwargs):
        super(TextModule, self).__init__(*args, **kwargs)
        self._content = TextTensor(content) if not isinstance(content, TextTensor) else content
        self.activation = activation  # An identity function if nothing is passed
        self.memo = {} if memoize else None
        self.target_embedding = None
        self.key = key
        self.register_forward_pre_hook(self.pre_forward_hook)
        self.register_forward_hook(self.post_forward_hook)

    @staticmethod
    def pre_forward_hook(module, input: List[TextTensor]):
        for tensor in input:
            assert isinstance(tensor, module.tensor_class)


    @staticmethod
    def post_forward_hook(module, input, output):
        module.reset_formatting()
        if module.key is not None:
            if isinstance(output,TextTensor):
                print(f"Could not set key '{module.key}', Module output is not a TextTensor")
            else:
                output.set_key_(module.key)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content.content if isinstance(content, TextModule) else content if isinstance(content, TextTensor) else TextTensor(content)
        assert self._content is not None
        self.unformatted_content = TextTensor(self._content.content)

    def forward(self, *input) -> TextTensor:
        if self.memo is None:
            return self._forward(*input)
        # Memoization
        input_tuple = langtorch.tensor_or_tensors_to_tuple(input)
        if input_tuple in self.memo:
            return self.memo[input_tuple]

        output = self._forward(*input)
        self.memo[input_tuple] = output
        return output

    def _forward(self, input) -> TextTensor:
        return self.activation(self.content * input)

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content)

    def __contains__(self, item):
        return item in self.content

    def embed(self):
        self.embedding = get_embedding(self.content)

from typing import Optional, Union, List
from ...tensor import TextTensor, ChatTensor
import langtorch.utils
import torch
from .module import TextModule


class ChatModule(TextModule):
    tensor_class = ChatTensor
    def __init__(self, content = "", activation=lambda x:x, key="assistant", keep_history = True):
        super().__init__(content, activation, key)
        self.content = ChatTensor(self.content)
        if keep_history:
            self.register_forward_hook(self.append_history)

    @staticmethod
    def append_history(module, input, output):
        output.set_key_(module.key)

from typing import Optional, Union, List
import numpy as np
import csv
import torch
from .embedding import get_embedding
from .text import Text


class Chat(Text):
    allowed_keys = ["user", "assistant"]
    @classmethod
    def _str_formatter(cls, instance):
        return "\n".join([f"{k}: {cls.concatenate_terminals(v)}" for k,v in instance.items()])


class ChatML(Chat):
    allowed_keys = ["user", "assistant", "system"]
    @classmethod
    def _str_formatter(cls, instance):
        if instance.keys()[-1] == "user":
            return "\n".join([f"<|im_start|>{k}\n{v}<|im_end|>" for k, v in instance.items()]) + "\n<|im_start|>assistant"
        else:
            return "\n".join([f"<|im_start|>{k}\n{v}<|im_end|>" for k, v in instance.items()])

class HumanMessage:
    def __new__(cls, content):
        from .texttensor import TextTensor, ChatTensor
        if isinstance(content, str):
            return Chat(content).set_key("user")
        elif isinstance(content, TextTensor):
            return ChatTensor(content, parse=False).set_key("user")
        else:
            raise ValueError("Content must be of type Text or str.")

class AIMessage:
    def __new__(cls, content):
        from .texttensor import TextTensor, ChatTensor
        if isinstance(content, str):
            return Chat(content).set_key("assistant")
        elif isinstance(content, TextTensor):
            return ChatTensor(content, parse=False).set_key("assistant")
        else:
            raise ValueError("Content must be of type Text or str.")


### MESSAGE ALIASES
User, Assistant = HumanMessage, AIMessage
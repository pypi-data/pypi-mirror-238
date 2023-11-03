from .texttensor import TextTensor
from ..text import Markdown
import torch
import multiprocessing
import numpy as np
import sys
import io
from .. utils import zeros_like

class MarkdownTensor(TextTensor):
    text_class = Markdown #replace parser


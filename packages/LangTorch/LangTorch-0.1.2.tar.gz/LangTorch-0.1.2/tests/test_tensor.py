import sys


sys.path.append("../src")
from langtorch import TextTensor, TextModule
from langtorch import get_session
import unittest
import numpy as np
import torch


class TestInit(unittest.TestCase):
    # def test_content_and_metadata(self):
    #     tensor = TextTensor("Testing embeddings").embed()
    #     self.assertTrue(isinstance(tensor.embedding, torch.Tensor))
    #     # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.


    def test_inv(self):
        pass

if __name__ == "__main__":
    unittest.main()

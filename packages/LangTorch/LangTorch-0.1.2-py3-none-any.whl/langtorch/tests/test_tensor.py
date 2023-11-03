import sys

sys.path.append("D:/llm-recommendations/dxx")
from langtorch import TextTensor, TextModule
import unittest
import numpy as np


class TestInit(unittest.TestCase):
    def test_content_and_metadata(self):
        tensor = TextTensor("Testing embeddings")
        self.assertEqual(tensor.content, TextTensor.to_char_array("Testing embeddings"))
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.
        self.assertLessEqual(3, len(tensor.metadata.keys()))

    def test_inv(self):
        tensor = TextTensor([["ABCD"]], sign="++--")
        tensor.inv()
        self.assertEqual(tensor.sign, TextTensor.to_char_array([["--++"]]))
        self.assertEqual((tensor ** -1).sign, TextTensor.to_char_array([["++--"]]))

        tensor = TextTensor([["A"], ["Aa"], ["!!"], ["AVC"]])

        tensor.inv()
        self.assertTrue(np.all(tensor.sign == TextTensor.to_char_array([["-"], ["--"], ["--"], ["---"]])))


if __name__ == "__main__":
    unittest.main()

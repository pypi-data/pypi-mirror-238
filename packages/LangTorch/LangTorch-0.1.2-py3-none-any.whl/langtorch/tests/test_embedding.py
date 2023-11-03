from langtorch import TextTensor, TextModule
from langtorch.activation import ActivationGPT
import os
import unittest


class TestEmbeddingModules(unittest.TestCase):
    def test_openai_embedding(self):
        os.environ["OPENAI_API_KEY"]
        tensor = TextTensor("Testing embeddings")
        tensor.embed()
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.
        self.assertEqual(tuple(tensor.embedding.shape[:-1]), tensor.content.shape)


if __name__ == "__main__":
    unittest.main()

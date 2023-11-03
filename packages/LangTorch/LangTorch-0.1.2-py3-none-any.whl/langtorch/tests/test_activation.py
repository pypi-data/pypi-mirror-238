import sys

sys.path.append("D:/langtorch/src")
from langtorch import TextTensor, TextModule
from langtorch.tt.activation import ActivationGPT
from langtorch.api.call import chat, auth
import unittest


class TestActivationModules(unittest.TestCase):

    def test_openai_activation(self):
        auth(key_path="D:/Techne/api_keys.json")
        tensor = TextTensor(["Testing answer yes if you hear me", "Testing answer yes if you hear me"])
        activation = ActivationGPT("Answer with 'yes'", model="gpt-3.5-turbo-0613", temperature=0.)
        module = TextModule("{input}. Say it two times", activation=activation)
        result = module(tensor)
        # Assert the expected result. Since I don't know the exact expected output, I'll just check if it contains "yes" twice as an example.
        self.assertEqual(result[0].lower().count("yes"), 2)


if __name__ == "__main__":
    unittest.main()

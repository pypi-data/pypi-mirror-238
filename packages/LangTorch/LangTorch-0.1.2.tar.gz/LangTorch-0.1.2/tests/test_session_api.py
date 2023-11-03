import unittest
import sys
sys.path.append("../src")

from langtorch.session import Session

import os
import asyncio
import random
from omegaconf import OmegaConf
from langtorch import TextTensor
from langtorch.api import auth
from langtorch.tt import ActivationGPT

import logging

logging.basicConfig(level=logging.DEBUG)


# class TestSessionAPI(unittest.TestCase):
#     def setUp(self):
#         # Create a sample config file for testing
#         self.config_path = "test_config.yaml"
#     def test_api_cache(self):
#         with Session(self.config_path) as session:
#             auth("D:/Techne/jutro_keys.json")
#             session.key1 = TextTensor(["test. Answer yes"]*3)
#             session.val1 = ActivationGPT()(session.key1)
#
#
#
#     # def tearDown(self):
#     #     # Cleanup: remove the test config file after each test
#     #     os.remove(self.config_path)
#
#
# if __name__ == '__main__':
#     unittest.main()


session = Session("test_config.yaml")
from langtorch import Text

# print(Text.from_messages(*session.get_responses("openai","chat")[0][0][0]["messages"]))
# print(Text.from_messages(*session.get_responses("openai","chat")[1][0][0]["messages"]))
# print([Text.from_messages(choice['message']) for choice in session.get_responses("openai","chat")[1][0][1]["choices"]])
#
# print(Text.from_messages(*session.get_responses("openai","chat")))
# print(Text.from_messages(*session.get_responses("openai","chat")[1][0][0]["messages"]))
# print([Text.from_messages(choice['message']) for choice in session.get_responses("openai","chat")[1][0][1]["choices"]])

print((session.completions[0]))

from langtorch import TextTensor, TextModule, ChatTensor, Text
from langtorch.chat import User, Assistant
from langtorch import ActivationGPT
from langtorch.methods import CoT
import os

# Usage:
# activation = ActivationGPT(system_message="You are a math assistant.", T=0.5, model="gpt-3.5-turbo")
# cot_module = CoT(activation=activation)
#
# input_tensor = TextTensor(["4, 8, 9, 15, 12, 2, 1"])
# result = cot_module(input_tensor)
# print(result)
# Usage
text_tensor = TextTensor(["Hey", "this", "is", "a", "vector."])
print(text_tensor)  # Outputs: Hey, this, is, a, vector.



# text_tensor = ChatTensor(["Hey{:user}this{:assistant}is{:user}", "a{:assistant}vector.{:user}"])
# print(text_tensor)  # Outputs: Hey, this, is, a, vector.
#
# chat1 = User("Hello ")
# chat2 = Assistant("world!")
# print(chat1.items(), chat2.items())
# chat3 = chat1 + chat2
# chat3 = chat1 + TextTensor("world!")
# print(type(chat3))  # Outputs: <class '__main__.ChatTensor'>
# print(chat3)       # Outputs: user: Hello assistant: world!

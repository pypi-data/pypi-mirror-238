import sys

import numpy as np

sys.path.append("D:/llm-recommendations/dxx")
from langtorch import TextTensor, TextModule

f = lambda x: x + ('||')

F = np.vectorize(f, otypes=['<U'])
arr = TextTensor.to_char_array(["ass", "Aass"])
print(arr)

print(F(arr))

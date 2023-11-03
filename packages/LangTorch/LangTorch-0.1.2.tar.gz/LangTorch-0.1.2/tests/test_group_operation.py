import sys
# sys.path.append("D:/llm-recommendations/dxx")
# import unittest
# import torch
# from langtorch import TextTensor
# from torch.autograd import Function
from collections import OrderedDict

o1 = OrderedDict({"key": "value", "": "check", "": "second"})

print("".join(o1.values()))

# class BroadcastTextTensor(Function):
#     @staticmethod
#     def forward(ctx, A, B):
#         # Save original shapes for the backward pass
#         ctx.original_shapes = A.shape, B.shape
#
#         # Align shapes for broadcasting by adding singleton dimensions
#         max_dims = max(A.dim(), B.dim())
#         for _ in range(max_dims - A.dim()):
#             A = A.unsqueeze(0)
#         for _ in range(max_dims - B.dim()):
#             B = B.unsqueeze(0)
#
#         # Expand tensors dimension-by-dimension
#         expanded_sizes = []
#         for dim in range(max_dims):
#             A_dim_size = A.size(dim)
#             B_dim_size = B.size(dim)
#
#             if A_dim_size != B_dim_size:
#                 if A_dim_size == 1:
#                     A_dim_size = B_dim_size
#                 elif B_dim_size == 1:
#                     B_dim_size = A_dim_size
#
#             expanded_sizes.append(max(A_dim_size, B_dim_size))
#
#         A = A.expand(*expanded_sizes)
#         B = B.expand(*expanded_sizes)
#
#         return A, B
#
#     @staticmethod
#     def backward(ctx, grad_A, grad_B):
#         A_shape, B_shape = ctx.original_shapes
#
#         # Reduce the gradients along any expanded dimensions for A
#         for dim, size in enumerate(A_shape):
#             if grad_A.size(dim) != size:
#                 grad_A = grad_A.sum(dim=dim, keepdim=True)
#
#         # Reduce the gradients along any expanded dimensions for B
#         for dim, size in enumerate(B_shape):
#             if grad_B.size(dim) != size:
#                 grad_B = grad_B.sum(dim=dim, keepdim=True)
#
#         # Reshape the gradients to match the original shapes
#         grad_A = grad_A.reshape(A_shape)
#         grad_B = grad_B.reshape(B_shape)
#
#         return grad_A, grad_B
#
#
# def mul_format(s1, s2):
#     return
#
# class MulTextTensor(torch.autograd.Function):
#     """TextModule * TextModule"""
#     @staticmethod
#     def forward(ctx, input, task):
#         # Perform the forward pass computation
#         ctx.save_for_backward(input, task)
#
#         # TODO task key analogy pointer? reference? value?
#         # if "{task}" in str(input):
#         #     return input.format(task = str(task))
#         # TODO optimise by keeping track of valid attributes
#         all_attrs = [attr for attr in dir(input) if not attr.startswith("_") and not attr.endswith("_")]
#         if "{input}" not in str(task) and input.key == "input":
#             task+="{input}"
#         output = []
#         attrs = []
#         for attr in all_attrs:
#             try:
#                 value = getattr(input, attr)
#                 if not callable(value) and attr!="key" and value is not None:
#                     attrs.append((f"{input.key}.{attr}", str(value)))
#             except:
#                 pass
#         for t in input.flat:
#             output.append(str(task.format(**(dict(attrs + [(input.key,str(t))])))))
#         return TextTensor(output).reshape(input.shape)
#
#
#     @staticmethod
#     def backward(ctx, grad_output):
#         # Perform the backward pass computation
#         input, other = ctx.saved_tensors
#         grad_input = grad_output + "This problem occured with the following: " + other
#         grad_other = grad_output + "This problem occured with the following: " + input
#         return grad_input, grad_other
#
# CustomTorchFunction = MulTextTensor
# class TestGroupAxioms(unittest.TestCase):
#
#     def setUp(self):
#         # This is a placeholder for a sample set of elements. Adjust as necessary.
#         self.elements = [TextTensor("aa"),TextTensor("bb"), TextTensor("aabb",sign = "++--")]
#         self.elements = self.elements + [m**-1 for m in self.elements]
#         self.identity = TextTensor("")
#
#     def test_closure(self):
#         for a in self.elements:
#             for b in self.elements:
#                 result = CustomTorchFunction.apply(a, b)
#                 # Adjust the condition below as necessary
#                 self.assertIn(result, self.elements, msg=f"Failed for {a} and {b}")
#
#     def test_associativity(self):
#         for a in self.elements:
#             for b in self.elements:
#                 for c in self.elements:
#                     lhs = CustomTorchFunction.apply(CustomTorchFunction.apply(a, b), c)
#                     rhs = CustomTorchFunction.apply(a, CustomTorchFunction.apply(b, c))
#                     self.assertTrue(torch.equal(lhs, rhs))
#
#     def test_identity_element(self):
#         # This is a placeholder for the identity element. Adjust as necessary.
#         for a in self.elements:
#             self.assertTrue(torch.equal(CustomTorchFunction.apply(a, self.identity), a))
#             self.assertTrue(torch.equal(CustomTorchFunction.apply(self.identity, a), a))
#
#     def test_inverse_element(self):
#         for a in self.elements:
#             found = False
#             for b in self.elements:
#                 if torch.equal(CustomTorchFunction.apply(a, b), self.identity) and torch.equal(CustomTorchFunction.apply(b, a), self.identity):
#                     found = True
#                     a.signed_str()
#                     b.signed_str()
#                     CustomTorchFunction.apply(a, b).signed_str()
#                     print("---------")
#                     break
#             self.assertTrue(found, msg=f"Inverse not found for {a}")
#
# # if __name__ == "__main__":
# #     # unittest.main()
# #     t1 = TextTensor(["abs","aa"], sign = ["++-","-+"])
# #     t2 = TextTensor(["abs","aa"], sign = ["++-","-+"])
# #     t3 = TextTensor("oo", sign = '-+')
# #     print(BroadcastTextTensor.apply(t1,t3)[0].signed_str())

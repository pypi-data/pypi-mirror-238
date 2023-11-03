from .text import Text
import ast

class Code(Text):
    @classmethod
    def _str_formatter(cls, instance):
        return "\n".join([str(v) for v in instance.values()])

    @classmethod
    def _input_formatter(cls, instance):
        try:
            ast.parse(str(instance))
        except SyntaxError:
            raise ValueError(f"Invalid Python code: {instance}")
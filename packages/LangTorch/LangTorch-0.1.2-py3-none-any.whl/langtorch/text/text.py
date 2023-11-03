import torch
import logging
from pyparsing import *

# Configure logging level
logging.basicConfig(level=logging.ERROR)  # Change to logging.INFO to suppress debug messages


escaped_char = Suppress("\\") + oneOf("{}:`")
LBRACE, RBRACE, COLON, BACKTICK = map(Suppress, '{}:`')
value = CharsNotIn('{}:`')
value_w_colon = CharsNotIn('{}`')
value_backticked = CharsNotIn('`')
key = CharsNotIn('{}', min=1)  # Ensure key has at least one character

# Redefining unnamed string patterns with improved backtick handling
unnamed_string1 = (LBRACE + value("value") + (Optional(COLON) ^ StringEnd()) + RBRACE)
unnamed_string2 = (LBRACE + BACKTICK + value("value") + BACKTICK + COLON + RBRACE)
unnamed_string3 = (LBRACE + BACKTICK + value("value") + BACKTICK + RBRACE)
unnamed_string4 = (LBRACE + BACKTICK + value("value") + BACKTICK + COLON + RBRACE)
empty_unnamed_string1 = (LBRACE + RBRACE).setParseAction(lambda t: '')
empty_unnamed_string2 = (BACKTICK + BACKTICK).setParseAction(lambda t: '')
unnamed_string5 = value_w_colon("value")
unnamed_string6 = BACKTICK + value_backticked("value") + BACKTICK

# Redefining the named string patterns with improved backtick handling
# Patterns for named strings

named_string1 = Group(value("value") + LBRACE + COLON + key("key") + RBRACE)
named_string2 = Group(BACKTICK + value("value") + BACKTICK + LBRACE + COLON + key("key") + RBRACE)
named_string3 = Group(LBRACE + value("value") + COLON + key("key") + RBRACE)
named_string4 = Group(LBRACE + BACKTICK + value("value") + BACKTICK + COLON + key("key") + RBRACE)
named_string5 = Group(value("value") + LBRACE + BACKTICK + BACKTICK + COLON + RBRACE)
empty_named_string = (LBRACE + COLON + RBRACE).setParseAction(lambda t: ('',''))

# Patterns for empty strings and backticked content
backticked_empty_key = Group(LBRACE + BACKTICK + BACKTICK + COLON + key("key") + RBRACE)

# Grouping the unnamed string patterns with the new patterns
unnamed_string = (unnamed_string1
                  | unnamed_string2
                  | unnamed_string3
                  | unnamed_string4
                  | empty_unnamed_string1
                  | unnamed_string5
                  | unnamed_string6
                  | empty_unnamed_string2)

# Grouping the named string patterns with the new pattern for backticked empty key
named_string = (empty_named_string
                | named_string1
                | named_string2
                | named_string3
                | named_string4
                | backticked_empty_key
                | named_string5)

# Constructing the final parser pattern with preference for unnamed strings
TextParser = ZeroOrMore(named_string | unnamed_string) + StringEnd()


class TextIdentity(str):
    def __eq__(self, other):
        return other == "" or other == ("", "") or other == 1 or isinstance(other, TextIdentity)

    def __str__(self):
        return ""

    def __repr__(self):
        return self.__str__()


class Text(str):
    identity = TextIdentity()
    parser = TextParser
    allowed_keys = None

    @classmethod
    def parse(cls, arg):
        parsed_result = cls.parser.parseString(arg)
        arg = [(res.key if "key" in res else "", res.value if "value" in res else "") if isinstance(res,
                                                                                                    ParseResults) else res
               for res in parsed_result]
        return arg


    def __new__(cls, *args, parse = True, **kwargs):
        """
        Construct a new Text instance. Allows for various input formats.

        Args:
            *args: Flexible input data. Can be a parsable string, string sequences, key-value pairs, dicts...
            parse (bool, optional): Enable or disable the automatic parsing of string content.
                                    Disable for strings that contain '{:}' symbols
            **kwargs: Additional named textual data entries.

        Returns:
            Text: A structured textual instance.

        Raises:
            ParseException: If automatic parsing fails. Consider disabling parsing if this occurs.
            ValueError: When an unsupported input format is provided e.g. a TextTensor is passed.
        """
        if len(args) == 0: return Text.identity
        content = cls.constructors(*(list(args) + list(kwargs.items())), parse = parse)
        assert cls.is_valid_tree(content)

        for i in range(len(content)):
            if isinstance(content[i], torch.Tensor) and hasattr(content[i], "content"):
                content[i] = content[i].sum().item()
            assert isinstance(content[i], str) or (0 < len(content[i]) <= 2)
        instance = super().__new__(cls, cls.concatenate_terminals(content))
        instance._content = tuple(content)
        return instance

    @classmethod
    def from_messages(cls, *messages):
        """Text from a list of dicts with keys 'role' and 'content'"""
        if isinstance(messages[0], list):
            messages = messages[0]
        text = []
        for m in messages:
            if isinstance(m, list):
                for mm in m:
                    text.append(mm["role"],m["content"])
            else:
                text.append((m["role"],m["content"]))
        return cls(*text)

    @staticmethod
    def dict_of_dicts_to_abstract_syntax_tree(cls, dicts):
        import ast
        return ast.literal_eval(str(dicts).replace(":",": ").replace("{","{ ").replace("}"," }"))


    @classmethod
    def constructors(cls, *args, parse = True):
        """Reformats a wide array of construtor patterns into a unified AST-like format"""
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        if len(args) == 1 and ((isinstance(args[0], tuple) and len(args[0]) > 2) or isinstance(args[0], list)):
            # List or tuple of strings / named strings
            args = args[0]
        elif isinstance(args[0], dict):
            # Dictionary of named strings
            args = args[0].items()
        elif isinstance(args[0], Text) and len(args) == 1:
            # Passing cls instance to itself
            args = args[0].content
        elif all([isinstance(arg, str) for arg in args]):
            if parse:
                try:
                    result = []
                    for arg in args:
                        arg = cls.parse(arg)
                        result += arg
                    args = result
                except ParseException as E:
                    print(f"Last parsed string: {arg}")
                    raise ParseException(str(E) + "\nYou may want to disable string parsing, with parse = False")
            else:
                pass
        if any([isinstance(arg, torch.Tensor) for arg in args]):
            raise ValueError("You cannot initialise Text from a TextTensor. Use tensor.item() or otherwise transform the tensor to a string, list or dictionary.")

        def simplify(arg, parse):
            if isinstance(arg, dict):
                return Text.constructors(list(arg.items()), parse=parse)
            elif isinstance(arg, Text):
                return Text.constructors(arg.items(), parse=parse)
            return Text.constructors(arg, parse=parse)

        content = [arg if cls.is_terminal(arg) else ((arg[0], simplify(arg[1], parse=parse)) if (isinstance(arg, tuple) and len(arg)==2) else simplify(arg, parse = parse)) for arg in args]
        return content

    @classmethod
    def is_terminal(cls, entry):
        if isinstance(entry, str) and not isinstance(entry, Text):
            return True
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and isinstance(entry[1], str):
            return True
        return False

    @classmethod
    def is_valid_tree(cls, entry):
        if isinstance(entry, cls):
            entry = entry.items()
        # Base cases
        if cls.is_terminal(entry):
            return True

        # Recursive cases
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and (
                isinstance(entry[1], list) or isinstance(entry[1], tuple)):
            return all(cls.is_valid_tree(child) for child in entry[1])
        if isinstance(entry, list):
            return all(cls.is_valid_tree(child) for child in entry)

        # If none of the above cases match, it's not valid
        return False

    @classmethod
    def _str_formatter(cls, instance) -> str:
        """
        Formats the human-readable string of a Text instance. Subclasses of Text can reimplement this method!

        Args:
            instance (Text): An instance of the Text class.

        Returns:
            str: A string representation of the instance.
        """
        return cls.concatenate_terminals(instance.items())

    @classmethod
    def concatenate_terminals(cls, entry) -> str:
        result = ""

        # Base cases
        if isinstance(entry, str):
            return entry
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and isinstance(entry[1], str):
            return entry[1]

        # Recursive cases
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and (
                isinstance(entry[1], list) or isinstance(entry[1], tuple)):
            return ''.join(cls.concatenate_terminals(child) for child in entry[1])
        if isinstance(entry, list):
            return ''.join(cls.concatenate_terminals(child) for child in entry)

        return result

    def __str__(self):
        return self.__class__._str_formatter(self)

    def __repr__(self):
        return self.__str__()

    def to_tensor(self):
        from langtorch import TextTensor
        return TextTensor(self)


    @property
    def content(self):
        return [m for m in self._content]

    def items(self):
        """
        Retrieves key-value pairs from the Text object, allowing for structured data extraction
        and further processing.

        Returns:
            List[Tuple[str, Union[str, Tuple[...]]]]: A list of key-value pairs representing the Text's content.
        """
        return [(arg[0], arg[1]) if isinstance(arg, tuple) else ('', arg) for arg in self._content]
        # return [(arg[0], str(self.__class__(arg[1])))) if isinstance(arg, tuple) else ('', str(self.__class__(arg))) for arg in self._content]

    def keys(self):
        return [s[0] for s in self.items()]

    def values(self):
        return [s[1] for s in self.items()]

    def set_key(self, keys, inplace = False):
        """
        Override keys for the textual entries, used for restructuring the content.
        Useful for substituting the key right before passing TextTensor to a Module.

        Args:
            keys (Union[Text, str, List[str]]): The new key or keys to apply
            inplace bool: .

        Returns:
            Text: A new Text instance with updated keys.
        """
        #The use of Text._str_formatter(t) instead of str(t) here and elsewhere is for subclasses of Text to reimplement __str__
        if isinstance(keys, Text):
            if len(keys.values()) == len(self.values()):
                content = [(k,v) for k,v in zip(keys.values(), self.values())]
            else:
                content = [(Text._str_formatter(keys), Text._str_formatter(self))]
        elif isinstance(keys, str):
            content = [(keys, Text._str_formatter(self))]
        else:
            # TODO assert len(keys) == len(self.keys())
            content = [(k,v) for k,v in zip(keys, self.values())]

        if inplace:
            self._content = tuple(content)
            return self
        else:
            return self.__class__(*content)

    def set_key_(self, keys):
        self.set_key(keys, inplace=True)

    @property
    def iloc(self):
        class iloclist(list):
            def __init__(self, text):
                super().__init__(text.items())

            def __getitem__(self, key):
                try:
                    return self.__class__(super().__getitem__(key), parse=False)
                except:
                    return self.__class__.identity
        return iloclist(self)

    @property
    def loc(self):
        class locdict(dict):
            def __init__(self, text):
                result_dict = {k: [(k,v) for key, v in text.items() if key == k] for k, _ in text.items()}
                super().__init__(result_dict)
                self.text = text

            def __getitem__(self, key):
                try:
                    if "." in key:
                        keys = key.split(".")
                        top_level_key = keys.pop(0)
                        sub_key = ".".join(keys)
                        print(top_level_key, sub_key, Text(super().__getitem__(top_level_key), parse=False).items())
                        return self.text.__class__(super().__getitem__(top_level_key), parse=False)[sub_key]
                except Exception:
                    pass
                try:
                    return self.text.__class__(super().__getitem__(key), parse = False)
                except:
                    return self.text.__class__.identity
        return locdict(self)

    def split(self, on=""):
        from langtorch import TextTensor
        return TextTensor(str(self).split() if on == "" else str(self).split(on), parse=False)


    def __getitem__(self, index):
        if isinstance(index, str):
            return self.loc[index] #Text(*[m for m in self.items() if m[0] == index])
        return self.iloc[index]

    def __or__(self, other):
        return

    def __iter__(self):
        for s in self.content:
            yield s

    def __add__(self, other):
        if isinstance(other, str) and not isinstance(other, Text):
            return self.__class__(*self.content, other, parse = False)
        elif isinstance(other, Text):
            return self.__class__(*self.content, *other.content, parse = False)
        else:
            raise TypeError(f'Cannot add {type(other)}')

    def __mul__(self, other, strict = False):
        if isinstance(other, str) and not isinstance(other, Text):
            try:
                other = Text(other)
            except ParseException:
                other = Text(other, parse = False)

        content = self.items()
        result = content
        formatted_indices = []
        indices_to_delete = []
        positional_j = 0
        for i, (k, v) in enumerate(content):
            if v == "*":
                logging.debug(f"Wildcard {(k, v)} ::filled with:: {other.items()}")
                if k == "":
                    result = result[:i] + list(other.items()) + result[i+1:]
                else:
                    result[i] = (k,other.items())
                return self.__class__(*result, parse = False) # TODO the case of the other having a re-key pattern
        for j, (k_, v_) in enumerate(other.items()):
            # Wildcard case -> Adding a key
            if v_ == "*":
                for i in indices_to_delete:
                    result.pop(i)
                result = [(k_,result)]
                indices_to_delete, formatted_indices = [],[]
            elif k_ == "" and j not in formatted_indices: # Positional arguments
                for i, (k, v) in enumerate(content):
                    if v == str(positional_j):
                        logging.debug(f"Place at numbered spot: {(k,v_)} ::at:: {i}")
                        result[i] = (k,v_)
                        positional_j += 1
                        formatted_indices.append(i)
                        break
                else:
                    for i, (k, v) in enumerate(content):
                        if v == "":
                            logging.debug(f"Place: {(k,v_)} ::at:: {i}")
                            result[i] = (k,v_)
                            formatted_indices.append(i)
                            if v_ == k:
                                indices_to_delete.append(i)
                            break
                    else:
                        logging.debug(f"Append {(k_,v_)} ::to:: {content}")
                        result += [(k_,v_)]
            else:
                for i, (k, v) in enumerate(content):
                    if i not in formatted_indices:
                        if (k,v) == (v_,k_):
                            logging.debug(f"Identity: {(k_,v_)} ::with:: {content[i]}")
                            formatted_indices.append(i)
                            indices_to_delete.append(i)
                            break
                        elif v == k_:
                            logging.debug(f"Replace content: {(k_,v_)} ::with:: {content[i]}")
                            result[i] = (k,v_)
                            formatted_indices.append(i)
                            break
                        elif k == v_:
                            logging.debug(f"Replace key: {(k_,v_)} ::with:: {content[i]}")
                            result[i] = (k_,v)
                            formatted_indices.append(i)
                            break
                        elif k == k_:
                            logging.debug(f"Concatenate: {(k_,v_)} ::with:: {content[i]}")
                            result[i] = (k,v+v_)
                            break
                else:
                    logging.debug(f"Append {(k_, v_)} ::to:: {content}")
                    # Append the ones that didn't have a {key}
                    # If you don't want this consider using | operation
                    result += [(k_, v_)]
        for i in indices_to_delete:
            result.pop(i)
        return self.__class__(*result, parse = False)


    def format(self, *args, **kwargs):
        other = Text(*args, parse = False) + Text(kwargs, parse = False)
        return self.__mul__(other, strict = True)

    def inv(self):
        return self.__class__(*[(v,k) for k,v in self.items()], parse = False)

    def __pow__(self, power):
        if power == -1:
            return self.inv()
        else:
            raise ValueError("Can only use power -1")

    def method_apply(self, method: str, *args, to = "values", **kwargs):
        assert to in ["values","keys","both"]
        if to == "values":
            return self.__class__(*list((k, getattr(v, method)(*args, **kwargs)) for k,v in self.items()), parse = False)
        elif to == "keys":
            return self.__class__(*list((getattr(k, method)(*args, **kwargs), v) for k,v in self.items()), parse = False)
        elif to == "both":
            return self.__class__(*list((getattr(k, method)(*args, **kwargs), getattr(v, method)(*args, **kwargs)) for k,v in self.items()), parse = False)

    def inspect(self):
        return "|".join(f"{v} "+"{"+k+"}, " for k,v in self.items())

    def upper(self):
        return self.method_apply("upper")

    def lower(self):
        return self.method_apply("lower")

class MulTextTensor(torch.autograd.Function):
    """Text * Text"""

    @staticmethod
    def forward(ctx, input, other):
        # Perform the forward pass computation
        ctx.save_for_backward(input, other)
        return input * other

    @staticmethod
    def backward(ctx, grad_output):
        # Perform the backward pass computation
        input, task = ctx.saved_tensors
        grad_input = grad_output + "This problem occured with the following: " + task
        grad_other = grad_output + "This problem occured with the following: " + input
        return grad_input, grad_other
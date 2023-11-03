from markdown_it import MarkdownIt
from markdown_it.token import Token
from typing import List, Union, Tuple, Any
from .text import Text

class Node:
    def __init__(self, node_type: str, content: Any = None):
        self.node_type = node_type
        self.children = [] if content is None else [content]

class Markdown(Text):
    @classmethod
    def parse(cls, arg: str) -> List[Union[str, Tuple[str, Union[str, List]]]]:
        md = MarkdownIt()
        tokens = md.parse(arg)

        root = Node('root')
        stack = [root]
        key_mapping = {'ul': 'bullet_list', 'ol': 'ordered_list', 'h1': 'header_h1', 'h2': 'header_h2',
                       'h3': 'header_h3', 'h4': 'header_h4', 'h5': 'header_h5', 'h6': 'header_h6'}

        for token in tokens:
            if token.nesting == 1:  # Opening tags
                new_node = Node(key_mapping.get(token.tag, token.tag))
                stack[-1].children.append(new_node)
                stack.append(new_node)
            elif token.nesting == -1:  # Closing tags
                stack.pop()
            elif token.type == 'inline':
                stack[-1].children.append(token.content)

        def tree_to_tuples(node: Node) -> Any:
            if not node.children:
                return None
            if all(isinstance(child, str) for child in node.children):
                return (node.node_type, ' '.join(node.children))
            simplified_children = [(tree_to_tuples(child) if isinstance(child, Node) else child) for child in node.children]
            # Simplify cases where leaf nodes are a list of one paragraph to just the content.
            if len(simplified_children) == 1 and isinstance(simplified_children[0], tuple) and simplified_children[0][0] in ['p']:
                return (node.node_type, simplified_children[0][1])
            return (node.node_type, simplified_children)

        return [tree_to_tuples(child) for child in root.children]


    @classmethod
    def _str_formatter(cls, instance: List[Union[str, Tuple[str, Union[str, List]]]]) -> str:
        return cls.to_markdown(instance)

    @classmethod
    def to_markdown(cls, entry: Union[str, Tuple[str, Union[str, List]]]) -> str:
        result = ""
        newline = '\n'

        key_to_md = {
            'header_h1': '# ',
            'header_h2': '## ',
            'header_h3': '### ',
            'header_h4': '#### ',
            'header_h5': '##### ',
            'header_h6': '###### ',
            'bullet_list': '- ',
            'ordered_list': '1. ',
            'blockquote': '> ',
            'code': '```',
            'p': ''
        }

        # Base cases
        if isinstance(entry, str):
            return entry
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and isinstance(entry[1], str):
            return f"{key_to_md.get(entry[0], '')}{entry[1]}\n"

        # Recursive cases
        if isinstance(entry, tuple) and len(entry) == 2 and isinstance(entry[0], str) and isinstance(entry[1],
                                                                                                     list):
            # Special case for code blocks
            if entry[0] == 'code':
                return f"{key_to_md.get(entry[0], '')}\n{entry[1]}\n{key_to_md.get(entry[0], '')}\n\n"
            elif entry[0] in ['bullet_list', 'ordered_list']:
                # Handling of list items
                return f"{newline.join([key_to_md.get(entry[0], '') + cls.to_markdown(child[1]) for child in entry[1]])}\n\n"
            else:
                return f"{key_to_md.get(entry[0], '')}{newline.join([cls.to_markdown(child) for child in entry[1]])}\n\n"

        if isinstance(entry, list):
            return newline.join([cls.to_markdown(child) for child in entry])

        return result

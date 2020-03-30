from . import ast
from .lexer import tokenize
from .spec import TokenSpecification, FORMAT_TOKEN_TYPES, TERMINAL_TOKEN_TYPES, EOF

STOP = "STOP"


class BetterParser:
    def __init__(self, string):
        self.string = string
        self.tokens = tokenize(string) 
        self._stack = []
        self._tree = []

    @property
    def tree(self):
        return self._tree

    def parse(self):
        print("STRING", self.string)

        self._tree = []
        self._stack = []
        format_elements = []
        text_elements = []
        token_iter = iter(self.tokens)
        current_token = next(token_iter, STOP)
        format_token = None
        paragraph = None

        for token in self.tokens:
            print(token)
        print("\n=============================")

        while current_token != STOP:
            if current_token.type in FORMAT_TOKEN_TYPES:
                self._stack.append(current_token)
                print(f"[{current_token.type}]")
                element = ast.AST_BY_TOKEN_TYPE[current_token.type]()
                format_elements.append(element)
                current_token = next(token_iter, STOP)
            else:
                if paragraph is None:
                    paragraph = ast.Paragraph()
                paragraph.elements.append(ast.Text(current_token.value))

            while self._stack and current_token != STOP:
                if current_token.type in FORMAT_TOKEN_TYPES:
                    if current_token.type == self._stack[-1].type:
                        format_token = self._stack.pop()
                        print(f"[/{current_token.type}]")
                        if text_elements:
                            text_element = text_elements.pop()
                        if format_elements:
                            format_element = format_elements.pop()
                            format_element.elements.append(text_element)
                            print(format_element.eval())
                    else:
                        print(f"[{current_token.type}]")
                        self._stack.append(current_token)
                        element = ast.AST_BY_TOKEN_TYPE[current_token.type]()
                        format_elements.append(element)
                else:
                    print(current_token.value)
                    text_elements.append(ast.Text(current_token.value))

                current_token = next(token_iter, STOP)

            if current_token.type in TERMINAL_TOKEN_TYPES:
                print("---------------------------------")
                self._tree.append(paragraph)
                paragraph = None

            if current_token != STOP:
                print(current_token.value)
                current_token = next(token_iter, STOP)

    def format_node(self, current_token):
        pass

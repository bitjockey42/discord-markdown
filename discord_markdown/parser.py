from . import ast
from .spec import (
    TokenSpecification,
    NONFORMAT_TOKEN_TYPES,
    FORMAT_TOKEN_TYPES,
    NESTED_TOKEN_TYPES,
    TERMINAL_TOKEN_TYPES,
    QUOTE_TOKEN_TYPES,
    EOF,
)

STOP_ITERATION = "STOP_ITERATION"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_iter = iter(self.tokens)
        self.eof = self.tokens[-1]
        self._format_tokens = []
        self._tree = []

    @property
    def tree(self):
        return self._tree

    def print(self):
        for node in self.tree:
            print(node.eval(), end="")

    def parse(self):
        self._tree = []
        self._format_tokens = []
        self.token_iter = iter(self.tokens)

        elem = None
        paragraph = ast.Paragraph()
        current_token = next(self.token_iter, STOP_ITERATION)

        while current_token != STOP_ITERATION:
            if current_token.type in TERMINAL_TOKEN_TYPES:
                self._tree.append(paragraph)
                paragraph = None
                elem = None

            if current_token.type in NONFORMAT_TOKEN_TYPES:
                if paragraph is None:
                    paragraph = ast.Paragraph()
                elem = ast.Text(current_token.value)

            if elem is not None:
                paragraph.elements.append(elem)
            current_token = next(self.token_iter, STOP_ITERATION)

class ParseError(Exception):
    pass

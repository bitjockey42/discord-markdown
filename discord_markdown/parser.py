from . import ast
from .ast import AST_BY_TOKEN_TYPE, Paragraph
from .spec import (
    TokenSpecification,
    FORMAT_TOKEN_TYPES,
    NESTED_TOKEN_TYPES,
    TERMINAL_TOKEN_TYPES,
    QUOTE_TOKEN_TYPES,
    EOF,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_iter = iter(self.tokens)
        self.eof = self.tokens[-1]
        self._stack = []
        self._tree = []

    @property
    def tree(self):
        return self._tree

    def print(self):
        for node in self.tree:
            print(node.eval(), end="")

    def parse(self):
        self._tree = []
        self._stack = []
        self.token_iter = iter(self.tokens)

        current_token = next(self.token_iter)
        paragraph = ast.Paragraph()

        while current_token != self.eof:
            paragraph.elements.append(ast.Text(current_token.value))

            if current_token != self.eof:
                current_token = next(self.token_iter)

            self._tree.append(paragraph)


class ParseError(Exception):
    pass

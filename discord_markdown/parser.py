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

STOP_ITERATION = "STOP_ITERATION"


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

        current_token = next(self.token_iter, STOP_ITERATION)
        paragraph = None

        while current_token != STOP_ITERATION:
            if current_token.type in TERMINAL_TOKEN_TYPES:
                print("END", [e.eval() for e in paragraph.elements])
                self._tree.append(paragraph)
                paragraph = None
            else:
                if paragraph is None:
                    paragraph = ast.Paragraph()
                paragraph.elements.append(ast.Text(current_token.value))
                print("TEXT", [e.eval() for e in paragraph.elements])

            current_token = next(self.token_iter, STOP_ITERATION)


class ParseError(Exception):
    pass

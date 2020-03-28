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
        current_token = next(self.token_iter, STOP_ITERATION)
        paragraph = None


class ParseError(Exception):
    pass

from . import ast
from .spec import TokenSpecification

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._stack = []
        self._tree = []

    @property
    def tree(self):
        return self._tree

    def parse(self):
        for token in self.tokens:
            if token.type == TokenSpecification.TEXT.name:
                self._tree.append(ast.Text(token.value))

from . import ast
from .spec import TokenSpecification

FORMAT_TOKEN_TYPES = [
    TokenSpecification.BOLD.name,
    TokenSpecification.ITALIC.name,
    TokenSpecification.UNDERLINE.name,
]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_iter = iter(tokens)
        self.eof = self.tokens[-1]
        self._stack = []
        self._tree = []

    @property
    def tree(self):
        return self._tree

    def parse(self):
        # If the token is a format token, add it to the stack
        # If the stack is not empty, pop
        # If the current token is a format token, pop from non-empty stack
        token = next(self.token_iter)

        while token != self.eof:
            print(token)
            token = next(self.token_iter)

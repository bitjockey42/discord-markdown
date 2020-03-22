from .ast import AST_BY_TOKEN_TYPE


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
        current_token = next(self.token_iter)

        while current_token != self.eof:
            current_token = next(self.token_iter)

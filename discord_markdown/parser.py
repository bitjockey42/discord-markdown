from .ast import AST_BY_TOKEN_TYPE
from .spec import TokenSpecification, NONFORMAT_TOKEN_TYPES


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
        node = None
        current_token = next(self.token_iter)

        while current_token != self.eof:
            if current_token.type not in NONFORMAT_TOKEN_TYPES:
                self._stack.append(current_token)

            while self._stack:
                if current_token.type not in NONFORMAT_TOKEN_TYPES:
                    format_token = self._stack.pop()
                    if current_token.type != format_token.type:
                        raise ParseError("Sorry")
            
            current_token = next(self.token_iter)

        print(self._stack)


class ParseError(Exception):
    pass
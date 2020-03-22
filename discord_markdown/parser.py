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
        text_node = None
        node = None
        current_token = next(self.token_iter)

        while current_token != self.eof:
            if current_token.type not in NONFORMAT_TOKEN_TYPES:
                self._stack.append(current_token)
            else:
                node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](
                    current_token.value
                )

            current_token = next(self.token_iter)

            while self._stack:
                if current_token.type not in NONFORMAT_TOKEN_TYPES:
                    format_token = self._stack.pop()
                    if current_token.type != format_token.type:
                        raise ParseError("Sorry")
                    node = AST_BY_TOKEN_TYPE[current_token.type](text_node)
                else:
                    text_node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](
                        current_token.value
                    )
                current_token = next(self.token_iter)

            self._tree.append(node)

        print(self._stack)


class ParseError(Exception):
    pass

from .ast import AST_BY_TOKEN_TYPE
from .spec import TokenSpecification, NONFORMAT_TOKEN_TYPES, QUOTE_TOKEN_TYPES


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
        print("TOKENS", self.tokens)
        self.token_iter = iter(self.tokens)
        node = None
        current_token = next(self.token_iter)
        is_quote = False
        quote_token = None

        while current_token != self.eof:
            text_node = ""

            if current_token.type in QUOTE_TOKEN_TYPES:
                is_quote = True
                quote_token = current_token

            if current_token.type not in NONFORMAT_TOKEN_TYPES:
                self._stack.append(current_token)
            else:
                node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](
                    current_token.value
                )

            current_token = next(self.token_iter)

            while self._stack:
                print("STACK", self._stack)
                if current_token.type not in NONFORMAT_TOKEN_TYPES:
                    if self._stack[-1].type != current_token.type:
                        self._stack.append(current_token)
                    else:
                        format_token = self._stack.pop()
                        if current_token.type == TokenSpecification.BOLD_ITALIC.name:
                            node = AST_BY_TOKEN_TYPE[TokenSpecification.BOLD.name](
                                AST_BY_TOKEN_TYPE[TokenSpecification.ITALIC.name](node)
                            )
                        else:
                            node = AST_BY_TOKEN_TYPE[current_token.type](node)
                elif (
                    is_quote
                    and quote_token.type == TokenSpecification.INLINE_QUOTE.name
                    and current_token.type == TokenSpecification.NEWLINE.name
                ):
                    node = AST_BY_TOKEN_TYPE[quote_token.type](node)
                    self._stack.pop()
                    is_quote = False
                    quote_token = None
                else:
                    text_node = text_node + current_token.value
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_node)

                if current_token != self.eof:
                    current_token = next(self.token_iter)

            self._tree.append(node)

        print([e.eval() for e in self._tree])


class ParseError(Exception):
    pass

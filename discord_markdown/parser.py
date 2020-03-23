from .ast import AST_BY_TOKEN_TYPE, Paragraph
from .spec import TokenSpecification, NONFORMAT_TOKEN_TYPES, QUOTE_TOKEN_TYPES, EOF


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

    def print(self):
        for node in self.tree:
            print(node.eval(), end="")

    def parse(self):
        self.token_iter = iter(self.tokens)
        node = None
        current_token = next(self.token_iter)
        is_quote = False
        quote_token = None
        create_paragraph = False
        elems = []

        while current_token != self.eof:
            text_node = ""
            elem = None

            if current_token.type in QUOTE_TOKEN_TYPES:
                is_quote = True
                quote_token = current_token

            if current_token.type not in NONFORMAT_TOKEN_TYPES:
                self._stack.append(current_token)
            else:
                node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](
                    current_token.value
                )
                elems.append(node)

            current_token = next(self.token_iter)

            # Group specific formatted text into a single node
            while self._stack and not create_paragraph:
                if current_token.type not in NONFORMAT_TOKEN_TYPES:
                    if self._stack[-1].type != current_token.type:
                        self._stack.append(current_token)
                    else:
                        format_token = self._stack.pop()
                        if current_token.type == TokenSpecification.BOLD_ITALIC.name:
                            elem = AST_BY_TOKEN_TYPE[TokenSpecification.BOLD.name](
                                AST_BY_TOKEN_TYPE[TokenSpecification.ITALIC.name](elem)
                            )
                        else:
                            elem = AST_BY_TOKEN_TYPE[current_token.type](elem)
                elif (
                    is_quote
                    and quote_token.type == TokenSpecification.INLINE_QUOTE.name
                    and current_token.type == TokenSpecification.NEWLINE.name
                ):
                    elem = AST_BY_TOKEN_TYPE[quote_token.type](elem)
                    self._stack.pop()
                    is_quote = False
                    quote_token = None
                elif (
                    is_quote
                    and quote_token.type == TokenSpecification.BLOCK_QUOTE.name
                    and current_token.type == EOF
                ):
                    elem = AST_BY_TOKEN_TYPE[quote_token.type](elem)
                    self._stack.pop()
                    is_quote = False
                    quote_token = None
                else:
                    text_node = text_node + current_token.value
                    elem = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_node)

                if current_token != self.eof:
                    current_token = next(self.token_iter)

            if elem and elem.type != TokenSpecification.NEWLINE.name:
                elems.append(elem)

            if current_token.type == TokenSpecification.NEWLINE.name or current_token.type == EOF:
                print("ELEMS", elems)
                print("Did this work")
                node = Paragraph(elems)
                elems = []

            self._tree.append(node)

            print("TREE", self._tree)


class ParseError(Exception):
    pass

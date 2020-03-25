from .ast import AST_BY_TOKEN_TYPE, Paragraph
from .spec import (
    TokenSpecification,
    FORMAT_TOKEN_TYPES,
    TERMINAL_TOKEN_TYPES,
    NONFORMAT_TOKEN_TYPES,
    QUOTE_TOKEN_TYPES,
    CODE_TOKEN_TYPES,
    EOF,
)


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

    def _parse(self):
        self.token_iter = iter(self.tokens)
        node = None
        current_token = next(self.token_iter)
        is_quote = False
        end_quote = False
        quote_token = None
        code_token = None
        create_paragraph = False
        is_code = False
        elems = []

        print("TOKENS", self.tokens)

        while current_token != self.eof:
            text_node = ""
            elem = None

            if current_token.type in QUOTE_TOKEN_TYPES:
                is_quote = True
                quote_token = current_token

            if current_token.type in CODE_TOKEN_TYPES:
                is_code = True
                code_token = current_token

            if current_token.type not in NONFORMAT_TOKEN_TYPES:
                self._stack.append(current_token)
            else:
                if current_token.type != TokenSpecification.NEWLINE.name:
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
                            print("BOLD ITALIC THING")
                            elem = AST_BY_TOKEN_TYPE[TokenSpecification.BOLD.name](
                                AST_BY_TOKEN_TYPE[TokenSpecification.ITALIC.name](elem),
                                md_tag="**",
                            )
                            elems.append(elem)
                        else:
                            elem = AST_BY_TOKEN_TYPE[format_token.type](
                                elem, md_tag=format_token.value
                            )
                elif (
                    is_quote
                    and quote_token.type == TokenSpecification.INLINE_QUOTE.name
                    and current_token.type == TokenSpecification.NEWLINE.name
                ) or (
                    is_quote
                    and quote_token.type == TokenSpecification.BLOCK_QUOTE.name
                    and current_token.type == EOF
                ):
                    elem = AST_BY_TOKEN_TYPE[quote_token.type](
                        elem, md_tag=quote_token.value
                    )
                    self._stack.pop()
                    is_quote = False
                    end_quote = True
                    quote_token = None
                else:
                    text_node = text_node + current_token.value
                    elem = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_node)

                if current_token != self.eof:
                    current_token = next(self.token_iter)

            if elem and current_token.type != TokenSpecification.NEWLINE.name:
                elems.append(elem)

            # Create a new paragraph node since we reached the NEWLINE or EOF
            if (
                current_token.type == TokenSpecification.NEWLINE.name
                or current_token.type == EOF
                or end_quote
            ):
                print("ELEMS", "".join([e.eval() for e in elems]))
                node = Paragraph(elems)
                self._tree.append(node)
                elems = []
                end_quote = False

            # print("TREE", self._tree)

    def parse(self):
        self._tree = []
        elems = []
        format_tokens = []
        token_iter = iter(self.tokens)
        current_token = next(self.token_iter)
        node = None
        create_new_paragraph = False

        while current_token != self.eof:
            # RULES:
            # Create new paragraph if NEWLINE, EOF, are hit:
            #   if the current format token is a SINGLE quote:
            #       then start a new paragraph on NEWLINE
            #   if BLOCK QUOTE:
            #       then create paragraph when EOF
            #   else:
            #       then create paragraph on NEWLINE
            #
            # When the token is a FORMAT type (e.g. BOLD):
            #   if the last item isn't the same token type:
            #       add the format token to the stack
            #   else:
            #       pop from the stack if it is the same format token type as the last thing
            #
            # While stack is not empty and we aren't making a new paragraph yet, look through each token
            #   create_new_paragraph = False
            #
            format_token = None

            if current_token.type in FORMAT_TOKEN_TYPES:
                format_tokens.append(current_token)
            else:
                if current_token.type != TokenSpecification.NEWLINE.name:
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](
                        current_token.value
                    )
                    elems.append(node)

            current_token = next(self.token_iter)

            while format_tokens and not create_new_paragraph:
                if current_token.type in FORMAT_TOKEN_TYPES:
                    if current_token.type == format_tokens[-1].type:
                        format_token = format_tokens.pop()
                        node = AST_BY_TOKEN_TYPE[format_token.type](node, md_tag=format_token.value)
                        elems.append(node)
                    else:
                        format_tokens.append(current_token)
                elif current_token.type in TERMINAL_TOKEN_TYPES:
                    create_new_paragraph = True
                else:
                    text_value = current_token.value
                    if node:
                        text_value = node.value + text_value
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_value)
                    elems.append(node)

                if current_token != self.eof:
                    current_token = next(self.token_iter)

            if create_new_paragraph or current_token == self.eof:
                self._tree.append(Paragraph(elems))
                elems = []
                create_new_paragraph = False

class ParseError(Exception):
    pass

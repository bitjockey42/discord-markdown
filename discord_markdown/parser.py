from . import ast
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

    def parse(self):
        self._tree = []
        elems = []
        format_tokens = []
        token_iter = iter(self.tokens)
        current_token = next(self.token_iter)
        node = None
        create_new_paragraph = False
        print(self.tokens)

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

                        if format_token.type == TokenSpecification.BOLD_ITALIC.name:
                            node = ast.BoldText(ast.ItalicText(node))
                        else:
                            node = AST_BY_TOKEN_TYPE[format_token.type](
                                node, md_tag=format_token.value
                            )

                        elems.append(node)
                    else:
                        format_tokens.append(current_token)
                elif current_token.type in TERMINAL_TOKEN_TYPES:
                    create_new_paragraph = True
                else:
                    text_value = current_token.value
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_value)

                if current_token != self.eof:
                    current_token = next(self.token_iter)

            print(self.tokens)
            print([e.eval() for e in elems])

            if create_new_paragraph or current_token.type in TERMINAL_TOKEN_TYPES:
                self._tree.append(Paragraph(elems))
                elems = []
                create_new_paragraph = False


class ParseError(Exception):
    pass

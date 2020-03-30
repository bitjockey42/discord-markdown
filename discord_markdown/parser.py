from . import ast
from .ast import AST_BY_TOKEN_TYPE, Paragraph
from .spec import (
    TokenSpecification,
    FORMAT_TOKEN_TYPES,
    TERMINAL_TOKEN_TYPES,
    NONFORMAT_TOKEN_TYPES,
    QUOTE_TOKEN_TYPES,
    EOF,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_iter = iter(self.tokens)
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
        current_token = next(self.token_iter)
        create_new_paragraph = False
        is_quote = False
        quote_token = None
        is_code_block = False

        while current_token != self.eof:
            format_token = None
            node = None

            if current_token.type in QUOTE_TOKEN_TYPES:
                is_quote = True
                quote_token = current_token
            elif current_token.type == TokenSpecification.CODE_BLOCK.name:
                is_code_block = True

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
                if (
                    is_quote
                    and quote_token.type == TokenSpecification.INLINE_QUOTE.name
                    and current_token.type == TokenSpecification.NEWLINE.name
                ) or (
                    is_quote
                    and quote_token.type == TokenSpecification.BLOCK_QUOTE.name
                    and current_token.type == EOF
                ):
                    format_tokens.pop()
                    node = AST_BY_TOKEN_TYPE[quote_token.type](
                        node, md_tag=quote_token.value
                    )
                    is_quote = False
                    create_new_paragraph = True
                    quote_token = None
                    elems.append(node)
                elif (
                    is_quote
                    and quote_token.type == TokenSpecification.BLOCK_QUOTE.name
                    and current_token.type in NONFORMAT_TOKEN_TYPES
                ):
                    text_value = current_token.value
                    if node is not None:
                        text_value = node.value + text_value
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_value)
                elif current_token.type in FORMAT_TOKEN_TYPES:
                    if current_token.type == format_tokens[-1].type:
                        format_token = format_tokens.pop()

                        if format_token.type == TokenSpecification.BOLD_ITALIC.name:
                            node = ast.BoldText(ast.ItalicText(node))
                        else:
                            node = AST_BY_TOKEN_TYPE[format_token.type](
                                node, md_tag=format_token.value
                            )

                        if not format_tokens:
                            elems.append(node)

                        if is_code_block:
                            is_code_block = False
                    else:
                        format_tokens.append(current_token)
                elif not is_code_block and current_token.type in TERMINAL_TOKEN_TYPES:
                    create_new_paragraph = True
                elif is_code_block:
                    text_value = current_token.value
                    if node is not None:
                        text_value = node.value + text_value
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_value)
                else:
                    text_value = current_token.value
                    node = AST_BY_TOKEN_TYPE[TokenSpecification.TEXT.name](text_value)

                if current_token != self.eof:
                    current_token = next(self.token_iter)

            if create_new_paragraph or current_token.type in TERMINAL_TOKEN_TYPES:
                self._tree.append(Paragraph(elems))
                elems = []
                create_new_paragraph = False


class ParseError(Exception):
    pass

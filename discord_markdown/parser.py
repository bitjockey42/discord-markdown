from . import ast
from .ast import AST_BY_TOKEN_TYPE, Paragraph
from .spec import (
    TokenSpecification,
    FORMAT_TOKEN_TYPES,
    NESTED_TOKEN_TYPES,
    TERMINAL_TOKEN_TYPES,
    QUOTE_TOKEN_TYPES,
    EOF,
)

STOP_ITERATION = "STOP_ITERATION"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_iter = iter(self.tokens)
        self.eof = self.tokens[-1]
        self._format_tokens = []
        self._tree = []

    @property
    def tree(self):
        return self._tree

    def print(self):
        for node in self.tree:
            print(node.eval(), end="")

    def parse(self):
        self._tree = []
        self._format_tokens = []
        self.token_iter = iter(self.tokens)

        text_elem = None
        current_token = next(self.token_iter, STOP_ITERATION)
        paragraph = None

        while current_token != STOP_ITERATION:
            if current_token.type in TERMINAL_TOKEN_TYPES:
                self._tree.append(paragraph)
                paragraph = None
                text_elem = None
            else:
                if paragraph is None:
                    paragraph = ast.Paragraph()

                if current_token.type in FORMAT_TOKEN_TYPES:
                    self._format_tokens.append(current_token)
                else:
                    text_elem = ast.Text(current_token.value)
                    paragraph.elements.append(text_elem)

                while self._format_tokens and current_token != STOP_ITERATION:
                    if current_token != STOP_ITERATION:
                        current_token = next(current_token, STOP_ITERATION)

            current_token = next(self.token_iter, STOP_ITERATION)


    def _handle_formatted_text(self, current_token, paragraph, text_elem):
        if current_token.type == self._format_tokens[-1].type:
            format_token = self._format_tokens.pop()

            if format_token.type == TokenSpecification.BOLD_ITALIC.name:
                elem = ast.BoldText(ast.ItalicText(text_elem))
            else:
                elem = AST_BY_TOKEN_TYPE[format_token.type](
                    text_elem, md_tag=format_token.value
                )

            if not self._format_tokens:
                paragraph.elements.append(elem)
        else:
            self._format_tokens.append(current_token)


class ParseError(Exception):
    pass

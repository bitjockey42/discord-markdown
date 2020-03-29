from . import ast
from .spec import (
    TokenSpecification,
    NONFORMAT_TOKEN_TYPES,
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

        if len(self.tokens) == 1 and self.tokens[0].type in TERMINAL_TOKEN_TYPES:
            return

        elem = None
        text_elem = None
        paragraph = ast.Paragraph()
        current_token = next(self.token_iter, STOP_ITERATION)


        print("------------------TOKENS-----------------")
        for token in self.tokens:
            print(token)

        while current_token != STOP_ITERATION:
            if current_token.type in FORMAT_TOKEN_TYPES:
                self._format_tokens.append(current_token)
            else:
                if paragraph is None:
                    paragraph = ast.Paragraph()

                if current_token.type not in TERMINAL_TOKEN_TYPES:
                    paragraph.elements.append(ast.Text(current_token.value))

            current_token = next(self.token_iter, STOP_ITERATION)

            while self._format_tokens:
                if current_token.type in FORMAT_TOKEN_TYPES:
                    if current_token.type == self._format_tokens[-1].type:
                        format_token = self._format_tokens.pop()

                        node = ast.AST_BY_TOKEN_TYPE[format_token.type](
                            [text_elem], md_tag=format_token.value
                        )

                        if not self._format_tokens:
                            paragraph.elements.append(node)
                    else:
                        self._format_tokens.append(current_token)
                else:
                    text_elem = ast.Text(current_token.value)

                if current_token != self.eof:
                    current_token = next(self.token_iter, STOP_ITERATION)
            
            print("--------------------BEFORE------------------------")
            for elem in paragraph.elements:
                print(elem.eval())

            if current_token == STOP_ITERATION or current_token.type in TERMINAL_TOKEN_TYPES:
                print("---------------------PARAGRAPH---------------------")
                if paragraph.elements:
                    self._tree.append(paragraph)
                print("MARKDOWN", [(e.eval(True), e) for e in paragraph.elements])
                print("HTML", [(e.eval(False), e) for e in paragraph.elements])
                paragraph = None


class ParseError(Exception):
    pass

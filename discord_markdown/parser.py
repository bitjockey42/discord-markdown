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
        self._text_elems = []
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
        self._text_elems = []
        self.token_iter = iter(self.tokens)

        if len(self.tokens) == 1 and self.tokens[0].type in TERMINAL_TOKEN_TYPES:
            return

        elem = None
        text_elem = None
        paragraph = ast.Paragraph()
        format_token = None
        format_node = None
        current_token = next(self.token_iter, STOP_ITERATION)


        print("------------------TOKENS-----------------")
        for token in self.tokens:
            print(token)

        while current_token != STOP_ITERATION:
            if current_token.type in FORMAT_TOKEN_TYPES:
                format_node = ast.AST_BY_TOKEN_TYPE[current_token.type]()
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

                        if not self._format_tokens:
                            if format_node is not None:
                                paragraph.elements.append(format_node)
                    else:
                        node = ast.AST_BY_TOKEN_TYPE[current_token.type]()
                        format_node.elements.append(node)
                        self._format_tokens.append(current_token)
                else:
                    text_elem = ast.Text(current_token.value)
                    if format_node.elements:
                        format_node.elements[-1].elements.append(text_elem)
                    else:
                        format_node.elements.append(text_elem)

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

    def build_tree(self):
        self.token_iter = iter(self.tokens, STOP_ITERATION)


class ParseError(Exception):
    pass

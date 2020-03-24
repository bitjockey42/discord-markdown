from .compiler import Compiler
from .parser import Parser
from .lexer import tokenize


def convert_to_html(text):
    return Compiler(text).compile()


def parse_text(text):
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    return parser.tree

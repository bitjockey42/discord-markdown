from .compiler import Compiler
from .parser import Parser
from .lexer import tokenize


def convert_to_html(text):
    return Compiler(text).compile(markdown=False)


def parse_text(text):
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    return parser.tree


class DiscordMarkdown:
    def __init__(self, text):
        self._compiler = Compiler(text)

    def markdown(self):
        return self._compiler.compile(True)

    def html(self):
        return self._compiler.compile(False)

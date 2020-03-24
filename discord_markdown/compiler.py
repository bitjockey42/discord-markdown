from .lexer import tokenize
from .parser import Parser


class Compiler:
    def __init__(self, text):
        self._text = text
        self._tokens = tokenize(self._text)
        self._parser = Parser(self._tokens)
        self._code = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._tokens = tokenize(self._text)

    @property
    def tokens(self):
        return self._tokens

    @property
    def code(self):
        return self._code

    def compile(self, markdown=False):
        print(self._tokens)
        if not self._parser.tree:
            self._parser.parse()
        self._code = ""
        for node in self._parser.tree:
            self._code = self._code + node.eval(markdown=markdown)
        self._code = self._code.strip()
        return self._code

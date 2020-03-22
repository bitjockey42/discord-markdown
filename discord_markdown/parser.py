from . import ast


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._stack = []

    def parse(self):
        pass
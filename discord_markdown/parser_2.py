from . import ast
from .lexer import tokenize
from .spec import TokenSpecification, FORMAT_TOKEN_TYPES

STOP = "STOP"


class BetterParser:
    def __init__(self, string):
        self.string = string
        self.tokens = tokenize(string) 

    def parse(self):
        print("STRING", self.string)

        stack = []
        token_iter = iter(self.tokens)
        current_token = next(token_iter, STOP)
        format_token = None

        for token in self.tokens:
            print(token)

        while current_token != STOP:
            if current_token.type in FORMAT_TOKEN_TYPES:
                stack.append(current_token)
                print(f"[{current_token.type}]")
            else:
                print(current_token.value)

            current_token = next(token_iter, STOP)

            while stack:
                if current_token.type in FORMAT_TOKEN_TYPES:
                    if current_token.type == stack[-1].type:
                        format_token = stack.pop()
                        print(f"[/{current_token.type}]")
                    else:
                        print(f"[{current_token.type}]")
                        stack.append(current_token)
                else:
                    print(current_token.value)
                
                current_token = next(token_iter, STOP)

            current_token = next(token_iter, STOP)

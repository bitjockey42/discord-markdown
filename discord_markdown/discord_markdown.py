from .compiler import Compiler


def convert_to_html(text):
    return Compiler(text).compile()

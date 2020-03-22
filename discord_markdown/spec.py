import collections
import enum

from . import ast


Token = collections.namedtuple("Token", ["type", "value", "line", "column"])
TokenSpec = collections.namedtuple("TokenSpec", ["name", "pattern", "instances"])


class TokenSpecification(enum.Enum):
    CODE_BLOCK = ("CODE_BLOCK", r"`", r"{3}\w*")
    INLINE_CODE = ("INLINE_CODE", r"`", r"{1}")
    SPOILER = ("SPOILER", r"\|", r"{2}")
    BOLD_ITALIC = ("BOLD_ITALIC", r"\*", r"{3}")
    BOLD = ("BOLD", r"\*", r"{2}")
    UNDERLINE = ("UNDERLINE", r"_", r"{2}")
    ITALIC = ("ITALIC", r"\*|_", r"{1}")
    STRIKETHROUGH = ("STRIKETHROUGH", r"~", r"{2}")
    BLOCK_QUOTE = ("BLOCK_QUOTE", r">", r"{3}")
    INLINE_QUOTE = ("INLINE_QUOTE", r">", r"{1}")
    NEWLINE = ("NEWLINE", r"\n", "")
    SPACE = ("SPACE", r"[ \t]+", "")
    TEXT = ("TEXT", r"[\S\s]?", "")


AST_BY_TOKEN_TYPE = {
    TokenSpecification.TEXT.name: ast.Text,
    TokenSpecification.BOLD.name: ast.BoldText,
    TokenSpecification.ITALIC.name: ast.ItalicText,
    TokenSpecification.UNDERLINE.name: ast.UnderlineText,
    TokenSpecification.STRIKETHROUGH.name: ast.StrikethroughText,
    TokenSpecification.BLOCK_QUOTE.name: ast.BlockQuote,
    TokenSpecification.INLINE_QUOTE.name: ast.InlineQuote,
    TokenSpecification.CODE_BLOCK.name: ast.CodeBlock,
    TokenSpecification.INLINE_CODE.name: ast.InlineCode,
}


NONFORMAT_TOKEN_TYPES = [
    TokenSpecification.SPACE,
    TokenSpecification.NEWLINE,
]

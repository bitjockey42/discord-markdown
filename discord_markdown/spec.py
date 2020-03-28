import collections
import enum


EOF = "EOF"

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


FORMAT_TOKEN_TYPES = [
    TokenSpecification.CODE_BLOCK.name,
    TokenSpecification.BLOCK_QUOTE.name,
    TokenSpecification.INLINE_CODE.name,
    TokenSpecification.INLINE_QUOTE.name,
    TokenSpecification.BOLD.name,
    TokenSpecification.BOLD_ITALIC.name,
    TokenSpecification.SPOILER.name,
    TokenSpecification.UNDERLINE.name,
    TokenSpecification.ITALIC.name,
    TokenSpecification.STRIKETHROUGH.name,
]


NONFORMAT_TOKEN_TYPES = [
    TokenSpecification.TEXT.name,
    TokenSpecification.SPACE.name,
    TokenSpecification.NEWLINE.name,
    EOF,
]


TERMINAL_TOKEN_TYPES = [
    TokenSpecification.NEWLINE.name,
    EOF,
]


QUOTE_TOKEN_TYPES = [
    TokenSpecification.INLINE_QUOTE.name,
    TokenSpecification.BLOCK_QUOTE.name,
]


CODE_TOKEN_TYPES = [
    TokenSpecification.CODE_BLOCK.name,
    TokenSpecification.INLINE_CODE.name,
]

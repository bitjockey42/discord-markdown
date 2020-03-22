import collections
import re

TOKEN_SPECIFICATION = [
    ("CODE_BLOCK", r"`", "{3}"),
    ("INLINE_CODE", r"`", "{1}"),
    ("SPOILER", r"\|", "{2}"),
    ("BOLD", r"\*", "{2}"),
    ("UNDERLINE", r"_", "{2}"),
    ("ITALIC", r"\*|_", "{1}"),
    ("STRIKETHROUGH", r"~", "{2}"),
    ("BLOCK_QUOTE", r">", "{3}"),
    ("INLINE_QUOTE", r">", "{1}"),
    ("NEWLINE", r"\n", ""),
    ("SPACE", r"[ \t]+", ""),
    ("TEXT", r"[\S\s]?", ""),
]
Token = collections.namedtuple("Token", ["type", "value", "line", "column"])


def tokenize(code, skip_newline=True):
    line_count = code.count("\n") + 1
    terminal_token = Token("TERM", value="", line=line_count, column=len(code))

    token_iter = tokenize_generator(code, skip_newline)
    current_token = next(token_iter, terminal_token)
    tokens = []
    text_tokens = []

    while current_token != terminal_token:
        if (current_token.line == terminal_token.line and current_token.column == terminal_token.column and current_token.value == ""):
            break            

        while current_token.type == "TEXT" or current_token.type == "SPACE":
            text_tokens.append(current_token)
            current_token = next(token_iter, terminal_token)

        if text_tokens:
            concat_text = [t.value for t in text_tokens]
            concat_text_token = Token(
                "TEXT",
                value="".join(concat_text),
                line=text_tokens[0].line,
                column=text_tokens[0].column
            )
            text_tokens = []
            tokens.append(concat_text_token)

        if current_token != terminal_token:
            tokens.append(current_token)

        current_token = next(token_iter, terminal_token)

    return tokens


def tokenize_generator(code, skip_newline=True):
    tok_regex = "|".join(
        "(?P<%s>%s)%s" % token_regex for token_regex in TOKEN_SPECIFICATION
    )
    print(tok_regex)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        token_type = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if token_type == "NEWLINE":
            line_start = mo.end()
            line_num += 1
            if skip_newline:
                continue
        yield Token(token_type, value, line_num, column)

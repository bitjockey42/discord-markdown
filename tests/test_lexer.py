import pytest

from discord_markdown.lexer import tokenize, Token


def test_bold():
    text = "**Bold**"
    assert tokenize(text) == [
        Token("BOLD", value="**", line=1, column=0),
        Token("TEXT", value="Bold", line=1, column=2),
        Token("BOLD", value="**", line=1, column=6),
    ]


def test_italic():
    text = "_Italic_"
    assert tokenize(text) == [
        Token("ITALIC", value="_", line=1, column=0),
        Token("TEXT", value="Italic", line=1, column=1),
        Token("ITALIC", value="_", line=1, column=7),
    ]

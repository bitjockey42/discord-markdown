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


def test_italic_alt():
    text = "*Italic*"
    assert tokenize(text) == [
        Token("ITALIC", value="*", line=1, column=0),
        Token("TEXT", value="Italic", line=1, column=1),
        Token("ITALIC", value="*", line=1, column=7),
    ]


def test_underline():
    text = "__Underline__"
    assert tokenize(text) == [
        Token("UNDERLINE", value="__", line=1, column=0),
        Token("TEXT", value="Underline", line=1, column=2),
        Token("UNDERLINE", value="__", line=1, column=11),
    ]


def test_strikethrough():
    text = "~~Strikethrough~~"
    assert tokenize(text) == [
        Token("STRIKETHROUGH", value="~~", line=1, column=0),
        Token("TEXT", value="Strikethrough", line=1, column=2),
        Token("STRIKETHROUGH", value="~~", line=1, column=15),
    ]


def test_bold_italic():
    text = "***Bold Italics***"
    assert tokenize(text) == [
        Token("BOLD_ITALIC", value="***", line=1, column=0),
        Token("TEXT", value="Bold Italics", line=1, column=3),
        Token("BOLD_ITALIC", value="***", line=1, column=15),
    ]


def test_underline_italic():
    text = "__*underline italics*__" 
    assert tokenize(text) == [
        Token("UNDERLINE", value="__", line=1, column=0),
        Token("ITALIC", value="*", line=1, column=2),
        Token("TEXT", value="underline italics", line=1, column=3),
        Token("ITALIC", value="*", line=1, column=20),
        Token("UNDERLINE", value="__", line=1, column=21),
    ]


def test_underline_bold():
    text = "__**underline bold**__"


def test_underline_bold_italics():
    text = "__***underline bold italics***__"

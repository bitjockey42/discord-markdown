import pytest

from discord_markdown.lexer import tokenize
from discord_markdown.parser import Parser
from discord_markdown import ast


def assert_tree(parser_tree, expected, markdown=False):
    assert [(node.eval(markdown), node.HTML_TAG) for node in parser_tree] == [
        (e.eval(markdown), e.HTML_TAG) for e in expected
    ]


def test_plain_text():
    text = "Simple example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [ast.Paragraph([ast.Text(text)])])


def test_paragraph_text():
    text = (
        "This is the first paragraph.\nThis is the second one.\nThis is the third one."
    )
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph([ast.Text("This is the first paragraph.")]),
            ast.Paragraph([ast.Text("This is the second one.")]),
            ast.Paragraph([ast.Text("This is the third one.")]),
        ],
    )


def test_bold_text():
    text = "This is **formatted**"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [ast.Paragraph([ast.Text("This is "), ast.BoldText(ast.Text("formatted"))])],
    )


def test_bold_alt_text():
    text = "**formatted**"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [ast.Paragraph([ast.BoldText(ast.Text("formatted"))])])


@pytest.mark.parametrize("text", [("This is *formatted*"), ("This is _formatted_")])
def test_italic_text(text):
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [ast.Paragraph([ast.Text("This is "), ast.ItalicText(ast.Text("formatted"))]),],
    )


def test_underline_text():
    text = "An __underlined__ example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("An "),
                    ast.UnderlineText(ast.Text("underlined")),
                    ast.Text(" example"),
                ]
            )
        ],
    )


def test_strikethrough_text():
    text = "A ~~strikethrough~~ example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("A "),
                    ast.StrikethroughText(ast.Text("strikethrough")),
                    ast.Text(" example"),
                ]
            )
        ],
    )


def test_bold_italics_text():
    text = "This is ***bold italics***"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("This is "),
                    ast.BoldText(ast.ItalicText(ast.Text("bold italics"))),
                ]
            ),
        ],
    )

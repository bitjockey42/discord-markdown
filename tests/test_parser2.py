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

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


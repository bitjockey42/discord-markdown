import pytest

from discord_markdown.lexer import tokenize
from discord_markdown.parser import Parser
from discord_markdown import ast


def assert_tree(parser_tree, expected):
    assert [(node.eval(), node.HTML_TAG) for node in parser_tree] == [
        (e.eval(), e.HTML_TAG) for e in expected
    ]


def test_simple():
    text = "Simple example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [ast.Text(text)])


def test_formatted_text():
    text = "This is **formatted**"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [
        ast.Text("This is "),
        ast.BoldText(ast.Text("formatted")),
    ])

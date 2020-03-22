from discord_markdown.lexer import tokenize
from discord_markdown.parser import Parser
from discord_markdown import ast


def assert_tree(parser_tree, expected):
    assert [node.value for node in parser_tree] == [e.value for e in expected]


def test_simple():
    text = "Simple example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [ast.Text(text)])

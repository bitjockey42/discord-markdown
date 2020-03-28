import pytest

from discord_markdown.lexer import tokenize
from discord_markdown.parser import Parser
from discord_markdown import ast

from tests.fixtures import load_file


def assert_tree(parser_tree, expected, markdown=False):
    assert len(parser_tree) == len(expected)
    assert [(node.eval(markdown), node.HTML_TAG) for node in parser_tree] == [
        (e.eval(markdown), e.HTML_TAG) for e in expected
    ]


@pytest.mark.parametrize("markdown", [False, True])
def test_plain_text(markdown):
    text = "Simple example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    expected = [ast.Paragraph([ast.Text(text)])]
    assert_tree(parser.tree, expected, markdown)

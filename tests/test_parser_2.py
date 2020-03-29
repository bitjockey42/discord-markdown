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


def test_empty_text():
    text = ""
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [])


@pytest.mark.parametrize("markdown", [False, True])
def test_plain_text(markdown):
    text = "Simple example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    expected = [ast.Paragraph([ast.Text(text)])]
    assert_tree(parser.tree, expected, markdown)


@pytest.mark.parametrize("markdown", [False, True])
def test_paragraph_text(markdown):
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
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_bold_text(markdown):
    text = "This is **formatted**"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [ast.Paragraph([ast.Text("This is "), ast.BoldText([ast.Text("formatted")])])],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_bold_alt_text(markdown):
    text = "**formatted**"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [ast.Paragraph([ast.BoldText([ast.Text("formatted")])])],
        markdown=markdown,
    )

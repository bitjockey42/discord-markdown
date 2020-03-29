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


@pytest.mark.skip("FIXME")
@pytest.mark.parametrize("markdown", [False, True])
def test_bold_italics_text(markdown):
    text = "Here I _am_ in the **light** of ***day***\nLet the storm rage on"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("Here I "),
                    ast.ItalicText([ast.Text("am")], md_tag="_"),
                    ast.Text(" in the "),
                    ast.BoldText([ast.Text("light")]),
                    ast.Text(" of "),
                    ast.BoldText([ast.ItalicText([ast.Text("day")])]),
                ]
            ),
            ast.Paragraph([ast.Text("Let the storm rage on")]),
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_underline_text(markdown):
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
                    ast.UnderlineText([ast.Text("underlined")]),
                    ast.Text(" example"),
                ]
            )
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_underline_bold_text(markdown):
    text = "An __**underline bold**__ example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("An "),
                    ast.UnderlineText([ast.BoldText([ast.Text("underline bold")])]),
                    ast.Text(" example"),
                ]
            )
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_nested_formatting_text(markdown):
    text = "__This **_is nested_**__"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.UnderlineText(
                        [
                            ast.Text("This "),
                            ast.BoldText(
                                [ast.ItalicText([ast.Text("is nested")], md_tag="_")]
                            ),
                        ]
                    )
                ]
            )
        ],
    )

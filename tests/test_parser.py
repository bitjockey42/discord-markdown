import pytest

from discord_markdown.lexer import tokenize
from discord_markdown.parser import Parser
from discord_markdown import ast


def assert_tree(parser_tree, expected):
    assert [(node.eval(), node.HTML_TAG) for node in parser_tree] == [
        (e.eval(), e.HTML_TAG) for e in expected
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
            ast.Paragraph([ast.Text("\n"), ast.Text("This is the second one.")]),
            ast.Paragraph([ast.Text("\n"), ast.Text("This is the third one.")]),
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


def test_bold_italics_text():
    text = "This is ***formatted***"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("This is "),
                    ast.BoldText(ast.ItalicText(ast.Text("formatted"))),
                ]
            )
        ],
    )


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


def test_underline_italics_text():
    text = "An __*underline italics*__ example"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("An "),
                    ast.UnderlineText(ast.ItalicText(ast.Text("underline italics"))),
                    ast.Text(" example"),
                ]
            )
        ],
    )


def test_underline_bold_text():
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
                    ast.UnderlineText(ast.BoldText(ast.Text("underline bold"))),
                    ast.Text(" example"),
                ]
            )
        ],
    )


def test_multiple_formatted_text():
    text = "An __*underline italics*__ example.\nI **am** depressed."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("An "),
                    ast.UnderlineText(ast.ItalicText(ast.Text("underline italics"))),
                    ast.Text(" example."),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("\n"),
                    ast.Text("I "),
                    ast.BoldText(ast.Text("am")),
                    ast.Text(" depressed."),
                ]
            ),
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


def test_inline_code():
    text = "Run this command `echo hello`."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("Run this command "),
                    ast.InlineCode(ast.Text("echo hello")),
                    ast.Text("."),
                ]
            )
        ],
    )


def test_code_block():
    text = """```sh
    echo test
    ```"""
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [ast.CodeBlock(ast.Text("\n    echo test\n    ")), ast.Text("")]
            )
        ],
    )


@pytest.mark.skip("FIXME")
def test_inline_quote():
    text = "> This is a quote.\nThis isn't part of it."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph([ast.InlineQuote(ast.Text(" This is a quote."))]),
            ast.Paragraph([ast.Text("This isn't part of it.")]),
        ],
    )


def test_block_quote():
    text = ">>> This is a quote.\nThis should be part of it."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.BlockQuote(
                        ast.Text(" This is a quote.\nThis should be part of it.")
                    )
                ]
            )
        ],
    )


def test_spoiler_text():
    text = "The FBI says ||redacted here||."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("The FBI says "),
                    ast.SpoilerText(ast.Text("redacted here")),
                    ast.Text("."),
                ]
            )
        ],
    )

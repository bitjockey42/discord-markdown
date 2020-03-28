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
        [ast.Paragraph([ast.Text("This is "), ast.BoldText(ast.Text("formatted"))])],
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
        [ast.Paragraph([ast.BoldText(ast.Text("formatted"))])],
        markdown=markdown,
    )


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
                    ast.ItalicText(ast.Text("am"), md_tag="_"),
                    ast.Text(" in the "),
                    ast.BoldText(ast.Text("light")),
                    ast.Text(" of "),
                    ast.BoldText(ast.ItalicText(ast.Text("day"))),
                ]
            ),
            ast.Paragraph([ast.Text("Let the storm rage on")]),
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("text", [("This is *formatted*"), ("This is _formatted_")])
def test_italic_text(text):
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [ast.Paragraph([ast.Text("This is "), ast.ItalicText(ast.Text("formatted"))])],
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
                    ast.UnderlineText(ast.Text("underlined")),
                    ast.Text(" example"),
                ]
            )
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_underline_italics_text(markdown):
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
                    ast.UnderlineText(ast.BoldText(ast.Text("underline bold"))),
                    ast.Text(" example"),
                ]
            )
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_multiple_formatted_text(markdown):
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
                [ast.Text("I "), ast.BoldText(ast.Text("am")), ast.Text(" depressed.")]
            ),
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_strikethrough_text(markdown):
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
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_inline_code(markdown):
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
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_code_block(markdown):
    text = """```markdown
    This **is** _meta_
    ```"""
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.CodeBlock(
                        ast.Text("\n    This **is** _meta_\n    "), md_tag="```markdown"
                    ),
                    ast.Text(""),
                ]
            )
        ],
        markdown=markdown,
    )


@pytest.mark.skip("FIXME")
@pytest.mark.parametrize("markdown", [False, True])
def test_inline_quote(markdown):
    text = "> This is _a_ quote.\nThis isn't part of it."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                ast.InlineQuote(
                    [
                        ast.Text(" This is "),
                        ast.ItalicText(ast.Text("a"), md_tag="_"),
                        ast.Text("quote."),
                    ]
                ),
            ),
            ast.Paragraph([ast.Text("This isn't part of it.")]),
        ],
        markdown=markdown,
    )


@pytest.mark.skip("FIXME")
@pytest.mark.parametrize("markdown", [False, True])
def test_block_quote(markdown):
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
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_spoiler_text(markdown):
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
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_multiline_formatted_text(markdown):
    text = "_This\nshould be parsed as\none line_."
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.ItalicText(
                        ast.Text("This\nshould be parsed as\none line"), md_tag="_"
                    ),
                    ast.Text("."),
                ]
            )
        ],
        markdown=markdown,
    )


@pytest.mark.parametrize("markdown", [False, True])
def test_complex_markup(markdown):
    text = load_file("discord.md")
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("["),
                    ast.ItalicText(
                        ast.Text("Tiger looks at Kalahan contemplatively"), md_tag="_"
                    ),
                    ast.Text("]"),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("Tiger: ["),
                    ast.ItalicText(ast.Text("quietly"), md_tag="_"),
                    ast.Text("] "),
                    ast.CodeBlock(
                        ast.Text("\n= Had only Bull not gotten to you first... ="),
                        md_tag="```asciidoc",
                    ),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("Tiger: "),
                    ast.CodeBlock(
                        ast.Text(
                            "\n= You may do so. I simply wish her safe in her den. But I cannot and will not force you to do anything. And my power in the physical plane is greatly limited without one to call me mentor. ="  # noqa
                        ),
                        md_tag="```asciidoc",
                    ),
                ]
            ),
        ],
        markdown=markdown,
    )

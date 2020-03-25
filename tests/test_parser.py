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


def test_bold_italics_text():
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
                    ast.ItalicText(ast.Text("am")),
                    ast.Text(" in the "),
                    ast.BoldText(ast.Text("light")),
                    ast.Text(" of "),
                    ast.BoldText(ast.ItalicText(ast.Text("day"))),
                ]
            ),
            ast.Paragraph([ast.Text("Let the storm rage on")]),
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
                [ast.Text("I "), ast.BoldText(ast.Text("am")), ast.Text(" depressed."),]
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
                [ast.CodeBlock(ast.Text("\n    This **is** _meta_\n    ")), ast.Text("")]
            )
        ],
    )


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


def test_annoying():
    text = "[_Tiger looks at Kalahan contemplatively_]\nTiger: [_quietly_] ```asciidoc\n= Had only Bull not gotten to you first... =```\nTiger: ```asciidoc\n= You may do so. I simply wish her safe in her den. But I cannot and will not force you to do anything. And my power in the physical plane is greatly limited without one to call me mentor. =```"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    assert_tree(parser.tree, [], markdown=True)
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("["),
                    ast.ItalicText(ast.Text("Tiger looks at Kalahan contemplatively")),
                    ast.Text("]"),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("Tiger: ["),
                    ast.ItalicText(ast.Text("quietly")),
                    ast.Text("]"),
                    ast.CodeBlock(
                        ast.Text("= Had only Bull not gotten to you first... =")
                    ),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("Tiger: "),
                    ast.CodeBlock(
                        ast.Text(
                            "= You may do so. I simply wish her safe in her den. But I cannot and will not force you to do anything. And my power in the physical plane is greatly limited without one to call me mentor. ="
                        )
                    ),
                ]
            ),
        ],
    )

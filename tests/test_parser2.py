import pytest

from discord_markdown.lexer import tokenize
from discord_markdown.parser import Parser
from discord_markdown import ast


def assert_tree(parser_tree, expected, markdown=False):
    assert [(node.eval(markdown), node.HTML_TAG) for node in parser_tree] == [
        (e.eval(markdown), e.HTML_TAG) for e in expected
    ]


def test_annoying():
    text = "[_Tiger looks at Kalahan contemplatively_]\nTiger: [_quietly_] ```asciidoc\n= Had only Bull not gotten to you first... =```\nTiger: ```asciidoc\n= You may do so. I simply wish her safe in her den. But I cannot and will not force you to do anything. And my power in the physical plane is greatly limited without one to call me mentor. =```"
    tokens = tokenize(text)
    parser = Parser(tokens)
    parser.parse()
    # assert_tree(parser.tree, [], markdown=True)
    assert_tree(
        parser.tree,
        [
            ast.Paragraph(
                [
                    ast.Text("["),
                    ast.ItalicText(ast.Text("Tiger looks at Kalahan contemplatively"), md_tag="_"),
                    ast.Text("]"),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("Tiger: ["),
                    ast.ItalicText(ast.Text("quietly"), md_tag="_"),
                    ast.Text("] "),
                    ast.CodeBlock(
                        ast.Text("= Had only Bull not gotten to you first... ="),
                        md_tag="```asciidoc"
                    ),
                ]
            ),
            ast.Paragraph(
                [
                    ast.Text("Tiger: "),
                    ast.CodeBlock(
                        ast.Text(
                            "= You may do so. I simply wish her safe in her den. But I cannot and will not force you to do anything. And my power in the physical plane is greatly limited without one to call me mentor. ="
                        ),
                        md_tag="```asciidoc"
                    ),
                ]
            ),
        ],
        markdown=True,
    )

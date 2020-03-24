import pytest

from discord_markdown.compiler import Compiler


@pytest.mark.parametrize(
    "markdown,expected", [(False, "<p>Simple example</p>"), (True, "Simple example"),]
)
def test_compile_simple(markdown, expected):
    text = "Simple example"
    compiler = Compiler(text)
    assert compiler.compile(markdown) == expected


@pytest.mark.parametrize(
    "markdown,expected",
    [
        (
            False,
            "<p>Here I <i>am</i> in the <b>light</b> of <b><i>day</i></b></p><p>Let the storm rage on</p>",
        ),
        (True, "Here I _am_ in the **light** of ***day***\nLet the storm rage on"),
    ],
)
def test_compile_formatted(markdown, expected):
    text = "Here I _am_ in the **light** of ***day***\nLet the storm rage on"
    compiler = Compiler(text)
    assert compiler.compile(markdown) == expected


def test_compile_code_block():
    text = """```sh
    echo test
    ```"""
    compiler = Compiler(text)
    assert compiler.compile() == "<p><pre><code>\n    echo test\n    </code></pre></p>"


def test_compile_block_quote():
    text = ">>> This is a quote.\nThis should be part of it."
    compiler = Compiler(text)
    assert (
        compiler.compile()
        == "<p><blockquote> This is a quote.\nThis should be part of it.</blockquote></p>"
    )


def test_compile_inline_quote():
    text = "> This is a quote.\nAnd this should not be part of it"
    compiler = Compiler(text)
    assert (
        compiler.compile()
        == "<p><q> This is a quote.</q></p><p>And this should not be part of it</p>"
    )

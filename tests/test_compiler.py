import pytest

from discord_markdown.compiler import Compiler


def test_compile_simple():
    text = "Simple example"
    compiler = Compiler(text)
    assert compiler.compile(markdown=False) == "<p>Simple example</p>"
    assert compiler.compile(markdown=True) == text


def test_compile_formatted():
    text = "Here I _am_ in the **light** of ***day***\nLet the storm rage on"
    compiler = Compiler(text)
    assert (
        compiler.compile(markdown=False)
        == "<p>Here I <i>am</i> in the <b>light</b> of <b><i>day</i></b></p><p>Let the storm rage on</p>"
    )
    assert compiler.compile(markdown=True) == text


def test_compile_code_block():
    text = """```sh
    echo test
    ```"""
    compiler = Compiler(text)
    assert (
        compiler.compile(markdown=False)
        == "<p><pre><code>\n    echo test\n    </code></pre></p>"
    )
    assert compiler.compile(markdown=True) == text


def test_compile_block_quote():
    text = ">>> This is a quote.\nThis should be part of it."
    compiler = Compiler(text)
    assert (
        compiler.compile(markdown=False)
        == "<p><blockquote> This is a quote.\nThis should be part of it.</blockquote></p>"
    )
    assert compiler.compile(markdown=True) == text


def test_compile_inline_quote():
    text = "> This is a quote.\nAnd this should not be part of it"
    compiler = Compiler(text)
    assert (
        compiler.compile()
        == "<p><q> This is a quote.</q></p><p>And this should not be part of it</p>"
    )
    assert compiler.compile(True) == text

from discord_markdown.compiler import Compiler


def test_compile_simple():
    text = "Simple example"
    compiler = Compiler(text)
    assert compiler.compile() == "Simple example"


def test_compile_formatted():
    text = "Here I _am_ in the **light** of ***day***\nLet the storm rage on"
    compiler = Compiler(text)
    assert (
        compiler.compile()
        == "Here I <i>am</i> in the <b>light</b> of <b><i>day</i></b>\nLet the storm rage on"
    )

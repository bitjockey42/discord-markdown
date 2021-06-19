from discord_markdown.lexer import tokenize, Token


def test_bold():
    text = "**Bold**"
    assert tokenize(text) == [
        Token("BOLD", value="**", line=1, column=0),
        Token("TEXT", value="Bold", line=1, column=2),
        Token("BOLD", value="**", line=1, column=6),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_bold_inline():
    text = "Is this **Bold**"
    assert tokenize(text) == [
        Token("TEXT", value="Is this ", line=1, column=0),
        Token("BOLD", value="**", line=1, column=8),
        Token("TEXT", value="Bold", line=1, column=10),
        Token("BOLD", value="**", line=1, column=14),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_italic():
    text = "_Italic_"
    assert tokenize(text) == [
        Token("ITALIC", value="_", line=1, column=0),
        Token("TEXT", value="Italic", line=1, column=1),
        Token("ITALIC", value="_", line=1, column=7),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_italic_alt():
    text = "*Italic*"
    assert tokenize(text) == [
        Token("ITALIC", value="*", line=1, column=0),
        Token("TEXT", value="Italic", line=1, column=1),
        Token("ITALIC", value="*", line=1, column=7),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_underline():
    text = "__Underline__"
    assert tokenize(text) == [
        Token("UNDERLINE", value="__", line=1, column=0),
        Token("TEXT", value="Underline", line=1, column=2),
        Token("UNDERLINE", value="__", line=1, column=11),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_strikethrough():
    text = "~~Strikethrough~~"
    assert tokenize(text) == [
        Token("STRIKETHROUGH", value="~~", line=1, column=0),
        Token("TEXT", value="Strikethrough", line=1, column=2),
        Token("STRIKETHROUGH", value="~~", line=1, column=15),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_bold_italic():
    text = "***Bold Italics***"
    assert tokenize(text) == [
        Token("BOLD_ITALIC", value="***", line=1, column=0),
        Token("TEXT", value="Bold Italics", line=1, column=3),
        Token("BOLD_ITALIC", value="***", line=1, column=15),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_underline_italic():
    text = "__*underline italics*__"
    assert tokenize(text) == [
        Token("UNDERLINE", value="__", line=1, column=0),
        Token("ITALIC", value="*", line=1, column=2),
        Token("TEXT", value="underline italics", line=1, column=3),
        Token("ITALIC", value="*", line=1, column=20),
        Token("UNDERLINE", value="__", line=1, column=21),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_underline_bold():
    text = "__**underline bold**__"
    assert tokenize(text) == [
        Token("UNDERLINE", value="__", line=1, column=0),
        Token("BOLD", value="**", line=1, column=2),
        Token("TEXT", value="underline bold", line=1, column=4),
        Token("BOLD", value="**", line=1, column=18),
        Token("UNDERLINE", value="__", line=1, column=20),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_underline_bold_italics():
    text = "__***underline bold italics***__"
    assert tokenize(text) == [
        Token("UNDERLINE", value="__", line=1, column=0),
        Token("BOLD_ITALIC", value="***", line=1, column=2),
        Token("TEXT", value="underline bold italics", line=1, column=5),
        Token("BOLD_ITALIC", value="***", line=1, column=27),
        Token("UNDERLINE", value="__", line=1, column=30),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_inline_code():
    text = "`**test_`"
    assert tokenize(text) == [
        Token("INLINE_CODE", value="`", line=1, column=0),
        Token("TEXT", value="**test_", line=1, column=1),
        Token("INLINE_CODE", value="`", line=1, column=8),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_code_block():
    text = """```markdown
    This is **meta** and should be ignored```"""
    assert tokenize(text) == [
        Token(type='CODE_BLOCK', value='```markdown\n    This is **meta** and should be ignored```', line=1, column=0),
        Token(type='TEXT', value='', line=1, column=57),
        Token(type='EOF', value='', line=2, column=57),
    ]


def test_spoiler():
    text = "this is a ||spoiler||"
    assert tokenize(text) == [
        Token("TEXT", value="this is a ", line=1, column=0),
        Token("SPOILER", value="||", line=1, column=10),
        Token("TEXT", value="spoiler", line=1, column=12),
        Token("SPOILER", value="||", line=1, column=19),
        Token("EOF", value="", line=1, column=len(text)),
    ]


def test_inline_quote():
    text = "> this is part of it\nThis should not be"
    assert tokenize(text) == [
        Token("INLINE_QUOTE", value=">", line=1, column=0),
        Token("TEXT", value=" this is part of it", line=1, column=1),
        Token("NEWLINE", value="\n", line=2, column=20),
        Token("TEXT", value="This should not be", line=2, column=0),
        Token("EOF", value="", line=2, column=len(text)),
    ]


def test_multiline_quote():
    text = ">>> This should all\n be part of it"
    assert tokenize(text) == [
        Token("BLOCK_QUOTE", value=">>>", line=1, column=0),
        Token("TEXT", value=" This should all", line=1, column=3),
        Token("NEWLINE", value="\n", line=2, column=19),
        Token("TEXT", value=" be part of it", line=2, column=0),
        Token("EOF", value="", line=2, column=len(text)),
    ]

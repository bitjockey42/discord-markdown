from .spec import TokenSpecification


class NestedElement:
    HTML_TAG = ""
    MD_TAG = ""
    HAS_CLOSE_MD_TAG = True
    NAME = ""

    def __init__(self, elements=None, md_tag=None):
        if elements is None:
            elements = []
        self.elements = elements
        if md_tag is None:
            md_tag = self.MD_TAG
        self.md_tag = md_tag
        self.terminate = False

    def __add__(self, other):
        self.elements.append(other)
        return self

    def open(self, markdown=False):
        if markdown:
            return self.md_tag
        else:
            return f"<{self.HTML_TAG}>"

    def close(self, markdown=False):
        if markdown:
            return self.MD_TAG if self.HAS_CLOSE_MD_TAG else ""
        else:
            return f"</{self.HTML_TAG}>"

    def eval(self, markdown=False):
        evaluated = "".join([elem.eval(markdown) for elem in self.elements])
        return f"{self.open(markdown)}{evaluated}{self.close(markdown)}"


class Paragraph(NestedElement):
    HTML_TAG = "p"
    MD_TAG = "\n"

    def open(self, markdown=False):
        if markdown:
            return ""
        else:
            return f"<{self.HTML_TAG}>"


class Text:
    HTML_TAG = None
    MD_TAG = None
    NAME = TokenSpecification.TEXT.name

    def __init__(self, value=None, md_tag=None, style=None):
        self.value = value
        self.md_tag = None
        self.style = style

    def __add__(self, other):
        new_value = self.value + other.value
        return Text(new_value, self.md_tag, self.style)

    def eval(self, markdown=False):
        return self.value


class FormattedText(NestedElement):
    HTML_TAG = ""
    MD_TAG = ""
    HAS_CLOSE_MD_TAG = True
    NAME = ""

    def __init__(self, elements=None, md_tag=None, style=None):
        super().__init__(elements=elements, md_tag=md_tag)
        self.style = style

    def open(self, markdown=False):
        if markdown:
            open_tag = self.md_tag
        else:
            if self.style:
                open_tag = f"<{self.HTML_TAG} style='{self.style}'>"
            else:
                open_tag = f"<{self.HTML_TAG}>"
        return open_tag

    def close(self, markdown=False):
        if markdown:
            close_tag = self.md_tag if self.HAS_CLOSE_MD_TAG else ""
        else:
            close_tag = f"</{self.HTML_TAG}>"
        return close_tag


class CodeBlock(NestedElement):
    HTML_TAG = "code"
    MD_TAG = "```"
    NAME = TokenSpecification.CODE_BLOCK.name

    def open(self, markdown=False):
        if markdown:
            open_tag = self.md_tag
        else:
            close_tag = f"<pre><{self.HTML_TAG}>"

    def close(self, markdown=False):
        if markdown:
            close_tag = self.MD_TAG
        else:
            close_tag = f"</{self.HTML_TAG}></pre>"
        return close_tag


class BoldText(FormattedText):
    HTML_TAG = "b"
    MD_TAG = "**"
    NAME = TokenSpecification.BOLD.name


class ItalicText(FormattedText):
    HTML_TAG = "i"
    MD_TAG = "*"
    NAME = TokenSpecification.ITALIC.name


class UnderlineText(FormattedText):
    HTML_TAG = "u"
    MD_TAG = "__"
    NAME = TokenSpecification.UNDERLINE.name


class StrikethroughText(FormattedText):
    HTML_TAG = "s"
    MD_TAG = "~~"
    NAME = TokenSpecification.STRIKETHROUGH.name


class InlineCode(FormattedText):
    HTML_TAG = "code"
    MD_TAG = "`"
    NAME = TokenSpecification.INLINE_CODE.name


class InlineQuote(NestedElement):
    HTML_TAG = "q"
    MD_TAG = ">"
    HAS_CLOSE_MD_TAG = False
    NAME = TokenSpecification.INLINE_QUOTE.name


class BlockQuote(NestedElement):
    HTML_TAG = "blockquote"
    MD_TAG = ">>>"
    HAS_CLOSE_MD_TAG = False
    NAME = TokenSpecification.BLOCK_QUOTE.name


class SpoilerText(FormattedText):
    HTML_TAG = "span"
    MD_TAG = "||"
    NAME = TokenSpecification.SPOILER.name

    def __init__(self, value, md_tag=None, style="color: black; background: black;"):
        super().__init__(value, md_tag=md_tag, style=style)


AST_BY_TOKEN_TYPE = {
    TokenSpecification.TEXT.name: Text,
    TokenSpecification.BOLD.name: BoldText,
    TokenSpecification.ITALIC.name: ItalicText,
    TokenSpecification.UNDERLINE.name: UnderlineText,
    TokenSpecification.STRIKETHROUGH.name: StrikethroughText,
    TokenSpecification.BLOCK_QUOTE.name: BlockQuote,
    TokenSpecification.INLINE_QUOTE.name: InlineQuote,
    TokenSpecification.CODE_BLOCK.name: CodeBlock,
    TokenSpecification.INLINE_CODE.name: InlineCode,
    TokenSpecification.SPOILER.name: SpoilerText,
}

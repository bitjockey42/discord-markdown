from .spec import TokenSpecification


class Paragraph:
    HTML_TAG = "p"

    def __init__(self, elements):
        self.elements = elements

    def eval(self, markdown=False):
        evaluated = "".join([elem.eval() for elem in self.elements])
        return f"<{self.HTML_TAG}>{evaluated}</{self.HTML_TAG}>"


class Text:
    HTML_TAG = None

    def __init__(self, value, style=None):
        self.value = value
        self.style = style

    def eval(self, markdown=False):
        return self.value


class FormattedText(Text):
    HTML_TAG = ""
    MD_TAG = ""

    def open(self, markdown=False):
        if markdown:
            open_tag = self.HTML_TAG
        else:
            if self.style:
                open_tag = f"<{self.HTML_TAG} style='{self.style}'>"
            else:
                open_tag = f"<{self.HTML_TAG}>"
        return open_tag

    def close(self, markdown=False):
        return f"</{self.HTML_TAG}>" if self.HTML_TAG else ""

    def eval(self, markdown=False):
        return f"{self.open(markdown)}{self.value.eval(markdown)}{self.close(markdown)}"


class ParagraphText(FormattedText):
    HTML_TAG = "p"


class BoldText(FormattedText):
    HTML_TAG = "b"


class ItalicText(FormattedText):
    HTML_TAG = "i"


class UnderlineText(FormattedText):
    HTML_TAG = "u"


class StrikethroughText(FormattedText):
    HTML_TAG = "s"


class InlineCode(FormattedText):
    HTML_TAG = "code"


class CodeBlock(FormattedText):
    HTML_TAG = "code"

    def eval(self, markdown=False):
        return f"<pre>{self.open(markdown)}{self.value.eval(markdown)}{self.close(markdown)}</pre>"


class InlineQuote(FormattedText):
    HTML_TAG = "q"


class BlockQuote(FormattedText):
    HTML_TAG = "blockquote"


class SpoilerText(FormattedText):
    HTML_TAG = "span"

    def __init__(self, value, style="color: black; background: black;"):
        super().__init__(value, style=style)


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

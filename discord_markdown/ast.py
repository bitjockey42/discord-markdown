from .spec import TokenSpecification


class Paragraph:
    HTML_TAG = "p"

    def __init__(self, elements):
        self.elements = elements

    def open(self, markdown=False):
        if markdown:
            return ""
        else:
            return f"<{self.HTML_TAG}>"

    def close(self, markdown=False):
        if markdown:
            return "\n"
        else:
            return f"</{self.HTML_TAG}>"

    def eval(self, markdown=False):
        evaluated = "".join([elem.eval(markdown) for elem in self.elements])
        return f"{self.open(markdown)}{evaluated}{self.close(markdown)}"


class Text:
    HTML_TAG = None
    MD_TAG = None

    def __init__(self, value, md_tag=None, style=None):
        self.value = value
        self.md_tag = None
        self.style = style

    def eval(self, markdown=False):
        return self.value


class FormattedText(Text):
    HTML_TAG = ""
    MD_TAG = ""
    HAS_CLOSE_MD_TAG = True

    def __init__(self, value, md_tag=None, style=None):
        super().__init__(value, style=style)
        if md_tag is None:
            md_tag = self.MD_TAG
        self.md_tag = md_tag

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

    def eval(self, markdown=False):
        return f"{self.open(markdown)}{self.value.eval(markdown)}{self.close(markdown)}"


class ParagraphText(FormattedText):
    HTML_TAG = "p"
    MD_TAG = "\n"


class BoldText(FormattedText):
    HTML_TAG = "b"
    MD_TAG = "**"


class ItalicText(FormattedText):
    HTML_TAG = "i"
    MD_TAG = "*"


class UnderlineText(FormattedText):
    HTML_TAG = "u"
    MD_TAG = "__"


class StrikethroughText(FormattedText):
    HTML_TAG = "s"
    MD_TAG = "~~"


class InlineCode(FormattedText):
    HTML_TAG = "code"
    MD_TAG = "`"


class CodeBlock(FormattedText):
    HTML_TAG = "code"
    MD_TAG = "```"

    def close(self, markdown=False):
        if markdown:
            close_tag = self.MD_TAG
        else:
            close_tag = f"</{self.HTML_TAG}>"
        return close_tag

    def eval(self, markdown=False):
        evaluated = (
            f"{self.open(markdown)}{self.value.eval(markdown)}{self.close(markdown)}"
        )
        if markdown:
            return evaluated
        else:
            return f"<pre>{evaluated}</pre>"


class InlineQuote(FormattedText):
    HTML_TAG = "q"
    MD_TAG = ">"
    HAS_CLOSE_MD_TAG = False


class BlockQuote(FormattedText):
    HTML_TAG = "blockquote"
    MD_TAG = ">>>"
    HAS_CLOSE_MD_TAG = False


class SpoilerText(FormattedText):
    HTML_TAG = "span"
    MD_TAG = "||"

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

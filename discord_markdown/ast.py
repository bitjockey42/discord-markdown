class Text:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class FormattedText(Text):
    HTML_TAG = ""

    @property
    def open(self):
        return f"<{self.HTML_TAG}>"

    @property
    def close(self):
        return f"</{self.HTML_TAG}>"

    def eval(self):
        return f"{self.open}{self.value.eval()}{self.close}"


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

    def eval(self):
        return f"<pre>{self.open}{self.value.eval()}{self.close}</pre>"

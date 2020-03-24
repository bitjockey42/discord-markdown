# Discord Markdown

I needed to render some Discord chat logs as HTML, and found that the Markdown implementation in Discord isn't quite compliant with Common Markdown as Discord uses a simplified version. 

So I wrote this library that allows you to convert a discord message written in the Markdown formatting syntax specified [here](https://support.discordapp.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-) to html.


## Installation

You can install the library from `pypi`:

```sh
pip install discord-markdown
```

## Usage

```python
from discord_markdown.discord_markdown import convert_to_html

text = "_This_ **is** an __example__.\nThis should be a different paragraph."
html = convert_to_html(text)

assert html == '<p><i>This</i> <b>is</b> an <u>example</u>.</p><p>This should be a different paragraph.</p>'
```

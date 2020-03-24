# Discord Markdown

I needed to parse some Discord chat logs for something, and found that the Markdown implementation isn't compliant with Common Markdown as Discord uses a simplified version.

This is very early stage and probably won't be ready for use for awhile.

```python
from discord_markdown.discord_markdown import convert_to_html

convert_to_html("_This_ **is** an __example__.\nThis should be a different paragraph.")
```

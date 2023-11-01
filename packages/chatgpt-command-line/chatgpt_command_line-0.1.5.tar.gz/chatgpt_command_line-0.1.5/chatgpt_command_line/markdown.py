from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.rules_inline.linkify import linkify
from pygments import highlight
from pygments.formatters import \
    HtmlFormatter  # pylint: disable=no-name-in-module
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name


def highlight_code(code: str, lang: str, _options: dict) -> str:
    if not lang:
        lexer = get_lexer_by_name("md")
    lexer = get_lexer_by_name(lang)
    style = get_style_by_name("monokai")
    formatter = HtmlFormatter(style=style)
    return highlight(code, lexer, formatter)

CSS = """
<style>
@import url("https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.min.css");
@import url("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/styles/github.min.css");
.markdown-body {img {max-width: 8rem!important;}}
::-webkit-scrollbar-track {
  border-radius: 10px;
  background-color: #f5f5f5;
}
::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-image: linear-gradient(to bottom, #8f8f8f, #e6e6e6);
  border: 3px solid #f5f5f5;
}
::-webkit-scrollbar-thumb:hover {
  background-image: linear-gradient(to bottom, #737373, #bfc1c2);
}
</style>
"""
JS = """<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
"""
def render_markdown(markdown: str) -> str:
    markdownit = MarkdownIt(
        "js-default",
        {
            "html": True,
            "typographer": True,
            "highlight": highlight_code,
            "renderer": RendererHTML(),
        },
    )
    return CSS+ markdownit.render(markdown) +JS

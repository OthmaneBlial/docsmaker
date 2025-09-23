"""Markdown parsing with MarkdownIt and plugins."""

import re
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.attrs import attrs_plugin

try:
    from mdit_py_plugins.table import table_plugin as _TABLE_PLUGIN
except Exception:
    try:
        from mdit_py_plugins.tables import tables_plugin as _TABLE_PLUGIN
    except Exception:
        _TABLE_PLUGIN = None


class Parser:
    """Markdown parser using MarkdownIt."""

    def __init__(self):
        """Initialize the parser with plugins."""
        self.md = (
            MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": True})
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .use(tasklists_plugin, enabled=True)
            .use(deflist_plugin)
            .use(attrs_plugin)
        )
        # markdown-it ships a "table" rule that is disabled in the CommonMark preset
        # by default, so opt in explicitly to ensure GitHub-style tables render.
        self.md.enable("table")
        if _TABLE_PLUGIN:
            self.md.use(_TABLE_PLUGIN)  # GFM tables

    def parse(self, md_src: str) -> str:
        """Parse Markdown source to HTML."""
        tokens = self.md.parse(md_src)

        # Heading ids + .md links -> .html
        for i, t in enumerate(tokens):
            if t.type == "inline" and t.children:
                # add id to the previous heading_open
                if i > 0 and tokens[i-1].type == "heading_open":
                    text_parts = []
                    for ch in t.children:
                        if ch.type in ("text", "code_inline"):
                            text_parts.append(ch.content)
                    slug = self._github_slug("".join(text_parts))
                    tokens[i-1].attrSet("id", slug)  # anchor without visible symbol

                # rewrite links *.md -> *.html
                for ch in t.children:
                    if ch.type == "link_open":
                        href = ch.attrGet("href") or ""
                        if href.endswith(".md") or ".md#" in href:
                            ch.attrSet("href", href.replace(".md", ".html", 1))

        html = self.md.renderer.render(tokens, self.md.options, {})

        # Prism line numbers. Also force plaintext when language is missing.
        html = html.replace("<pre><code", '<pre class="line-numbers"><code')
        html = re.sub(
            r'(<pre class="line-numbers"><code)(?![^>]*class="language-")',
            r'\1 class="language-none"',
            html,
            flags=re.I,
        )
        return html

    def _github_slug(self, text: str) -> str:
        """Generate GitHub-style slug from text."""
        s = re.sub(r"[^\w\- ]+", "", text.lower()).strip().replace(" ", "-")
        return re.sub(r"-{2,}", "-", s) or "section"

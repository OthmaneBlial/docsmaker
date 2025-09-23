"""Site building logic."""

import json
import re
import shutil
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .config import Config
from .parser import Parser
from .utils import ensure, read, title_from_md, humanize, collect_headings


class Page:
    """Represents a documentation page."""

    def __init__(self, stem: str, md_path: Path, html: str, title: str, emoji: str, label: str, content: str, toc_items: List):
        self.stem = stem
        self.md = md_path.name
        self.html = html
        self.title = title
        self.emoji = emoji
        self.label = label
        self.content = content
        self.toc_items = toc_items


class Builder:
    """Orchestrates the site building process."""

    def __init__(self, config: Config, parser: Parser):
        self.config = config
        self.parser = parser
        self.pages: List[Page] = []
        self.theme_path = Path("themes") / self.config.theme
        self.theme_config = self._load_theme_config()
        # Build template search paths for inheritance
        template_paths = []
        current_path = self.theme_path
        visited = set()
        while current_path and str(current_path) not in visited:
            visited.add(str(current_path))
            templates_path = current_path / "templates"
            if templates_path.exists():
                template_paths.append(str(templates_path))
                extends = self._get_theme_extends(current_path)
                if extends:
                    current_path = Path("themes") / extends
                else:
                    current_path = None
            else:
                current_path = None
        # Enable autoescaping to avoid accidentally rendering unsafe HTML via templates
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_paths),
            autoescape=select_autoescape(("html", "xml")),
        )

    def _load_theme_config(self) -> Dict[str, Any]:
        """Load theme configuration with inheritance."""
        config = {}
        current_path = self.theme_path
        visited = set()
        while current_path and str(current_path) not in visited:
            visited.add(str(current_path))
            config_path = current_path / "config.yaml"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    theme_config = yaml.safe_load(f) or {}
                    # Merge, with current overriding base
                    config.update(theme_config)
                    extends = theme_config.get('extends')
                    if extends:
                        current_path = Path("themes") / extends
                    else:
                        current_path = None
            else:
                current_path = None
        return config

    def _get_theme_extends(self, theme_path: Path) -> Optional[str]:
        """Get the extends value from theme config."""
        config_path = theme_path / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                theme_config = yaml.safe_load(f) or {}
                return theme_config.get('extends')
        return None

    def build(self) -> None:
        """Build the documentation site."""
        docs_path = self.config.get_docs_path()
        out_path = self.config.get_out_path()

        if not docs_path.exists():
            raise SystemExit(f"docs/ not found: {docs_path}")

        if not self.theme_path.exists():
            raise SystemExit(f"Theme '{self.config.theme}' not found: {self.theme_path}")

        ensure(out_path)

        # Collect and sort Markdown files based on navigation
        md_files = self._collect_md_files(docs_path)
        if not md_files:
            raise SystemExit("no .md files in docs/")

        # Copy non-md assets and theme assets
        self._copy_assets(docs_path, out_path)
        self._copy_theme_assets(out_path)

        # Parse pages
        self.pages = []
        for md_path in md_files:
            md_content = read(md_path)
            html_content = self.parser.parse(md_content)
            title = title_from_md(md_content, humanize(md_path.stem))
            emoji, label = self._get_icon_and_label(md_path.stem, title)
            toc_items = collect_headings(html_content)
            page = Page(
                stem=md_path.stem,
                md_path=md_path,
                html=f"{md_path.stem}.html",
                title=title,
                emoji=emoji,
                label=label,
                content=html_content,
                toc_items=toc_items
            )
            self.pages.append(page)

        # Generate search index
        if self.config.enable_search:
            self._generate_search_index(out_path)

        # Write pages
        for i, page in enumerate(self.pages):
            self._write_page(out_path, page, i)

        # Write 404 page
        self._write_404_page(out_path)

        print(f"OK: {len(self.pages)} pages -> {out_path}/")

    def _collect_md_files(self, docs_path: Path) -> List[Path]:
        """Collect and sort Markdown files based on navigation config."""
        md_files = list(docs_path.glob("*.md"))
        if not self.config.navigation:
            # Default sorting
            order_first = ["index", "installation", "usage", "api", "examples", "faq", "changelog", "contributing"]
            return sorted(md_files, key=lambda p: (order_first.index(p.stem) if p.stem in order_first else 999, p.stem))

        # Sort based on navigation order
        nav_files = {item.file: idx for idx, item in enumerate(self.config.navigation)}
        return sorted(md_files, key=lambda p: nav_files.get(p.name, 999))

    def _get_icon_and_label(self, stem: str, title: str) -> tuple:
        """Get icon and label for a page."""
        if self.config.navigation:
            for item in self.config.navigation:
                if item.file == f"{stem}.md":
                    return item.icon, item.title
        # Fallback
        return "📄", title

    def _copy_assets(self, docs_path: Path, out_path: Path) -> None:
        """Copy non-markdown assets."""
        assets = out_path / "assets"
        for p in docs_path.rglob("*"):
            if p.is_file() and p.suffix.lower() != ".md":
                dst = assets / p.relative_to(docs_path)
                ensure(dst.parent)
                shutil.copy2(p, dst)

    def _copy_theme_assets(self, out_path: Path) -> None:
        """Copy theme assets with inheritance."""
        assets = out_path / "assets"
        current_path = self.theme_path
        visited = set()
        while current_path and str(current_path) not in visited:
            visited.add(str(current_path))
            theme_assets = current_path / "assets"
            if theme_assets.exists():
                for p in theme_assets.rglob("*"):
                    if p.is_file():
                        dst = assets / p.relative_to(theme_assets)
                        ensure(dst.parent)
                        # Don't overwrite if already exists (child takes precedence)
                        if not dst.exists():
                            shutil.copy2(p, dst)
                extends = self._get_theme_extends(current_path)
                if extends:
                    current_path = Path("themes") / extends
                else:
                    current_path = None
            else:
                current_path = None

    def _generate_search_index(self, out_path: Path) -> None:
        """Generate search index JSON."""
        idx = []
        for pg in self.pages:
            txt = re.sub(r"<[^>]+>", " ", pg.content)
            txt = re.sub(r"\s+", " ", txt).strip()
            idx.append({"title": pg.title, "url": pg.html, "content": txt[:2000]})
        (out_path / "search-index.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")

    def _write_page(self, out_path: Path, page: Page, index: int) -> None:
        """Write a single page."""
        prev_url = self.pages[index-1].html if index > 0 else None
        next_url = self.pages[index+1].html if index < len(self.pages)-1 else None
        sidebar = self._generate_sidebar(page.html)
        toc = self._generate_toc(page.toc_items)
        html_content = self._generate_html(page.title, sidebar, page.content, toc, prev_url, next_url)
        (out_path / page.html).write_text(html_content, encoding="utf-8")

    def _write_404_page(self, out_path: Path) -> None:
        """Write 404 page."""
        sidebar = self._generate_sidebar("")
        html_content = self._generate_html("Not Found", sidebar, "<h2>Not Found</h2><p>Use the sidebar to open a page.</p>", "<div></div>", None, None)
        (out_path / "404.html").write_text(html_content, encoding="utf-8")

    def _generate_sidebar(self, current_html: str) -> str:
        """Generate sidebar HTML."""
        items = []
        for p in self.pages:
            active = (p.html == current_html)
            cls = "item active" if active else "item"
            items.append(f'<li><a href="{p.html}" class="{cls}"><span class="emoji">{p.emoji}</span><span>{p.label}</span></a></li>')
        template = self.jinja_env.get_template("sidebar.html")
        return template.render(
            items="\n".join(items),
            site_name=self.config.site_name,
            **self.theme_config
        )

    def _generate_toc(self, toc_items: List) -> str:
        """Generate table of contents HTML."""
        if not toc_items:
            return "<div>No headings</div>"
        toc_html = []
        for level, hid, text in toc_items:
            indent = (level-1)*12
            toc_html.append(f'<div style="margin-left:{indent}px"><a class="u" href="#{hid}">{text}</a></div>')
        return "\n".join(toc_html)

    def _generate_html(self, title: str, sidebar: str, content: str, toc: str, prev_url: Optional[str], next_url: Optional[str]) -> str:
        """Generate full HTML page."""
        prev_link = f'<a href="{prev_url}" class="u">← Previous</a>' if prev_url else '<span class="muted">← Previous</span>'
        next_link = f'<a href="{next_url}" class="u">Next →</a>' if next_url else '<span class="muted">Next →</span>'
        template = self.jinja_env.get_template("base.html")
        return template.render(
            title=title,
            site_name=self.config.site_name,
            sidebar=sidebar,
            content=content,
            toc=toc,
            prev_link=prev_link,
            next_link=next_link,
            **self.theme_config
        )

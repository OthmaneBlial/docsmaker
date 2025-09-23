"""Utility functions for Docsmaker."""

import re
from pathlib import Path
from typing import List, Tuple


def ensure(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)


def read(path: Path) -> str:
    """Read file content as string."""
    return path.read_text(encoding="utf-8")


def title_from_md(md: str, fallback: str) -> str:
    """Extract title from Markdown content."""
    H_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", re.M)
    m = H_RE.search(md)
    return m.group(2).strip() if m else fallback


def humanize(stem: str) -> str:
    """Humanize a filename stem."""
    return stem.replace("_", " ").title()


def github_slug(text: str) -> str:
    """Generate GitHub-style slug from text."""
    s = re.sub(r"[^\w\- ]+", "", text.lower()).strip().replace(" ", "-")
    return re.sub(r"-{2,}", "-", s) or "section"


def collect_headings(html: str) -> List[Tuple[int, str, str]]:
    """Collect headings from HTML content."""
    items = re.findall(r"<h([1-3])\s+[^>]*id=\"([^\"]+)\"[^>]*>(.*?)</h\1>", html, flags=re.I | re.S)
    def _strip_tags(source: str) -> str:
        return re.sub(r"<[^>]+>", "", source).strip()

    return [(int(lvl), hid, _strip_tags(txt)) for lvl, hid, txt in items]


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return github_slug(text)

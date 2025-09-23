from docsmaker.parser import Parser


class TestParser:
    def test_parser_initialization(self):
        parser = Parser()
        assert parser.md is not None

    def test_parse_basic_markdown(self, parser, sample_markdown):
        html = parser.parse(sample_markdown)
        assert "<h1" in html
        assert "Hello World" in html
        assert "<h2" in html
        assert "Section 1" in html
        assert "<ul>" in html
        assert "<li>" in html
        assert "<code" in html
        assert "def hello():" in html

    def test_parse_heading_with_id(self, parser):
        md = "# My Heading\n\nContent"
        html = parser.parse(md)
        assert 'id="my-heading"' in html

    def test_parse_markdown_links_conversion(self, parser):
        md = "[Link](page.md)"
        html = parser.parse(md)
        assert 'href="page.html"' in html

    def test_parse_markdown_links_with_anchor(self, parser):
        md = "[Link](page.md#section)"
        html = parser.parse(md)
        assert 'href="page.html#section"' in html

    def test_parse_code_blocks_with_line_numbers(self, parser):
        md = "```\ncode\n```"
        html = parser.parse(md)
        assert 'class="line-numbers"' in html

    def test_parse_code_blocks_without_language(self, parser):
        md = "```\ncode\n```"
        html = parser.parse(md)
        assert 'class="language-none"' in html

    def test_parse_code_blocks_with_language(self, parser):
        md = "```python\ndef hello():\n    pass\n```"
        html = parser.parse(md)
        assert 'class="language-python"' in html

    def test_github_slug_generation(self, parser):
        # Test the private method via parse
        md = "# Hello World! @#$%\n\nContent"
        html = parser.parse(md)
        assert 'id="hello-world"' in html

    def test_github_slug_empty(self, parser):
        md = "# @#$%\n\nContent"
        html = parser.parse(md)
        assert 'id="section"' in html

    def test_parse_front_matter(self, parser):
        md = """---
title: Test
---

# Content
"""
        html = parser.parse(md)
        # Front matter should be parsed but not in output HTML
        assert "Content" in html
        assert "title: Test" not in html

    def test_parse_tasklists(self, parser):
        md = "- [x] Done\n- [ ] Todo"
        html = parser.parse(md)
        assert 'type="checkbox"' in html
        assert "checked" in html

    def test_parse_definition_lists(self, parser):
        md = "Term\n: Definition"
        html = parser.parse(md)
        assert "<dl>" in html
        assert "<dt>Term</dt>" in html
        assert "<dd>Definition</dd>" in html

import json
from pathlib import Path
from docsmaker.builder import Builder, Page
from docsmaker.config import Config


class TestPage:
    def test_page_creation(self):
        page = Page(
            stem="index",
            md_path=Path("docs/index.md"),
            html="index.html",
            title="Index",
            emoji="📖",
            label="Home",
            content="<h1>Index</h1>",
            toc_items=[(1, "index", "Index")]
        )
        assert page.stem == "index"
        assert page.html == "index.html"
        assert page.title == "Index"
        assert page.emoji == "📖"
        assert page.label == "Home"


class TestBuilder:
    def test_builder_initialization(self, sample_config, parser):
        builder = Builder(sample_config, parser)
        assert builder.config == sample_config
        assert builder.parser == parser
        assert builder.pages == []
        assert builder.theme_path == Path("themes") / "default"

    def test_load_theme_config(self, sample_config, parser, mocker):
        mocker.patch('pathlib.Path.exists', return_value=True)
        mocker.patch('builtins.open', mocker.mock_open(read_data="extends: base\ntheme_color: blue\n"))
        mocker.patch('yaml.safe_load', return_value={"extends": "base", "theme_color": "blue"})

        builder = Builder(sample_config, parser)
        config = builder._load_theme_config()
        assert config == {"extends": "base", "theme_color": "blue"}

    def test_get_theme_extends(self, tmp_path, sample_config, parser, mocker):
        theme_path = tmp_path / "themes" / "test"
        theme_path.mkdir(parents=True)
        config_file = theme_path / "config.yaml"
        config_file.write_text("extends: base\n")

        builder = Builder(sample_config, parser)
        extends = builder._get_theme_extends(theme_path)
        assert extends == "base"

    def test_collect_md_files_no_navigation(self, sample_config, parser, sample_docs_dir):
        builder = Builder(sample_config, parser)
        files = builder._collect_md_files(sample_docs_dir)
        assert len(files) == 2  # index.md and another.md
        assert any(f.name == "index.md" for f in files)

    def test_collect_md_files_with_navigation(self, parser, sample_docs_dir):
        config = Config(
            site_name="Test",
            docs_dir="docs",
            out_dir="site",
            navigation=[
                {"icon": "📖", "title": "Another", "file": "another.md"},
                {"icon": "🏠", "title": "Index", "file": "index.md"}
            ]
        )
        builder = Builder(config, parser)
        files = builder._collect_md_files(sample_docs_dir)
        assert files[0].name == "another.md"
        assert files[1].name == "index.md"

    def test_get_icon_and_label_from_navigation(self, sample_config, parser):
        builder = Builder(sample_config, parser)
        emoji, label = builder._get_icon_and_label("index", "Index Page")
        assert emoji == "📖"
        assert label == "Home"

    def test_get_icon_and_label_fallback(self, parser):
        config = Config(site_name="Test", docs_dir="docs", out_dir="site")
        builder = Builder(config, parser)
        emoji, label = builder._get_icon_and_label("unknown", "Unknown Page")
        assert emoji == "📄"
        assert label == "Unknown Page"

    def test_generate_search_index(self, tmp_path, sample_config, parser, mocker):
        builder = Builder(sample_config, parser)
        builder.pages = [
            Page("index", Path("index.md"), "index.html", "Index", "📖", "Home", "<h1>Index</h1>", []),
            Page("page", Path("page.md"), "page.html", "Page", "📄", "Page", "<h2>Page</h2>", [])
        ]

        out_path = tmp_path / "site"
        out_path.mkdir()

        builder._generate_search_index(out_path)

        index_file = out_path / "search-index.json"
        assert index_file.exists()
        data = json.loads(index_file.read_text())
        assert len(data) == 2
        assert data[0]["title"] == "Index"
        assert data[0]["url"] == "index.html"

    def test_generate_toc(self, sample_config, parser):
        builder = Builder(sample_config, parser)
        toc_items = [(1, "heading1", "Heading 1"), (2, "heading2", "Heading 2")]
        toc_html = builder._generate_toc(toc_items)
        assert "heading1" in toc_html
        assert "Heading 1" in toc_html
        assert 'margin-left:0px' in toc_html
        assert 'margin-left:12px' in toc_html

    def test_generate_toc_empty(self, sample_config, parser):
        builder = Builder(sample_config, parser)
        toc_html = builder._generate_toc([])
        assert "No headings" in toc_html

    def test_generate_sidebar(self, sample_config, parser, mocker):
        builder = Builder(sample_config, parser)
        builder.pages = [
            Page("index", Path("index.md"), "index.html", "Index", "📖", "Home", "", []),
        ]
        builder.jinja_env = mocker.MagicMock()
        template = mocker.MagicMock()
        template.render.return_value = "<sidebar>content</sidebar>"
        builder.jinja_env.get_template.return_value = template

        sidebar = builder._generate_sidebar("index.html")
        assert sidebar == "<sidebar>content</sidebar>"
        template.render.assert_called_once()

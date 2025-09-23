import json
from pathlib import Path
from docsmaker.config import Config
from docsmaker.parser import Parser
from docsmaker.builder import Builder


class TestFullBuildProcess:
    def test_full_build_with_sample_docs(self, tmp_path, sample_docs_dir, monkeypatch):
        # Create a minimal theme
        theme_dir = tmp_path / "themes" / "default"
        theme_dir.mkdir(parents=True)
        config_yaml = theme_dir / "config.yaml"
        config_yaml.write_text("theme_color: blue\n")

        templates_dir = theme_dir / "templates"
        templates_dir.mkdir()
        base_html = templates_dir / "base.html"
        base_html.write_text("""
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ site_name }}</h1>
    {{ sidebar }}
    {{ content }}
    {{ toc }}
    {{ prev_link }} {{ next_link }}
</body>
</html>
""")

        sidebar_html = templates_dir / "sidebar.html"
        sidebar_html.write_text("""
<div class="sidebar">
    <h2>{{ site_name }}</h2>
    {{ items }}
</div>
""")

        # Change to tmp_path so themes are found
        monkeypatch.chdir(tmp_path)

        # Load config
        config_path = sample_docs_dir / "conf.yaml"
        config = Config.from_yaml(config_path)

        # Override paths
        config.docs_dir = str(sample_docs_dir)
        config.out_dir = "output"

        parser = Parser()
        builder = Builder(config, parser)

        # Build
        builder.build()

        # Check output
        out_path = Path("output")
        assert out_path.exists()

        # Check HTML files
        index_html = out_path / "index.html"
        assert index_html.exists()
        content = index_html.read_text()
        assert "<h1>Test Docs</h1>" in content
        assert "Welcome to the docs" in content

        another_html = out_path / "another.html"
        assert another_html.exists()
        content = another_html.read_text()
        assert "Hello World" in content

        # Check 404
        not_found_html = out_path / "404.html"
        assert not_found_html.exists()

        # Check search index
        search_index = out_path / "search-index.json"
        assert search_index.exists()
        data = json.loads(search_index.read_text())
        assert len(data) == 2
        assert data[0]["title"] == "Index"

        # Check assets directory state (themes may or may not ship assets)
        assets_dir = out_path / "assets"
        assert not assets_dir.exists() or assets_dir.is_dir()

    def test_build_with_navigation_ordering(self, tmp_path):
        # Create docs with navigation
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        # Create files
        (docs_dir / "page1.md").write_text("# Page 1\n\nContent 1")
        (docs_dir / "page2.md").write_text("# Page 2\n\nContent 2")
        (docs_dir / "index.md").write_text("# Index\n\nIndex content")

        # Config with navigation
        config_data = {
            "site_name": "Test",
            "docs_dir": "docs",
            "out_dir": "site",
            "navigation": [
                {"icon": "1️⃣", "title": "Page 1", "file": "page1.md"},
                {"icon": "2️⃣", "title": "Page 2", "file": "page2.md"},
                {"icon": "🏠", "title": "Home", "file": "index.md"}
            ]
        }
        config_path = docs_dir / "conf.yaml"
        import yaml
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f)

        # Create minimal theme
        theme_dir = tmp_path / "themes" / "default"
        theme_dir.mkdir(parents=True)
        (theme_dir / "config.yaml").write_text("")

        templates_dir = theme_dir / "templates"
        templates_dir.mkdir()
        (templates_dir / "base.html").write_text("""
<html><body>{{ content }}</body></html>
""")
        (templates_dir / "sidebar.html").write_text("""
<div>{{ items }}</div>
""")

        config = Config.from_yaml(config_path)
        config.docs_dir = str(docs_dir)
        config.out_dir = str(tmp_path / "output")

        parser = Parser()
        builder = Builder(config, parser)
        builder.build()

        # Check order: page1, page2, index
        assert builder.pages[0].stem == "page1"
        assert builder.pages[1].stem == "page2"
        assert builder.pages[2].stem == "index"

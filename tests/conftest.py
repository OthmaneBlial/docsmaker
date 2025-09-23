import pytest
import yaml
from docsmaker.config import Config
from docsmaker.parser import Parser
from docsmaker.builder import Builder


@pytest.fixture
def sample_config_data():
    """Sample configuration data."""
    return {
        "site_name": "Test Docs",
        "docs_dir": "docs",
        "out_dir": "site",
        "theme": "default",
        "enable_search": True,
        "navigation": [
            {"icon": "📖", "title": "Home", "file": "index.md"},
            {"icon": "🚀", "title": "Getting Started", "file": "getting-started.md"}
        ]
    }


@pytest.fixture
def sample_config_file(tmp_path, sample_config_data):
    """Create a temporary config file."""
    config_path = tmp_path / "conf.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(sample_config_data, f)
    return config_path


@pytest.fixture
def sample_config(sample_config_file):
    """Load sample config."""
    return Config.from_yaml(sample_config_file)


@pytest.fixture
def sample_markdown():
    """Sample markdown content."""
    return """
# Hello World

This is a test document.

## Section 1

Some content here.

- List item 1
- List item 2

[Link to another page](another.md)

```python
def hello():
    print("Hello, World!")
```
"""


@pytest.fixture
def sample_docs_dir(tmp_path, sample_markdown):
    """Create a temporary docs directory with sample files."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Create index.md
    (docs_dir / "index.md").write_text("# Index\n\nWelcome to the docs.")

    # Create another.md
    (docs_dir / "another.md").write_text(sample_markdown)

    # Create conf.yaml
    conf_data = {
        "site_name": "Test Docs",
        "docs_dir": "docs",
        "out_dir": "site",
        "theme": "default",
        "enable_search": True
    }
    with open(docs_dir / "conf.yaml", 'w') as f:
        yaml.dump(conf_data, f)

    return docs_dir


@pytest.fixture
def parser():
    """Parser instance."""
    return Parser()


@pytest.fixture
def builder(sample_config, parser):
    """Builder instance."""
    return Builder(sample_config, parser)

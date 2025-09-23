# API Reference

## Programmatic Usage

Docsmaker can be used programmatically in Python code.

### Basic Example

```python
from docsmaker import Config, Parser, Builder

# Load configuration
config = Config.from_yaml("docs/conf.yaml")

# Create parser and builder
parser = Parser()
builder = Builder(config, parser)

# Build the site
builder.build()
```

### Classes

#### Config

Configuration management.

```python
from docsmaker import Config

# Load from YAML
config = Config.from_yaml("docs/conf.yaml")

# Or create programmatically
config = Config(
    site_name="My Docs",
    theme="default",
    out_dir="_build"
)
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| site_name | str | Site title |
| docs_dir | str | Markdown source directory |
| out_dir | str | Output directory |
| theme | str | Theme name |
| enable_search | bool | Enable search index |
| navigation | list | Navigation items |
| plugins | dict | Plugin configurations |

#### Builder

Site generation orchestrator.

```python
builder = Builder(config, parser)
builder.build()  # Generate site
```

#### Parser

Markdown processing.

```python
parser = Parser()
html = parser.parse(markdown_content)
```

### CLI Commands

| Command | Function | Options |
|---------|----------|---------|
| build | Generate site | --config, --out-dir |
| serve | Start server | --config, --host, --port |
| init | Create docs structure | --docs-dir |
| clean | Remove output | --out-dir |
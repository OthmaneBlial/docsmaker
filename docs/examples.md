# Examples

## Basic Documentation Site

Create a simple docs site:

```bash
mkdir my-docs
cd my-docs
pip install docsmakerpy
mkdir docs
```

Create `docs/conf.yaml`:

```yaml
site_name: My Project Docs
theme: default
```

Create `docs/index.md`:

```markdown
# Welcome

This is my documentation.
```

Build and serve:

```bash
docsmaker build
docsmaker serve
```

## Custom Theme

Use a custom theme:

```yaml
# conf.yaml
site_name: My Docs
theme: custom
```

Theme structure:

```
themes/
  custom/
    config.yaml
    templates/
      base.html
      sidebar.html
    assets/
      css/
      js/
```

## Navigation

Define custom navigation:

```yaml
navigation:
  - icon: "🏠"
    title: "Home"
    file: "index.md"
  - icon: "📚"
    title: "Guide"
    file: "guide.md"
```

## Programmatic Build

Build from Python:

```python
from pathlib import Path
from docsmaker import Config, Builder, Parser

config = Config(
    site_name="API Docs",
    docs_dir="api-docs",
    out_dir="build"
)

parser = Parser()
builder = Builder(config, parser)
builder.build()
```

## Plugin Example

Add a plugin for syntax highlighting:

```yaml
plugins:
  codehilite:
    style: monokai
```

## Use Cases

- **Open Source Projects**: Generate docs from README and guides
- **API Documentation**: Document REST APIs with examples
- **Internal Wikis**: Company knowledge base
- **Product Manuals**: User guides and tutorials
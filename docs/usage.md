# Usage

## Installation

Install from PyPI:

```bash
pip install docsmakerpy
```

For development with live reload:

```bash
pip install docsmakerpy[serve]
```

## Basic Workflow

1. Create a `docs` directory in your project root
2. Add your Markdown files (e.g., `index.md`, `usage.md`)
3. Create a `conf.yaml` configuration file
4. Build the site: `docsmaker build`
5. Serve locally: `docsmaker serve`

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `build` | Generate static site | `docsmaker build` |
| `serve` | Start local server | `docsmaker serve --port 8000` |
| `init` | Create initial docs structure | `docsmaker init` |
| `clean` | Remove build artifacts | `docsmaker clean` |

## Configuration

Create `docs/conf.yaml`:

```yaml
site_name: My Documentation
theme: default
output_dir: _build
```

## Sample Project Structure

```
my-project/
├── docs/
│   ├── conf.yaml
│   ├── index.md
│   └── usage.md
└── pyproject.toml
# Docsmaker

[![CI](https://github.com/OthmaneBlial/docsmaker/actions/workflows/ci.yml/badge.svg)](https://github.com/OthmaneBlial/docsmaker/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/OthmaneBlial/docsmakerpy/branch/main/graph/badge.svg)](https://codecov.io/gh/OthmaneBlial/docsmakerpy)
[![PyPI version](https://img.shields.io/pypi/v/docsmakerpy.svg)](https://pypi.org/project/docsmakerpy/)
[![PyPI downloads](https://img.shields.io/pypi/dm/docsmakerpy.svg)](https://pypi.org/project/docsmakerpy/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Transform Your Markdown into Stunning Documentation Sites

**Docsmaker** is a powerful, modular Python package that effortlessly converts your Markdown documentation into beautiful, static HTML websites. Designed for developers, open-source maintainers, and technical writers who demand professional documentation without the complexity.

### ✨ Why Choose Docsmaker?

- **🚀 Blazing Fast**: Generate static sites in seconds with optimized performance
- **🎨 Fully Customizable**: Beautiful themes with Jinja2 templating and CSS customization
- **🔌 Extensible**: Plugin system for advanced Markdown processing and integrations
- **🛠️ Developer-Friendly**: Simple CLI, live reload for development, and comprehensive API
- **📱 Responsive**: Mobile-first design that looks great on all devices
- **🔒 Secure**: No server-side dependencies - pure static HTML output

### 📸 Screenshots

*Coming soon - showcase of generated documentation sites with various themes*

## Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Installation](#installation)
- [Usage](#basic-usage)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Community](#-community)
- [License](#-license)

## 🚀 Quick Start

### Installation

Install Docsmaker from PyPI:

```bash
pip install docsmakerpy
```

For development with live reload:

```bash
pip install docsmakerpy[serve]
```

### Basic Usage

1. Create a `docs` directory with your Markdown files and a `conf.yaml` config file.

2. Build your site:

```bash
docsmakerpy build
```

3. Serve locally (with live reload if installed):

```bash
docsmakerpy serve
```

## 📚 Documentation

For detailed documentation, see the `docs/` directory or visit the generated site after building.

## ✨ Features

### Core Capabilities
- **📝 Advanced Markdown Processing**: Full CommonMark support with extensions (tables, code blocks, footnotes, etc.)
- **🎨 Theme System**: Pre-built themes with easy customization using Jinja2 templates and CSS
- **🔧 Plugin Architecture**: Extend functionality with custom Markdown plugins and processors
- **⚡ Static Site Generation**: Lightning-fast builds producing pure HTML/CSS/JS sites
- **🖥️ Command-Line Interface**: Intuitive CLI with comprehensive options and help
- **🔄 Live Development**: Optional live reload server for instant preview during development

### Advanced Features
- **📊 Configuration Management**: YAML-based config with validation and inheritance
- **🔍 Search Integration**: Built-in search functionality with generated index
- **📱 Responsive Design**: Mobile-first themes that adapt to all screen sizes
- **🌐 Multi-language Support**: Ready for internationalization and localization
- **🚀 Performance Optimized**: Minimal dependencies and optimized asset loading
- **🔒 Security First**: No runtime dependencies - completely static output

### Ecosystem
- **📦 PyPI Distribution**: Easy installation with pip
- **🐍 Python 3.8+**: Broad compatibility across modern Python versions
- **🧪 Comprehensive Testing**: Full test suite with CI/CD integration
- **📚 Rich Documentation**: Extensive docs with examples and guides

## 🤝 Contributing

We welcome contributions from the community! Whether it's bug reports, feature requests, documentation improvements, or code contributions, every bit helps make Docsmaker better.

### Ways to Contribute
- 🐛 **Report Issues**: Found a bug? [Open an issue](https://github.com/OthmaneBlial/docsmaker/issues) with details
- 💡 **Suggest Features**: Have an idea? [Start a discussion](https://github.com/OthmaneBlial/docsmaker/discussions)
- 📖 **Improve Documentation**: Help make our docs clearer and more comprehensive
- 🧪 **Write Tests**: Increase our test coverage and ensure stability
- 🎨 **Design Themes**: Create new themes or improve existing ones

For detailed contribution guidelines, see our [Contributing Guide](docs/contributing.md).

## 🌟 Community

- **📧 Discussions**: Join conversations on [GitHub Discussions](https://github.com/OthmaneBlial/docsmaker/discussions)
- **🐦 Social Media**: Follow us for updates and tips
- **💬 Discord**: Chat with the community (coming soon)
- **📧 Newsletter**: Stay updated with our latest releases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
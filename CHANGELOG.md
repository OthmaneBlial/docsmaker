# Changelog

All notable changes to Docsmaker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced documentation and examples
- Improved CI/CD pipeline
- Additional theme customization options

### Fixed
- Minor bug fixes and performance improvements

## [0.1.0] - 2024-09-23

### Added
- Initial release of Docsmaker
- Core functionality for generating static documentation sites from Markdown
- Support for custom themes with Jinja2 templating
- Plugin system for extending Markdown processing
- Command-line interface with build and serve commands
- YAML-based configuration system
- Live reload development server (optional)
- Comprehensive test suite
- Basic theme with responsive design
- Documentation generation with search index

### Technical Details
- Python 3.8+ compatibility
- Dependencies: typer, pyyaml, pydantic, markdown-it-py, mdit-py-plugins, jinja2
- Modular architecture with separate CLI, builder, parser, and config modules
- Static HTML output with no runtime dependencies

---

## Version History

### Pre-1.0 Releases

This project follows semantic versioning. Versions 0.x.x may contain breaking changes as the API stabilizes.

### Contributing to Changelog

When contributing changes:

1. Add entries under `[Unreleased]` section
2. Categorize changes as:
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` for vulnerability fixes

3. Reference issue/PR numbers when applicable
4. Keep descriptions clear and concise

Example:
```
### Added
- New feature description (#123)

### Fixed
- Bug fix description (#124)
```

---

For the latest updates, check the [GitHub repository](https://github.com/OthmaneBlial/docsmaker).
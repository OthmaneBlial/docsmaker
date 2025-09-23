import pytest
from docsmaker.config import Config, NavigationItem


class TestNavigationItem:
    def test_navigation_item_creation(self):
        item = NavigationItem(icon="📖", title="Home", file="index.md")
        assert item.icon == "📖"
        assert item.title == "Home"
        assert item.file == "index.md"


class TestConfig:
    def test_config_creation_with_defaults(self):
        config = Config()
        assert config.site_name == "Docsmaker Documentation"
        assert config.docs_dir == "docs"
        assert config.out_dir == "site"
        assert config.theme == "default"
        assert config.enable_search is True
        assert config.navigation == []
        assert config.plugins is None

    def test_config_creation_with_custom_values(self, sample_config_data):
        config = Config(**sample_config_data)
        assert config.site_name == "Test Docs"
        assert config.docs_dir == "docs"
        assert config.out_dir == "site"
        assert config.theme == "default"
        assert config.enable_search is True
        assert len(config.navigation) == 2
        assert config.navigation[0].title == "Home"

    def test_config_validation_empty_dirs(self):
        with pytest.raises(ValueError, match="Directory path cannot be empty"):
            Config(docs_dir="")
        with pytest.raises(ValueError, match="Directory path cannot be empty"):
            Config(out_dir="")

    def test_from_yaml_success(self, sample_config_file):
        config = Config.from_yaml(sample_config_file)
        assert config.site_name == "Test Docs"
        assert config.docs_dir == "docs"

    def test_from_yaml_file_not_found(self, tmp_path):
        non_existent = tmp_path / "missing.yaml"
        config = Config.from_yaml(non_existent)
        # Should create default config
        assert config.site_name == "Docsmaker Documentation"
        assert config.docs_dir == "docs"
        assert config.out_dir == "site"
        assert config.theme == "default"
        assert config.enable_search is True
        assert non_existent.exists()  # File should be created

    def test_from_yaml_invalid_yaml(self, tmp_path):
        invalid_yaml = tmp_path / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content: [")
        with pytest.raises(Exception):  # yaml.YAMLError
            Config.from_yaml(invalid_yaml)

    def test_get_docs_path(self, sample_config):
        path = sample_config.get_docs_path()
        assert path.name == "docs"
        assert path.is_absolute()

    def test_get_out_path(self, sample_config):
        path = sample_config.get_out_path()
        assert path.name == "site"
        assert path.is_absolute()

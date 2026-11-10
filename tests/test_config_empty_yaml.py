"""Regression tests: empty / comment-only / non-mapping config files."""
from docsmaker.config import Config
import pytest


def test_from_yaml_empty_file_returns_defaults(tmp_path):
    empty_yaml = tmp_path / "empty.yaml"
    empty_yaml.write_text("", encoding="utf-8")
    config = Config.from_yaml(empty_yaml)
    assert config.site_name == "Docsmaker Documentation"
    assert config.docs_dir == "docs"
    assert config.out_dir == "site"


def test_from_yaml_comment_only_file_returns_defaults(tmp_path):
    comment_yaml = tmp_path / "comment.yaml"
    comment_yaml.write_text("  \n# only a comment\n", encoding="utf-8")
    config = Config.from_yaml(comment_yaml)
    assert config.site_name == "Docsmaker Documentation"


def test_from_yaml_non_mapping_raises_clear_error(tmp_path):
    list_yaml = tmp_path / "list.yaml"
    list_yaml.write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected a mapping"):
        Config.from_yaml(list_yaml)

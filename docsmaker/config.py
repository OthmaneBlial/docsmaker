"""Configuration loading and validation using Pydantic."""

import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class NavigationItem(BaseModel):
    """Navigation item model."""
    icon: str = Field(..., description="Icon for the navigation item")
    title: str = Field(..., description="Title of the navigation item")
    file: str = Field(..., description="Markdown file path")


class Config(BaseModel):
    """Main configuration model."""
    site_name: str = Field("Docsmaker Documentation", description="Name of the site")
    docs_dir: str = Field("docs", description="Directory containing Markdown files")
    out_dir: str = Field("site", description="Output directory for generated site")
    theme: str = Field("default", description="Theme to use")
    enable_search: bool = Field(True, description="Enable search functionality")
    navigation: List[NavigationItem] = Field(default_factory=list, description="Navigation structure")
    plugins: Optional[Dict[str, Any]] = Field(None, description="Plugin configurations")

    @field_validator('docs_dir', 'out_dir')
    @classmethod
    def validate_dirs(cls, v):
        """Ensure directories are valid paths."""
        if not v:
            raise ValueError("Directory path cannot be empty")
        return v

    @classmethod
    def from_yaml(cls, path: Path) -> 'Config':
        """Load configuration from YAML file, creating default if not exists."""
        if not path.exists():
            # Create default config
            default_config = cls()
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(default_config.model_dump(), f, default_flow_style=False, sort_keys=False)
            return default_config
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def get_docs_path(self) -> Path:
        """Get the absolute path to docs directory."""
        return Path(self.docs_dir).resolve()

    def get_out_path(self) -> Path:
        """Get the absolute path to output directory."""
        return Path(self.out_dir).resolve()
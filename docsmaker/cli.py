"""CLI commands using Typer."""

import typer
from pathlib import Path
from .config import Config
from .parser import Parser
from .builder import Builder

try:
    import livereload
except ImportError:
    livereload = None

app = typer.Typer()


@app.command()
def build(
    config_file: Path = typer.Option("docs/conf.yaml", "--config", "-c", help="Path to config file"),
    out_dir: str = typer.Option(None, "--out-dir", "-o", help="Output directory override"),
) -> None:
    """Generate the documentation site."""
    try:
        config = Config.from_yaml(config_file)
        if out_dir:
            config.out_dir = out_dir
        parser = Parser()
        builder = Builder(config, parser)
        builder.build()
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def serve(
    config_file: Path = typer.Option("docs/conf.yaml", "--config", "-c", help="Path to config file"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
) -> None:
    """Start a local server with live reload."""
    if livereload is None:
        typer.echo("Error: livereload package is required for serving. Install it with 'pip install livereload'", err=True)
        raise typer.Exit(code=1)

    try:
        config = Config.from_yaml(config_file)
        out_dir = Path(config.out_dir)
        if not out_dir.exists():
            typer.echo(f"Error: Output directory {out_dir} does not exist. Run 'docsmaker build' first.", err=True)
            raise typer.Exit(code=1)

        server = livereload.Server()
        server.watch(str(out_dir), delay=1)
        typer.echo(f"Serving {out_dir} at http://{host}:{port}")
        server.serve(root=str(out_dir), host=host, port=port, open_url_delay=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def init(
    docs_dir: str = typer.Option("docs", "--docs-dir", help="Directory for docs"),
) -> None:
    """Create initial docs structure."""
    # Placeholder for init functionality
    typer.echo("Init command not implemented yet.")


@app.command()
def clean(
    out_dir: str = typer.Option("site", "--out-dir", "-o", help="Output directory to clean"),
) -> None:
    """Clean the output directory."""
    out_path = Path(out_dir)
    if out_path.exists():
        import shutil
        shutil.rmtree(out_path)
        typer.echo(f"Cleaned {out_path}")
    else:
        typer.echo(f"Directory {out_path} does not exist")


if __name__ == "__main__":
    app()
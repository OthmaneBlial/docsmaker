import pytest
from unittest.mock import MagicMock
from click.exceptions import Exit
from docsmaker.cli import build, serve, clean


class TestBuildCommand:
    def test_build_success(self, sample_config_file, mocker):
        mock_config = mocker.patch('docsmaker.cli.Config.from_yaml')
        mock_config.return_value = MagicMock()
        mock_parser = mocker.patch('docsmaker.cli.Parser')
        mock_builder = mocker.patch('docsmaker.cli.Builder')
        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        build(sample_config_file)

        mock_config.assert_called_once_with(sample_config_file)
        mock_parser.assert_called_once()
        mock_builder.assert_called_once()
        mock_builder.return_value.build.assert_called_once()
        mock_echo.assert_not_called()

    def test_build_with_out_dir_override(self, sample_config_file, mocker):
        mock_config = mocker.patch('docsmaker.cli.Config.from_yaml')
        config_mock = MagicMock()
        mock_config.return_value = config_mock
        mocker.patch('docsmaker.cli.Parser')
        mock_builder = mocker.patch('docsmaker.cli.Builder')

        build(sample_config_file, out_dir="custom_site")

        assert config_mock.out_dir == "custom_site"
        mock_builder.return_value.build.assert_called_once()

    def test_build_config_not_found(self, tmp_path, mocker):
        missing_config = tmp_path / "missing.yaml"
        # Config.from_yaml now creates default config if not exists
        mock_config = mocker.patch('docsmaker.cli.Config.from_yaml')
        config_mock = MagicMock()
        mock_config.return_value = config_mock
        mock_parser = mocker.patch('docsmaker.cli.Parser')
        mock_builder = mocker.patch('docsmaker.cli.Builder')
        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        build(missing_config)

        mock_config.assert_called_once_with(missing_config)
        mock_parser.assert_called_once()
        mock_builder.assert_called_once()
        mock_echo.assert_not_called()

    def test_build_general_error(self, sample_config_file, mocker):
        mock_config = mocker.patch('docsmaker.cli.Config.from_yaml', side_effect=Exception("build error"))
        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        with pytest.raises(Exit):
            build(sample_config_file)

        mock_config.assert_called_once_with(sample_config_file)
        mock_echo.assert_called_once_with("Error: build error", err=True)


class TestServeCommand:
    def test_serve_success(self, sample_config_file, tmp_path, mocker):
        # Mock livereload to be available
        mock_livereload = mocker.MagicMock()
        mocker.patch('docsmaker.cli.livereload', mock_livereload)

        mock_config = mocker.patch('docsmaker.cli.Config.from_yaml')
        config_mock = MagicMock()
        config_mock.out_dir = str(tmp_path / "site")
        mock_config.return_value = config_mock

        out_dir = tmp_path / "site"
        out_dir.mkdir()

        mock_server = mocker.patch('docsmaker.cli.livereload.Server')
        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        serve(sample_config_file, host="127.0.0.1", port=8000)

        mock_server.assert_called_once()
        mock_server.return_value.watch.assert_called_once_with(str(out_dir), delay=1)
        mock_server.return_value.serve.assert_called_once_with(
            root=str(out_dir), host="127.0.0.1", port=8000, open_url_delay=1
        )
        mock_echo.assert_called_with(f"Serving {out_dir} at http://127.0.0.1:8000")

    def test_serve_livereload_not_installed(self, sample_config_file, mocker):
        # Simulate livereload not installed
        mocker.patch('docsmaker.cli.livereload', None)
        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        with pytest.raises(Exit):
            serve(sample_config_file, host="127.0.0.1", port=8000)

        mock_echo.assert_called_once_with(
            "Error: livereload package is required for serving. Install it with 'pip install livereload'",
            err=True
        )

    def test_serve_output_dir_not_exist(self, sample_config_file, mocker):
        # Mock livereload to be available
        mock_livereload = mocker.MagicMock()
        mocker.patch('docsmaker.cli.livereload', mock_livereload)

        mock_config = mocker.patch('docsmaker.cli.Config.from_yaml')
        config_mock = MagicMock()
        config_mock.out_dir = "nonexistent"
        mock_config.return_value = config_mock

        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        with pytest.raises(Exit):
            serve(sample_config_file, host="127.0.0.1", port=8000)

        mock_echo.assert_any_call("Error: Output directory nonexistent does not exist. Run 'docsmaker build' first.", err=True)


class TestCleanCommand:
    def test_clean_existing_dir(self, tmp_path, mocker):
        out_dir = tmp_path / "site"
        out_dir.mkdir()

        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        clean(str(out_dir))

        assert not out_dir.exists()
        mock_echo.assert_called_once_with(f"Cleaned {out_dir}")

    def test_clean_nonexistent_dir(self, tmp_path, mocker):
        out_dir = tmp_path / "nonexistent"

        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        clean(str(out_dir))

        mock_echo.assert_called_once_with(f"Directory {out_dir} does not exist")


class TestInitCommand:
    def test_init_placeholder(self, mocker):
        mock_echo = mocker.patch('docsmaker.cli.typer.echo')

        from docsmaker.cli import init
        init()

        mock_echo.assert_called_once_with("Init command not implemented yet.")

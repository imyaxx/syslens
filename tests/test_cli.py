from typer.testing import CliRunner

from syslens.cli import app

runner = CliRunner()


def test_info_command() -> None:
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0
    assert "Hostname:" in result.output
    assert "Operating system:" in result.output
    assert "Kernel:" in result.output
    assert "Architecture:" in result.output
    assert "Python version:" in result.output

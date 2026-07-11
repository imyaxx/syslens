import pytest
from typer.testing import CliRunner

import syslens.system.cli
from syslens.cli import app
from syslens.system.resources import ResourceUsage

runner = CliRunner()


def test_info_command() -> None:
    result = runner.invoke(app, ["system", "info"])

    assert result.exit_code == 0
    assert "Hostname:" in result.output
    assert "Operating system:" in result.output
    assert "Kernel:" in result.output
    assert "Architecture:" in result.output
    assert "Python version:" in result.output


def test_resources_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(syslens.system.cli, "get_cpu_usage_percent", lambda: 25.0)
    monkeypatch.setattr(
        syslens.system.cli,
        "get_memory_usage",
        lambda: ResourceUsage(8 * 1024**3, 3 * 1024**3, 37.5),
    )
    monkeypatch.setattr(
        syslens.system.cli,
        "get_disk_usage",
        lambda: ResourceUsage(100 * 1024**3, 40 * 1024**3, 40.0),
    )

    result = runner.invoke(app, ["system", "resources"])

    assert result.exit_code == 0
    assert "CPU usage: 25.0%" in result.output
    assert "Memory: 3.0 GiB / 8.0 GiB (37.5%)" in result.output
    assert "Disk: 40.0 GiB / 100.0 GiB (40.0%)" in result.output


@pytest.mark.parametrize("command", ["info", "resources"])
def test_old_root_commands_are_not_available(command: str) -> None:
    result = runner.invoke(app, [command])

    assert result.exit_code != 0

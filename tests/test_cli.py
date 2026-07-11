import pytest
from typer.testing import CliRunner

import syslens.cli
from syslens.cli import app
from syslens.system.resources import ResourceUsage

runner = CliRunner()


def test_info_command() -> None:
    result = runner.invoke(app, ["info"])

    assert result.exit_code == 0
    assert "Hostname:" in result.output
    assert "Operating system:" in result.output
    assert "Kernel:" in result.output
    assert "Architecture:" in result.output
    assert "Python version:" in result.output


def test_resources_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(syslens.cli, "get_cpu_usage_percent", lambda: 25.0)
    monkeypatch.setattr(
        syslens.cli,
        "get_memory_usage",
        lambda: ResourceUsage(8 * 1024**3, 3 * 1024**3, 37.5),
    )
    monkeypatch.setattr(
        syslens.cli,
        "get_disk_usage",
        lambda: ResourceUsage(100 * 1024**3, 40 * 1024**3, 40.0),
    )

    result = runner.invoke(app, ["resources"])

    assert result.exit_code == 0
    assert "CPU usage: 25.0%" in result.output
    assert "Memory: 3.0 GiB / 8.0 GiB (37.5%)" in result.output
    assert "Disk: 40.0 GiB / 100.0 GiB (40.0%)" in result.output

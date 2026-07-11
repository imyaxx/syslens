from pathlib import Path
from types import SimpleNamespace

import pytest

from syslens.system import resources
from syslens.system.resources import ResourceUsage


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 0.0),
        (1024**3, 1.0),
        (int(2.5 * 1024**3), 2.5),
    ],
)
def test_bytes_to_gib(value: int, expected: float) -> None:
    assert resources.bytes_to_gib(value) == expected


def test_get_cpu_usage_percent(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_cpu_percent(*, interval: float) -> float:
        assert interval == 0.1
        return 42.5

    monkeypatch.setattr(resources.psutil, "cpu_percent", fake_cpu_percent)

    assert resources.get_cpu_usage_percent() == 42.5


def test_get_memory_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    memory = SimpleNamespace(total=8_000, available=3_000, percent=62.5)
    monkeypatch.setattr(resources.psutil, "virtual_memory", lambda: memory)

    assert resources.get_memory_usage() == ResourceUsage(
        total_bytes=8_000,
        used_bytes=5_000,
        percent=62.5,
    )


def test_get_disk_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    disk = SimpleNamespace(total=10_000, used=4_000, percent=40.0)

    def fake_disk_usage(path: Path) -> SimpleNamespace:
        assert path == Path.home()
        return disk

    monkeypatch.setattr(resources.psutil, "disk_usage", fake_disk_usage)

    assert resources.get_disk_usage() == ResourceUsage(
        total_bytes=10_000,
        used_bytes=4_000,
        percent=40.0,
    )

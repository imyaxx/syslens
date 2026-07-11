from dataclasses import dataclass
from pathlib import Path

import psutil

BYTES_PER_GIB = 1024**3


@dataclass(frozen=True)
class ResourceUsage:
    total_bytes: int
    used_bytes: int
    percent: float


def get_cpu_usage_percent() -> float:
    return psutil.cpu_percent(interval=0.1)


def get_memory_usage() -> ResourceUsage:
    memory = psutil.virtual_memory()
    return ResourceUsage(
        total_bytes=memory.total,
        used_bytes=memory.total - memory.available,
        percent=memory.percent,
    )


def get_disk_usage() -> ResourceUsage:
    disk = psutil.disk_usage(Path.home())
    return ResourceUsage(
        total_bytes=disk.total,
        used_bytes=disk.used,
        percent=disk.percent,
    )


def bytes_to_gib(value: int) -> float:
    return value / BYTES_PER_GIB

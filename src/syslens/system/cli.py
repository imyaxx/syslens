import typer

from syslens.system.info import (
    get_architecture,
    get_hostname,
    get_kernel,
    get_operating_system,
    get_python_version,
)
from syslens.system.resources import (
    bytes_to_gib,
    get_cpu_usage_percent,
    get_disk_usage,
    get_memory_usage,
)

app = typer.Typer()


@app.command()
def info() -> None:
    """Show basic system information."""
    typer.echo(f"Hostname: {get_hostname()}")
    typer.echo(f"Operating system: {get_operating_system()}")
    typer.echo(f"Kernel: {get_kernel()}")
    typer.echo(f"Architecture: {get_architecture()}")
    typer.echo(f"Python version: {get_python_version()}")


@app.command()
def resources() -> None:
    """Show CPU, memory, and disk usage."""
    memory = get_memory_usage()
    disk = get_disk_usage()

    typer.echo(f"CPU usage: {get_cpu_usage_percent():.1f}%")
    typer.echo(
        f"Memory: {bytes_to_gib(memory.used_bytes):.1f} GiB / "
        f"{bytes_to_gib(memory.total_bytes):.1f} GiB ({memory.percent:.1f}%)"
    )
    typer.echo(
        f"Disk: {bytes_to_gib(disk.used_bytes):.1f} GiB / "
        f"{bytes_to_gib(disk.total_bytes):.1f} GiB ({disk.percent:.1f}%)"
    )

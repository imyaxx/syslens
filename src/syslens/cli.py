from importlib.metadata import version
from typing import Annotated

import typer

from syslens.system.info import (
    get_architecture,
    get_hostname,
    get_kernel,
    get_operating_system,
    get_python_version,
)

app = typer.Typer(add_completion=False)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(version("syslens"))
        raise typer.Exit


@app.callback()
def main(
    version_requested: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the application version and exit.",
        ),
    ] = None,
) -> None:
    """Inspect system information from the command line."""


@app.command()
def info() -> None:
    """Show basic system information."""
    typer.echo(f"Hostname: {get_hostname()}")
    typer.echo(f"Operating system: {get_operating_system()}")
    typer.echo(f"Kernel: {get_kernel()}")
    typer.echo(f"Architecture: {get_architecture()}")
    typer.echo(f"Python version: {get_python_version()}")

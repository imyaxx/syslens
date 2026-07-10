from importlib.metadata import version
from typing import Annotated

import typer

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

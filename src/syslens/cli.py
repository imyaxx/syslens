from importlib.metadata import version
from typing import Annotated

import typer

from syslens.network.cli import app as network_app
from syslens.system.cli import app as system_app

app = typer.Typer(add_completion=False)
app.add_typer(network_app, name="network")
app.add_typer(system_app, name="system")


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

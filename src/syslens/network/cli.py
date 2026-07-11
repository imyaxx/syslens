import typer

from syslens.network.info import (
    get_default_gateway,
    get_dns_servers,
    get_hostname,
    get_local_ip,
    get_network_interfaces,
)

app = typer.Typer()


@app.command()
def info() -> None:
    """Show basic network information."""
    typer.echo(f"Hostname: {get_hostname()}")
    typer.echo(f"Local IP: {get_local_ip()}")
    typer.echo(f"Default Gateway: {get_default_gateway()}")
    typer.echo(f"DNS Servers: {', '.join(get_dns_servers())}")
    typer.echo(f"Network Interfaces: {', '.join(get_network_interfaces())}")

import asyncio
import click
from rich.console import Console
from rich.table import Table

from .api import stream_and_render
from .config import load_config, get_api_key, get_model, get_repo_path

console = Console()

@click.group()
def cli():
    """A terminal-based CLI agent for the k2-think-cerebras API."""
    pass

@cli.command()
@click.argument("prompt", nargs=-1)
def query(prompt):
    """
    Sends a query to the Cerebras API.
    """
    if not prompt:
        console.print("[bold yellow]Please provide a prompt.[/bold yellow]")
        return

    full_prompt = " ".join(prompt)
    console.print(f"[bold cyan]Querying with model: {get_model()}[/bold cyan]")
    try:
        asyncio.run(stream_and_render(full_prompt))
    except ValueError as e:
        # Error is already printed in the api module
        pass
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

@cli.command()
def config():
    """
    Displays the current configuration.
    """
    config_data = load_config()
    if not config_data:
        console.print("[bold yellow]Configuration file not found or empty.[/bold yellow]")
        return

    table = Table(title="CLI Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="magenta")

    api_key = get_api_key()
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if api_key and len(api_key) > 8 else "Not set"

    table.add_row("API Key", masked_key)
    table.add_row("Model", get_model())
    table.add_row("Repo Path", get_repo_path())

    console.print(table)

if __name__ == "__main__":
    cli()
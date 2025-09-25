import asyncio
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from .api import stream_and_render, chat_with_history
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
def chat():
    """
    Starts an interactive chat session with the Cerebras API.
    """
    console.print(f"[bold cyan]Starting chat with model: {get_model()}[/bold cyan]")
    console.print("[bold green]Type 'exit' or 'quit' to end the conversation.[/bold green]")
    console.print("[bold green]Type 'clear' to clear the conversation history.[/bold green]")
    
    try:
        asyncio.run(interactive_chat())
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

async def interactive_chat():
    """Handles the interactive chat loop."""
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    
    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]")
        
        if user_input.lower() in ['exit', 'quit']:
            console.print("[bold yellow]Ending chat session.[/bold yellow]")
            break
        
        if user_input.lower() == 'clear':
            messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
            console.print("[bold yellow]Conversation history cleared.[/bold yellow]")
            continue
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Get response from API
        response = await chat_with_history(messages)
        
        # Add assistant response to history
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    cli()
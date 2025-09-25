import asyncio
from cerebras.cloud.sdk import AsyncCerebras
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from .config import get_api_key, get_model

console = Console()

async def get_client() -> AsyncCerebras:
    """Initializes and returns the async Cerebras client."""
    api_key = get_api_key()
    if not api_key or api_key == "YOUR_CEREBRAS_API_KEY":
        console.print("[bold red]Error: API key not found or not set.[/bold red]")
        console.print("Please set your API key in `config.yml`.")
        raise ValueError("API key not configured.")
    return AsyncCerebras(api_key=api_key)

async def stream_and_render(prompt: str):
    """
    Streams the response from the Cerebras API and renders it in the terminal.
    """
    client = await get_client()
    model = get_model()

    full_response = ""
    try:
        with Live(console=console, screen=False, auto_refresh=False) as live:
            async with client.chat.completions.with_streaming_response.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            ) as stream:
                async for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        live.update(Markdown(full_response), refresh=True)
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

    return full_response
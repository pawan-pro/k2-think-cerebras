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

    try:
        # For now, use a non-streaming response to avoid the async iteration issue
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Display the full response at once
        full_response = response.choices[0].message.content
        console.print(Markdown(full_response))
        
        return full_response
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        return ""
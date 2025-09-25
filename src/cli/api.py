import asyncio
import re
from cerebras.cloud.sdk import AsyncCerebras
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
import pandas as pd
import matplotlib.pyplot as plt

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
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        
        full_response = response.choices[0].message.content
        
        # Check if the response contains Python code that should be executed
        if should_execute_code(prompt, full_response):
            execute_code_from_response(full_response)
        else:
            console.print(Markdown(full_response))
        
        return full_response
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        return ""

def should_execute_code(prompt: str, response: str) -> bool:
    """
    Determines if the AI response contains code that should be executed based on the user's request.
    """
    # Check if the prompt is asking to create or generate something visual
    execution_keywords = [
        'create chart', 'generate chart', 'plot', 'visualize', 
        'show data', 'make graph', 'create graph', 'display chart',
        'chart of', 'graph of', 'plot of'
    ]
    
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in execution_keywords)

def execute_code_from_response(response: str):
    """
    Extracts and executes Python code from the AI response.
    """
    try:
        # Extract code blocks from the response using regex
        code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)\n```', response, re.DOTALL)
        
        if not code_blocks:
            # If no code blocks found with triple backticks, try to find Python code differently
            console.print(Markdown(response))
            return
        
        for code_block in code_blocks:
            try:
                # First, let's analyze the CSV file structure if it involves loading CSV data
                if 'pd.read_csv' in code_block and 'treasury.csv' in code_block:
                    # Read the CSV to understand its structure before executing the full code
                    try:
                        csv_df = pd.read_csv('treasury.csv')
                        console.print(f"[bold blue]CSV Analysis:[/bold blue] Found {len(csv_df.columns)} columns: {list(csv_df.columns)}")
                        console.print(f"[bold blue]First few rows shape:[/bold blue] {csv_df.shape}")
                        
                        # If the CSV doesn't have the expected columns, we should inform the user
                        # rather than try to execute potentially incorrect code
                        expected_date_col = None
                        expected_value_col = None
                        
                        for col in csv_df.columns:
                            if col.lower() in ['date', 'time', 'day', 'month', 'year']:
                                expected_date_col = col
                            if '10' in col.upper() or 'YEAR' in col.upper() or 'YIELD' in col.upper():
                                expected_value_col = col
                        
                        if not expected_date_col or not expected_value_col:
                            console.print(f"[bold yellow]Warning: The CSV doesn't have clearly identifiable date and value columns.[/bold yellow]")
                            console.print(f"[bold yellow]Available columns: {list(csv_df.columns)}[/bold yellow]")
                            console.print(f"[bold yellow]Possible date column: {expected_date_col}[/bold yellow]")
                            console.print(f"[bold yellow]Possible 10Y column: {expected_value_col}[/bold yellow]")
                            console.print(f"[bold yellow]Executing response as text for manual adjustment:[/bold yellow]")
                            console.print(Markdown(response))
                            return
                    except Exception as csv_error:
                        console.print(f"[bold yellow]Could not analyze CSV structure: {str(csv_error)}[/bold yellow]")
                
                # Execute the extracted code
                exec_globals = {"pd": pd, "plt": plt}
                exec(code_block.strip(), exec_globals)
                
                # Show the plot if matplotlib was used
                if 'plt' in code_block:
                    plt.show()
                    
                console.print(f"[bold green]Code executed successfully![/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error executing code: {str(e)}[/bold red]")
                # Instead of falling back to text, let's try to give more helpful info
                console.print(f"[bold yellow]The code tried to execute but encountered an issue with your specific data format.[/bold yellow]")
                console.print(f"[bold yellow]Your CSV file might have a different structure than expected.[/bold yellow]")
                try:
                    # Show information about the actual CSV file
                    df = pd.read_csv('treasury.csv')
                    console.print(f"[bold blue]Actual CSV structure:[/bold blue]")
                    console.print(f"  Columns: {list(df.columns)}")
                    console.print(f"  Shape: {df.shape}")
                    console.print(f"  Sample data:\n{df.head(3)}")
                    console.print(f"[bold yellow]You may need to adjust the column names in the generated code.[/bold yellow]")
                except Exception:
                    console.print(f"[bold yellow]Could not read your CSV file to provide structure info.[/bold yellow]")
                
                console.print(f"[bold yellow]Here is the suggested code (you may need to modify column names):[/bold yellow]")
                console.print(Markdown(response))
                return
                
    except Exception as e:
        console.print(f"[bold red]Error processing code: {str(e)}[/bold red]")
        console.print(f"[bold yellow]Displaying response as text:[/bold yellow]")
        console.print(Markdown(response))

async def chat_with_history(messages: list):
    """
    Sends a conversation with message history to the Cerebras API.
    """
    client = await get_client()
    model = get_model()

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
        )
        
        full_response = response.choices[0].message.content
        
        # Check if the response contains Python code that should be executed
        if len(messages) > 0 and should_execute_code(messages[-1]["content"], full_response):
            execute_code_from_response(full_response)
        else:
            console.print(f"[bold green]Assistant:[/bold green] {full_response}")
        
        return full_response
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        return ""
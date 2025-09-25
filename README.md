# K2-Think-Cerebras CLI Agent

This repository contains a terminal-based CLI agent for interacting with the k2-think-cerebras API. The agent allows you to send natural language queries to the Cerebras models and receive responses directly in your terminal.

## Features

-   **Asynchronous Processing**: All API calls are made asynchronously, ensuring the interface remains responsive.
-   **Interactive Chat**: Engage in multi-turn conversations with the AI assistant.
-   **Single Query Mode**: Send one-off queries to the API.
-   **Configurable**: Easily configure your API key, model, and other settings via a `config.yml` file.
-   **Rich Terminal Output**: Clean and readable output, with syntax highlighting for code.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Rename `config.yml.example` to `config.yml`.
2.  Open `config.yml` and add your Cerebras API key:

    ```yaml
    api_key: "YOUR_CEREBRAS_API_KEY"
    model: "qwen-3-coder-480b"
    repo_path: "."
    ```

## Usage

You can run the CLI agent using the following command:

```bash
python -m src.cli.main [COMMAND]
```

### Commands

-   `query`: Send a single query to the Cerebras API.
-   `chat`: Start an interactive chat session with the Cerebras API.
-   `config`: Display the current configuration.

### Examples

**Send a query:**

```bash
python -m src.cli.main query "Write a Python function to calculate the factorial of a number."
```

**Start an interactive chat:**

```bash
python -m src.cli.main chat
```

**Check configuration:**

```bash
python -m src.cli.main config
```

## Development

### Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest discover -s tests
```
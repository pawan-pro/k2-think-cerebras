import yaml
from pathlib import Path

CONFIG_FILE = Path("config.yml")

def load_config() -> dict:
    """Loads the configuration from the YAML file."""
    if not CONFIG_FILE.is_file():
        return {}
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def get_api_key() -> str:
    """Returns the Cerebras API key from the configuration."""
    config = load_config()
    return config.get("api_key")

def get_model() -> str:
    """Returns the model name from the configuration."""
    config = load_config()
    return config.get("model", "qwen-3-coder-480b")

def get_repo_path() -> str:
    """Returns the repository path from the configuration."""
    config = load_config()
    return config.get("repo_path", ".")
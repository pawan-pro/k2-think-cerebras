import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

# List available models (useful to confirm access)
models = client.models.list()
print("Available models:", models)

# Ask your first coding question using Qwen coder model
resp = client.chat.completions.create(
    model="qwen-3-coder-480b",
    messages=[{"role": "user", "content": "Write a Python script for async web scraping."}]
)
print(resp)

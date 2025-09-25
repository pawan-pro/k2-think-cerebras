import os
import re
import subprocess
import datetime
from cerebras.cloud.sdk import Cerebras

def load_todo(todo_file="todo.md"):
    try:
        with open(todo_file, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def extract_codeblock(message_content):
    """
    Extracts python code block from string (in triple backticks)
    """
    # Make sure message_content is a string and strip leading/trailing spaces
    if not isinstance(message_content, str):
        message_content = str(message_content)
    message_content = message_content.strip()
    # Regex to capture code block; tolerant of whitespace and extra lines
    match = re.search(r"```(?:python)?\s*\n(.*?)\n```", message_content, re.DOTALL)
    return match.group(1).strip() if match else None

def main():
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        print("Set the environment variable CEREBRAS_API_KEY with your API key.")
        return

    todo_content = load_todo()
    if not todo_content.strip():
        print("[Error] todo.md is empty!")
        return

    client = Cerebras(api_key=api_key)
    prompt = (
        f"You are a Python automation agent working in my repo. Here is the task from todo.md:\n"
        f"{todo_content}\n"
        "Please generate python scripts as needed to accomplish the task"
        "Your code may generate or update any files in the repo as needed."
    )

    response = client.chat.completions.create(
        model="qwen-3-coder-480b",
        messages=[{"role": "user", "content": prompt}]
    )

    # Access model message content directly
    try:
        model_message = response.choices[0].message.content
    except Exception as e:
        print("[Error] Unexpected SDK response format:", e)
        #print("[Raw output]:", response)
        return

    # Print debug info to confirm code block content
    # print("[DEBUG] model_message:", repr(model_message))

    code = extract_codeblock(model_message)
    if not code:
        print("[Error] No Python code block found in model output. Here is the output:")
        #print(model_message)
        return

    # Save generated code/script into the repo with a timestamped filename
    script_name = f"generated_agent_task_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    with open(script_name, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[Info] Saved code to {script_name}.\n")
    #print(code)
    print("\n[Info] Now executing generated script...")

    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    #print("[Execution stdout]:\n", result.stdout)
    #print("[Execution stderr]:\n", result.stderr)

    # Show repo directory contents after script execution
    print("\n[Info] Files in repo after execution:")
    for fname in os.listdir(os.getcwd()):
        print(" -", fname)

if __name__ == "__main__":
    main()

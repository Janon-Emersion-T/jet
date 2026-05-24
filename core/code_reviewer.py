from core.brain import ask_brain
from tools.system_tools import read_project_file

def review_code_file(file_path: str) -> str:
    file_content = read_project_file(file_path)

    if file_content.startswith("Blocked") or file_content.startswith("File not found") or file_content.startswith("That path"):
        return file_content

    prompt = f"""
You are JARVIS, Janon's local senior software engineer.

Review this code carefully.

Focus on:
1. Bugs
2. Security issues
3. Missing error handling
4. Performance problems
5. Code structure improvements
6. Practical next steps

Do not rewrite the whole file unless asked.

CODE:
{file_content}
"""

    return ask_brain(prompt)
from pathlib import Path
from datetime import datetime

from core.brain import ask_brain
from tools.system_tools import read_project_file, write_project_file

def propose_patch(file_path: str, instruction: str) -> str:
    original = read_project_file(file_path)

    if original.startswith("Blocked") or original.startswith("File not found") or original.startswith("That path"):
        return original

    prompt = f"""
You are JARVIS, Janon's local senior software engineer.

Improve the file based on this instruction:
{instruction}

Rules:
- Return the FULL updated file content only.
- Do not use markdown.
- Do not explain.
- Preserve existing functionality unless the instruction says otherwise.
- Keep code clean, safe, and practical.

ORIGINAL FILE:
{original}
"""

    updated_content = ask_brain(prompt)

    path = Path(file_path).expanduser()
    proposal_path = str(path) + f".proposal-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    result = write_project_file(proposal_path, updated_content)

    return f"{result}\nProposal created for review:\n{proposal_path}"
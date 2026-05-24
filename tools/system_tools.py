import os
import subprocess
from pathlib import Path

from datetime import datetime
import shutil

HOME = str(Path.home())

ALLOWED_COMMANDS = {
    "pwd": ["pwd"],
    "ls": ["ls", "-la"],
    "disk": ["df", "-h"],
    "memory": ["free", "-h"],
    "date": ["date"],
    "whoami": ["whoami"],
    "python version": ["python3", "--version"],
    "node version": ["node", "--version"],
    "npm version": ["npm", "--version"],
    "git version": ["git", "--version"],
}

PROJECT_DIRS = [
    f"{HOME}/Projects",
    f"{HOME}/JET",
    f"{HOME}/Desktop",
    f"{HOME}/Documents",
]

def is_allowed_code_file(path: Path) -> bool:
    allowed_extensions = [
        ".py", ".php", ".js", ".jsx", ".ts", ".tsx",
        ".blade.php", ".json", ".md", ".txt", ".css", ".html"
    ]

    path_str = str(path)

    if any(path_str.endswith(ext) for ext in allowed_extensions):
        return True

    if ".proposal-" in path_str:
        return True

    if ".backup-" in path_str:
        return True

    return False

def run_safe_command(command_key: str) -> str:
    if command_key not in ALLOWED_COMMANDS:
        return "Command blocked. This command is not approved."

    try:
        result = subprocess.run(
            ALLOWED_COMMANDS[command_key],
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "Command completed with no output."

    except Exception as e:
        return f"Command error: {e}"


def list_projects() -> str:
    found = []

    for directory in PROJECT_DIRS:
        path = Path(directory)

        if path.exists():
            for item in path.iterdir():
                if item.is_dir():
                    found.append(str(item))

    if not found:
        return "No projects found in common folders."

    return "Projects found:\n" + "\n".join(f"- {p}" for p in found)


def inspect_folder(folder_path: str) -> str:
    path = Path(folder_path).expanduser()

    if not path.exists():
        return "Folder not found."

    if not path.is_dir():
        return "That path is not a folder."

    items = list(path.iterdir())[:50]

    if not items:
        return "Folder is empty."

    return "\n".join(
        f"{'[DIR]' if item.is_dir() else '[FILE]'} {item.name}"
        for item in items
    )

def detect_project_stack(folder_path: str) -> str:
    path = Path(folder_path).expanduser()

    if not path.exists() or not path.is_dir():
        return "Project folder not found."

    detected = []

    checks = {
        "Laravel / PHP": ["artisan", "composer.json"],
        "Node / React / Vite": ["package.json", "vite.config.js"],
        "Python": ["requirements.txt", "main.py"],
        "Electron": ["electron", "main.cjs"],
        "Git Repository": [".git"],
        "Tailwind CSS": ["tailwind.config.js"],
    }

    for stack, files in checks.items():
        if any((path / file).exists() for file in files):
            detected.append(stack)

    if not detected:
        return "No known stack detected."

    return "Detected stack:\n" + "\n".join(f"- {item}" for item in detected)


def scan_project_files(folder_path: str) -> str:
    path = Path(folder_path).expanduser()

    if not path.exists() or not path.is_dir():
        return "Project folder not found."

    allowed_extensions = [".py", ".php", ".js", ".jsx", ".blade.php", ".json", ".env.example"]

    found = []

    for item in path.rglob("*"):
        if item.is_file() and any(str(item).endswith(ext) for ext in allowed_extensions):
            if any(skip in str(item) for skip in ["node_modules", "vendor", ".git", "venv"]):
                continue

            found.append(str(item))

        if len(found) >= 100:
            break

    if not found:
        return "No readable project files found."

    return "Project files found:\n" + "\n".join(f"- {file}" for file in found)

def read_project_file(file_path: str, max_chars: int = 8000) -> str:
    path = Path(file_path).expanduser()

    if not path.exists():
        return "File not found."

    if not path.is_file():
        return "That path is not a file."

    blocked_parts = [".env", "id_rsa", "id_ed25519", "storage/logs", ".git"]

    if any(part in str(path) for part in blocked_parts):
        return "Blocked. This file may contain secrets or sensitive system data."

    allowed_extensions = [
        ".py", ".php", ".js", ".jsx", ".ts", ".tsx",
        ".blade.php", ".json", ".md", ".txt", ".css", ".html"
    ]

    if not is_allowed_code_file(path):
        return "Blocked. This file type is not approved for reading."

    try:
        content = path.read_text(errors="replace")

        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[TRUNCATED: file is longer than preview limit]"

        return f"File: {path}\n\n{content}"

    except Exception as e:
        return f"File read error: {e}"
    
def write_project_file(file_path: str, content: str) -> str:
    path = Path(file_path).expanduser()

    blocked_parts = [".env", "id_rsa", "id_ed25519", "storage/logs", ".git"]

    if any(part in str(path) for part in blocked_parts):
        return "Blocked. This file may contain secrets or sensitive system data."

    allowed_extensions = [
        ".py", ".php", ".js", ".jsx", ".ts", ".tsx",
        ".blade.php", ".json", ".md", ".txt", ".css", ".html"
    ]

    if not is_allowed_code_file(path):
        return "Blocked. This file type is not approved for writing."

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            backup_path = path.with_suffix(path.suffix + f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
            shutil.copy2(path, backup_path)

        path.write_text(content)

        return f"File written successfully: {path}"

    except Exception as e:
        return f"File write error: {e}"
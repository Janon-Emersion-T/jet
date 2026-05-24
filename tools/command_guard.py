from pathlib import Path
import shlex

from tools.project_context_tools import get_current_project_path

DANGEROUS_PATTERNS = [
    "rm -rf", "sudo", "su ", "chmod 777", "chown", "mkfs", "dd ",
    ":(){", "shutdown", "reboot", "killall", "pkill", "curl | sh",
    "wget | sh", ">", ">>", "&& rm", "; rm", "| bash", "| sh",
]

ALLOWED_NPM_COMMANDS = {
    "build": ["npm", "run", "build"],
    "test": ["npm", "test"],
    "lint": ["npm", "run", "lint"],
    "audit": ["npm", "audit"],
}

ALLOWED_COMPOSER_COMMANDS = {
    "validate": ["composer", "validate"],
    "audit": ["composer", "audit"],
    "dump-autoload": ["composer", "dump-autoload"],
    "test": ["composer", "test"],
}


def get_workspace():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return Path(project).resolve(), None


def is_inside_workspace(path: Path, workspace: Path) -> bool:
    try:
        path.resolve().relative_to(workspace.resolve())
        return True
    except ValueError:
        return False


def block_dangerous_command(command_text: str):
    lowered = command_text.lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern in lowered:
            return True, f"Blocked dangerous command pattern: {pattern}"
    return False, None


def require_project_file(workspace: Path, filename: str):
    target = workspace / filename
    if not target.exists():
        return False, f"{filename} not found in current project."
    return True, None


def parse_safe_args(raw: str):
    try:
        return shlex.split(raw)
    except Exception:
        return []

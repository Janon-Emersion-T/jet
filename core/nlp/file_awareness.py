from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Dict, List, Optional


FILE_PATTERN = re.compile(
    r"(?P<path>[\w./~-]+\.(?:py|php|js|ts|jsx|tsx|md|txt|json|env|html|css|sql|blade\.php|yml|yaml|csv|xlsx|docx|pdf))",
    re.IGNORECASE,
)
FILE_ACTIONS = {
    "read": "read",
    "open": "read",
    "review": "read",
    "inspect": "read",
    "edit": "write",
    "update": "write",
    "write": "write",
    "delete": "delete",
    "remove": "delete",
}


@dataclass
class FileTarget:
    mention: str
    resolved_path: str
    exists: bool
    within_project: bool


@dataclass
class FileAwarenessResult:
    action: str = "none"
    targets: List[FileTarget] = field(default_factory=list)
    primary_target: Optional[str] = None


def _project_root(project_root: Optional[str] = None) -> Path:
    if project_root:
        return Path(project_root).expanduser().resolve()
    try:
        from tools.project_context_tools import get_current_project_path

        return get_current_project_path() or Path.cwd().resolve()
    except Exception:
        return Path.cwd().resolve()


def understand_file_command(text: str, entities: Optional[Dict[str, str]] = None,
                            project_root: Optional[str] = None) -> FileAwarenessResult:
    lowered = (text or "").lower()
    root = _project_root(project_root)
    mentions = [match.group("path") for match in FILE_PATTERN.finditer(text or "")]
    if entities and entities.get("file") and entities["file"] not in mentions:
        mentions.insert(0, entities["file"])

    action = next((value for key, value in FILE_ACTIONS.items() if key in lowered.split()), "none")
    targets = []
    for mention in dict.fromkeys(mentions):
        candidate = Path(mention).expanduser()
        resolved = (root / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
        try:
            resolved.relative_to(root)
            inside = True
        except ValueError:
            inside = False
        targets.append(FileTarget(mention, str(resolved), resolved.exists(), inside))

    return FileAwarenessResult(
        action=action,
        targets=targets,
        primary_target=targets[0].resolved_path if targets else None,
    )

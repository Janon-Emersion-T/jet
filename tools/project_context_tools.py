import json
from pathlib import Path
from datetime import datetime

from tools.system_tools import (
    detect_project_stack,
    scan_project_files,
    read_project_file,
)

from tools.event_tools import emit_event

STORAGE_DIR = Path("storage")
REGISTRY_FILE = STORAGE_DIR / "project_registry.json"
RECENT_FILE = STORAGE_DIR / "recent_projects.json"
CURRENT_FILE = STORAGE_DIR / "current_project.json"

MAX_RECENT = 10
MAX_MULTI_FILES = 8


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path, default):
    _ensure_storage()
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def _save_json(path, data):
    _ensure_storage()
    path.write_text(json.dumps(data, indent=4))


def _resolve_path(path_text: str) -> Path:
    return Path(path_text).expanduser().resolve()


def register_project_shortcut(name: str, path_text: str) -> str:
    name = name.lower().strip()
    path = _resolve_path(path_text)

    if not name:
        return "Project shortcut name is required."

    if not path.exists() or not path.is_dir():
        return "Project folder not found."

    registry = _load_json(REGISTRY_FILE, {})
    registry[name] = {
        "path": str(path),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "last_used_at": None,
    }

    _save_json(REGISTRY_FILE, registry)
    return f"Project shortcut registered: {name} -> {path}"


def list_project_shortcuts() -> str:
    registry = _load_json(REGISTRY_FILE, {})

    if not registry:
        return "No project shortcuts registered yet."

    lines = ["Project shortcut registry:"]
    for name, data in registry.items():
        lines.append(f"- {name}: {data['path']}")

    return "\n".join(lines)


def resolve_project(project_name_or_path: str) -> Path | None:
    key = project_name_or_path.lower().strip()
    registry = _load_json(REGISTRY_FILE, {})

    if key in registry:
        return Path(registry[key]["path"]).expanduser().resolve()

    path = _resolve_path(project_name_or_path)
    if path.exists() and path.is_dir():
        return path

    return None


def remember_recent_project(project_name_or_path: str) -> str:
    project = resolve_project(project_name_or_path)

    if not project:
        return "Project not found."

    recent = _load_json(RECENT_FILE, [])

    recent = [item for item in recent if item.get("path") != str(project)]
    recent.insert(0, {
        "path": str(project),
        "used_at": datetime.now().isoformat(timespec="seconds"),
    })

    recent = recent[:MAX_RECENT]
    _save_json(RECENT_FILE, recent)

    return f"Recent project remembered: {project}"


def list_recent_projects() -> str:
    recent = _load_json(RECENT_FILE, [])

    if not recent:
        return "No recent projects remembered yet."

    lines = ["Recent project memory:"]
    for item in recent:
        lines.append(f"- {item['path']} | {item.get('used_at', 'unknown time')}")

    return "\n".join(lines)


def set_current_project(project_name_or_path: str) -> str:
    project = resolve_project(project_name_or_path)

    if not project:
        return "Project not found."

    _save_json(CURRENT_FILE, {
        "path": str(project),
        "set_at": datetime.now().isoformat(timespec="seconds"),
    })

    remember_recent_project(str(project))

    emit_event(
        "PROJECT_CONTEXT_SET",
        "Project context set",
        f"Current project context set to: {project}",
    )

    return f"Current project context set to: {project}"


def get_current_project_path() -> Path | None:
    data = _load_json(CURRENT_FILE, {})
    path_text = data.get("path")

    if not path_text:
        return None

    path = Path(path_text).expanduser().resolve()
    return path if path.exists() and path.is_dir() else None


def show_current_project_context() -> str:
    project = get_current_project_path()

    if not project:
        return "No current project context set."

    stack = detect_project_stack(str(project))
    return f"Current project: {project}\n\n{stack}"


def auto_detect_active_project() -> str:
    cwd = Path.cwd().resolve()

    markers = [
        ".git",
        "artisan",
        "composer.json",
        "package.json",
        "requirements.txt",
        "main.py",
        "vite.config.js",
    ]

    current = cwd

    while current != current.parent:
        if any((current / marker).exists() for marker in markers):
            set_current_project(str(current))
            return f"Active project auto-detected and selected: {current}"

        current = current.parent

    return "No active project detected from current folder."


def read_multiple_files_safely(files_text: str) -> str:
    current_project = get_current_project_path()

    if not current_project:
        return "No current project selected. Use: use project <name-or-path>"

    files = [
        item.strip()
        for item in files_text.replace(",", "\n").splitlines()
        if item.strip()
    ]

    if not files:
        return "No files provided."

    if len(files) > MAX_MULTI_FILES:
        return f"Too many files. Maximum allowed is {MAX_MULTI_FILES} files at once."

    output = [f"Reading files from project: {current_project}"]

    for file_name in files:
        target = (current_project / file_name).resolve()

        if not str(target).startswith(str(current_project)):
            output.append(f"\nBlocked path traversal attempt: {file_name}")
            continue

        output.append("\n" + "=" * 80)
        output.append(f"FILE: {file_name}")
        output.append("=" * 80)
        output.append(read_project_file(str(target), max_chars=6000))

    return "\n".join(output)

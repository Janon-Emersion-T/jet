from pathlib import Path
from datetime import datetime
import hashlib
import json

from tools.command_guard import get_workspace

SNAPSHOT_ROOT = Path("storage/project_snapshots")
SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", "__pycache__",
    "storage/logs", "bootstrap/cache", "dist", "build", ".next",
}

ALLOWED_SUFFIXES = {
    ".py", ".php", ".js", ".jsx", ".ts", ".tsx", ".json",
    ".md", ".txt", ".css", ".html", ".env.example",
}


def _ensure():
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)


def _skip(path: Path):
    blocked_parts = {
        ".git",
        "node_modules",
        "vendor",
        "venv",
        "__pycache__",
        "dist",
        "build",
        ".next",
    }

    path_text = str(path)

    if any(part in path.parts for part in blocked_parts):
        return True

    blocked_paths = [
        "storage/project_backups",
        "storage/project_snapshots",
        "storage/logs",
        "bootstrap/cache",
    ]

    return any(blocked in path_text for blocked in blocked_paths)


def _hash_file(path: Path):
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        return None


def snapshot_project_state():
    workspace, error = get_workspace()
    if error:
        return error

    _ensure()

    snapshot_id = datetime.now().strftime("%Y%m%d%H%M%S")
    files = {}

    for file in workspace.rglob("*"):
        if _skip(file) or not file.is_file():
            continue

        if file.suffix not in ALLOWED_SUFFIXES and not str(file).endswith(".blade.php"):
            continue

        file_hash = _hash_file(file)
        if not file_hash:
            continue

        relative = str(file.relative_to(workspace))
        files[relative] = {
            "hash": file_hash,
            "size": file.stat().st_size,
            "modified_at": datetime.fromtimestamp(file.stat().st_mtime).isoformat(timespec="seconds"),
        }

    data = {
        "id": snapshot_id,
        "project": str(workspace),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "file_count": len(files),
        "files": files,
    }

    path = SNAPSHOT_ROOT / f"{snapshot_id}.json"
    path.write_text(json.dumps(data, indent=4))

    return (
        "PROJECT SNAPSHOT CREATED\n"
        f"ID: {snapshot_id}\n"
        f"Project: {workspace}\n"
        f"Tracked files: {len(files)}"
    )


def list_project_snapshots():
    _ensure()

    snapshots = []
    for file in sorted(SNAPSHOT_ROOT.glob("*.json"), reverse=True):
        try:
            snapshots.append(json.loads(file.read_text()))
        except Exception:
            continue

    if not snapshots:
        return "No project snapshots found."

    lines = ["PROJECT SNAPSHOTS"]
    for item in snapshots[:20]:
        lines.append(
            f"- {item['id']} | {item.get('file_count', 0)} files | {item.get('project')}"
        )

    return "\n".join(lines)


def compare_project_snapshots(old_id: str, new_id: str):
    old_file = SNAPSHOT_ROOT / f"{old_id}.json"
    new_file = SNAPSHOT_ROOT / f"{new_id}.json"

    if not old_file.exists():
        return "Old snapshot not found."

    if not new_file.exists():
        return "New snapshot not found."

    old = json.loads(old_file.read_text())
    new = json.loads(new_file.read_text())

    old_files = old.get("files", {})
    new_files = new.get("files", {})

    added = sorted(set(new_files) - set(old_files))
    removed = sorted(set(old_files) - set(new_files))
    changed = sorted(
        file for file in set(old_files) & set(new_files)
        if old_files[file]["hash"] != new_files[file]["hash"]
    )

    lines = [
        "SNAPSHOT COMPARISON",
        f"Old: {old_id}",
        f"New: {new_id}",
        "",
        f"Added files: {len(added)}",
        f"Removed files: {len(removed)}",
        f"Changed files: {len(changed)}",
    ]

    if added:
        lines.append("\nADDED:")
        lines.extend(f"- {file}" for file in added[:80])

    if removed:
        lines.append("\nREMOVED:")
        lines.extend(f"- {file}" for file in removed[:80])

    if changed:
        lines.append("\nCHANGED:")
        lines.extend(f"- {file}" for file in changed[:120])

    return "\n".join(lines)

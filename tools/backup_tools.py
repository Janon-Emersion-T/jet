from pathlib import Path
from datetime import datetime
import shutil
import json

from tools.command_guard import get_workspace, is_inside_workspace

BACKUP_ROOT = Path("storage/project_backups")

SKIP_DIRS = {
    ".git",
    "node_modules",
    "vendor",
    "venv",
    "__pycache__",
    "storage/logs",
    "bootstrap/cache",
    "dist",
    "build",
    ".next",
}


def _ensure():
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)


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


def create_project_backup():
    workspace, error = get_workspace()

    if error:
        return error

    _ensure()

    backup_id = datetime.now().strftime("%Y%m%d%H%M%S")

    target = BACKUP_ROOT / backup_id
    target.mkdir(parents=True, exist_ok=True)

    copied = 0

    for item in workspace.rglob("*"):
        if _skip(item):
            continue

        relative = item.relative_to(workspace)
        destination = target / relative

        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)
            copied += 1
        except Exception:
            continue

    meta = {
        "id": backup_id,
        "project": str(workspace),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "files_copied": copied,
    }

    (target / "backup_meta.json").write_text(
        json.dumps(meta, indent=4)
    )

    return (
        "PROJECT BACKUP CREATED\n"
        f"ID: {backup_id}\n"
        f"Project: {workspace}\n"
        f"Files copied: {copied}"
    )


def list_project_backups():
    _ensure()

    backups = []

    for folder in sorted(BACKUP_ROOT.iterdir(), reverse=True):
        meta = folder / "backup_meta.json"

        if meta.exists():
            try:
                backups.append(json.loads(meta.read_text()))
            except Exception:
                continue

    if not backups:
        return "No project backups found."

    lines = ["PROJECT BACKUPS"]

    for item in backups[:20]:
        lines.append(
            f"- {item['id']} | "
            f"{item.get('files_copied', 0)} files | "
            f"{item.get('project')}"
        )

    return "\n".join(lines)


def restore_project_backup(
    backup_id: str,
    confirmed: bool = False
):
    workspace, error = get_workspace()

    if error:
        return error

    backup_path = BACKUP_ROOT / backup_id

    if not backup_path.exists():
        return "Backup not found."

    if not confirmed:
        return (
            "RESTORE BLOCKED\n"
            "Restore mode requires confirmation because it overwrites files.\n"
            f"Use: confirm restore backup {backup_id}"
        )

    restored = 0

    for item in backup_path.rglob("*"):
        if item.name == "backup_meta.json":
            continue

        if item.is_dir():
            continue

        relative = item.relative_to(backup_path)

        destination = (
            workspace / relative
        ).resolve()

        if not is_inside_workspace(destination, workspace):
            continue

        try:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(item, destination)

            restored += 1

        except Exception:
            continue

    return (
        "PROJECT BACKUP RESTORED\n"
        f"ID: {backup_id}\n"
        f"Project: {workspace}\n"
        f"Files restored: {restored}"
    )
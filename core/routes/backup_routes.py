from tools.backup_tools import (
    create_project_backup,
    list_project_backups,
    restore_project_backup,
)

from tools.snapshot_tools import (
    snapshot_project_state,
    list_project_snapshots,
    compare_project_snapshots,
)


def handle_backup_routes(user_input: str, text: str, clean_text: str):
    if text in ["create backup", "backup project", "create project backup"]:
        return create_project_backup()

    if text in ["list backups", "project backups", "show backups"]:
        return list_project_backups()

    if text.startswith("restore backup "):
        backup_id = user_input.replace("restore backup ", "", 1).strip()
        return restore_project_backup(backup_id, confirmed=False)

    if text.startswith("confirm restore backup "):
        backup_id = user_input.replace("confirm restore backup ", "", 1).strip()
        return restore_project_backup(backup_id, confirmed=True)

    if text in ["snapshot project", "create snapshot", "snapshot project state"]:
        return snapshot_project_state()

    if text in ["list snapshots", "project snapshots", "show snapshots"]:
        return list_project_snapshots()

    if text.startswith("compare snapshots "):
        command = user_input.replace("compare snapshots ", "", 1).strip()
        parts = command.split()

        if len(parts) != 2:
            return "Invalid format. Use: compare snapshots OLD_ID NEW_ID"

        return compare_project_snapshots(parts[0], parts[1])

    return None

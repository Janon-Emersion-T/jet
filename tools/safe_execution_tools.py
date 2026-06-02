import subprocess
import json
from pathlib import Path
from datetime import datetime
import shlex

from tools.command_guard import (
    get_workspace,
    block_dangerous_command,
    require_project_file,
    ALLOWED_NPM_COMMANDS,
    ALLOWED_COMPOSER_COMMANDS,
)

MAX_OUTPUT = 12000
APPROVAL_DIR = Path("storage/command_approvals")


def _ensure():
    APPROVAL_DIR.mkdir(parents=True, exist_ok=True)


def _approval_file(command_id):
    return APPROVAL_DIR / f"{command_id}.json"


def _save_approval(command_type, command_key, command):
    _ensure()
    command_id = datetime.now().strftime("%Y%m%d%H%M%S")
    data = {
        "id": command_id,
        "type": command_type,
        "key": command_key,
        "command": command,
        "approved": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _approval_file(command_id).write_text(json.dumps(data, indent=4))
    return data


def _save_shell_approval(command_text: str, cwd: str | None = None):
    command = shlex.split(command_text)
    approval = _save_approval("shell", "shell", command)
    if cwd:
        data = json.loads(_approval_file(approval["id"]).read_text())
        data["cwd"] = cwd
        _approval_file(approval["id"]).write_text(json.dumps(data, indent=4))
        return data
    return approval


def _run(command, cwd, timeout=90):
    blocked, reason = block_dangerous_command(" ".join(command))
    if blocked:
        return reason

    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip() or result.stderr.strip() or "No output."
        return output[:MAX_OUTPUT]
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except Exception as e:
        return f"Command failed: {e}"


def request_npm_run(script_name: str):
    workspace, error = get_workspace()
    if error:
        return error

    ok, msg = require_project_file(workspace, "package.json")
    if not ok:
        return msg

    if script_name not in ALLOWED_NPM_COMMANDS:
        return (
            "NPM command blocked.\n"
            "Allowed commands:\n"
            + "\n".join(f"- {key}" for key in ALLOWED_NPM_COMMANDS)
        )

    command = ALLOWED_NPM_COMMANDS[script_name]
    approval = _save_approval("npm", script_name, command)

    return (
        "COMMAND APPROVAL REQUIRED\n"
        f"ID: {approval['id']}\n"
        f"Command: {' '.join(command)}\n\n"
        f"To execute: confirm command {approval['id']}"
    )


def request_composer_run(script_name: str):
    workspace, error = get_workspace()
    if error:
        return error

    ok, msg = require_project_file(workspace, "composer.json")
    if not ok:
        return msg

    if script_name not in ALLOWED_COMPOSER_COMMANDS:
        return (
            "Composer command blocked.\n"
            "Allowed commands:\n"
            + "\n".join(f"- {key}" for key in ALLOWED_COMPOSER_COMMANDS)
        )

    command = ALLOWED_COMPOSER_COMMANDS[script_name]
    approval = _save_approval("composer", script_name, command)

    return (
        "COMMAND APPROVAL REQUIRED\n"
        f"ID: {approval['id']}\n"
        f"Command: {' '.join(command)}\n\n"
        f"To execute: confirm command {approval['id']}"
    )


def request_shell_command(command_text: str, cwd: str | None = None):
    workspace, error = get_workspace()
    if error:
        return error

    command_text = (command_text or "").strip()
    if not command_text:
        return "Shell command is required."

    blocked, reason = block_dangerous_command(command_text)
    if blocked:
        return (
            "Shell command blocked.\n"
            f"{reason}\n\n"
            f"Command: {command_text}"
        )

    try:
        command = shlex.split(command_text)
    except Exception:
        return "Invalid shell command syntax."

    approval = _save_shell_approval(command_text, cwd=cwd or str(workspace))

    return (
        "COMMAND APPROVAL REQUIRED\n"
        f"ID: {approval['id']}\n"
        f"Command: {command_text}\n"
        f"Workspace: {workspace}\n\n"
        f"To execute: confirm command {approval['id']}"
    )


def confirm_command(command_id: str):
    workspace, error = get_workspace()
    if error:
        return error

    file = _approval_file(command_id)
    if not file.exists():
        return "Approval request not found."

    data = json.loads(file.read_text())
    command = data["command"]
    cwd = Path(data.get("cwd") or workspace)

    data["approved"] = True
    data["approved_at"] = datetime.now().isoformat(timespec="seconds")
    file.write_text(json.dumps(data, indent=4))

    return (
        "APPROVED COMMAND EXECUTION\n"
        f"Project: {cwd}\n"
        f"Command: {' '.join(command)}\n\n"
        + _run(command, cwd)
    )


def list_command_approvals():
    _ensure()
    files = sorted(APPROVAL_DIR.glob("*.json"), reverse=True)

    if not files:
        return "No command approvals found."

    lines = ["COMMAND APPROVALS"]
    for file in files[:20]:
        data = json.loads(file.read_text())
        status = "approved" if data.get("approved") else "pending"
        lines.append(f"- {data['id']} | {status} | {' '.join(data['command'])}")

    return "\n".join(lines)

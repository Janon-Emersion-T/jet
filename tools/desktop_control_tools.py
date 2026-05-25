import json
import subprocess
from pathlib import Path
from datetime import datetime

DESKTOP_DIR = Path("storage/desktop_control")
ACTION_FILE = DESKTOP_DIR / "desktop_actions.json"

ALLOWED_APPS = {
    "code": ["code"],
    "vscode": ["code"],
    "terminal": ["gnome-terminal"],
    "firefox": ["firefox"],
    "chrome": ["google-chrome"],
    "files": ["nautilus"],
    "file manager": ["nautilus"],
}

ALLOWED_ACTION_TYPES = ["keyboard", "mouse", "app_launcher"]


# ============================================================
# Storage Helpers
# ============================================================

def _ensure():
    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
    if not ACTION_FILE.exists():
        ACTION_FILE.write_text(json.dumps([], indent=4), encoding="utf-8")


def _load():
    _ensure()
    try:
        return json.loads(ACTION_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(items):
    _ensure()
    ACTION_FILE.write_text(json.dumps(items, indent=4), encoding="utf-8")


def _new_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def _create_action(action_type: str, details: dict):
    if action_type not in ALLOWED_ACTION_TYPES:
        return None, "Unsupported desktop action type."

    items = _load()

    action = {
        "id": _new_id(),
        "type": action_type,
        "details": details,
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "executed_at": None,
        "result": None,
    }

    items.append(action)
    _save(items)

    return action, None


def _find_action(action_id: str):
    items = _load()

    for index, action in enumerate(items):
        if action.get("id") == action_id:
            return items, index, action

    return items, None, None


# ============================================================
# Phase 196 — Desktop Control Status
# ============================================================

def desktop_control_status() -> str:
    return """DESKTOP CONTROL MODE — PHASE 196

Status:
Active with approval queue.

Safety Rules:
- JARVIS will not silently click.
- JARVIS will not silently type.
- JARVIS will not launch unrestricted apps.
- Every desktop action must be requested first.
- Execution requires: confirm desktop action <id>

Available Actions:
197. Keyboard automation
198. Mouse automation
199. App launcher
200. Desktop action executor
"""


# ============================================================
# Phase 197 — Keyboard Automation
# ============================================================

def keyboard_automation_request(text_to_type: str) -> str:
    text_to_type = text_to_type.strip()

    if not text_to_type:
        return "Keyboard text is required."

    if len(text_to_type) > 500:
        return "Keyboard automation blocked. Maximum allowed text length is 500 characters."

    action, error = _create_action("keyboard", {
        "text": text_to_type,
    })

    if error:
        return error

    return f"""KEYBOARD AUTOMATION REQUEST CREATED — PHASE 197

ID: {action['id']}
Action: type text
Text:
{text_to_type}

To execute:
confirm desktop action {action['id']}
"""


# ============================================================
# Phase 198 — Mouse Automation
# ============================================================

def mouse_automation_request(details: str) -> str:
    details = details.strip()

    if not details:
        return "Mouse action details are required."

    parts = details.split()

    if len(parts) not in [2, 3]:
        return """Invalid mouse format.

Use:
mouse automation request <x> <y>
mouse automation request <x> <y> click

Example:
mouse automation request 500 300
mouse automation request 500 300 click
"""

    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        return "Mouse coordinates must be numbers."

    action_mode = "move"

    if len(parts) == 3:
        if parts[2].lower() != "click":
            return "Only optional mouse action supported is: click"
        action_mode = "click"

    action, error = _create_action("mouse", {
        "x": x,
        "y": y,
        "mode": action_mode,
    })

    if error:
        return error

    return f"""MOUSE AUTOMATION REQUEST CREATED — PHASE 198

ID: {action['id']}
Mode: {action_mode}
Coordinates: {x}, {y}

To execute:
confirm desktop action {action['id']}
"""


# ============================================================
# Phase 199 — App Launcher
# ============================================================

def app_launcher_request(app_name: str) -> str:
    app_name = app_name.lower().strip()

    if not app_name:
        return "App name is required."

    if app_name not in ALLOWED_APPS:
        return (
            "App launch blocked. App is not in allowlist.\n\n"
            "Allowed apps:\n"
            + "\n".join(f"- {name}" for name in sorted(ALLOWED_APPS.keys()))
        )

    action, error = _create_action("app_launcher", {
        "app": app_name,
        "command": ALLOWED_APPS[app_name],
    })

    if error:
        return error

    return f"""APP LAUNCHER REQUEST CREATED — PHASE 199

ID: {action['id']}
App: {app_name}
Command: {' '.join(ALLOWED_APPS[app_name])}

To execute:
confirm desktop action {action['id']}
"""


# ============================================================
# Phase 200 — Action Executor
# ============================================================

def confirm_desktop_action(action_id: str) -> str:
    items, index, action = _find_action(action_id)

    if action is None:
        return "Desktop action not found."

    if action.get("status") == "executed":
        return f"Desktop action {action_id} was already executed."

    try:
        result = _execute_action(action)
    except Exception as e:
        result = f"Desktop action failed: {e}"

    action["status"] = "executed" if not result.startswith("Desktop action failed") else "failed"
    action["executed_at"] = datetime.now().isoformat(timespec="seconds")
    action["result"] = result

    items[index] = action
    _save(items)

    return f"""DESKTOP ACTION EXECUTED — PHASE 200

ID: {action_id}
Type: {action['type']}
Status: {action['status']}

Result:
{result}
"""


def _execute_action(action: dict) -> str:
    action_type = action.get("type")
    details = action.get("details", {})

    if action_type == "keyboard":
        return _execute_keyboard(details)

    if action_type == "mouse":
        return _execute_mouse(details)

    if action_type == "app_launcher":
        return _execute_app_launcher(details)

    return "Unsupported action type."


def _execute_keyboard(details: dict) -> str:
    try:
        import pyautogui
    except Exception:
        return "Desktop action failed: pyautogui is not installed."

    text = details.get("text", "")

    if not text:
        return "Desktop action failed: empty keyboard text."

    pyautogui.write(text, interval=0.02)

    return "Typed requested text."


def _execute_mouse(details: dict) -> str:
    try:
        import pyautogui
    except Exception:
        return "Desktop action failed: pyautogui is not installed."

    x = int(details.get("x"))
    y = int(details.get("y"))
    mode = details.get("mode", "move")

    pyautogui.moveTo(x, y, duration=0.2)

    if mode == "click":
        pyautogui.click()
        return f"Moved mouse to {x}, {y} and clicked."

    return f"Moved mouse to {x}, {y}."


def _execute_app_launcher(details: dict) -> str:
    app = details.get("app")
    command = details.get("command")

    if app not in ALLOWED_APPS:
        return "Desktop action failed: app is not allowlisted."

    if not command:
        return "Desktop action failed: missing app command."

    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return f"Launched app: {app}"


def list_desktop_actions() -> str:
    items = _load()

    if not items:
        return "No desktop actions found."

    lines = ["DESKTOP ACTION REQUESTS"]

    for item in reversed(items[-30:]):
        details = item.get("details", {})
        lines.append(
            f"- {item['id']} | {item['status']} | {item['type']} | {details}"
        )

    return "\n".join(lines)


def desktop_control_help() -> str:
    return """DESKTOP CONTROL COMMANDS — PHASES 196–200

196. desktop control status

197. keyboard automation request <text>
     Example:
     keyboard automation request Hello from JARVIS

198. mouse automation request <x> <y>
     mouse automation request <x> <y> click
     Example:
     mouse automation request 500 300
     mouse automation request 500 300 click

199. app launcher request <app>
     Allowed apps:
     code, vscode, terminal, firefox, chrome, files, file manager

200. list desktop actions
     confirm desktop action <id>
"""

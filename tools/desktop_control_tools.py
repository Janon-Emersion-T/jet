import json
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("storage/desktop_control")
BASE_DIR.mkdir(parents=True, exist_ok=True)

QUEUE_FILE = BASE_DIR / "approval_queue.json"
LOG_FILE = BASE_DIR / "execution_logs.json"
ALLOWLIST_FILE = BASE_DIR / "app_allowlist.json"
KILL_FILE = BASE_DIR / "emergency_stop.json"

ACTION_EXPIRY_MINUTES = 10
MAX_TEXT_LENGTH = 300


def _now():
    return datetime.now()


def _now_str():
    return _now().isoformat(timespec="seconds")


def _read(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _log(action_id, event, details=None):
    logs = _read(LOG_FILE, [])
    logs.append({
        "action_id": action_id,
        "event": event,
        "details": details or {},
        "time": _now_str(),
    })
    _write(LOG_FILE, logs)


def emergency_stop():
    _write(KILL_FILE, {"active": True, "time": _now_str()})
    _log("system", "emergency_stop_enabled")
    return {"success": True, "message": "Emergency stop enabled. Desktop actions blocked."}


def clear_emergency_stop():
    _write(KILL_FILE, {"active": False, "time": _now_str()})
    _log("system", "emergency_stop_cleared")
    return {"success": True, "message": "Emergency stop cleared."}


def is_emergency_stopped():
    state = _read(KILL_FILE, {"active": False})
    return bool(state.get("active"))


def _new_action(action_type, payload):
    queue = _read(QUEUE_FILE, [])
    action = {
        "id": f"desktop_action_{len(queue)+1}",
        "type": action_type,
        "payload": payload,
        "status": "pending_confirmation",
        "created_at": _now_str(),
        "expires_at": (_now() + timedelta(minutes=ACTION_EXPIRY_MINUTES)).isoformat(timespec="seconds"),
        "executed": False,
    }
    queue.append(action)
    _write(QUEUE_FILE, queue)
    _log(action["id"], "created", {"type": action_type})
    return action


def request_keyboard_text(text):
    if len(text) > MAX_TEXT_LENGTH:
        return {"success": False, "error": f"Keyboard text too long. Max {MAX_TEXT_LENGTH} characters."}
    return _new_action("keyboard_text", {"text": text})


def request_mouse_click(x, y):
    try:
        x = int(x)
        y = int(y)
    except Exception:
        return {"success": False, "error": "Mouse coordinates must be numbers."}

    if x < 0 or y < 0 or x > 10000 or y > 10000:
        return {"success": False, "error": "Mouse coordinates outside safe bounds."}

    return _new_action("mouse_click", {"x": x, "y": y})


def allow_app(app_name):
    apps = _read(ALLOWLIST_FILE, [])
    if app_name not in apps:
        apps.append(app_name)
    _write(ALLOWLIST_FILE, apps)
    return {"success": True, "allowlist": apps}


def list_allowed_apps():
    return _read(ALLOWLIST_FILE, [])


def request_app_launch(app_name):
    allowed = list_allowed_apps()
    if app_name not in allowed:
        return {"success": False, "error": f"App not allowlisted: {app_name}"}
    return _new_action("app_launch", {"app": app_name})


def list_actions():
    return _read(QUEUE_FILE, [])


def cancel_action(action_id):
    queue = _read(QUEUE_FILE, [])
    for action in queue:
        if action["id"] == action_id and action["status"] == "pending_confirmation":
            action["status"] = "cancelled"
            _write(QUEUE_FILE, queue)
            _log(action_id, "cancelled")
            return {"success": True, "action": action}
    return {"success": False, "error": "Pending action not found."}


def execute_action(action_id):
    if is_emergency_stopped():
        return {"success": False, "error": "Emergency stop is active."}

    queue = _read(QUEUE_FILE, [])

    for action in queue:
        if action["id"] != action_id:
            continue

        if action.get("executed"):
            return {"success": False, "error": "Replay blocked. Action already executed."}

        if action["status"] != "pending_confirmation":
            return {"success": False, "error": f"Action is not pending. Current status: {action['status']}"}

        if datetime.fromisoformat(action["expires_at"]) < _now():
            action["status"] = "expired"
            _write(QUEUE_FILE, queue)
            _log(action_id, "expired")
            return {"success": False, "error": "Action expired."}

        try:
            import pyautogui

            if action["type"] == "keyboard_text":
                pyautogui.write(action["payload"]["text"], interval=0.01)

            elif action["type"] == "mouse_click":
                pyautogui.click(action["payload"]["x"], action["payload"]["y"])

            elif action["type"] == "app_launch":
                import subprocess
                subprocess.Popen([action["payload"]["app"]])

            else:
                return {"success": False, "error": "Unsupported action type."}

            action["status"] = "executed"
            action["executed"] = True
            action["executed_at"] = _now_str()
            _write(QUEUE_FILE, queue)
            _log(action_id, "executed")
            return {"success": True, "action": action}

        except Exception as e:
            _log(action_id, "failed", {"error": str(e)})
            return {"success": False, "error": str(e)}

    return {"success": False, "error": "Action not found."}

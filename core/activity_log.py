import json
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("storage")
ACTIVITY_LOG_FILE = LOG_DIR / "ui_activity_log.jsonl"


def _ensure_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_activity(event_type: str, payload: dict | None = None):
    _ensure_dir()
    entry = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "event_type": event_type,
        "payload": payload or {},
    }
    with ACTIVITY_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def list_recent_activity(limit: int = 50):
    _ensure_dir()
    if not ACTIVITY_LOG_FILE.exists():
        return []

    lines = ACTIVITY_LOG_FILE.read_text(encoding="utf-8").splitlines()
    entries = []
    for line in reversed(lines[-limit:]):
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
    return entries

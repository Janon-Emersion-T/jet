import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


CHAT_STORAGE_PATH = Path("storage/chat_sessions.json")


def _now() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _ensure_storage() -> None:
    CHAT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CHAT_STORAGE_PATH.exists():
        CHAT_STORAGE_PATH.write_text(
            json.dumps({"sessions": []}, indent=4),
            encoding="utf-8",
        )


def _load_data() -> Dict:
    _ensure_storage()

    try:
        return json.loads(CHAT_STORAGE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"sessions": []}


def _save_data(data: Dict) -> None:
    CHAT_STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHAT_STORAGE_PATH.write_text(json.dumps(data, indent=4), encoding="utf-8")


def _default_title(message: str) -> str:
    clean = " ".join((message or "").strip().split())

    if not clean:
        return "New chat"

    return clean[:42] + ("..." if len(clean) > 42 else "")


def list_chat_sessions() -> List[Dict]:
    data = _load_data()

    sessions = data.get("sessions", [])

    sorted_sessions = sorted(
        sessions,
        key=lambda item: item.get("updated_at", ""),
        reverse=True,
    )

    return [
        {
            "id": session["id"],
            "title": session.get("title", "New chat"),
            "created_at": session.get("created_at"),
            "updated_at": session.get("updated_at"),
            "message_count": len(session.get("messages", [])),
        }
        for session in sorted_sessions
    ]


def create_chat_session(title: str = "New chat") -> Dict:
    data = _load_data()

    session = {
        "id": str(uuid.uuid4()),
        "title": title or "New chat",
        "created_at": _now(),
        "updated_at": _now(),
        "messages": [
            {
                "role": "jarvis",
                "text": "JARVIS desktop interface online. Awaiting your command, Janon.",
                "created_at": _now(),
            }
        ],
    }

    data.setdefault("sessions", []).append(session)
    _save_data(data)

    return session


def get_chat_session(chat_id: str) -> Optional[Dict]:
    data = _load_data()

    for session in data.get("sessions", []):
        if session.get("id") == chat_id:
            return session

    return None


def ensure_chat_session(chat_id: Optional[str] = None) -> Dict:
    if chat_id:
        existing = get_chat_session(chat_id)

        if existing:
            return existing

    return create_chat_session()


def append_message(chat_id: str, role: str, text: str) -> Dict:
    data = _load_data()

    for session in data.get("sessions", []):
        if session.get("id") == chat_id:
            message = {
                "role": role,
                "text": text,
                "created_at": _now(),
            }

            session.setdefault("messages", []).append(message)
            session["updated_at"] = _now()

            user_messages = [
                item for item in session.get("messages", [])
                if item.get("role") == "user"
            ]

            if role == "user" and len(user_messages) == 1:
                session["title"] = _default_title(text)

            _save_data(data)
            return session

    session = create_chat_session()
    return append_message(session["id"], role, text)


def rename_chat_session(chat_id: str, title: str) -> Optional[Dict]:
    data = _load_data()

    for session in data.get("sessions", []):
        if session.get("id") == chat_id:
            session["title"] = title.strip() or "New chat"
            session["updated_at"] = _now()
            _save_data(data)
            return session

    return None


def delete_chat_session(chat_id: str) -> bool:
    data = _load_data()

    original_count = len(data.get("sessions", []))

    data["sessions"] = [
        session for session in data.get("sessions", [])
        if session.get("id") != chat_id
    ]

    deleted = len(data["sessions"]) < original_count

    if deleted:
        _save_data(data)

    return deleted


def build_recent_context(chat_id: str, limit: int = 8) -> str:
    session = get_chat_session(chat_id)

    if not session:
        return ""

    messages = session.get("messages", [])[-limit:]

    lines = []

    for message in messages:
        role = message.get("role", "unknown")
        text = message.get("text", "")

        if not text:
            continue

        lines.append(f"{role.upper()}: {text}")

    return "\n".join(lines)
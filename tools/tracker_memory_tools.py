import sqlite3
from datetime import datetime

DB_PATH = "storage/memory.db"


def _conn():
    return sqlite3.connect(DB_PATH)


def init_tracker_memory():
    conn = _conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracker_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracker_type TEXT NOT NULL,
            title TEXT NOT NULL,
            details TEXT,
            status TEXT DEFAULT 'open',
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_tracker_item(tracker_type: str, title: str, details: str = ""):
    init_tracker_memory()

    conn = _conn()
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO tracker_memory
        (tracker_type, title, details, status, created_at, updated_at)
        VALUES (?, ?, ?, 'open', ?, ?)
    """, (tracker_type, title, details, now, now))

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return f"{tracker_type.title()} tracker item added: #{item_id} {title}"


def list_tracker_items(tracker_type: str):
    init_tracker_memory()

    conn = _conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, details, status, created_at
        FROM tracker_memory
        WHERE tracker_type = ?
        ORDER BY id DESC
        LIMIT 30
    """, (tracker_type,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No {tracker_type} tracker items found."

    lines = [f"{tracker_type.upper()} TRACKER"]
    for item_id, title, details, status, created_at in rows:
        lines.append(f"- #{item_id} | {status} | {title} | {created_at}")
        if details:
            lines.append(f"  {details[:300]}")

    return "\n".join(lines)


def update_tracker_status(item_id: str, status: str):
    init_tracker_memory()

    conn = _conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tracker_memory
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (status, datetime.now().isoformat(timespec="seconds"), item_id))

    conn.commit()
    changed = cursor.rowcount
    conn.close()

    if not changed:
        return "Tracker item not found."

    return f"Tracker item #{item_id} updated to: {status}"

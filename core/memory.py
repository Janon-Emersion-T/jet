import sqlite3
import json
from datetime import datetime
from pathlib import Path

from core.vector_memory.vector_store import (
    get_vector_memory_summary,
    list_vector_memory_data,
)

DB_PATH = "storage/memory.db"

Path("storage").mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def normalize_for_memory(value):
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    try:
        return json.dumps(value, indent=2, ensure_ascii=False, default=str)
    except Exception:
        return str(value)


def init_memory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            jarvis_response TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT UNIQUE,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_memory(user_input: str, jarvis_response):
    conn = get_connection()
    cursor = conn.cursor()

    safe_response = normalize_for_memory(jarvis_response)

    cursor.execute("""
        INSERT INTO memory (user_input, jarvis_response, created_at)
        VALUES (?, ?, ?)
    """, (str(user_input), safe_response, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def save_fact(fact: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO facts (fact, created_at)
            VALUES (?, ?)
        """, (fact.strip(), datetime.now().isoformat()))
        conn.commit()
        result = "Fact saved to memory."
    except sqlite3.IntegrityError:
        result = "I already remember that."

    conn.close()
    return result


def list_facts_data(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fact, created_at
        FROM facts
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "fact": row[1],
            "created_at": row[2],
        }
        for row in rows
    ]


def list_recent_memories(limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_input, jarvis_response, created_at
        FROM memory
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "user_input": row[1],
            "jarvis_response": row[2],
            "created_at": row[3],
        }
        for row in rows
    ]


def get_memory_overview(limit: int = 12):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM memory")
    memory_count = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM facts")
    fact_count = cursor.fetchone()[0] or 0

    conn.close()

    recent_facts = list_facts_data(limit=limit)
    recent_memories = list_recent_memories(limit=limit)
    vector_summary = get_vector_memory_summary()
    vector_memories = list_vector_memory_data(limit=limit)

    return {
        "stats": {
            "facts": fact_count,
            "memories": memory_count,
            "vector_memories": vector_summary.get("active", 0),
            "semantic_index": vector_summary.get("total", 0),
        },
        "recent_facts": recent_facts,
        "recent_memories": recent_memories,
        "vector_summary": vector_summary,
        "vector_memories": vector_memories,
        "has_vector_index": bool(vector_summary.get("total")),
    }

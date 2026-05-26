import sqlite3
import json
from datetime import datetime
from pathlib import Path

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

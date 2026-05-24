import sqlite3
from datetime import datetime

DB_PATH = "storage/memory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

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

def save_memory(user_input: str, jarvis_response: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memory (user_input, jarvis_response, created_at)
        VALUES (?, ?, ?)
    """, (user_input, jarvis_response, datetime.now().isoformat()))

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
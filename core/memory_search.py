import sqlite3

DB_PATH = "storage/memory.db"

def search_memory(query: str, limit: int = 5) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    like_query = f"%{query}%"

    cursor.execute("""
        SELECT user_input, jarvis_response, created_at
        FROM memory
        WHERE user_input LIKE ? OR jarvis_response LIKE ?
        ORDER BY id DESC
        LIMIT ?
    """, (like_query, like_query, limit))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No matching memory found."

    results = []

    for user_input, jarvis_response, created_at in rows:
        results.append(
            f"Date: {created_at}\n"
            f"User: {user_input}\n"
            f"JARVIS: {jarvis_response[:500]}"
        )

    return "\n\n---\n\n".join(results)


def get_relevant_memory(query: str, limit: int = 5) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    words = [w for w in query.lower().split() if len(w) > 3]

    if not words:
        conn.close()
        return ""

    conditions = " OR ".join(
        ["LOWER(user_input) LIKE ? OR LOWER(jarvis_response) LIKE ?" for _ in words]
    )

    params = []
    for word in words:
        params.extend([f"%{word}%", f"%{word}%"])

    cursor.execute(f"""
        SELECT user_input, jarvis_response
        FROM memory
        WHERE {conditions}
        ORDER BY id DESC
        LIMIT ?
    """, (*params, limit))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return ""

    return "\n".join(
        f"- User previously asked: {u}\n  JARVIS replied: {r[:300]}"
        for u, r in rows
    )


def list_facts(limit: int = 20) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fact, created_at
        FROM facts
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No saved facts yet."

    return "\n".join(f"- {fact}" for fact, created_at in rows)
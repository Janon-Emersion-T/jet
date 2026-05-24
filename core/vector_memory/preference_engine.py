from core.vector_memory.vector_store import _load_meta


def get_user_preferences():
    memories = [
        m for m in _load_meta()
        if m.get("active", True)
        and (
            "preference" in m.get("tags", [])
            or "prefer" in m.get("text", "").lower()
            or "always" in m.get("text", "").lower()
            or "never" in m.get("text", "").lower()
        )
    ]

    if not memories:
        return "No user preferences found."

    memories = sorted(memories, key=lambda x: x.get("importance", 0), reverse=True)

    lines = ["USER PREFERENCE ENGINE"]
    for item in memories[:20]:
        lines.append(
            f"- {item['id']} | importance {item['importance']} | {item['text']}"
        )

    return "\n".join(lines)

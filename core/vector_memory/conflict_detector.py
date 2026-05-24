from core.vector_memory.vector_store import _load_meta


def detect_memory_conflicts():
    memories = [m for m in _load_meta() if m.get("active", True)]

    if not memories:
        return "No memories available for conflict detection."

    conflicts = []

    for a in memories:
        for b in memories:
            if a["id"] == b["id"]:
                continue

            a_text = a["text"].lower()
            b_text = b["text"].lower()

            if "always" in a_text and "never" in b_text:
                shared = set(a_text.split()) & set(b_text.split())
                if len(shared) >= 3:
                    conflicts.append((a, b))

    if not conflicts:
        return "No obvious memory conflicts detected."

    lines = ["POSSIBLE MEMORY CONFLICTS"]
    for a, b in conflicts[:10]:
        lines.append(
            f"\n- {a['id']}: {a['text']}\n"
            f"  conflicts with\n"
            f"  {b['id']}: {b['text']}"
        )

    return "\n".join(lines)

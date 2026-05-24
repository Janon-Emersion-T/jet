from core.vector_memory.vector_store import (
    add_vector_memory,
    search_vector_memory,
    list_vector_memories,
    cleanup_low_importance,
)
from core.vector_memory.conflict_detector import detect_memory_conflicts
from core.vector_memory.preference_engine import get_user_preferences


def handle_vector_memory_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("remember semantic "):
        content = user_input.replace("remember semantic ", "", 1).strip()
        return add_vector_memory(
            content,
            tags=["semantic"],
            source="manual"
        )

    if text.startswith("remember preference "):
        content = user_input.replace("remember preference ", "", 1).strip()
        return add_vector_memory(
            content,
            tags=["preference"],
            source="preference"
        )

    if text.startswith("semantic search "):
        query = user_input.replace("semantic search ", "", 1).strip()
        return search_vector_memory(query)

    if text in ["vector memories", "list vector memories", "semantic memories"]:
        return list_vector_memories()

    if text in ["memory cleanup", "cleanup memory"]:
        return cleanup_low_importance()

    if text in ["memory conflicts", "detect memory conflicts"]:
        return detect_memory_conflicts()

    if text in ["user preferences", "preference engine"]:
        return get_user_preferences()

    return None

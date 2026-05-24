from core.memory import save_fact
from core.memory_search import search_memory, list_facts


def handle_memory_routes(user_input: str, text: str, clean_text: str):
    if clean_text.startswith("remember that "):
        fact = user_input.replace("remember that ", "", 1).strip()
        return save_fact(fact)

    if clean_text in [
        "list facts",
        "show facts",
        "what do you remember"
    ]:
        return list_facts()

    if clean_text.startswith("search memory "):
        query = user_input.replace("search memory ", "", 1).strip()
        return search_memory(query)

    return None

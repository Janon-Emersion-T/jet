from typing import Dict, List


_CONVERSATION_LINKS: List[Dict[str, str]] = []


def link_conversation_turn(user_text: str, intent: str, clean_text: str, entities: Dict[str, str]) -> None:
    _CONVERSATION_LINKS.append({
        "user_text": user_text,
        "intent": intent,
        "clean_text": clean_text,
        "file": entities.get("file", ""),
        "repo": entities.get("github_repo", ""),
        "url": entities.get("url", ""),
        "phase_start": entities.get("phase_start", ""),
        "phase_end": entities.get("phase_end", ""),
    })

    if len(_CONVERSATION_LINKS) > 25:
        _CONVERSATION_LINKS.pop(0)


def get_recent_conversation_links(limit: int = 5) -> List[Dict[str, str]]:
    return _CONVERSATION_LINKS[-limit:]


def format_conversation_links(limit: int = 5) -> str:
    links = get_recent_conversation_links(limit)

    if not links:
        return "No recent NLP conversation links found."

    lines = ["RECENT NLP CONVERSATION LINKS"]

    for item in links:
        lines.append(
            f"- Intent: {item['intent']} | Command: {item['clean_text']} | "
            f"File: {item['file'] or '-'} | Repo: {item['repo'] or '-'} | URL: {item['url'] or '-'}"
        )

    return "\n".join(lines)

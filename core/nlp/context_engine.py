from typing import Dict, Optional


_LAST_CONTEXT: Dict[str, Optional[str]] = {
    "last_intent": None,
    "last_file": None,
    "last_repo": None,
    "last_url": None,
    "last_command": None,
}


FOLLOW_UP_WORDS = [
    "continue",
    "do it",
    "next",
    "proceed",
    "again",
    "same",
    "go on",
    "move on",
    "yes",
    "ok",
    "okay",
]


def update_context(intent: str, clean_text: str, entities: Dict[str, str]) -> None:
    _LAST_CONTEXT["last_intent"] = intent
    _LAST_CONTEXT["last_command"] = clean_text

    if entities.get("file"):
        _LAST_CONTEXT["last_file"] = entities["file"]

    if entities.get("github_repo"):
        _LAST_CONTEXT["last_repo"] = entities["github_repo"]

    if entities.get("url"):
        _LAST_CONTEXT["last_url"] = entities["url"]


def is_follow_up(clean_text: str) -> bool:
    text = clean_text.strip().lower()
    return text in FOLLOW_UP_WORDS or any(text.startswith(word + " ") for word in FOLLOW_UP_WORDS)


def resolve_contextual_command(clean_text: str, intent: str, entities: Dict[str, str]) -> str:
    if not is_follow_up(clean_text):
        return clean_text

    last_intent = _LAST_CONTEXT.get("last_intent")
    last_file = _LAST_CONTEXT.get("last_file")
    last_repo = _LAST_CONTEXT.get("last_repo")
    last_url = _LAST_CONTEXT.get("last_url")
    last_command = _LAST_CONTEXT.get("last_command")

    if last_intent == "project_analysis" and last_repo:
        return f"analyze project {last_repo}"

    if last_intent == "project_analysis":
        return "analyze project"

    if last_intent == "devops":
        return last_command or "git status"

    if last_intent == "database":
        return last_command or "database analyzer"

    if last_intent == "content":
        return last_command or "generate content"

    if last_file:
        return f"read file {last_file}"

    if last_url:
        return f"open browser {last_url}"

    return last_command or clean_text

from typing import Dict, Optional


INTENT_TO_ROUTE_HINT = {
    "project_analysis": "project",
    "devops": "devops",
    "database": "database",
    "content": "content",
    "email": "email",
    "browser_control": "browser",
    "google_search": "browser",
    "memory": "memory",
    "task": "task",
    "patch_workflow": "patch",
    "camera": "vision",
    "nlp": "nlp",
}


def resolve_route_hint(intent: str, clean_text: str, entities: Dict[str, str]) -> Optional[str]:
    if entities.get("file"):
        return "file"

    if entities.get("github_repo"):
        return "github"

    if entities.get("url"):
        return "browser"

    if intent in INTENT_TO_ROUTE_HINT:
        return INTENT_TO_ROUTE_HINT[intent]

    if "laravel" in clean_text:
        return "laravel"

    if "nginx" in clean_text or "server" in clean_text:
        return "devops"

    if "mysql" in clean_text or "migration" in clean_text:
        return "database"

    return None

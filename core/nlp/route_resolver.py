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
    "web_development": "web_development",
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

    if any(term in clean_text for term in ["laravel", "blade", "tailwind", "alpine", "vite", "migration", "controller", "model", "view", "readme", "web application"]):
        return "web_development"

    if intent in INTENT_TO_ROUTE_HINT:
        return INTENT_TO_ROUTE_HINT[intent]

    if "nginx" in clean_text or "server" in clean_text:
        return "devops"

    if "mysql" in clean_text or "migration" in clean_text:
        return "database"

    return None

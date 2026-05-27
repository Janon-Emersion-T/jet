ROUTE_COMMAND_PREFIX = {
    "devops": "devops:",
    "database": "database:",
    "email": "email:",
    "content": "content:",
    "project": "project:",
    "browser": "browser:",
    "memory": "memory:",
    "task": "task:",
    "patch": "patch:",
    "vision": "vision:",
    "laravel": "laravel:",
}


def map_route_command(clean_text: str, route_hint: str | None) -> str:
    if not route_hint:
        return clean_text

    prefix = ROUTE_COMMAND_PREFIX.get(route_hint)

    if not prefix:
        return clean_text

    if clean_text.startswith(prefix):
        return clean_text

    return f"{prefix} {clean_text}"

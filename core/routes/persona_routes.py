import re

from core.persona_registry import (
    format_persona_team,
    get_persona,
    load_persona_settings,
    set_default_persona,
)


def handle_persona_routes(user_input: str, text: str, clean_text: str):
    lowered = user_input.strip().lower()
    if lowered in ["my team", "show my team", "jarvis team", "list specialists", "list experts"]:
        return format_persona_team()

    match = re.match(r"^(?:who is|show persona|show specialist)\s+([a-z]+)\??$", lowered)
    if match:
        name = match.group(1)
        if name not in load_persona_settings()["personas"]:
            return f"Unknown specialist: {name}. Use `show my team` to list configured personas."
        persona = get_persona(name)
        return f"{persona.name} - {persona.role}\n{persona.identity}"

    match = re.match(r"^(?:set default assistant|switch assistant to|use)\s+([a-z]+)$", lowered)
    if match:
        name = match.group(1)
        if set_default_persona(name):
            persona = get_persona(name)
            return f"Default assistant set to {persona.name}, your {persona.role}."
        return f"Unknown specialist: {name}. Use `show my team` to list configured personas."

    return None

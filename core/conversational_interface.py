from dataclasses import dataclass
import re
from typing import Optional

from core.persona_registry import Persona, explicitly_addressed_persona, get_persona


@dataclass
class ConversationalRequest:
    original_text: str
    routed_text: str
    persona: Persona
    explicitly_addressed: bool


def _remove_address(text: str, persona: Persona) -> str:
    pattern = rf"^\s*(?:(?:hey|hi|hello|ask|tell)\s+|talk\s+to\s+)?{re.escape(persona.name)}\s*(?:[,,:]|\bto\b|\babout\b)?\s*"
    return re.sub(pattern, "", text, flags=re.IGNORECASE).strip() or text


def _natural_tool_phrase(text: str) -> str:
    rewritten = text.strip()
    substitutions = [
        (r"^(?:could you |can you |please )?(?:tell me )?(?:what(?:'s| is) (?:the )?weather like|how(?:'s| is) (?:the )?weather)(?:\s+in\s+(.+))?\??$", lambda m: f"weather in {m.group(1)}" if m.group(1) else "weather"),
        (r"^(?:could you |can you |please )?(?:tell me )?(?:do i need an umbrella|is it raining)(?:\s+in\s+(.+))?\??$", lambda m: f"weather in {m.group(1)}" if m.group(1) else "weather"),
        (r"^(?:could you |can you |please )?(?:tell me )?where (?:am i|do you think i am)(?:\s+(?:right now|at))?\??$", lambda m: "current location"),
        (r"^(?:could you |can you |please )?show me (?:the )?weather(?:\s+in\s+(.+))?\??$", lambda m: f"weather in {m.group(1)}" if m.group(1) else "weather"),
        (r"^(?:could you |can you |please )?(?:read|open) (?:the )?(?:file )?([\w./~-]+\.[a-z0-9.]+)\??$", lambda m: f"read file {m.group(1)}"),
        (r"^(?:could you |can you |please )?(?:review|look at|inspect) (?:the )?(?:file )?([\w./~-]+\.[a-z0-9.]+)\??$", lambda m: f"review file {m.group(1)}"),
        (r"^(?:could you |can you |please )?(?:check|show me) (?:the )?(?:git|repository|repo) status\??$", lambda m: "git status"),
        (r"^(?:could you |can you |please )?(?:show me|check) (?:what(?:'s| is) changed|the changes)(?: in git)?\??$", lambda m: "git diff"),
        (r"^(?:could you |can you |please )?(?:email|notify) me (?:whenever|when) (?:something|anything) needs (?:my )?attention\??$", lambda m: "enable attention emails"),
    ]
    for pattern, replacement in substitutions:
        match = re.match(pattern, rewritten, flags=re.IGNORECASE)
        if match:
            return replacement(match).strip(" ?.")
    return rewritten


def interpret_conversation(text: str, domain: Optional[str] = None) -> ConversationalRequest:
    explicit = explicitly_addressed_persona(text)
    persona = explicit or get_persona(domain=domain)
    routed = _remove_address(text, persona) if explicit else text
    routed = _natural_tool_phrase(routed)
    return ConversationalRequest(text, routed, persona, bool(explicit))

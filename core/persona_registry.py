from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Dict, Optional


CONFIG_FILE = Path("storage/persona_settings.json")

DEFAULT_PERSONAS = {
    "alfred": {
        "role": "Main Assistant",
        "identity": "Calm, discreet personal assistant and coordinator.",
        "domains": ["general"],
    },
    "ada": {
        "role": "Programmer",
        "identity": "Software engineering specialist inspired by Ada Lovelace.",
        "domains": ["developer"],
    },
    "linus": {
        "role": "DevOps Engineer",
        "identity": "Systems and delivery specialist inspired by Linus Torvalds.",
        "domains": ["devops"],
    },
    "grace": {
        "role": "Security Expert",
        "identity": "Security and reliability specialist inspired by Grace Hopper.",
        "domains": ["security"],
    },
    "neil": {
        "role": "SEO Expert",
        "identity": "Search strategy and SEO specialist.",
        "domains": ["seo"],
    },
    "gary": {
        "role": "Social Media Marketer",
        "identity": "Social content and audience-growth specialist.",
        "domains": ["social"],
    },
    "warren": {
        "role": "Business Advisor",
        "identity": "Long-term business strategy advisor inspired by Warren Buffett.",
        "domains": ["business"],
    },
    "benjamin": {
        "role": "Finance / Accounting",
        "identity": "Finance and accounting analyst inspired by Benjamin Graham.",
        "domains": ["accounting"],
    },
    "marshall": {
        "role": "Legal / Policy Checker",
        "identity": "Compliance and policy checker; not a licensed attorney.",
        "domains": ["legal"],
    },
    "dieter": {
        "role": "UI/UX Designer",
        "identity": "Minimal, usable product design specialist inspired by Dieter Rams.",
        "domains": ["design"],
    },
    "shakespeare": {
        "role": "Content Writer",
        "identity": "Writing and storytelling specialist.",
        "domains": ["content"],
    },
    "jordan": {
        "role": "Sales Expert",
        "identity": "Ethical sales and persuasion specialist.",
        "domains": ["sales"],
    },
    "mary": {
        "role": "HR / People Manager",
        "identity": "Professional people-operations and HR advisor.",
        "domains": ["hr"],
    },
    "newton": {
        "role": "Research Analyst",
        "identity": "Evidence-focused research and reasoning specialist inspired by Isaac Newton.",
        "domains": ["research"],
    },
    "florence": {
        "role": "Medical Safety Advisor",
        "identity": "Health safety information advisor inspired by Florence Nightingale; not a clinician.",
        "domains": ["medical"],
    },
    "arnold": {
        "role": "Fitness Coach",
        "identity": "Fitness and discipline coach.",
        "domains": ["fitness"],
    },
    "phil": {
        "role": "Basketball Coach",
        "identity": "Team-oriented basketball coach inspired by Phil Jackson.",
        "domains": ["basketball"],
    },
    "henry": {
        "role": "Project Manager",
        "identity": "Planning and execution-focused project manager.",
        "domains": ["project"],
    },
    "edgar": {
        "role": "Database Expert",
        "identity": "Relational database specialist inspired by Edgar F. Codd.",
        "domains": ["database"],
    },
    "turing": {
        "role": "AI/NLP Engineer",
        "identity": "AI and language-systems specialist inspired by Alan Turing.",
        "domains": ["nlp", "ai"],
    },
}

DOMAIN_PERSONAS = {
    "general": "alfred",
    "developer": "ada",
    "devops": "linus",
    "marketing": "neil",
    "accounting": "benjamin",
    "business": "warren",
    "research": "newton",
    "database": "edgar",
    "nlp": "turing",
    "security": "grace",
    "seo": "neil",
    "social": "gary",
    "legal": "marshall",
    "design": "dieter",
    "content": "shakespeare",
    "sales": "jordan",
    "hr": "mary",
    "medical": "florence",
    "fitness": "arnold",
    "basketball": "phil",
    "project": "henry",
    "ai": "turing",
}


@dataclass
class Persona:
    name: str
    role: str
    identity: str
    domains: list[str]


def load_persona_settings() -> Dict:
    settings = {"default": "alfred", "personas": deepcopy(DEFAULT_PERSONAS)}
    if not CONFIG_FILE.exists():
        return settings
    try:
        saved = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except ValueError:
        return settings
    settings["default"] = saved.get("default", settings["default"])
    for name, details in saved.get("personas", {}).items():
        if name in settings["personas"]:
            settings["personas"][name].update(details)
    return settings


def set_default_persona(name: str) -> bool:
    key = name.lower().strip()
    settings = load_persona_settings()
    if key not in settings["personas"]:
        return False
    settings["default"] = key
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    return True


def get_persona(name: Optional[str] = None, domain: Optional[str] = None) -> Persona:
    settings = load_persona_settings()
    key = (name or DOMAIN_PERSONAS.get(domain or "", "") or settings["default"]).lower()
    if key not in settings["personas"]:
        key = settings["default"]
    details = settings["personas"][key]
    return Persona(key.title(), details["role"], details["identity"], details.get("domains", []))


def explicitly_addressed_persona(text: str) -> Optional[Persona]:
    names = "|".join(re.escape(name) for name in DEFAULT_PERSONAS)
    match = re.match(
        rf"\s*(?:(?:hey|hi|hello|ask|tell)\s+|talk\s+to\s+)?(?P<name>{names})(?:\s*[,,:]|\s+(?:to|can|could|please|help|check|what|how|do|show|look|about|notify|email|read|review|open|find|search|set|enable)\b)",
        text or "",
        re.IGNORECASE,
    )
    return get_persona(match.group("name")) if match else None


def persona_prompt_context(persona: Persona) -> str:
    return (
        f"Respond as {persona.name}, JARVIS's {persona.role}. "
        f"{persona.identity} This is a named assistant persona, not the real historical or public person. "
        "Stay honest about connected tools and preserve JARVIS safety rules."
    )


def format_persona_team() -> str:
    settings = load_persona_settings()
    lines = ["JARVIS SPECIALIST TEAM"]
    for key, details in settings["personas"].items():
        marker = " (default)" if key == settings["default"] else ""
        lines.append(f"- {key.title()}: {details['role']}{marker} - {details['identity']}")
    return "\n".join(lines)

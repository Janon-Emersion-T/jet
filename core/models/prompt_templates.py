import json
from pathlib import Path

TEMPLATE_PATH = Path("storage/prompt_templates.json")

DEFAULT_TEMPLATES = {
    "general": "You are JARVIS, Janon's private local AI assistant. Answer clearly and practically.",
    "coding": "You are JARVIS coding mode. Inspect carefully, avoid assumptions, and prefer safe changes.",
    "fast": "You are JARVIS fast mode. Answer briefly and directly.",
    "long_context": "You are JARVIS long-context mode. Analyze deeply, preserve structure, and summarize clearly.",
}


def ensure_prompt_templates():
    TEMPLATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not TEMPLATE_PATH.exists():
        TEMPLATE_PATH.write_text(json.dumps(DEFAULT_TEMPLATES, indent=4))

    return load_prompt_templates()


def load_prompt_templates():
    if not TEMPLATE_PATH.exists():
        return ensure_prompt_templates()

    with TEMPLATE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_prompt_templates(templates: dict):
    current = load_prompt_templates()
    current.update(templates)

    TEMPLATE_PATH.write_text(json.dumps(current, indent=4), encoding="utf-8")
    return current
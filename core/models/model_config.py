import json
from pathlib import Path

CONFIG_PATH = Path("storage/model_settings.json")

DEFAULT_SETTINGS = {
    "general_model": "llama3.2",
    "coding_model": "qwen2.5-coder",
    "fast_model": "llama3.2",
    "long_context_model": "llama3.1",
    "fallback_model": "llama3.2",
    "temperature": 0.3,
    "max_tokens": 4096,
}


def ensure_model_settings():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_SETTINGS, indent=4))

    return load_model_settings()


def load_model_settings():
    if not CONFIG_PATH.exists():
        return ensure_model_settings()

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_model_settings(settings: dict):
    current = load_model_settings()
    current.update(settings)

    CONFIG_PATH.write_text(json.dumps(current, indent=4), encoding="utf-8")
    return current
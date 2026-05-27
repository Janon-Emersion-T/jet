from copy import deepcopy
import json
from pathlib import Path
from typing import Dict


CONFIG_FILE = Path("storage/environment_settings.json")
DEFAULT_SETTINGS = {
    "default_weather_city": "",
    "use_ip_location": True,
    "saved_location_label": "",
    "saved_latitude": None,
    "saved_longitude": None,
}


def load_environment_settings() -> Dict:
    settings = deepcopy(DEFAULT_SETTINGS)
    if CONFIG_FILE.exists():
        try:
            settings.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
        except ValueError:
            pass
    return settings


def save_environment_settings(updates: Dict) -> Dict:
    settings = load_environment_settings()
    settings.update(updates)
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    return settings


def environment_status() -> str:
    settings = load_environment_settings()
    source = "IP-based approximate location" if settings["use_ip_location"] else "saved location only"
    city = settings["default_weather_city"] or "automatic location"
    saved = settings["saved_location_label"] or "none"
    return (
        "LIVE ENVIRONMENT SETTINGS\n"
        f"Weather default: {city}\n"
        f"Location source: {source}\n"
        f"Saved location: {saved}\n"
        "Weather provider: Open-Meteo (read-only)\n"
        "Automatic location provider: ipapi.co (IP-based, not GPS)"
    )

from copy import deepcopy
import json
import os
from pathlib import Path
from typing import Dict


CONFIG_FILE = Path("storage/notification_settings.json")
DEFAULT_SETTINGS = {
    "attention_email": "lkprofessionals234@gmail.com",
    "email_attention_events": True,
    "attention_event_types": [
        "PATCH_APPLIED",
        "PATCH_ROLLED_BACK",
        "SECURITY_COMMAND_BLOCKED",
        "APPROVAL_REQUIRED",
        "ERROR",
        "FAILED",
        "SECURITY",
    ],
}


def load_notification_settings() -> Dict:
    settings = deepcopy(DEFAULT_SETTINGS)
    if CONFIG_FILE.exists():
        try:
            settings.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
        except ValueError:
            pass
    configured = os.getenv("JARVIS_ATTENTION_EMAIL", "").strip()
    if configured:
        settings["attention_email"] = configured
    return settings


def save_notification_settings(updates: Dict) -> Dict:
    settings = load_notification_settings()
    settings.update(updates)
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    return settings


def notification_status() -> str:
    settings = load_notification_settings()
    enabled = "ON" if settings["email_attention_events"] else "OFF"
    return (
        "ATTENTION NOTIFICATIONS\n"
        f"Email alerts: {enabled}\n"
        f"Recipient: {settings['attention_email']}\n"
        "Policy: only events requiring attention trigger an email."
    )

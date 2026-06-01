import json
from pathlib import Path
from typing import Any, Dict


CONFIG_PATH = Path("storage/social_channels.json")


DEFAULT_CONFIG = {
    "whatsapp": {
        "enabled": False,
        "auto_reply": False,
        "connection_mode": "web",
        "phone_number_id": "",
        "access_token": "",
        "verify_token": "jarvis_whatsapp_verify_token",
        "api_version": "v20.0",
        "business_name": "LKProfessionals (Pvt) Ltd.",
        "web_session_name": "default",
        "web_headless": True,
    },
    "facebook": {
        "enabled": False,
        "auto_reply": False,
    },
    "instagram": {
        "enabled": False,
        "auto_reply": False,
    },
    "linkedin": {
        "enabled": False,
        "auto_reply": False,
    },
    "tiktok": {
        "enabled": False,
        "auto_reply": False,
    },
    "email": {
        "enabled": False,
        "auto_reply": False,
    },
}


def _ensure_config_file() -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(
            json.dumps(DEFAULT_CONFIG, indent=4),
            encoding="utf-8",
        )


def load_social_channels() -> Dict[str, Any]:
    _ensure_config_file()

    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = DEFAULT_CONFIG.copy()

    for channel, defaults in DEFAULT_CONFIG.items():
        data.setdefault(channel, defaults)

        for key, value in defaults.items():
            data[channel].setdefault(key, value)

    return data


def save_social_channel(channel: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    data = load_social_channels()

    if channel not in data:
        raise ValueError(f"Unsupported channel: {channel}")

    data[channel].update(settings)

    CONFIG_PATH.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8",
    )

    return data[channel]


def get_social_channel(channel: str) -> Dict[str, Any]:
    data = load_social_channels()

    if channel not in data:
        raise ValueError(f"Unsupported channel: {channel}")

    return data[channel]

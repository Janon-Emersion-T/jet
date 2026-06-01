from copy import deepcopy
import json
from pathlib import Path
from typing import Dict


CONFIG_FILE = Path("storage/nlp/config.json")
DEFAULT_CONFIG = {
    "enabled": True,
    "audit_enabled": True,
    "memory_enabled": True,
    "knowledge_enabled": True,
    "semantic_cache_enabled": True,
    "default_role": "operator",
    "confidence_threshold": 0.35,
    "analysis_engine": "phase000",
    "features": {
        "file_awareness": True,
        "safety_planning": True,
        "target_resolution": True,
        "task_planning": True,
        "voice_understanding": True,
        "domain_understanding": True,
    },
}


def load_nlp_config() -> Dict:
    if not CONFIG_FILE.exists():
        return deepcopy(DEFAULT_CONFIG)
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return deepcopy(DEFAULT_CONFIG)
    config = deepcopy(DEFAULT_CONFIG)
    config.update({key: value for key, value in data.items() if key != "features"})
    config["features"].update(data.get("features", {}))
    return config


def save_nlp_config(updates: Dict) -> Dict:
    config = load_nlp_config()
    config.update({key: value for key, value in updates.items() if key != "features"})
    config["features"].update(updates.get("features", {}))
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return config

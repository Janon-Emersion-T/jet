from collections import Counter
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional


MEMORY_FILE = Path("storage/nlp/intent_memory.json")
MAX_TURNS = 250


def _load() -> Dict:
    if not MEMORY_FILE.exists():
        return {"turns": [], "shortcuts": {}, "recoveries": []}
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"turns": [], "shortcuts": {}, "recoveries": []}


def _save(data: Dict) -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def remember_intent(text: str, intent: str, route_hint: Optional[str],
                    success: Optional[bool] = None) -> None:
    data = _load()
    data["turns"].append({
        "text": text, "intent": intent, "route_hint": route_hint,
        "success": success, "at": datetime.now().isoformat(timespec="seconds"),
    })
    data["turns"] = data["turns"][-MAX_TURNS:]
    _save(data)


def remember_recovery(failed_text: str, corrected_text: str, reason: str = "") -> None:
    data = _load()
    data["recoveries"].append({
        "failed": failed_text, "corrected": corrected_text, "reason": reason,
        "at": datetime.now().isoformat(timespec="seconds"),
    })
    data["recoveries"] = data["recoveries"][-50:]
    _save(data)


def learn_shortcut(alias: str, command: str) -> None:
    data = _load()
    data["shortcuts"][alias.strip().lower()] = command.strip()
    _save(data)


def expand_personal_shortcut(text: str) -> str:
    data = _load()
    return data["shortcuts"].get(text.strip().lower(), text)


def intent_patterns() -> Dict[str, int]:
    return dict(Counter(turn["intent"] for turn in _load()["turns"]))


def command_habits(limit: int = 5) -> List[Dict]:
    counter = Counter((turn["text"], turn["intent"]) for turn in _load()["turns"])
    return [
        {"command": command, "intent": intent, "count": count}
        for (command, intent), count in counter.most_common(limit)
    ]


def repeated_command_optimizations() -> List[str]:
    suggestions = []
    for item in command_habits():
        if item["count"] >= 3:
            suggestions.append(
                f"Create a shortcut for '{item['command']}' ({item['count']} recent uses)."
            )
    return suggestions

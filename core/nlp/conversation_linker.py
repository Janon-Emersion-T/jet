from typing import Dict, List


_CONVERSATION_TRAIL: List[Dict[str, str]] = []


def remember_turn(user_text: str, intent: str, clean_text: str) -> None:
    _CONVERSATION_TRAIL.append({
        "user_text": user_text,
        "intent": intent,
        "clean_text": clean_text,
    })

    if len(_CONVERSATION_TRAIL) > 20:
        _CONVERSATION_TRAIL.pop(0)


def get_recent_turns(limit: int = 5) -> List[Dict[str, str]]:
    return _CONVERSATION_TRAIL[-limit:]


def infer_from_recent_context(clean_text: str, intent: str) -> Dict[str, str]:
    hints = {}

    recent = get_recent_turns(5)

    if clean_text in ["continue", "next", "proceed", "ok", "okay"]:
        for item in reversed(recent):
            if item.get("intent") not in ["general", "general_chat"]:
                hints["previous_intent"] = item["intent"]
                hints["previous_command"] = item["clean_text"]
                break

    return hints

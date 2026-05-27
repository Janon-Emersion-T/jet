def guard_intent_confidence(intent: str, confidence: float, clean_text: str) -> str:
    if confidence >= 0.45:
        return intent

    if clean_text in [
        "continue",
        "next",
        "proceed",
        "ok",
        "okay",
        "yes",
        "do it",
    ]:
        return intent

    return "general"

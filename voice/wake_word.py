WAKE_WORDS = [
    "hey jarvis",
    "jarvis",
    "hey jabbies",
    "jabbies",
    "hey jet",
]


def has_wake_word(text: str) -> bool:
    lowered = text.lower().strip()
    return any(word in lowered for word in WAKE_WORDS)

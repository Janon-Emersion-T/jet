CORRECTIONS = {
    "hey joey": "hey jarvis",
    "hey jabbies": "hey jarvis",
    "jabbies": "jarvis",
    "jarvies": "jarvis",
    "look online": "use internet",
    "hey jorys": "hey jarvis",
    "hey jones": "hey jarvis",
    "here johnny": "hey jarvis",
    "here, johnny": "hey jarvis",
}


def correct_voice_command(text: str) -> str:
    cleaned = text.strip().lower()

    for wrong, right in CORRECTIONS.items():
        cleaned = cleaned.replace(wrong, right)

    return cleaned

from voice.voice_config import VOICE_CONFIG


def is_noise_or_silence(text: str) -> bool:
    lowered = text.lower().strip()

    if not lowered:
        return True

    if lowered in ["__interrupted__", "[blank_audio]", "blank audio"]:
        return True

    cleaned = (
        lowered.replace("(", "")
        .replace(")", "")
        .replace("[", "")
        .replace("]", "")
        .replace(".", "")
        .strip()
    )

    return any(
        phrase in cleaned
        for phrase in VOICE_CONFIG["ignore_noise_phrases"]
    )
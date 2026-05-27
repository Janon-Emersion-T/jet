from dataclasses import dataclass
import re
from typing import Optional

from voice.command_correction import correct_voice_command
from voice.wake_word import has_wake_word


@dataclass
class VoiceIntent:
    raw_text: str
    clean_text: str
    wake_word_detected: bool
    follow_up: bool
    confirmation: Optional[bool]
    dictation: Optional[str]


def clean_voice_command(text: str) -> str:
    cleaned = correct_voice_command(text or "")
    cleaned = re.sub(r"\b(?:um+|uh+|erm|please)\b", "", cleaned, flags=re.I)
    return re.sub(r"\s+", " ", cleaned).strip(" ,.")


def parse_voice_intent(text: str) -> VoiceIntent:
    cleaned = clean_voice_command(text)
    lowered = cleaned.lower()
    confirmation = None
    if re.search(r"\b(?:confirm|yes proceed|approve)\b", lowered):
        confirmation = True
    elif re.search(r"\b(?:cancel|no stop|do not)\b", lowered):
        confirmation = False
    dictation_match = re.search(r"\b(?:write|type|dictate)\s+(?:this\s+)?(?:down\s+)?(.+)", cleaned, re.I)
    return VoiceIntent(
        raw_text=text,
        clean_text=cleaned,
        wake_word_detected=has_wake_word(cleaned),
        follow_up=lowered in {"yes", "no", "confirm", "continue", "do it", "cancel"},
        confirmation=confirmation,
        dictation=dictation_match.group(1).strip() if dictation_match else None,
    )

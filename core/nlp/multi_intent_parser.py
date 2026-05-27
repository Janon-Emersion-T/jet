import re
from dataclasses import dataclass, field
from typing import List, Dict

from core.nlp.phase000a_foundation_router import normalize_text


@dataclass
class MultiIntentItem:
    index: int
    raw_text: str
    clean_text: str
    connector: str = ""
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class MultiIntentResult:
    original_text: str
    is_multi_intent: bool
    commands: List[MultiIntentItem]


CONNECTOR_PATTERNS = [
    r"\bthen\b",
    r"\band then\b",
    r"\bafter that\b",
    r"\bnext\b",
    r"\balso\b",
    r"\band also\b",
    r"\n+",
    r";",
]


PROTECTED_PHRASES = [
    "read and explain",
    "check and tell",
    "find and show",
    "analyze and report",
]


def _protect_phrases(text: str) -> str:
    protected = text
    for i, phrase in enumerate(PROTECTED_PHRASES):
        protected = protected.replace(phrase, f"__PROTECTED_{i}__")
    return protected


def _restore_phrases(text: str) -> str:
    restored = text
    for i, phrase in enumerate(PROTECTED_PHRASES):
        restored = restored.replace(f"__PROTECTED_{i}__", phrase)
    return restored


def _split_multi_command(text: str) -> List[str]:
    protected = _protect_phrases(text)

    pattern = "|".join(f"({p})" for p in CONNECTOR_PATTERNS)
    parts = re.split(pattern, protected, flags=re.IGNORECASE)

    commands = []
    buffer = ""

    for part in parts:
        if not part:
            continue

        candidate = part.strip()
        if not candidate:
            continue

        if re.fullmatch(pattern, candidate, flags=re.IGNORECASE):
            if buffer.strip():
                commands.append(_restore_phrases(buffer.strip()))
                buffer = ""
            continue

        buffer = f"{buffer} {candidate}".strip()

    if buffer.strip():
        commands.append(_restore_phrases(buffer.strip()))

    return [cmd.strip() for cmd in commands if cmd.strip()]


def parse_multi_intent_command(user_input: str) -> MultiIntentResult:
    original = user_input or ""
    normalized = normalize_text(original)

    commands = _split_multi_command(normalized)

    if len(commands) <= 1:
        return MultiIntentResult(
            original_text=original,
            is_multi_intent=False,
            commands=[
                MultiIntentItem(
                    index=1,
                    raw_text=original.strip(),
                    clean_text=normalized.strip(),
                )
            ] if original.strip() else [],
        )

    items = [
        MultiIntentItem(
            index=i + 1,
            raw_text=cmd,
            clean_text=cmd,
        )
        for i, cmd in enumerate(commands)
    ]

    return MultiIntentResult(
        original_text=original,
        is_multi_intent=True,
        commands=items,
    )


def format_multi_intent_report(user_input: str) -> str:
    result = parse_multi_intent_command(user_input)

    lines = [
        "PHASE NLP-000O — MULTI-INTENT COMMAND PARSING",
        "",
        f"Original: {result.original_text}",
        f"Multi-intent: {'YES' if result.is_multi_intent else 'NO'}",
        f"Detected commands: {len(result.commands)}",
        "",
    ]

    for item in result.commands:
        lines.append(f"{item.index}. {item.clean_text}")

    return "\n".join(lines)

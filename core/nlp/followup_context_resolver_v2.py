from dataclasses import dataclass
from typing import Dict, Optional

from core.nlp.context_engine import is_follow_up


_LAST_FOLLOWUP_CONTEXT: Dict[str, Optional[str]] = {
    "last_command": None,
    "last_intent": None,
    "last_route_hint": None,
    "last_subject": None,
}


@dataclass
class FollowupResolution:
    original_text: str
    resolved_text: str
    is_follow_up: bool
    confidence: float
    reason: str


def remember_followup_context(
    command: str,
    intent: str = "",
    route_hint: str = "",
    subject: str = "",
) -> None:
    if command:
        _LAST_FOLLOWUP_CONTEXT["last_command"] = command
    if intent:
        _LAST_FOLLOWUP_CONTEXT["last_intent"] = intent
    if route_hint:
        _LAST_FOLLOWUP_CONTEXT["last_route_hint"] = route_hint
    if subject:
        _LAST_FOLLOWUP_CONTEXT["last_subject"] = subject


def resolve_followup_v2(user_input: str) -> FollowupResolution:
    text = (user_input or "").strip().lower()

    if not text:
        return FollowupResolution(user_input, "", False, 0.0, "Empty command.")

    if not is_follow_up(text):
        return FollowupResolution(user_input, user_input, False, 1.0, "Not a follow-up command.")

    last_command = _LAST_FOLLOWUP_CONTEXT.get("last_command")
    last_intent = _LAST_FOLLOWUP_CONTEXT.get("last_intent")
    last_route_hint = _LAST_FOLLOWUP_CONTEXT.get("last_route_hint")
    last_subject = _LAST_FOLLOWUP_CONTEXT.get("last_subject")

    if text in ["continue", "go on", "next", "proceed", "move on"]:
        if last_command:
            return FollowupResolution(
                user_input,
                last_command,
                True,
                0.86,
                "Resolved using the previous command.",
            )

    if text in ["again", "same", "do it again"]:
        if last_command:
            return FollowupResolution(
                user_input,
                last_command,
                True,
                0.9,
                "Resolved as repeat of previous command.",
            )

    if text in ["yes", "ok", "okay", "do it"]:
        if last_command:
            return FollowupResolution(
                user_input,
                last_command,
                True,
                0.75,
                "Resolved as confirmation-style follow-up.",
            )

    if last_subject and last_intent:
        return FollowupResolution(
            user_input,
            f"{last_intent} {last_subject}",
            True,
            0.65,
            "Resolved using last subject and intent.",
        )

    if last_route_hint and last_command:
        return FollowupResolution(
            user_input,
            f"{last_route_hint}: {last_command}",
            True,
            0.6,
            "Resolved using last route hint and command.",
        )

    return FollowupResolution(
        user_input,
        user_input,
        True,
        0.25,
        "Follow-up detected but no strong previous context exists.",
    )


def format_followup_v2_report(user_input: str) -> str:
    result = resolve_followup_v2(user_input)

    return f"""PHASE NLP-000R — FOLLOW-UP CONTEXT RESOLVER V2

Original: {result.original_text}
Resolved: {result.resolved_text}
Is follow-up: {'YES' if result.is_follow_up else 'NO'}
Confidence: {result.confidence}
Reason: {result.reason}"""

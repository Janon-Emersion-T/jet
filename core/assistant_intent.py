from __future__ import annotations

import json
import re
from dataclasses import dataclass

from core.brain import ask_brain
from core.capabilities import list_capabilities


@dataclass
class AssistantIntentPlan:
    mode: str = "none"
    command: str | None = None
    answer: str | None = None
    confidence: float = 0.0


def _extract_json(text: str) -> dict | None:
    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def plan_assistant_action(user_input: str, chat_context: str | None = None) -> AssistantIntentPlan:
    prompt = f"""
Convert the user's natural language request into either:
1. an internal JARVIS command,
2. a direct assistant answer,
3. or a short clarification question.

Capabilities:
{list_capabilities()}

Chat context:
{chat_context if chat_context else "No active chat context provided."}

Rules:
- Prefer mode "command" when the request sounds like JARVIS should do an action.
- Use only realistic internal commands, not explanations.
- If the user is just chatting, asking for advice, or asking for an explanation, use mode "answer".
- If this is a follow-up like "do it", "I want you to do it", or "yes", infer the real action from chat context.
- If you still cannot infer the action, use mode "clarify".
- Never claim email, calendar, or other unconnected tools are available.
- Return strict JSON only.

JSON schema:
{{
  "mode": "command" | "answer" | "clarify",
  "command": "string",
  "answer": "string",
  "confidence": 0.0
}}

Examples:
- "can you check the project health for me" -> {{"mode":"command","command":"project health score","answer":"","confidence":0.86}}
- "open google and search laravel queues" -> {{"mode":"command","command":"search google for laravel queues","answer":"","confidence":0.82}}
- With context about creating `/var/www/csl` and installing Laravel, "I want you to do it" -> {{"mode":"command","command":"install laravel project /var/www/csl","answer":"","confidence":0.91}}
- "Create a Laravel web application in /var/www/testJarvis" -> {{"mode":"command","command":"create laravel web application /var/www/testJarvis","answer":"","confidence":0.94}}
- "build the csl website with home about media blogs and contact us pages" -> {{"mode":"command","command":"build website pages for the current laravel project","answer":"","confidence":0.92}}
- With context about the current Laravel app, "install livewire" -> {{"mode":"command","command":"install livewire in the current project","answer":"","confidence":0.88}}
- "what is dependency injection" -> {{"mode":"answer","command":"","answer":"Dependency injection is ...","confidence":0.90}}

User request:
{user_input}
"""

    raw = ask_brain(prompt, route_hint="fast", max_tokens=300)
    data = _extract_json(raw)

    if not data:
        return AssistantIntentPlan()

    mode = str(data.get("mode", "none")).strip().lower()
    command = str(data.get("command", "")).strip() or None
    answer = str(data.get("answer", "")).strip() or None

    try:
        confidence = float(data.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0

    return AssistantIntentPlan(
        mode=mode,
        command=command,
        answer=answer,
        confidence=confidence,
    )

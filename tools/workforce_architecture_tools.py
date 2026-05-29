from __future__ import annotations

import json
from pathlib import Path


WORKFORCE_DIR = Path("storage/workforce")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_entries(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def ai_executive_assistant_framework() -> str:
    briefs = _list_entries(WORKFORCE_DIR / "executive_framework.json", "briefs")
    cadences = _list_entries(WORKFORCE_DIR / "executive_framework.json", "cadences")
    return "\n".join(
        [
            "AI EXECUTIVE ASSISTANT FRAMEWORK - PHASE 498",
            "Mode: executive-support framework overview.",
            f"Executive briefs: {len(briefs)}",
            f"Decision cadences: {len(cadences)}",
            "Scope: prep decisions, summarize tradeoffs, maintain follow-ups, and escalate only what truly needs senior attention.",
        ]
    )


def ai_company_workforce_ecosystem() -> str:
    roles = _list_entries(WORKFORCE_DIR / "workforce.json", "roles")
    automations = _list_entries(WORKFORCE_DIR / "workforce.json", "automations")
    return "\n".join(
        [
            "AI COMPANY WORKFORCE ECOSYSTEM - PHASE 499",
            "Mode: workforce-ecosystem overview.",
            f"AI role definitions: {len(roles)}",
            f"Automation programs: {len(automations)}",
            "Governance: each AI role should have scope, owner, audit trail, and explicit collaboration rules with humans and other agents.",
        ]
    )


def jarvis_prime_architecture_foundation() -> str:
    layers = _list_entries(WORKFORCE_DIR / "jarvis_prime.json", "layers")
    principles = _list_entries(WORKFORCE_DIR / "jarvis_prime.json", "principles")
    return "\n".join(
        [
            "JARVIS PRIME ARCHITECTURE FOUNDATION - PHASE 500",
            "Mode: architecture-foundation overview.",
            f"Architecture layers: {len(layers)}",
            f"Guiding principles: {len(principles)}",
            "Foundation: natural language entry, modular tools, governed autonomy, distributed runtime, and human-centered oversight.",
        ]
    )

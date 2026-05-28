from __future__ import annotations

import json
from pathlib import Path


AUTONOMY_DIR = Path("storage/autonomy")


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


def ai_civilization_sandbox() -> str:
    agents = _list_entries(AUTONOMY_DIR / "civilization.json", "agents")
    institutions = _list_entries(AUTONOMY_DIR / "civilization.json", "institutions")
    return "\n".join(
        [
            "AI CIVILIZATION SANDBOX - PHASE 481",
            "Mode: civilization-scale simulation overview.",
            f"Agents modeled: {len(agents)}",
            f"Institutions modeled: {len(institutions)}",
            "Use case: governance experiments, incentive design, resource allocation, and conflict-resolution scenarios.",
        ]
    )


def autonomous_learning_curriculum() -> str:
    lessons = _list_entries(AUTONOMY_DIR / "curriculum.json", "lessons")
    tracks = sorted(
        {
            str(item.get("track", "general"))
            for item in lessons
            if isinstance(item, dict) and item.get("track")
        }
    )
    return "\n".join(
        [
            "AUTONOMOUS LEARNING CURRICULUM - PHASE 482",
            "Mode: learning-curriculum overview.",
            f"Lessons tracked: {len(lessons)}",
            f"Tracks: {', '.join(tracks) if tracks else 'none'}",
            "Learning loop: benchmark current skill, assign practice, review evidence, then promote cautiously.",
        ]
    )


def recursive_self_improvement_framework() -> str:
    experiments = _list_entries(AUTONOMY_DIR / "self_improvement.json", "experiments")
    active = [item for item in experiments if isinstance(item, dict) and item.get("status", "planned") != "done"]
    return "\n".join(
        [
            "RECURSIVE SELF-IMPROVEMENT FRAMEWORK - PHASE 483",
            "Mode: controlled improvement backlog.",
            f"Tracked experiments: {len(experiments)}",
            f"Open experiments: {len(active)}",
            "Policy: proposals, benchmarks, rollback plans, and human review stay ahead of any recursive change loop.",
        ]
    )


def self_diagnostic_evolution_engine() -> str:
    diagnostics = _list_entries(AUTONOMY_DIR / "diagnostics.json", "checks")
    failing = [item for item in diagnostics if isinstance(item, dict) and item.get("status") == "failing"]
    return "\n".join(
        [
            "SELF-DIAGNOSTIC EVOLUTION ENGINE - PHASE 484",
            "Mode: diagnostic readiness overview.",
            f"Checks tracked: {len(diagnostics)}",
            f"Failing checks: {len(failing)}",
            "Purpose: detect capability drift, degraded routing, weak confidence, and repeated failure clusters before mutation.",
        ]
    )


def self_healing_software_architecture() -> str:
    incidents = _list_entries(AUTONOMY_DIR / "self_healing.json", "incidents")
    remediations = [item for item in incidents if isinstance(item, dict) and item.get("remediation")]
    return "\n".join(
        [
            "SELF-HEALING SOFTWARE ARCHITECTURE - PHASE 485",
            "Mode: recovery-pattern overview.",
            f"Incident patterns tracked: {len(incidents)}",
            f"Patterns with remediations: {len(remediations)}",
            "Design note: self-healing should begin with diagnosis, isolation, restart plans, and rollback-safe recovery steps.",
        ]
    )

from __future__ import annotations

import json
import os
from pathlib import Path


PLATFORM_DIR = Path("storage/jarvis_platform")


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


def enterprise_grade_jarvis_os() -> str:
    services = _list_entries(PLATFORM_DIR / "jarvis_os.json", "services")
    controls = _list_entries(PLATFORM_DIR / "jarvis_os.json", "controls")
    return "\n".join(
        [
            "ENTERPRISE-GRADE JARVIS OS - PHASE 493",
            "Mode: platform-service overview.",
            f"Core services: {len(services)}",
            f"Governance controls: {len(controls)}",
            "Objective: unify routing, approvals, observability, policy, and lifecycle management under one operating model.",
        ]
    )


def ai_native_desktop_environment() -> str:
    widgets = _list_entries(PLATFORM_DIR / "desktop.json", "widgets")
    shell = os.getenv("JARVIS_DESKTOP_SHELL", "").strip() or "not configured"
    return "\n".join(
        [
            "AI-NATIVE DESKTOP ENVIRONMENT - PHASE 494",
            "Mode: desktop-environment overview.",
            f"Shell profile: {shell}",
            f"Widgets tracked: {len(widgets)}",
            "Focus: commands, context, approvals, notifications, and workspace memory inside one desktop loop.",
        ]
    )


def unified_cognitive_dashboard() -> str:
    panels = _list_entries(PLATFORM_DIR / "dashboard.json", "panels")
    signals = _list_entries(PLATFORM_DIR / "dashboard.json", "signals")
    return "\n".join(
        [
            "UNIFIED COGNITIVE DASHBOARD - PHASE 495",
            "Mode: dashboard overview.",
            f"Panels tracked: {len(panels)}",
            f"Signals aggregated: {len(signals)}",
            "Purpose: bring system health, memory, approvals, projects, and risks into one operator-facing cockpit.",
        ]
    )


def general_purpose_autonomous_operator() -> str:
    playbooks = _list_entries(PLATFORM_DIR / "operator.json", "playbooks")
    guarded = [item for item in playbooks if isinstance(item, dict) and bool(item.get("approval_required", True))]
    return "\n".join(
        [
            "GENERAL-PURPOSE AUTONOMOUS OPERATOR - PHASE 496",
            "Mode: operator-playbook review.",
            f"Playbooks tracked: {len(playbooks)}",
            f"Approval-gated playbooks: {len(guarded)}",
            "Policy: useful autonomy means bounded scope, visible plans, rollback paths, and human override everywhere it counts.",
        ]
    )


def human_ai_collaborative_workspace() -> str:
    spaces = _list_entries(PLATFORM_DIR / "workspace.json", "spaces")
    collaborators = sum(int(item.get("people", 0) or 0) for item in spaces if isinstance(item, dict))
    return "\n".join(
        [
            "HUMAN-AI COLLABORATIVE WORKSPACE - PHASE 497",
            "Mode: collaboration-space overview.",
            f"Spaces tracked: {len(spaces)}",
            f"Human collaborators represented: {collaborators}",
            "Design goal: shared tasks, transparent decisions, commentable plans, and human legibility before cleverness.",
        ]
    )

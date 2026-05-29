from __future__ import annotations

import json
from pathlib import Path


COMMAND_CENTER_DIR = Path("storage/command_center")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(COMMAND_CENTER_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def ai_operations_cockpit() -> str:
    return _render("AI OPERATIONS COCKPIT - PHASE 1521", "operations-cockpit overview", "operations_cockpit.json", "cockpit_panels", "healthy", "missing", "Cockpit panels tracked", "Healthy panels", "Missing panels", "Guardrail: operations cockpits should preserve human comprehension, drill-down paths, and separation between signal and automated action.")


def multi_project_command_center() -> str:
    return _render("MULTI-PROJECT COMMAND CENTER - PHASE 1522", "multi-project-command overview", "multi_project_command_center.json", "project_views", "coordinated", "fragmented", "Project views tracked", "Coordinated views", "Fragmented views", "Guardrail: multi-project command centers should preserve project isolation, scoped permissions, and visible cross-project dependencies.")


def developer_productivity_intelligence() -> str:
    return _render("DEVELOPER PRODUCTIVITY INTELLIGENCE - PHASE 1523", "developer-productivity overview", "developer_productivity_intelligence.json", "productivity_signals", "useful", "noisy", "Productivity signals tracked", "Useful signals", "Noisy signals", "Guardrail: productivity intelligence should preserve consent, avoid surveillance creep, and keep metrics advisory rather than punitive.")


def autonomous_backlog_grooming() -> str:
    return _render("AUTONOMOUS BACKLOG GROOMING - PHASE 1524", "backlog-grooming overview", "autonomous_backlog_grooming.json", "backlog_items", "triaged", "stale", "Backlog items tracked", "Triaged items", "Stale items", "Guardrail: backlog grooming should preserve product intent, visible rationale, and human override for priority changes.")


def self_prioritizing_task_engine() -> str:
    return _render("SELF-PRIORITIZING TASK ENGINE - PHASE 1525", "task-prioritization overview", "self_prioritizing_task_engine.json", "task_routes", "prioritized", "misranked", "Task routes tracked", "Prioritized routes", "Misranked routes", "Guardrail: self-prioritization should preserve explicit business goals, user override, and traceable ranking criteria.")


def requirement_ambiguity_detector() -> str:
    return _render("REQUIREMENT AMBIGUITY DETECTOR - PHASE 1526", "requirement-ambiguity overview", "requirement_ambiguity_detector.json", "requirements", "clear", "ambiguous", "Requirements tracked", "Clear requirements", "Ambiguous requirements", "Guardrail: ambiguity detection should preserve source wording, avoid silent reinterpretation, and flag uncertainty explicitly.")


def specification_completeness_scorer() -> str:
    return _render("SPECIFICATION COMPLETENESS SCORER - PHASE 1527", "spec-completeness overview", "specification_completeness_scorer.json", "spec_sections", "complete", "missing", "Spec sections tracked", "Complete sections", "Missing sections", "Guardrail: completeness scoring should preserve nuance, indicate confidence, and avoid implying correctness from coverage alone.")


def client_brief_intelligence_layer() -> str:
    return _render("CLIENT BRIEF INTELLIGENCE LAYER - PHASE 1528", "client-brief overview", "client_brief_intelligence.json", "briefs", "well-scoped", "vague", "Client briefs tracked", "Well-scoped briefs", "Vague briefs", "Guardrail: client brief intelligence should preserve source intent, stakeholder nuance, and explicit uncertainty where requirements are inferred.")


def proposal_to_code_pipeline() -> str:
    return _render("PROPOSAL-TO-CODE PIPELINE - PHASE 1529", "proposal-to-code overview", "proposal_to_code_pipeline.json", "delivery_paths", "connected", "broken", "Delivery paths tracked", "Connected paths", "Broken paths", "Guardrail: proposal-to-code automation should preserve approval gates, scope traceability, and rollback for mismatched implementation.")


def contract_to_delivery_tracker() -> str:
    return _render("CONTRACT-TO-DELIVERY TRACKER - PHASE 1530", "contract-to-delivery overview", "contract_to_delivery_tracker.json", "delivery_tracks", "aligned", "drifting", "Delivery tracks tracked", "Aligned tracks", "Drifting tracks", "Guardrail: contract-to-delivery tracking should preserve obligation visibility, change-order clarity, and auditable milestone status.")

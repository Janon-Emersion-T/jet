from __future__ import annotations

import json
from pathlib import Path


RELEASE_INCIDENT_DIR = Path("storage/release_incident")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RELEASE_INCIDENT_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def release_readiness_gatekeeper() -> str:
    return _render("RELEASE-READINESS GATEKEEPER - PHASE 1671", "release-readiness overview", "release_readiness_gatekeeper.json", "release_checks", "ready", "blocked", "Release checks tracked", "Ready checks", "Blocked checks", "Guardrail: readiness gates should preserve explicit criteria and avoid treating unknowns as approval by default.")


def deployment_checklist_autopilot() -> str:
    return _render("DEPLOYMENT CHECKLIST AUTOPILOT - PHASE 1672", "deployment-checklist overview", "deployment_checklist_autopilot.json", "checklist_items", "complete", "missing", "Checklist items tracked", "Complete items", "Missing items", "Guardrail: deployment checklists should preserve environment-specific steps and require human confirmation for irreversible actions.")


def rollback_drill_assistant() -> str:
    return _render("ROLLBACK DRILL ASSISTANT - PHASE 1673", "rollback-drill overview", "rollback_drill_assistant.json", "rollback_runs", "practiced", "untested", "Rollback runs tracked", "Practiced runs", "Untested runs", "Guardrail: rollback drill support should preserve environment safety and distinguish tabletop readiness from proven automated recovery.")


def incident_postmortem_generator() -> str:
    return _render("INCIDENT POSTMORTEM GENERATOR - PHASE 1674", "incident-postmortem overview", "incident_postmortem_generator.json", "postmortem_sections", "complete", "thin", "Postmortem sections tracked", "Complete sections", "Thin sections", "Guardrail: postmortem generation should preserve factual chronology, avoid blameful language, and keep root-cause uncertainty visible.")


def sla_breach_predictor() -> str:
    return _render("SLA BREACH PREDICTOR - PHASE 1675", "sla-breach overview", "sla_breach_predictor.json", "sla_windows", "safe", "at-risk", "SLA windows tracked", "Safe windows", "At-risk windows", "Guardrail: SLA prediction should preserve customer-specific commitments and expose the assumptions behind each risk signal.")


def error_budget_tracker() -> str:
    return _render("ERROR-BUDGET TRACKER - PHASE 1676", "error-budget overview", "error_budget_tracker.json", "budget_periods", "within-budget", "burning", "Budget periods tracked", "Within-budget periods", "Burning periods", "Guardrail: error-budget tracking should preserve SLI/SLO definitions and avoid punitive interpretation without service context.")


def uptime_communication_assistant() -> str:
    return _render("UPTIME COMMUNICATION ASSISTANT - PHASE 1677", "uptime-communication overview", "uptime_communication_assistant.json", "incident_updates", "clear", "unclear", "Incident updates tracked", "Clear updates", "Unclear updates", "Guardrail: uptime communication should preserve factual accuracy, status-page consistency, and avoid masking uncertainty during active incidents.")


def client_status_page_generator() -> str:
    return _render("CLIENT STATUS-PAGE GENERATOR - PHASE 1678", "status-page overview", "client_status_page_generator.json", "status_pages", "ready", "stale", "Status pages tracked", "Ready pages", "Stale pages", "Guardrail: status-page generation should preserve tenant-specific scope and ensure private incident details are not exposed publicly.")


def production_hotfix_planner() -> str:
    return _render("PRODUCTION HOTFIX PLANNER - PHASE 1679", "production-hotfix overview", "production_hotfix_planner.json", "hotfix_plans", "controlled", "risky", "Hotfix plans tracked", "Controlled plans", "Risky plans", "Guardrail: hotfix planning should preserve rollback clarity, blast-radius awareness, and change-window discipline.")


def safe_maintenance_window_scheduler() -> str:
    return _render("SAFE MAINTENANCE WINDOW SCHEDULER - PHASE 1680", "maintenance-window overview", "maintenance_window_scheduler.json", "maintenance_windows", "safe", "disruptive", "Maintenance windows tracked", "Safe windows", "Disruptive windows", "Guardrail: maintenance scheduling should preserve customer-impact awareness, timezone coverage, and explicit rollback staffing assumptions.")

from __future__ import annotations

import json
from pathlib import Path


EXECUTIVE_MODES_DIR = Path("storage/executive_modes")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(EXECUTIVE_MODES_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def scope_creep_detector() -> str:
    return _render("SCOPE CREEP DETECTOR - PHASE 1531", "scope-creep overview", "scope_creep_detector.json", "scope_changes", "controlled", "creeping", "Scope changes tracked", "Controlled changes", "Creeping changes", "Guardrail: scope-creep detection should preserve agreed baselines, transparent deltas, and human judgment on justified expansion.")


def project_profitability_analyzer() -> str:
    return _render("PROJECT PROFITABILITY ANALYZER - PHASE 1532", "project-profitability overview", "project_profitability_analyzer.json", "project_margins", "profitable", "loss-making", "Project margins tracked", "Profitable projects", "Loss-making projects", "Guardrail: profitability analysis should preserve accounting clarity, context for strategic investment, and explicit assumption disclosure.")


def delivery_risk_predictor() -> str:
    return _render("DELIVERY RISK PREDICTOR - PHASE 1533", "delivery-risk overview", "delivery_risk_predictor.json", "delivery_paths", "low-risk", "high-risk", "Delivery paths tracked", "Low-risk paths", "High-risk paths", "Guardrail: delivery risk prediction should preserve uncertainty disclosure, avoid false precision, and surface the drivers behind scores.")


def deadline_recovery_planner() -> str:
    return _render("DEADLINE RECOVERY PLANNER - PHASE 1534", "deadline-recovery overview", "deadline_recovery_planner.json", "recovery_plans", "recoverable", "slipping", "Recovery plans tracked", "Recoverable plans", "Slipping plans", "Guardrail: deadline recovery planning should preserve quality floors, team wellbeing, and explicit tradeoff visibility.")


def resource_allocation_optimizer() -> str:
    return _render("RESOURCE ALLOCATION OPTIMIZER - PHASE 1535", "resource-allocation overview", "resource_allocation_optimizer.json", "allocation_models", "balanced", "overloaded", "Allocation models tracked", "Balanced models", "Overloaded models", "Guardrail: resource allocation should preserve fairness, capacity realism, and human override for sensitive staffing choices.")


def ai_project_manager_mode() -> str:
    return _render("AI PROJECT MANAGER MODE - PHASE 1536", "project-manager-mode overview", "ai_project_manager_mode.json", "pm_workflows", "organized", "unclear", "PM workflows tracked", "Organized workflows", "Unclear workflows", "Guardrail: project manager mode should preserve stakeholder visibility, accountable decision logs, and respectful escalation patterns.")


def ai_cto_mode() -> str:
    return _render("AI CTO MODE - PHASE 1537", "cto-mode overview", "ai_cto_mode.json", "technology_tracks", "sound", "risky", "Technology tracks tracked", "Sound tracks", "Risky tracks", "Guardrail: CTO guidance should preserve architectural rationale, security review, and long-term maintainability over short-term speed.")


def ai_cfo_mode() -> str:
    return _render("AI CFO MODE - PHASE 1538", "cfo-mode overview", "ai_cfo_mode.json", "finance_views", "clear", "opaque", "Finance views tracked", "Clear views", "Opaque views", "Guardrail: CFO guidance should preserve accounting accuracy, explicit uncertainty ranges, and separation between forecast and fact.")


def ai_coo_mode() -> str:
    return _render("AI COO MODE - PHASE 1539", "coo-mode overview", "ai_coo_mode.json", "operations_tracks", "smooth", "blocked", "Operations tracks tracked", "Smooth tracks", "Blocked tracks", "Guardrail: COO guidance should preserve process clarity, accountable owners, and escalation routes for operational bottlenecks.")


def founder_command_dashboard() -> str:
    return _render("FOUNDER COMMAND DASHBOARD - PHASE 1540", "founder-command overview", "founder_command_dashboard.json", "command_panels", "actionable", "noisy", "Command panels tracked", "Actionable panels", "Noisy panels", "Guardrail: founder dashboards should preserve signal over vanity, clear decision context, and explicit uncertainty where data is partial.")

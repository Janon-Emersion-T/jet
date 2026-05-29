from __future__ import annotations

import json
from pathlib import Path


LKPROFESSIONALS_GROWTH_DIR = Path("storage/lkprofessionals_growth")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(LKPROFESSIONALS_GROWTH_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def company_wide_ai_nervous_system() -> str:
    return _render("COMPANY-WIDE AI NERVOUS SYSTEM - PHASE 1541", "company-ai-nervous-system overview", "company_ai_nervous_system.json", "signal_routes", "connected", "siloed", "Signal routes tracked", "Connected routes", "Siloed routes", "Guardrail: company-wide AI coordination should preserve domain boundaries, audit trails, and role-scoped permissions.")


def lkprofessionals_operations_brain() -> str:
    return _render("LKPROFESSIONALS OPERATIONS BRAIN - PHASE 1542", "lkprofessionals-operations overview", "lkprofessionals_operations_brain.json", "operations_views", "coherent", "fragmented", "Operations views tracked", "Coherent views", "Fragmented views", "Guardrail: operations intelligence should preserve client confidentiality, explicit ownership, and reviewable operational assumptions.")


def client_portfolio_intelligence() -> str:
    return _render("CLIENT PORTFOLIO INTELLIGENCE - PHASE 1543", "client-portfolio overview", "client_portfolio_intelligence.json", "portfolio_accounts", "healthy", "at-risk", "Portfolio accounts tracked", "Healthy accounts", "At-risk accounts", "Guardrail: portfolio intelligence should preserve client context, avoid reductive scoring, and surface the evidence behind risk flags.")


def retainer_management_assistant() -> str:
    return _render("RETAINER MANAGEMENT ASSISTANT - PHASE 1544", "retainer-management overview", "retainer_management_assistant.json", "retainer_plans", "on-track", "drifting", "Retainer plans tracked", "On-track plans", "Drifting plans", "Guardrail: retainer management should preserve contractual clarity, delivery evidence, and transparent variance handling.")


def recurring_revenue_optimizer() -> str:
    return _render("RECURRING REVENUE OPTIMIZER - PHASE 1545", "recurring-revenue overview", "recurring_revenue_optimizer.json", "revenue_streams", "retained", "churning", "Revenue streams tracked", "Retained streams", "Churning streams", "Guardrail: revenue optimization should preserve customer trust, fair pricing, and transparent retention assumptions.")


def lead_to_invoice_workflow() -> str:
    return _render("LEAD-TO-INVOICE WORKFLOW - PHASE 1546", "lead-to-invoice overview", "lead_to_invoice_workflow.json", "workflow_steps", "connected", "broken", "Workflow steps tracked", "Connected steps", "Broken steps", "Guardrail: lead-to-invoice automation should preserve approval gates, client consent, and auditable handoffs across stages.")


def sales_pipeline_forecaster() -> str:
    return _render("SALES PIPELINE FORECASTER - PHASE 1547", "sales-pipeline overview", "sales_pipeline_forecaster.json", "pipeline_deals", "likely", "stalled", "Pipeline deals tracked", "Likely deals", "Stalled deals", "Guardrail: sales forecasting should preserve uncertainty ranges, note key assumptions, and avoid overstating confidence from sparse data.")


def proposal_follow_up_automator() -> str:
    return _render("PROPOSAL FOLLOW-UP AUTOMATOR - PHASE 1548", "proposal-follow-up overview", "proposal_follow_up_automator.json", "follow_ups", "timely", "spammy", "Follow-ups tracked", "Timely follow-ups", "Spammy follow-ups", "Guardrail: follow-up automation should preserve respectful cadence, opt-out handling, and accurate proposal context in each touchpoint.")


def client_satisfaction_predictor() -> str:
    return _render("CLIENT SATISFACTION PREDICTOR - PHASE 1549", "client-satisfaction overview", "client_satisfaction_predictor.json", "satisfaction_signals", "satisfied", "dissatisfied", "Satisfaction signals tracked", "Satisfied signals", "Dissatisfied signals", "Guardrail: satisfaction prediction should preserve qualitative nuance, explainability, and avoid replacing direct client communication.")


def churn_prevention_engine() -> str:
    return _render("CHURN PREVENTION ENGINE - PHASE 1550", "churn-prevention overview", "churn_prevention_engine.json", "retention_paths", "recoverable", "churning", "Retention paths tracked", "Recoverable paths", "Churning paths", "Guardrail: churn prevention should preserve customer trust, avoid manipulative retention, and surface the reasons behind intervention suggestions.")

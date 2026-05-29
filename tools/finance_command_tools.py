from __future__ import annotations

import json
from pathlib import Path


FINANCE_COMMAND_DIR = Path("storage/finance_command")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(FINANCE_COMMAND_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def payment_milestone_tracker() -> str:
    return _render("PAYMENT MILESTONE TRACKER - PHASE 1591", "payment-milestone overview", "payment_milestones.json", "payment_milestones", "on-track", "overdue", "Payment milestones tracked", "On-track milestones", "Overdue milestones", "Guardrail: payment tracking should preserve contract terms, invoice evidence, and avoid treating disputed milestones as settled.")


def invoice_dispute_assistant() -> str:
    return _render("INVOICE DISPUTE ASSISTANT - PHASE 1592", "invoice-dispute overview", "invoice_disputes.json", "invoice_disputes", "documented", "unresolved", "Invoice disputes tracked", "Documented disputes", "Unresolved disputes", "Guardrail: dispute assistance should preserve factual chronology, contractual nuance, and avoid overclaiming liability or entitlement.")


def cash_flow_prediction_engine() -> str:
    return _render("CASH-FLOW PREDICTION ENGINE - PHASE 1593", "cash-flow overview", "cash_flow_prediction.json", "cash_flow_scenarios", "stable", "strained", "Cash-flow scenarios tracked", "Stable scenarios", "Strained scenarios", "Guardrail: cash-flow forecasting should preserve uncertainty bands, timing assumptions, and separation between committed and expected cash.")


def expense_anomaly_detector() -> str:
    return _render("EXPENSE ANOMALY DETECTOR - PHASE 1594", "expense-anomaly overview", "expense_anomalies.json", "expense_events", "normal", "anomalous", "Expense events tracked", "Normal events", "Anomalous events", "Guardrail: anomaly detection should preserve explainability, category context, and avoid treating unusual spend as wrongdoing by default.")


def tax_planning_assistant() -> str:
    return _render("TAX PLANNING ASSISTANT - PHASE 1595", "tax-planning overview", "tax_planning_assistant.json", "tax_scenarios", "compliant", "uncertain", "Tax scenarios tracked", "Compliant scenarios", "Uncertain scenarios", "Guardrail: tax planning should preserve jurisdiction caveats, source traceability, and require professional review for filing decisions.")


def financial_runway_simulator() -> str:
    return _render("FINANCIAL RUNWAY SIMULATOR - PHASE 1596", "financial-runway overview", "financial_runway_simulator.json", "runway_models", "durable", "short", "Runway models tracked", "Durable models", "Short models", "Guardrail: runway simulation should preserve burn-rate assumptions, contingency visibility, and explicit uncertainty for revenue timing.")


def company_valuation_estimator() -> str:
    return _render("COMPANY VALUATION ESTIMATOR - PHASE 1597", "company-valuation overview", "company_valuation_estimator.json", "valuation_models", "defensible", "speculative", "Valuation models tracked", "Defensible models", "Speculative models", "Guardrail: valuation estimates should preserve methodology clarity, comparable limitations, and explicit non-advisory framing.")


def investor_pitch_intelligence() -> str:
    return _render("INVESTOR PITCH INTELLIGENCE - PHASE 1598", "investor-pitch overview", "investor_pitch_intelligence.json", "pitch_sections", "convincing", "weak", "Pitch sections tracked", "Convincing sections", "Weak sections", "Guardrail: pitch intelligence should preserve factual support, avoid inflated claims, and clearly separate vision from current traction.")


def board_report_generator() -> str:
    return _render("BOARD-REPORT GENERATOR - PHASE 1599", "board-report overview", "board_report_generator.json", "board_sections", "ready", "thin", "Board sections tracked", "Ready sections", "Thin sections", "Guardrail: board reporting should preserve material accuracy, risk disclosure, and balanced reporting rather than pure optimism.")


def executive_war_room_mode() -> str:
    return _render("EXECUTIVE WAR-ROOM MODE - PHASE 1600", "executive-war-room overview", "executive_war_room_mode.json", "decision_panels", "actionable", "chaotic", "Decision panels tracked", "Actionable panels", "Chaotic panels", "Guardrail: executive war-room support should preserve signal hierarchy, accountable owners, and explicit decision provenance.")

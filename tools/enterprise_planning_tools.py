from __future__ import annotations

import json
from pathlib import Path


ENTERPRISE_PLANNING_DIR = Path("storage/enterprise_planning")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def smart_procurement_ai() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "procurement.json", {})
    requests = payload.get("requests", []) if isinstance(payload, dict) else []
    optimized = [item for item in requests if isinstance(item, dict) and bool(item.get("optimized", False))]
    pending = [item for item in requests if isinstance(item, dict) and item.get("status") == "pending"]
    return _overview("SMART PROCUREMENT AI - PHASE 551", "procurement overview", [f"Requests tracked: {len(requests)}", f"Optimized requests: {len(optimized)}", f"Pending requests: {len(pending)}"], "Guardrail: procurement automation should preserve budget boundaries, vendor fairness, and approval workflows before committing spend.")


def autonomous_vendor_comparison() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "vendor_comparison.json", {})
    vendors = payload.get("vendors", []) if isinstance(payload, dict) else []
    shortlisted = [item for item in vendors if isinstance(item, dict) and bool(item.get("shortlisted", False))]
    compliant = [item for item in vendors if isinstance(item, dict) and bool(item.get("compliant", False))]
    return _overview("AUTONOMOUS VENDOR COMPARISON - PHASE 552", "vendor-comparison overview", [f"Vendors tracked: {len(vendors)}", f"Shortlisted vendors: {len(shortlisted)}", f"Compliant vendors: {len(compliant)}"], "Guardrail: vendor comparison should keep criteria transparent, auditable, and policy-aware before driving procurement choices.")


def financial_forecasting_engine() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "financial_forecasting.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    current = [item for item in models if isinstance(item, dict) and item.get("status") == "current"]
    stressed = [item for item in models if isinstance(item, dict) and bool(item.get("stress_tested", False))]
    return _overview("FINANCIAL FORECASTING ENGINE - PHASE 553", "financial-forecasting overview", [f"Forecast models: {len(models)}", f"Current models: {len(current)}", f"Stress-tested models: {len(stressed)}"], "Guardrail: forecasts should show assumptions, scenario coverage, and uncertainty rather than masquerading as certainty.")


def ai_driven_budgeting_assistant() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "budgeting.json", {})
    budgets = payload.get("budgets", []) if isinstance(payload, dict) else []
    over = [item for item in budgets if isinstance(item, dict) and item.get("variance") == "over"]
    approved = [item for item in budgets if isinstance(item, dict) and bool(item.get("approved", False))]
    return _overview("AI-DRIVEN BUDGETING ASSISTANT - PHASE 554", "budgeting overview", [f"Budgets tracked: {len(budgets)}", f"Over-variance budgets: {len(over)}", f"Approved budgets: {len(approved)}"], "Guardrail: budgeting guidance should honor explicit approval thresholds, variance visibility, and departmental accountability before reallocating funds.")


def enterprise_kpi_intelligence() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "kpi_intelligence.json", {})
    kpis = payload.get("kpis", []) if isinstance(payload, dict) else []
    improving = [item for item in kpis if isinstance(item, dict) and item.get("trend") == "up"]
    degrading = [item for item in kpis if isinstance(item, dict) and item.get("trend") == "down"]
    return _overview("ENTERPRISE KPI INTELLIGENCE - PHASE 555", "kpi-intelligence overview", [f"KPIs tracked: {len(kpis)}", f"Improving KPIs: {len(improving)}", f"Degrading KPIs: {len(degrading)}"], "Guardrail: KPI intelligence should show trend context, metric ownership, and measurement confidence before guiding strategy.")


def executive_board_briefing_generator() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "board_briefings.json", {})
    briefings = payload.get("briefings", []) if isinstance(payload, dict) else []
    ready = [item for item in briefings if isinstance(item, dict) and item.get("status") == "ready"]
    risks = [item for item in briefings if isinstance(item, dict) and bool(item.get("includes_risks", False))]
    return _overview("EXECUTIVE BOARD BRIEFING GENERATOR - PHASE 556", "board-briefing overview", [f"Briefings tracked: {len(briefings)}", f"Ready briefings: {len(ready)}", f"Risk-inclusive briefings: {len(risks)}"], "Guardrail: board materials should surface uncertainty, downside risk, and accountable sources before they shape executive decisions.")


def autonomous_strategy_planner() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "strategy_plans.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    prioritized = [item for item in plans if isinstance(item, dict) and bool(item.get("prioritized", False))]
    funded = [item for item in plans if isinstance(item, dict) and bool(item.get("funded", False))]
    return _overview("AUTONOMOUS STRATEGY PLANNER - PHASE 557", "strategy-planning overview", [f"Plans tracked: {len(plans)}", f"Prioritized plans: {len(prioritized)}", f"Funded plans: {len(funded)}"], "Guardrail: strategy planning should remain assumption-aware, resource-constrained, and human-directed before locking execution paths.")


def business_scenario_simulator() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "scenario_simulator.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    downside = [item for item in scenarios if isinstance(item, dict) and item.get("type") == "downside"]
    resilient = [item for item in scenarios if isinstance(item, dict) and bool(item.get("resilient", False))]
    return _overview("BUSINESS SCENARIO SIMULATOR - PHASE 558", "scenario-simulation overview", [f"Scenarios tracked: {len(scenarios)}", f"Downside scenarios: {len(downside)}", f"Resilient scenarios: {len(resilient)}"], "Guardrail: scenario simulation should expose assumptions, stress cases, and limits rather than overstate predictive certainty.")


def competitive_intelligence_engine() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "competitive_intelligence.json", {})
    competitors = payload.get("competitors", []) if isinstance(payload, dict) else []
    watchlist = [item for item in competitors if isinstance(item, dict) and bool(item.get("watchlist", False))]
    moving = [item for item in competitors if isinstance(item, dict) and item.get("trend") == "active"]
    return _overview("COMPETITIVE INTELLIGENCE ENGINE - PHASE 559", "competitive-intelligence overview", [f"Competitors tracked: {len(competitors)}", f"Watchlist competitors: {len(watchlist)}", f"Active-trend competitors: {len(moving)}"], "Guardrail: competitive intelligence should remain source-grounded, time-sensitive, and non-speculative before influencing strategy.")


def market_trend_prediction() -> str:
    payload = _safe_json(ENTERPRISE_PLANNING_DIR / "market_trends.json", {})
    signals = payload.get("signals", []) if isinstance(payload, dict) else []
    strong = [item for item in signals if isinstance(item, dict) and item.get("strength") == "strong"]
    emerging = [item for item in signals if isinstance(item, dict) and item.get("status") == "emerging"]
    return _overview("MARKET TREND PREDICTION - PHASE 560", "market-trend overview", [f"Signals tracked: {len(signals)}", f"Strong signals: {len(strong)}", f"Emerging signals: {len(emerging)}"], "Guardrail: trend prediction should communicate uncertainty, recency, and competing signals before it drives capital allocation.")

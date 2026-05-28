from __future__ import annotations

import json
from pathlib import Path


STRATEGIC_OPS_DIR = Path("storage/strategic_ops")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_opportunity_detection() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "opportunities.json", {})
    opportunities = payload.get("opportunities", []) if isinstance(payload, dict) else []
    scored = [item for item in opportunities if isinstance(item, dict) and bool(item.get("scored", False))]
    near_term = [item for item in opportunities if isinstance(item, dict) and item.get("horizon") == "near"]
    return _overview("AUTONOMOUS OPPORTUNITY DETECTION - PHASE 561", "opportunity-detection overview", [f"Opportunities tracked: {len(opportunities)}", f"Scored opportunities: {len(scored)}", f"Near-term opportunities: {len(near_term)}"], "Guardrail: opportunity detection should prioritize evidence, capacity fit, and downside awareness before promoting action.")


def ai_merger_acquisition_analyzer() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "ma_analysis.json", {})
    targets = payload.get("targets", []) if isinstance(payload, dict) else []
    viable = [item for item in targets if isinstance(item, dict) and bool(item.get("viable", False))]
    risks = [item for item in targets if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("AI MERGER/ACQUISITION ANALYZER - PHASE 562", "ma-analysis overview", [f"Targets tracked: {len(targets)}", f"Viable targets: {len(viable)}", f"High-risk targets: {len(risks)}"], "Guardrail: M and A analysis should stay diligence-first, source-grounded, and explicitly risk-weighted before influencing deals.")


def ai_contract_negotiation_assistant() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "contract_negotiation.json", {})
    drafts = payload.get("drafts", []) if isinstance(payload, dict) else []
    redlines = [item for item in drafts if isinstance(item, dict) and bool(item.get("redlines", False))]
    approved = [item for item in drafts if isinstance(item, dict) and item.get("status") == "approved"]
    return _overview("AI CONTRACT NEGOTIATION ASSISTANT - PHASE 563", "contract-negotiation overview", [f"Drafts tracked: {len(drafts)}", f"Drafts with redlines: {len(redlines)}", f"Approved drafts: {len(approved)}"], "Guardrail: negotiation support should remain counsel-reviewable, version-aware, and aligned with explicit commercial limits.")


def dynamic_pricing_engine() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "dynamic_pricing.json", {})
    products = payload.get("products", []) if isinstance(payload, dict) else []
    updated = [item for item in products if isinstance(item, dict) and bool(item.get("repriced", False))]
    constrained = [item for item in products if isinstance(item, dict) and bool(item.get("margin_floor", False))]
    return _overview("DYNAMIC PRICING ENGINE - PHASE 564", "dynamic-pricing overview", [f"Products tracked: {len(products)}", f"Repriced products: {len(updated)}", f"Margin-constrained products: {len(constrained)}"], "Guardrail: pricing automation should respect margin floors, fairness constraints, and override visibility before publishing changes.")


def supply_demand_forecasting() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "supply_demand.json", {})
    forecasts = payload.get("forecasts", []) if isinstance(payload, dict) else []
    shortages = [item for item in forecasts if isinstance(item, dict) and item.get("balance") == "shortage"]
    surplus = [item for item in forecasts if isinstance(item, dict) and item.get("balance") == "surplus"]
    return _overview("SUPPLY-DEMAND FORECASTING - PHASE 565", "supply-demand overview", [f"Forecasts tracked: {len(forecasts)}", f"Shortage forecasts: {len(shortages)}", f"Surplus forecasts: {len(surplus)}"], "Guardrail: supply-demand forecasts should show confidence bands, seasonality, and operational assumptions before changing commitments.")


def autonomous_logistics_planner() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "logistics_planner.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    optimized = [item for item in plans if isinstance(item, dict) and bool(item.get("optimized", False))]
    delayed = [item for item in plans if isinstance(item, dict) and item.get("status") == "delayed"]
    return _overview("AUTONOMOUS LOGISTICS PLANNER - PHASE 566", "logistics-planning overview", [f"Plans tracked: {len(plans)}", f"Optimized plans: {len(optimized)}", f"Delayed plans: {len(delayed)}"], "Guardrail: logistics planning should balance service reliability, cost, and operational constraints before dispatch decisions.")


def smart_warehouse_orchestration() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "warehouse.json", {})
    zones = payload.get("zones", []) if isinstance(payload, dict) else []
    automated = [item for item in zones if isinstance(item, dict) and bool(item.get("automated", False))]
    congested = [item for item in zones if isinstance(item, dict) and item.get("status") == "congested"]
    return _overview("SMART WAREHOUSE ORCHESTRATION - PHASE 567", "warehouse-orchestration overview", [f"Zones tracked: {len(zones)}", f"Automated zones: {len(automated)}", f"Congested zones: {len(congested)}"], "Guardrail: warehouse orchestration should preserve worker safety, inventory integrity, and fallback handling before acting autonomously.")


def delivery_route_optimization() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "delivery_routes.json", {})
    routes = payload.get("routes", []) if isinstance(payload, dict) else []
    optimized = [item for item in routes if isinstance(item, dict) and bool(item.get("optimized", False))]
    exceptions = [item for item in routes if isinstance(item, dict) and item.get("status") == "exception"]
    return _overview("DELIVERY ROUTE OPTIMIZATION - PHASE 568", "delivery-route overview", [f"Routes tracked: {len(routes)}", f"Optimized routes: {len(optimized)}", f"Exception routes: {len(exceptions)}"], "Guardrail: route optimization should respect delivery commitments, safety constraints, and exception handling before rerouting fleets.")


def fleet_management_ai() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "fleet_management.json", {})
    vehicles = payload.get("vehicles", []) if isinstance(payload, dict) else []
    healthy = [item for item in vehicles if isinstance(item, dict) and item.get("status") == "healthy"]
    offline = [item for item in vehicles if isinstance(item, dict) and item.get("status") == "offline"]
    return _overview("FLEET MANAGEMENT AI - PHASE 569", "fleet-management overview", [f"Vehicles tracked: {len(vehicles)}", f"Healthy vehicles: {len(healthy)}", f"Offline vehicles: {len(offline)}"], "Guardrail: fleet intelligence should foreground safety, maintenance state, and dispatch readiness before issuing operational guidance.")


def smart_retail_analytics() -> str:
    payload = _safe_json(STRATEGIC_OPS_DIR / "retail_analytics.json", {})
    stores = payload.get("stores", []) if isinstance(payload, dict) else []
    growing = [item for item in stores if isinstance(item, dict) and item.get("trend") == "up"]
    underperforming = [item for item in stores if isinstance(item, dict) and item.get("trend") == "down"]
    return _overview("SMART RETAIL ANALYTICS - PHASE 570", "retail-analytics overview", [f"Stores tracked: {len(stores)}", f"Growing stores: {len(growing)}", f"Underperforming stores: {len(underperforming)}"], "Guardrail: retail analytics should expose local context, data freshness, and uncertainty before pushing store-level interventions.")

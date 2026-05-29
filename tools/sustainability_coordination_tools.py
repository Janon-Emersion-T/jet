from __future__ import annotations

import json
from pathlib import Path


SUSTAINABILITY_COORDINATION_DIR = Path("storage/sustainability_coordination")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(SUSTAINABILITY_COORDINATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def infinite_scale_economic_coordination_ai() -> str:
    return _render("INFINITE-SCALE ECONOMIC COORDINATION AI - PHASE 1048", "economic-coordination overview", "economic_coordination.json", "markets", "coordinated", "distorted", "Markets tracked", "Coordinated markets", "Distorted markets", "Guardrail: economic coordination should preserve competition, fairness, and public accountability before optimization.")


def recursive_resource_optimization_framework() -> str:
    return _render("RECURSIVE RESOURCE OPTIMIZATION FRAMEWORK - PHASE 1049", "resource-optimization overview", "resource_optimization.json", "resource_loops", "optimized", "depleted", "Resource loops tracked", "Optimized loops", "Depleted loops", "Guardrail: resource optimization should preserve resilience, ecological limits, and human override before automation.")


def universal_sustainability_cognition_engine() -> str:
    return _render("UNIVERSAL SUSTAINABILITY COGNITION ENGINE - PHASE 1050", "sustainability-cognition overview", "sustainability_cognition.json", "models", "sustainable", "regressive", "Models tracked", "Sustainable models", "Regressive models", "Guardrail: sustainability cognition should preserve lifecycle accounting, justice, and uncertainty disclosure before recommendation.")


def autonomous_food_energy_water_balancing_ai() -> str:
    return _render("AUTONOMOUS FOOD-ENERGY-WATER BALANCING AI - PHASE 1051", "few-balancing overview", "food_energy_water.json", "balances", "balanced", "stressed", "Balances tracked", "Balanced systems", "Stressed systems", "Guardrail: food-energy-water balancing should preserve basic needs, equity, and contingency planning before optimization.")


def planetary_health_synchronization_system() -> str:
    return _render("PLANETARY HEALTH SYNCHRONIZATION SYSTEM - PHASE 1052", "planetary-health overview", "planetary_health.json", "signals", "synchronized", "drifting", "Signals tracked", "Synchronized signals", "Drifting signals", "Guardrail: planetary health synchronization should preserve local evidence, public-health ethics, and transparent baselines before coordination.")


def infinite_scale_urban_planning_substrate() -> str:
    return _render("INFINITE-SCALE URBAN PLANNING SUBSTRATE - PHASE 1053", "urban-planning overview", "urban_planning.json", "districts", "planned", "congested", "Districts tracked", "Planned districts", "Congested districts", "Guardrail: urban planning should preserve housing equity, accessibility, and community participation before rollout.")


def autonomous_transportation_intelligence_mesh() -> str:
    return _render("AUTONOMOUS TRANSPORTATION INTELLIGENCE MESH - PHASE 1054", "transportation-intelligence overview", "transportation_intelligence.json", "corridors", "coordinated", "delayed", "Corridors tracked", "Coordinated corridors", "Delayed corridors", "Guardrail: transportation intelligence should preserve safety, accessibility, and human override before dispatch.")


def recursive_infrastructure_adaptation_engine() -> str:
    return _render("RECURSIVE INFRASTRUCTURE ADAPTATION ENGINE - PHASE 1055", "infrastructure-adaptation overview", "infrastructure_adaptation.json", "assets", "adapted", "brittle", "Assets tracked", "Adapted assets", "Brittle assets", "Guardrail: infrastructure adaptation should preserve maintenance visibility, redundancy, and accountable approvals before changes.")


def universal_energy_stewardship_ai() -> str:
    return _render("UNIVERSAL ENERGY STEWARDSHIP AI - PHASE 1056", "energy-stewardship overview", "energy_stewardship.json", "grids", "stewarded", "wasteful", "Grids tracked", "Stewarded grids", "Wasteful grids", "Guardrail: energy stewardship should preserve reliability, affordability, and public-interest constraints before optimization.")


def adaptive_renewable_optimization_framework() -> str:
    return _render("ADAPTIVE RENEWABLE OPTIMIZATION FRAMEWORK - PHASE 1057", "renewable-optimization overview", "renewable_optimization.json", "portfolios", "optimized", "intermittent", "Portfolios tracked", "Optimized portfolios", "Intermittent portfolios", "Guardrail: renewable optimization should preserve grid stability, storage realism, and ecological siting review before action.")

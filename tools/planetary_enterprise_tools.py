from __future__ import annotations

import json
from pathlib import Path


PLANETARY_ENTERPRISE_DIR = Path("storage/planetary_enterprise")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(PLANETARY_ENTERPRISE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_planetary_coordination_intelligence() -> str:
    return _render("UNIVERSAL PLANETARY COORDINATION INTELLIGENCE - PHASE 1201", "planetary-coordination overview", "planetary_coordination.json", "coordination_loops", "coordinated", "fragmented", "Coordination loops tracked", "Coordinated loops", "Fragmented loops", "Guardrail: planetary coordination should preserve subsidiarity, transparency, and human accountability before orchestration.")


def adaptive_macroeconomic_balancing_ai() -> str:
    return _render("ADAPTIVE MACROECONOMIC BALANCING AI - PHASE 1202", "macroeconomic-balancing overview", "macroeconomic_balancing.json", "economies", "balanced", "volatile", "Economies tracked", "Balanced economies", "Volatile economies", "Guardrail: macroeconomic balancing should preserve democratic legitimacy, equity, and uncertainty disclosure before intervention.")


def autonomous_energy_allocation_substrate() -> str:
    return _render("AUTONOMOUS ENERGY ALLOCATION SUBSTRATE - PHASE 1203", "energy-allocation overview", "energy_allocation.json", "allocations", "optimized", "deprived", "Allocations tracked", "Optimized allocations", "Deprived allocations", "Guardrail: energy allocation should preserve fairness, critical-service priority, and public-interest review before action.")


def infinite_scale_supply_stabilization_framework() -> str:
    return _render("INFINITE-SCALE SUPPLY STABILIZATION FRAMEWORK - PHASE 1204", "supply-stabilization overview", "supply_stabilization.json", "supply_chains", "stabilized", "disrupted", "Supply chains tracked", "Stabilized chains", "Disrupted chains", "Guardrail: supply stabilization should preserve resilience, labor safeguards, and contingency planning before optimization.")


def recursive_distribution_equity_engine() -> str:
    return _render("RECURSIVE DISTRIBUTION EQUITY ENGINE - PHASE 1205", "distribution-equity overview", "distribution_equity.json", "distributions", "equitable", "skewed", "Distributions tracked", "Equitable distributions", "Skewed distributions", "Guardrail: distribution equity should preserve justice, local context, and appeals before reallocation.")


def universal_labor_optimization_ai() -> str:
    return _render("UNIVERSAL LABOR OPTIMIZATION AI - PHASE 1206", "labor-optimization overview", "labor_optimization.json", "labor_models", "optimized", "extractive", "Labor models tracked", "Optimized models", "Extractive models", "Guardrail: labor optimization should preserve worker dignity, consent, and fair conditions before deployment.")


def adaptive_automation_transition_framework() -> str:
    return _render("ADAPTIVE AUTOMATION TRANSITION FRAMEWORK - PHASE 1207", "automation-transition overview", "automation_transition.json", "transitions", "supported", "displacing", "Transitions tracked", "Supported transitions", "Displacing transitions", "Guardrail: automation transitions should preserve reskilling support, equity, and humane pacing before execution.")


def autonomous_innovation_prioritization_engine() -> str:
    return _render("AUTONOMOUS INNOVATION PRIORITIZATION ENGINE - PHASE 1208", "innovation-prioritization overview", "innovation_prioritization.json", "priorities", "prioritized", "neglected", "Priorities tracked", "Prioritized opportunities", "Neglected opportunities", "Guardrail: innovation prioritization should preserve public-interest goals, plural inputs, and reviewable criteria before ranking.")


def infinite_scale_capital_allocation_ai() -> str:
    return _render("INFINITE-SCALE CAPITAL ALLOCATION AI - PHASE 1209", "capital-allocation overview", "capital_allocation.json", "portfolios", "allocated", "concentrated", "Portfolios tracked", "Allocated portfolios", "Concentrated portfolios", "Guardrail: capital allocation should preserve anti-monopoly safeguards, transparency, and accountable oversight before automation.")


def recursive_entrepreneurship_simulation_framework() -> str:
    return _render("RECURSIVE ENTREPRENEURSHIP SIMULATION FRAMEWORK - PHASE 1210", "entrepreneurship-simulation overview", "entrepreneurship_simulation.json", "ventures", "simulated", "fragile", "Ventures tracked", "Simulated ventures", "Fragile ventures", "Guardrail: entrepreneurship simulation should preserve realism, inclusion, and non-exploitative guidance before recommendation.")

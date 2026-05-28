from __future__ import annotations

import json
from pathlib import Path


RESEARCH_STRATEGY_DIR = Path("storage/research_strategy")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RESEARCH_STRATEGY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join(
        [
            title,
            f"Mode: {mode}.",
            f"{key_label}: {len(items)}",
            f"{positive_label}: {len(positives)}",
            f"{risk_label}: {len(risks)}",
            guardrail,
        ]
    )


def cross_disciplinary_research_fusion_ai() -> str:
    return _render("CROSS-DISCIPLINARY RESEARCH FUSION AI - PHASE 1029", "research-fusion overview", "research_fusion.json", "programs", "fused", "blocked", "Programs tracked", "Fused programs", "Blocked programs", "Guardrail: research fusion should preserve disciplinary rigor, provenance, and explicit uncertainty before synthesis.")


def adaptive_interstellar_strategy_simulator() -> str:
    return _render("ADAPTIVE INTERSTELLAR STRATEGY SIMULATOR - PHASE 1030", "interstellar-strategy overview", "interstellar_strategy.json", "strategies", "adaptive", "fragile", "Strategies tracked", "Adaptive strategies", "Fragile strategies", "Guardrail: interstellar strategy simulation should remain speculative, bounded, and subordinate to accountable human judgment.")


def recursive_existential_risk_analyzer() -> str:
    return _render("RECURSIVE EXISTENTIAL RISK ANALYZER - PHASE 1031", "existential-risk overview", "existential_risk.json", "risks", "modeled", "escalating", "Risks tracked", "Modeled risks", "Escalating risks", "Guardrail: existential risk analysis should preserve calibration, external review, and transparent assumptions before escalation.")


def universal_predictive_civilization_engine() -> str:
    return _render("UNIVERSAL PREDICTIVE CIVILIZATION ENGINE - PHASE 1032", "predictive-civilization overview", "predictive_civilization.json", "scenarios", "predicted", "volatile", "Scenarios tracked", "Predicted scenarios", "Volatile scenarios", "Guardrail: civilization prediction should preserve humility, scenario diversity, and clear non-determinism before planning.")


def autonomous_cosmic_scale_operations_planner() -> str:
    return _render("AUTONOMOUS COSMIC-SCALE OPERATIONS PLANNER - PHASE 1033", "cosmic-operations overview", "cosmic_operations.json", "operations", "planned", "overextended", "Operations tracked", "Planned operations", "Overextended operations", "Guardrail: cosmic-scale planning should preserve layered approvals, feasibility checks, and reversible execution before coordination.")


def planetary_prosperity_balancing_framework() -> str:
    return _render("PLANETARY PROSPERITY BALANCING FRAMEWORK - PHASE 1034", "prosperity-balancing overview", "prosperity_balancing.json", "balances", "balanced", "uneven", "Balances tracked", "Balanced plans", "Uneven plans", "Guardrail: prosperity balancing should preserve equity, local context, and public accountability before optimization.")


def infinite_scale_moral_reasoning_mesh() -> str:
    return _render("INFINITE-SCALE MORAL REASONING MESH - PHASE 1035", "moral-reasoning overview", "moral_reasoning.json", "reasoners", "aligned", "contested", "Reasoners tracked", "Aligned reasoners", "Contested reasoners", "Guardrail: moral reasoning meshes should preserve plural values, appeal mechanisms, and human accountability before use.")


def human_flourishing_simulation_substrate() -> str:
    return _render("HUMAN FLOURISHING SIMULATION SUBSTRATE - PHASE 1036", "flourishing-simulation overview", "flourishing_simulation.json", "cohorts", "simulated", "stressed", "Cohorts tracked", "Simulated cohorts", "Stressed cohorts", "Guardrail: flourishing simulation should preserve dignity, non-reductionism, and careful interpretation before policy use.")


def autonomous_multi_generational_planning_system() -> str:
    return _render("AUTONOMOUS MULTI-GENERATIONAL PLANNING SYSTEM - PHASE 1037", "multi-generational-planning overview", "multi_generational_planning.json", "plans", "long_horizon", "unfunded", "Plans tracked", "Long-horizon plans", "Unfunded plans", "Guardrail: multi-generational planning should preserve intergenerational fairness, transparency, and human consent before adoption.")

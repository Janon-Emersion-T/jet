from __future__ import annotations

import json
from pathlib import Path


FORESIGHT_GOVERNANCE_DIR = Path("storage/foresight_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(FORESIGHT_GOVERNANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_logic_harmonization_network() -> str:
    return _render("UNIVERSAL LOGIC HARMONIZATION NETWORK - PHASE 1131", "logic-harmonization overview", "logic_harmonization.json", "systems", "harmonized", "conflicted", "Systems tracked", "Harmonized systems", "Conflicted systems", "Guardrail: logic harmonization should preserve formal diversity, proof visibility, and dispute resolution before consolidation.")


def adaptive_causal_inference_framework() -> str:
    return _render("ADAPTIVE CAUSAL INFERENCE FRAMEWORK - PHASE 1132", "causal-inference overview", "causal_inference.json", "models", "inferred", "confounded", "Models tracked", "Inferred models", "Confounded models", "Guardrail: causal inference should preserve identification limits, sensitivity analysis, and transparent assumptions before use.")


def autonomous_uncertainty_management_engine() -> str:
    return _render("AUTONOMOUS UNCERTAINTY MANAGEMENT ENGINE - PHASE 1133", "uncertainty-management overview", "uncertainty_management.json", "estimates", "bounded", "unbounded", "Estimates tracked", "Bounded estimates", "Unbounded estimates", "Guardrail: uncertainty management should preserve calibration, abstention paths, and human review before action.")


def infinite_scale_probabilistic_reasoning_ai() -> str:
    return _render("INFINITE-SCALE PROBABILISTIC REASONING AI - PHASE 1134", "probabilistic-reasoning overview", "probabilistic_reasoning.json", "reasoners", "calibrated", "skewed", "Reasoners tracked", "Calibrated reasoners", "Skewed reasoners", "Guardrail: probabilistic reasoning should preserve calibration metrics, interpretability, and oversight before deployment.")


def recursive_temporal_prediction_framework() -> str:
    return _render("RECURSIVE TEMPORAL PREDICTION FRAMEWORK - PHASE 1135", "temporal-prediction overview", "temporal_prediction.json", "timelines", "predicted", "drifting", "Timelines tracked", "Predicted timelines", "Drifting timelines", "Guardrail: temporal prediction should preserve uncertainty bands, update discipline, and scenario plurality before planning.")


def universal_future_simulation_substrate() -> str:
    return _render("UNIVERSAL FUTURE SIMULATION SUBSTRATE - PHASE 1136", "future-simulation overview", "future_simulation.json", "futures", "simulated", "speculative", "Futures tracked", "Simulated futures", "Speculative futures", "Guardrail: future simulation should preserve humility, transparency, and non-deterministic framing before recommendation.")


def adaptive_timeline_optimization_engine() -> str:
    return _render("ADAPTIVE TIMELINE OPTIMIZATION ENGINE - PHASE 1137", "timeline-optimization overview", "timeline_optimization.json", "timelines", "optimized", "brittle", "Timelines tracked", "Optimized timelines", "Brittle timelines", "Guardrail: timeline optimization should preserve rights, resilience, and reversible decisions before coordination.")


def autonomous_scenario_branching_intelligence() -> str:
    return _render("AUTONOMOUS SCENARIO BRANCHING INTELLIGENCE - PHASE 1138", "scenario-branching overview", "scenario_branching.json", "branches", "explored", "collapsed", "Branches tracked", "Explored branches", "Collapsed branches", "Guardrail: scenario branching should preserve diversity of futures, uncertainty disclosure, and human interpretation before action.")


def infinite_scale_strategic_foresight_layer() -> str:
    return _render("INFINITE-SCALE STRATEGIC FORESIGHT LAYER - PHASE 1139", "strategic-foresight overview", "strategic_foresight.json", "horizons", "scanned", "blind", "Horizons tracked", "Scanned horizons", "Blind horizons", "Guardrail: strategic foresight should preserve plural perspectives, anti-groupthink practices, and contestability before planning.")


def recursive_geopolitical_stability_simulator() -> str:
    return _render("RECURSIVE GEOPOLITICAL STABILITY SIMULATOR - PHASE 1140", "geopolitical-stability overview", "geopolitical_stability.json", "regions", "stabilized", "volatile", "Regions tracked", "Stabilized regions", "Volatile regions", "Guardrail: geopolitical simulation should preserve legitimacy, conflict sensitivity, and non-escalatory review before recommendation.")

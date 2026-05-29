from __future__ import annotations

import json
from pathlib import Path


PHIL_FUTURE_DIR = Path("storage/philosophy_future")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def cross_species_communication_research() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "cross_species_communication.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    translated = [item for item in studies if isinstance(item, dict) and bool(item.get("translated", False))]
    tentative = [item for item in studies if isinstance(item, dict) and bool(item.get("tentative", False))]
    return _overview("CROSS-SPECIES COMMUNICATION RESEARCH - PHASE 811", "cross-species-communication overview", [f"Studies tracked: {len(studies)}", f"Translated studies: {len(translated)}", f"Tentative studies: {len(tentative)}"], "Guardrail: cross-species interpretation should preserve uncertainty, welfare, and non-anthropomorphic caution.")


def ai_philosophy_engine() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "philosophy_engine.json", {})
    arguments = payload.get("arguments", []) if isinstance(payload, dict) else []
    grounded = [item for item in arguments if isinstance(item, dict) and bool(item.get("grounded", False))]
    contested = [item for item in arguments if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("AI PHILOSOPHY ENGINE - PHASE 812", "philosophy-engine overview", [f"Arguments tracked: {len(arguments)}", f"Grounded arguments: {len(grounded)}", f"Contested arguments: {len(contested)}"], "Guardrail: philosophical synthesis should preserve plural traditions, explicit assumptions, and non-definitive framing.")


def metaphysical_reasoning_sandbox() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "metaphysical_reasoning.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    explored = [item for item in models if isinstance(item, dict) and bool(item.get("explored", False))]
    speculative = [item for item in models if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("METAPHYSICAL REASONING SANDBOX - PHASE 813", "metaphysical-reasoning overview", [f"Models tracked: {len(models)}", f"Explored models: {len(explored)}", f"Speculative models: {len(speculative)}"], "Guardrail: metaphysical exploration should remain clearly speculative and separated from empirical claims.")


def existential_risk_simulation() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "existential_risk.json", {})
    risks = payload.get("risks", []) if isinstance(payload, dict) else []
    modeled = [item for item in risks if isinstance(item, dict) and bool(item.get("modeled", False))]
    severe = [item for item in risks if isinstance(item, dict) and item.get("severity") == "severe"]
    return _overview("EXISTENTIAL RISK SIMULATION - PHASE 814", "existential-risk overview", [f"Risks tracked: {len(risks)}", f"Modeled risks: {len(modeled)}", f"Severe risks: {len(severe)}"], "Guardrail: existential risk modeling should preserve uncertainty, non-alarmism, and broad expert review before action.")


def human_destiny_modeling_framework() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "human_destiny_modeling.json", {})
    futures = payload.get("futures", []) if isinstance(payload, dict) else []
    inclusive = [item for item in futures if isinstance(item, dict) and bool(item.get("inclusive", False))]
    fragile = [item for item in futures if isinstance(item, dict) and bool(item.get("fragile", False))]
    return _overview("HUMAN DESTINY MODELING FRAMEWORK - PHASE 815", "human-destiny-modeling overview", [f"Futures tracked: {len(futures)}", f"Inclusive futures: {len(inclusive)}", f"Fragile futures: {len(fragile)}"], "Guardrail: destiny modeling should preserve humility, pluralism, and avoid determinism.")


def autonomous_civilization_continuity_planning() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "civilization_continuity.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    resilient = [item for item in plans if isinstance(item, dict) and bool(item.get("resilient", False))]
    incomplete = [item for item in plans if isinstance(item, dict) and bool(item.get("incomplete", False))]
    return _overview("AUTONOMOUS CIVILIZATION CONTINUITY PLANNING - PHASE 816", "civilization-continuity overview", [f"Plans tracked: {len(plans)}", f"Resilient plans: {len(resilient)}", f"Incomplete plans: {len(incomplete)}"], "Guardrail: continuity planning should preserve societal rights, transparency, and democratic legitimacy before prioritization.")


def long_horizon_future_forecasting() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "future_forecasting.json", {})
    forecasts = payload.get("forecasts", []) if isinstance(payload, dict) else []
    calibrated = [item for item in forecasts if isinstance(item, dict) and bool(item.get("calibrated", False))]
    uncertain = [item for item in forecasts if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("LONG-HORIZON FUTURE FORECASTING - PHASE 817", "future-forecasting overview", [f"Forecasts tracked: {len(forecasts)}", f"Calibrated forecasts: {len(calibrated)}", f"Uncertain forecasts: {len(uncertain)}"], "Guardrail: long-horizon forecasting should preserve calibration, dissent, and explicit uncertainty before planning use.")


def ai_macro_history_engine() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "macro_history.json", {})
    eras = payload.get("eras", []) if isinstance(payload, dict) else []
    synthesized = [item for item in eras if isinstance(item, dict) and bool(item.get("synthesized", False))]
    disputed = [item for item in eras if isinstance(item, dict) and bool(item.get("disputed", False))]
    return _overview("AI MACRO-HISTORY ENGINE - PHASE 818", "macro-history overview", [f"Eras tracked: {len(eras)}", f"Synthesized eras: {len(synthesized)}", f"Disputed eras: {len(disputed)}"], "Guardrail: macro-history should preserve historiographic nuance and visible disagreement before pattern claims.")


def temporal_scenario_generator() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "temporal_scenarios.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    generated = [item for item in scenarios if isinstance(item, dict) and bool(item.get("generated", False))]
    branching = [item for item in scenarios if isinstance(item, dict) and bool(item.get("branching", False))]
    return _overview("TEMPORAL SCENARIO GENERATOR - PHASE 819", "temporal-scenario overview", [f"Scenarios tracked: {len(scenarios)}", f"Generated scenarios: {len(generated)}", f"Branching scenarios: {len(branching)}"], "Guardrail: temporal scenarios should remain exploratory, not predictive certainty, and should expose branching assumptions.")


def multiverse_simulation_sandbox() -> str:
    payload = _safe_json(PHIL_FUTURE_DIR / "multiverse_simulation.json", {})
    universes = payload.get("universes", []) if isinstance(payload, dict) else []
    simulated = [item for item in universes if isinstance(item, dict) and bool(item.get("simulated", False))]
    speculative = [item for item in universes if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("MULTIVERSE SIMULATION SANDBOX - PHASE 820", "multiverse-simulation overview", [f"Universes tracked: {len(universes)}", f"Simulated universes: {len(simulated)}", f"Speculative universes: {len(speculative)}"], "Guardrail: multiverse simulations should remain clearly theoretical and separated from operational decision support.")

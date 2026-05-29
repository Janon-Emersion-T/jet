from __future__ import annotations

import json
from pathlib import Path


RESILIENCE_FUTURE_DIR = Path("storage/resilience_defense_future")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def universal_coordination_intelligence() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "coordination_intelligence.json", {})
    hubs = payload.get("hubs", []) if isinstance(payload, dict) else []
    aligned = [item for item in hubs if isinstance(item, dict) and bool(item.get("aligned", False))]
    delayed = [item for item in hubs if isinstance(item, dict) and bool(item.get("delayed", False))]
    return _overview("UNIVERSAL COORDINATION INTELLIGENCE - PHASE 871", "coordination-intelligence overview", [f"Hubs tracked: {len(hubs)}", f"Aligned hubs: {len(aligned)}", f"Delayed hubs: {len(delayed)}"], "Guardrail: universal coordination should preserve local autonomy, transparency, and contestability before centralization.")


def hyper_scale_ethical_governance() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "ethical_governance.json", {})
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    reviewed = [item for item in policies if isinstance(item, dict) and bool(item.get("reviewed", False))]
    risky = [item for item in policies if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("HYPER-SCALE ETHICAL GOVERNANCE - PHASE 872", "ethical-governance overview", [f"Policies tracked: {len(policies)}", f"Reviewed policies: {len(reviewed)}", f"High-risk policies: {len(risky)}"], "Guardrail: large-scale governance should preserve plural oversight and appealability before enforcement.")


def ai_civilization_resilience_engine() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "civilization_resilience.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    resilient = [item for item in systems if isinstance(item, dict) and bool(item.get("resilient", False))]
    brittle = [item for item in systems if isinstance(item, dict) and bool(item.get("brittle", False))]
    return _overview("AI CIVILIZATION RESILIENCE ENGINE - PHASE 873", "civilization-resilience overview", [f"Systems tracked: {len(systems)}", f"Resilient systems: {len(resilient)}", f"Brittle systems: {len(brittle)}"], "Guardrail: resilience modeling should preserve uncertainty, redundancy, and human governance before action.")


def planetary_defense_intelligence() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "planetary_defense.json", {})
    threats = payload.get("threats", []) if isinstance(payload, dict) else []
    tracked = [item for item in threats if isinstance(item, dict) and bool(item.get("tracked", False))]
    severe = [item for item in threats if isinstance(item, dict) and item.get("severity") == "severe"]
    return _overview("PLANETARY DEFENSE INTELLIGENCE - PHASE 874", "planetary-defense overview", [f"Threats tracked: {len(threats)}", f"Tracked threats: {len(tracked)}", f"Severe threats: {len(severe)}"], "Guardrail: planetary defense support should preserve verification, de-escalation, and accountable human command before intervention.")


def asteroid_threat_analysis() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "asteroid_threats.json", {})
    objects = payload.get("objects", []) if isinstance(payload, dict) else []
    analyzed = [item for item in objects if isinstance(item, dict) and bool(item.get("analyzed", False))]
    near = [item for item in objects if isinstance(item, dict) and bool(item.get("near", False))]
    return _overview("ASTEROID THREAT ANALYSIS - PHASE 875", "asteroid-threat overview", [f"Objects tracked: {len(objects)}", f"Analyzed objects: {len(analyzed)}", f"Near-pass objects: {len(near)}"], "Guardrail: asteroid analysis should preserve measurement uncertainty and verified observational review before action.")


def solar_event_prediction_system() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "solar_events.json", {})
    events = payload.get("events", []) if isinstance(payload, dict) else []
    predicted = [item for item in events if isinstance(item, dict) and bool(item.get("predicted", False))]
    disruptive = [item for item in events if isinstance(item, dict) and bool(item.get("disruptive", False))]
    return _overview("SOLAR EVENT PREDICTION SYSTEM - PHASE 876", "solar-event-prediction overview", [f"Events tracked: {len(events)}", f"Predicted events: {len(predicted)}", f"Disruptive events: {len(disruptive)}"], "Guardrail: solar predictions should preserve scientific uncertainty and infrastructure coordination before alerts.")


def global_infrastructure_resilience_ai() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "infrastructure_resilience.json", {})
    assets = payload.get("assets", []) if isinstance(payload, dict) else []
    hardened = [item for item in assets if isinstance(item, dict) and bool(item.get("hardened", False))]
    exposed = [item for item in assets if isinstance(item, dict) and bool(item.get("exposed", False))]
    return _overview("GLOBAL INFRASTRUCTURE RESILIENCE AI - PHASE 877", "infrastructure-resilience overview", [f"Assets tracked: {len(assets)}", f"Hardened assets: {len(hardened)}", f"Exposed assets: {len(exposed)}"], "Guardrail: resilience planning should preserve public accountability and avoid opaque prioritization of essential infrastructure.")


def autonomous_emergency_adaptation() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "emergency_adaptation.json", {})
    responses = payload.get("responses", []) if isinstance(payload, dict) else []
    adaptive = [item for item in responses if isinstance(item, dict) and bool(item.get("adaptive", False))]
    overloaded = [item for item in responses if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("AUTONOMOUS EMERGENCY ADAPTATION - PHASE 878", "emergency-adaptation overview", [f"Responses tracked: {len(responses)}", f"Adaptive responses: {len(adaptive)}", f"Overloaded responses: {len(overloaded)}"], "Guardrail: emergency adaptation should preserve human command and robust fail-safe behavior before autonomy expands.")


def multi_generational_planning_framework() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "multi_generational_planning.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    long_range = [item for item in plans if isinstance(item, dict) and bool(item.get("long_range", False))]
    fragile = [item for item in plans if isinstance(item, dict) and bool(item.get("fragile", False))]
    return _overview("MULTI-GENERATIONAL PLANNING FRAMEWORK - PHASE 879", "multi-generational-planning overview", [f"Plans tracked: {len(plans)}", f"Long-range plans: {len(long_range)}", f"Fragile plans: {len(fragile)}"], "Guardrail: multi-generational planning should preserve intergenerational justice and humility about long-term prediction.")


def deep_future_civilization_simulator() -> str:
    payload = _safe_json(RESILIENCE_FUTURE_DIR / "deep_future_civilization.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    simulated = [item for item in scenarios if isinstance(item, dict) and bool(item.get("simulated", False))]
    divergent = [item for item in scenarios if isinstance(item, dict) and bool(item.get("divergent", False))]
    return _overview("DEEP FUTURE CIVILIZATION SIMULATOR - PHASE 880", "deep-future-civilization overview", [f"Scenarios tracked: {len(scenarios)}", f"Simulated scenarios: {len(simulated)}", f"Divergent scenarios: {len(divergent)}"], "Guardrail: deep future simulation should remain exploratory, non-deterministic, and transparent about assumptions.")

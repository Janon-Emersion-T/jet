from __future__ import annotations

import json
from pathlib import Path


RESILIENCE_MEMORY_DIR = Path("storage/resilience_memory")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def planetary_resilience_scenario_planner() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "resilience_scenarios.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    planned = [item for item in scenarios if isinstance(item, dict) and bool(item.get("planned", False))]
    fragile = [item for item in scenarios if isinstance(item, dict) and bool(item.get("fragile", False))]
    return _overview("PLANETARY RESILIENCE SCENARIO PLANNER - PHASE 921", "resilience-scenarios overview", [f"Scenarios tracked: {len(scenarios)}", f"Planned scenarios: {len(planned)}", f"Fragile scenarios: {len(fragile)}"], "Guardrail: resilience scenario planning should preserve uncertainty and public accountability before mobilization.")


def adaptive_civilization_memory_vault() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "memory_vault.json", {})
    vaults = payload.get("vaults", []) if isinstance(payload, dict) else []
    replicated = [item for item in vaults if isinstance(item, dict) and bool(item.get("replicated", False))]
    stale = [item for item in vaults if isinstance(item, dict) and bool(item.get("stale", False))]
    return _overview("ADAPTIVE CIVILIZATION MEMORY VAULT - PHASE 922", "memory-vault overview", [f"Vaults tracked: {len(vaults)}", f"Replicated vaults: {len(replicated)}", f"Stale vaults: {len(stale)}"], "Guardrail: civilization memory vaults should preserve provenance, rights, and update discipline before archival spread.")


def ai_assisted_existential_resilience_framework() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "existential_resilience.json", {})
    frameworks = payload.get("frameworks", []) if isinstance(payload, dict) else []
    strengthened = [item for item in frameworks if isinstance(item, dict) and bool(item.get("strengthened", False))]
    exposed = [item for item in frameworks if isinstance(item, dict) and bool(item.get("exposed", False))]
    return _overview("AI-ASSISTED EXISTENTIAL RESILIENCE FRAMEWORK - PHASE 923", "existential-resilience overview", [f"Frameworks tracked: {len(frameworks)}", f"Strengthened frameworks: {len(strengthened)}", f"Exposed frameworks: {len(exposed)}"], "Guardrail: existential resilience work should preserve broad expert input and non-alarmist communication before action.")


def human_machine_co_creativity_ecosystem() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "co_creativity.json", {})
    studios = payload.get("studios", []) if isinstance(payload, dict) else []
    collaborative = [item for item in studios if isinstance(item, dict) and bool(item.get("collaborative", False))]
    blocked = [item for item in studios if isinstance(item, dict) and bool(item.get("blocked", False))]
    return _overview("HUMAN-MACHINE CO-CREATIVITY ECOSYSTEM - PHASE 924", "co-creativity overview", [f"Studios tracked: {len(studios)}", f"Collaborative studios: {len(collaborative)}", f"Blocked studios: {len(blocked)}"], "Guardrail: co-creativity systems should preserve attribution, user agency, and meaningful human contribution before automation.")


def autonomous_cultural_renaissance_engine() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "cultural_renaissance.json", {})
    movements = payload.get("movements", []) if isinstance(payload, dict) else []
    renewed = [item for item in movements if isinstance(item, dict) and bool(item.get("renewed", False))]
    neglected = [item for item in movements if isinstance(item, dict) and bool(item.get("neglected", False))]
    return _overview("AUTONOMOUS CULTURAL RENAISSANCE ENGINE - PHASE 925", "cultural-renaissance overview", [f"Movements tracked: {len(movements)}", f"Renewed movements: {len(renewed)}", f"Neglected movements: {len(neglected)}"], "Guardrail: cultural renaissance support should preserve local voice, attribution, and non-extractive participation before scale.")


def universal_collaborative_intelligence_layer() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "collaborative_intelligence_layer.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    integrated = [item for item in layers if isinstance(item, dict) and bool(item.get("integrated", False))]
    fragmented = [item for item in layers if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("UNIVERSAL COLLABORATIVE INTELLIGENCE LAYER - PHASE 926", "collaborative-intelligence-layer overview", [f"Layers tracked: {len(layers)}", f"Integrated layers: {len(integrated)}", f"Fragmented layers: {len(fragmented)}"], "Guardrail: collaborative intelligence should preserve role clarity, consent, and explainable synthesis before scaling.")


def recursive_institutional_optimization_ai() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "institutional_optimization.json", {})
    institutions = payload.get("institutions", []) if isinstance(payload, dict) else []
    optimized = [item for item in institutions if isinstance(item, dict) and bool(item.get("optimized", False))]
    brittle = [item for item in institutions if isinstance(item, dict) and bool(item.get("brittle", False))]
    return _overview("RECURSIVE INSTITUTIONAL OPTIMIZATION AI - PHASE 927", "institutional-optimization overview", [f"Institutions tracked: {len(institutions)}", f"Optimized institutions: {len(optimized)}", f"Brittle institutions: {len(brittle)}"], "Guardrail: institutional optimization should preserve democratic legitimacy and avoid technocratic lock-in before reform.")


def ai_assisted_decentralized_governance_framework() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "decentralized_governance.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    delegated = [item for item in nodes if isinstance(item, dict) and bool(item.get("delegated", False))]
    conflicted = [item for item in nodes if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("AI-ASSISTED DECENTRALIZED GOVERNANCE FRAMEWORK - PHASE 928", "decentralized-governance overview", [f"Nodes tracked: {len(nodes)}", f"Delegated nodes: {len(delegated)}", f"Conflicted nodes: {len(conflicted)}"], "Guardrail: decentralized governance should preserve transparency, appeal paths, and accountable human participation before automation.")


def dynamic_civilization_adaptation_system() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "civilization_adaptation.json", {})
    adaptations = payload.get("adaptations", []) if isinstance(payload, dict) else []
    adaptive = [item for item in adaptations if isinstance(item, dict) and bool(item.get("adaptive", False))]
    unstable = [item for item in adaptations if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("DYNAMIC CIVILIZATION ADAPTATION SYSTEM - PHASE 929", "civilization-adaptation overview", [f"Adaptations tracked: {len(adaptations)}", f"Adaptive changes: {len(adaptive)}", f"Unstable changes: {len(unstable)}"], "Guardrail: civilization adaptation should preserve continuity, consent, and reversibility before large-scale change.")


def cross_domain_wisdom_synthesis_engine() -> str:
    payload = _safe_json(RESILIENCE_MEMORY_DIR / "wisdom_synthesis.json", {})
    syntheses = payload.get("syntheses", []) if isinstance(payload, dict) else []
    grounded = [item for item in syntheses if isinstance(item, dict) and bool(item.get("grounded", False))]
    thin = [item for item in syntheses if isinstance(item, dict) and bool(item.get("thin", False))]
    return _overview("CROSS-DOMAIN WISDOM SYNTHESIS ENGINE - PHASE 930", "wisdom-synthesis overview", [f"Syntheses tracked: {len(syntheses)}", f"Grounded syntheses: {len(grounded)}", f"Thin syntheses: {len(thin)}"], "Guardrail: wisdom synthesis should preserve nuance, source plurality, and clear uncertainty before advice.")

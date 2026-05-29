from __future__ import annotations

import json
from pathlib import Path


OMEGA_GOV_DIR = Path("storage/omega_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def planetary_adaptive_governance_intelligence() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "adaptive_governance.json", {})
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    adaptive = [item for item in policies if isinstance(item, dict) and bool(item.get("adaptive", False))]
    conflicted = [item for item in policies if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("PLANETARY ADAPTIVE GOVERNANCE INTELLIGENCE - PHASE 981", "adaptive-governance overview", [f"Policies tracked: {len(policies)}", f"Adaptive policies: {len(adaptive)}", f"Conflicted policies: {len(conflicted)}"], "Guardrail: adaptive governance should preserve democratic review, appeals, and visible value tradeoffs before deployment.")


def infinite_scale_ethical_simulation_framework() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "ethical_simulation.json", {})
    simulations = payload.get("simulations", []) if isinstance(payload, dict) else []
    scaled = [item for item in simulations if isinstance(item, dict) and bool(item.get("scaled", False))]
    unstable = [item for item in simulations if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("INFINITE-SCALE ETHICAL SIMULATION FRAMEWORK - PHASE 982", "ethical-simulation overview", [f"Simulations tracked: {len(simulations)}", f"Scaled simulations: {len(scaled)}", f"Unstable simulations: {len(unstable)}"], "Guardrail: ethical simulation should preserve pluralism, transparent assumptions, and clear non-authoritative framing before use.")


def cross_reality_cognition_research_layer() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "cross_reality_cognition.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    studied = [item for item in layers if isinstance(item, dict) and bool(item.get("studied", False))]
    noisy = [item for item in layers if isinstance(item, dict) and bool(item.get("noisy", False))]
    return _overview("CROSS-REALITY COGNITION RESEARCH LAYER - PHASE 983", "cross-reality-cognition overview", [f"Layers tracked: {len(layers)}", f"Studied layers: {len(studied)}", f"Noisy layers: {len(noisy)}"], "Guardrail: cross-reality cognition should remain research-bounded, uncertainty-aware, and empirically cautious before interpretation.")


def universal_knowledge_emergence_engine() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "knowledge_emergence.json", {})
    patterns = payload.get("patterns", []) if isinstance(payload, dict) else []
    emerged = [item for item in patterns if isinstance(item, dict) and bool(item.get("emerged", False))]
    brittle = [item for item in patterns if isinstance(item, dict) and bool(item.get("brittle", False))]
    return _overview("UNIVERSAL KNOWLEDGE EMERGENCE ENGINE - PHASE 984", "knowledge-emergence overview", [f"Patterns tracked: {len(patterns)}", f"Emerged patterns: {len(emerged)}", f"Brittle patterns: {len(brittle)}"], "Guardrail: knowledge emergence should preserve provenance, falsifiability, and human review before claims.")


def autonomous_interstellar_continuity_framework() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "interstellar_continuity.json", {})
    continuities = payload.get("continuities", []) if isinstance(payload, dict) else []
    maintained = [item for item in continuities if isinstance(item, dict) and bool(item.get("maintained", False))]
    degraded = [item for item in continuities if isinstance(item, dict) and bool(item.get("degraded", False))]
    return _overview("AUTONOMOUS INTERSTELLAR CONTINUITY FRAMEWORK - PHASE 985", "interstellar-continuity overview", [f"Continuities tracked: {len(continuities)}", f"Maintained continuities: {len(maintained)}", f"Degraded continuities: {len(degraded)}"], "Guardrail: interstellar continuity should preserve resilience, accountability, and repair paths before dependence.")


def civilization_scale_intelligence_harmonizer() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "intelligence_harmonizer.json", {})
    streams = payload.get("streams", []) if isinstance(payload, dict) else []
    harmonized = [item for item in streams if isinstance(item, dict) and bool(item.get("harmonized", False))]
    divergent = [item for item in streams if isinstance(item, dict) and bool(item.get("divergent", False))]
    return _overview("CIVILIZATION-SCALE INTELLIGENCE HARMONIZER - PHASE 986", "intelligence-harmonizer overview", [f"Streams tracked: {len(streams)}", f"Harmonized streams: {len(harmonized)}", f"Divergent streams: {len(divergent)}"], "Guardrail: intelligence harmonization should preserve disagreement, plurality, and anti-coercive synthesis before convergence.")


def recursive_planetary_stewardship_ai() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "planetary_stewardship.json", {})
    loops = payload.get("loops", []) if isinstance(payload, dict) else []
    stewarded = [item for item in loops if isinstance(item, dict) and bool(item.get("stewarded", False))]
    runaway = [item for item in loops if isinstance(item, dict) and bool(item.get("runaway", False))]
    return _overview("RECURSIVE PLANETARY STEWARDSHIP AI - PHASE 987", "planetary-stewardship overview", [f"Loops tracked: {len(loops)}", f"Stewarded loops: {len(stewarded)}", f"Runaway loops: {len(runaway)}"], "Guardrail: recursive stewardship should preserve braking mechanisms, ecological humility, and public oversight before automation.")


def infinite_collaborative_reasoning_substrate() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "collaborative_reasoning_substrate.json", {})
    substrates = payload.get("substrates", []) if isinstance(payload, dict) else []
    collaborative = [item for item in substrates if isinstance(item, dict) and bool(item.get("collaborative", False))]
    fractured = [item for item in substrates if isinstance(item, dict) and bool(item.get("fractured", False))]
    return _overview("INFINITE COLLABORATIVE REASONING SUBSTRATE - PHASE 988", "collaborative-reasoning-substrate overview", [f"Substrates tracked: {len(substrates)}", f"Collaborative substrates: {len(collaborative)}", f"Fractured substrates: {len(fractured)}"], "Guardrail: collaborative reasoning substrates should preserve attribution, role clarity, and controllability before scaling.")


def human_ai_co_evolution_framework() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "co_evolution_framework.json", {})
    pathways = payload.get("pathways", []) if isinstance(payload, dict) else []
    coevolved = [item for item in pathways if isinstance(item, dict) and bool(item.get("coevolved", False))]
    imbalanced = [item for item in pathways if isinstance(item, dict) and bool(item.get("imbalanced", False))]
    return _overview("HUMAN-AI CO-EVOLUTION FRAMEWORK - PHASE 989", "co-evolution-framework overview", [f"Pathways tracked: {len(pathways)}", f"Co-evolved pathways: {len(coevolved)}", f"Imbalanced pathways: {len(imbalanced)}"], "Guardrail: co-evolution frameworks should preserve human dignity, agency, and equitable benefit before optimization.")


def autonomous_universal_systems_governance() -> str:
    payload = _safe_json(OMEGA_GOV_DIR / "universal_systems_governance.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    governed = [item for item in systems if isinstance(item, dict) and bool(item.get("governed", False))]
    overloaded = [item for item in systems if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("AUTONOMOUS UNIVERSAL SYSTEMS GOVERNANCE - PHASE 990", "universal-systems-governance overview", [f"Systems tracked: {len(systems)}", f"Governed systems: {len(governed)}", f"Overloaded systems: {len(overloaded)}"], "Guardrail: systems governance should preserve accountability, transparency, and human override before autonomy.")

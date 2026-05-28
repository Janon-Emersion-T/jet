from __future__ import annotations

import json
from pathlib import Path


POLICY_SYSTEMS_DIR = Path("storage/policy_systems")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def universal_civic_education_engine() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "civic_education.json", {})
    curricula = payload.get("curricula", []) if isinstance(payload, dict) else []
    adaptive = [item for item in curricula if isinstance(item, dict) and bool(item.get("adaptive", False))]
    gaps = [item for item in curricula if isinstance(item, dict) and bool(item.get("gaps", False))]
    return _overview("UNIVERSAL CIVIC EDUCATION ENGINE - PHASE 911", "civic-education overview", [f"Curricula tracked: {len(curricula)}", f"Adaptive curricula: {len(adaptive)}", f"Gap-marked curricula: {len(gaps)}"], "Guardrail: civic education should preserve pluralism, factual grounding, and public accountability before personalization.")


def hyper_personalized_public_policy_simulator() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "public_policy_simulator.json", {})
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    simulated = [item for item in policies if isinstance(item, dict) and bool(item.get("simulated", False))]
    inequitable = [item for item in policies if isinstance(item, dict) and bool(item.get("inequitable", False))]
    return _overview("HYPER-PERSONALIZED PUBLIC POLICY SIMULATOR - PHASE 912", "public-policy-simulator overview", [f"Policies tracked: {len(policies)}", f"Simulated policies: {len(simulated)}", f"Inequitable policies: {len(inequitable)}"], "Guardrail: policy simulation should preserve privacy, fairness, and democratic legitimacy before recommendation.")


def ai_guided_social_equity_framework() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "social_equity.json", {})
    districts = payload.get("districts", []) if isinstance(payload, dict) else []
    supported = [item for item in districts if isinstance(item, dict) and bool(item.get("supported", False))]
    underserved = [item for item in districts if isinstance(item, dict) and bool(item.get("underserved", False))]
    return _overview("AI-GUIDED SOCIAL EQUITY FRAMEWORK - PHASE 913", "social-equity overview", [f"Districts tracked: {len(districts)}", f"Supported districts: {len(supported)}", f"Underserved districts: {len(underserved)}"], "Guardrail: social equity frameworks should preserve fairness, anti-discrimination review, and human accountability before allocation.")


def planetary_scale_coordination_dashboard() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "coordination_dashboard.json", {})
    streams = payload.get("streams", []) if isinstance(payload, dict) else []
    visible = [item for item in streams if isinstance(item, dict) and bool(item.get("visible", False))]
    blocked = [item for item in streams if isinstance(item, dict) and bool(item.get("blocked", False))]
    return _overview("PLANETARY-SCALE COORDINATION DASHBOARD - PHASE 914", "coordination-dashboard overview", [f"Streams tracked: {len(streams)}", f"Visible streams: {len(visible)}", f"Blocked streams: {len(blocked)}"], "Guardrail: large-scale dashboards should preserve transparency, scope limits, and local interpretation before coordination.")


def multi_civilization_diplomacy_simulator() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "diplomacy_simulator.json", {})
    dialogues = payload.get("dialogues", []) if isinstance(payload, dict) else []
    simulated = [item for item in dialogues if isinstance(item, dict) and bool(item.get("simulated", False))]
    tense = [item for item in dialogues if isinstance(item, dict) and bool(item.get("tense", False))]
    return _overview("MULTI-CIVILIZATION DIPLOMACY SIMULATOR - PHASE 915", "diplomacy-simulator overview", [f"Dialogues tracked: {len(dialogues)}", f"Simulated dialogues: {len(simulated)}", f"Tense dialogues: {len(tense)}"], "Guardrail: diplomacy simulations should preserve non-escalation and avoid overclaiming predictive certainty before use.")


def autonomous_galactic_logistics_research() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "galactic_logistics.json", {})
    routes = payload.get("routes", []) if isinstance(payload, dict) else []
    modeled = [item for item in routes if isinstance(item, dict) and bool(item.get("modeled", False))]
    infeasible = [item for item in routes if isinstance(item, dict) and bool(item.get("infeasible", False))]
    return _overview("AUTONOMOUS GALACTIC LOGISTICS RESEARCH - PHASE 916", "galactic-logistics overview", [f"Routes tracked: {len(routes)}", f"Modeled routes: {len(modeled)}", f"Infeasible routes: {len(infeasible)}"], "Guardrail: galactic logistics should remain research-oriented, uncertainty-aware, and non-operational without human review.")


def long_duration_societal_stability_engine() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "societal_stability.json", {})
    societies = payload.get("societies", []) if isinstance(payload, dict) else []
    stable = [item for item in societies if isinstance(item, dict) and bool(item.get("stable", False))]
    brittle = [item for item in societies if isinstance(item, dict) and bool(item.get("brittle", False))]
    return _overview("LONG-DURATION SOCIETAL STABILITY ENGINE - PHASE 917", "societal-stability overview", [f"Societies tracked: {len(societies)}", f"Stable societies: {len(stable)}", f"Brittle societies: {len(brittle)}"], "Guardrail: stability modeling should preserve rights, pluralism, and caution against optimizing for stasis over justice.")


def ai_guided_ethical_expansion_framework() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "ethical_expansion.json", {})
    expansions = payload.get("expansions", []) if isinstance(payload, dict) else []
    reviewed = [item for item in expansions if isinstance(item, dict) and bool(item.get("reviewed", False))]
    risky = [item for item in expansions if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("AI-GUIDED ETHICAL EXPANSION FRAMEWORK - PHASE 918", "ethical-expansion overview", [f"Expansions tracked: {len(expansions)}", f"Reviewed expansions: {len(reviewed)}", f"High-risk expansions: {len(risky)}"], "Guardrail: expansion frameworks should preserve ethics, consent, and public legitimacy before recommendation.")


def interdisciplinary_discovery_synthesizer() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "discovery_synthesizer.json", {})
    syntheses = payload.get("syntheses", []) if isinstance(payload, dict) else []
    linked = [item for item in syntheses if isinstance(item, dict) and bool(item.get("linked", False))]
    weak = [item for item in syntheses if isinstance(item, dict) and bool(item.get("weak", False))]
    return _overview("INTERDISCIPLINARY DISCOVERY SYNTHESIZER - PHASE 919", "discovery-synthesizer overview", [f"Syntheses tracked: {len(syntheses)}", f"Linked syntheses: {len(linked)}", f"Weak syntheses: {len(weak)}"], "Guardrail: interdisciplinary synthesis should preserve source fidelity and uncertainty before drawing conclusions.")


def universal_systems_thinking_engine() -> str:
    payload = _safe_json(POLICY_SYSTEMS_DIR / "systems_thinking.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    modeled = [item for item in systems if isinstance(item, dict) and bool(item.get("modeled", False))]
    entangled = [item for item in systems if isinstance(item, dict) and bool(item.get("entangled", False))]
    return _overview("UNIVERSAL SYSTEMS THINKING ENGINE - PHASE 920", "systems-thinking overview", [f"Systems tracked: {len(systems)}", f"Modeled systems: {len(modeled)}", f"Entangled systems: {len(entangled)}"], "Guardrail: systems thinking should preserve causal humility and avoid hiding value judgments inside structural models.")

from __future__ import annotations

import json
from pathlib import Path


FLOURISHING_DIR = Path("storage/flourishing_prosperity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def human_flourishing_optimization_engine() -> str:
    payload = _safe_json(FLOURISHING_DIR / "human_flourishing.json", {})
    domains = payload.get("domains", []) if isinstance(payload, dict) else []
    improved = [item for item in domains if isinstance(item, dict) and bool(item.get("improved", False))]
    fragile = [item for item in domains if isinstance(item, dict) and bool(item.get("fragile", False))]
    return _overview("HUMAN FLOURISHING OPTIMIZATION ENGINE - PHASE 881", "human-flourishing overview", [f"Domains tracked: {len(domains)}", f"Improved domains: {len(improved)}", f"Fragile domains: {len(fragile)}"], "Guardrail: flourishing optimization should preserve autonomy, plural values, and non-coercive guidance before recommendations.")


def universal_well_being_ai() -> str:
    payload = _safe_json(FLOURISHING_DIR / "universal_well_being.json", {})
    populations = payload.get("populations", []) if isinstance(payload, dict) else []
    supported = [item for item in populations if isinstance(item, dict) and bool(item.get("supported", False))]
    underserved = [item for item in populations if isinstance(item, dict) and bool(item.get("underserved", False))]
    return _overview("UNIVERSAL WELL-BEING AI - PHASE 882", "universal-well-being overview", [f"Populations tracked: {len(populations)}", f"Supported populations: {len(supported)}", f"Underserved populations: {len(underserved)}"], "Guardrail: well-being systems should preserve dignity, consent, and equitable treatment before optimization.")


def ai_assisted_spiritual_exploration() -> str:
    payload = _safe_json(FLOURISHING_DIR / "spiritual_exploration.json", {})
    journeys = payload.get("journeys", []) if isinstance(payload, dict) else []
    reflective = [item for item in journeys if isinstance(item, dict) and bool(item.get("reflective", False))]
    sensitive = [item for item in journeys if isinstance(item, dict) and bool(item.get("sensitive", False))]
    return _overview("AI-ASSISTED SPIRITUAL EXPLORATION - PHASE 883", "spiritual-exploration overview", [f"Journeys tracked: {len(journeys)}", f"Reflective journeys: {len(reflective)}", f"Sensitive journeys: {len(sensitive)}"], "Guardrail: spiritual exploration should preserve tradition, consent, and explicit non-authoritative framing before guidance.")


def cross_cultural_harmony_framework() -> str:
    payload = _safe_json(FLOURISHING_DIR / "cultural_harmony.json", {})
    exchanges = payload.get("exchanges", []) if isinstance(payload, dict) else []
    bridged = [item for item in exchanges if isinstance(item, dict) and bool(item.get("bridged", False))]
    tense = [item for item in exchanges if isinstance(item, dict) and bool(item.get("tense", False))]
    return _overview("CROSS-CULTURAL HARMONY FRAMEWORK - PHASE 884", "cultural-harmony overview", [f"Exchanges tracked: {len(exchanges)}", f"Bridged exchanges: {len(bridged)}", f"Tense exchanges: {len(tense)}"], "Guardrail: harmony frameworks should preserve cultural autonomy and avoid flattening meaningful difference.")


def autonomous_peace_negotiation_ai() -> str:
    payload = _safe_json(FLOURISHING_DIR / "peace_negotiation.json", {})
    dialogues = payload.get("dialogues", []) if isinstance(payload, dict) else []
    mediated = [item for item in dialogues if isinstance(item, dict) and bool(item.get("mediated", False))]
    stalled = [item for item in dialogues if isinstance(item, dict) and bool(item.get("stalled", False))]
    return _overview("AUTONOMOUS PEACE NEGOTIATION AI - PHASE 885", "peace-negotiation overview", [f"Dialogues tracked: {len(dialogues)}", f"Mediated dialogues: {len(mediated)}", f"Stalled dialogues: {len(stalled)}"], "Guardrail: peace negotiation support should preserve human accountability, non-escalation, and legitimacy before use.")


def conflict_prevention_intelligence() -> str:
    payload = _safe_json(FLOURISHING_DIR / "conflict_prevention.json", {})
    signals = payload.get("signals", []) if isinstance(payload, dict) else []
    prevented = [item for item in signals if isinstance(item, dict) and bool(item.get("prevented", False))]
    volatile = [item for item in signals if isinstance(item, dict) and item.get("risk") == "volatile"]
    return _overview("CONFLICT PREVENTION INTELLIGENCE - PHASE 886", "conflict-prevention overview", [f"Signals tracked: {len(signals)}", f"Prevented signals: {len(prevented)}", f"Volatile signals: {len(volatile)}"], "Guardrail: conflict prevention should preserve due process, evidence quality, and human review before intervention.")


def ai_assisted_ecological_restoration() -> str:
    payload = _safe_json(FLOURISHING_DIR / "ecological_restoration.json", {})
    sites = payload.get("sites", []) if isinstance(payload, dict) else []
    restored = [item for item in sites if isinstance(item, dict) and bool(item.get("restored", False))]
    degraded = [item for item in sites if isinstance(item, dict) and bool(item.get("degraded", False))]
    return _overview("AI-ASSISTED ECOLOGICAL RESTORATION - PHASE 887", "ecological-restoration overview", [f"Sites tracked: {len(sites)}", f"Restored sites: {len(restored)}", f"Degraded sites: {len(degraded)}"], "Guardrail: restoration planning should preserve local ecology, community stewardship, and long-term verification before execution.")


def universal_prosperity_simulation() -> str:
    payload = _safe_json(FLOURISHING_DIR / "prosperity_simulation.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    prosperous = [item for item in models if isinstance(item, dict) and bool(item.get("prosperous", False))]
    unequal = [item for item in models if isinstance(item, dict) and bool(item.get("unequal", False))]
    return _overview("UNIVERSAL PROSPERITY SIMULATION - PHASE 888", "prosperity-simulation overview", [f"Models tracked: {len(models)}", f"Prosperous models: {len(prosperous)}", f"Unequal models: {len(unequal)}"], "Guardrail: prosperity simulations should preserve equity, realism, and visibility into tradeoffs before policy use.")


def autonomous_post_scarcity_modeling() -> str:
    payload = _safe_json(FLOURISHING_DIR / "post_scarcity_modeling.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    abundant = [item for item in scenarios if isinstance(item, dict) and bool(item.get("abundant", False))]
    constrained = [item for item in scenarios if isinstance(item, dict) and bool(item.get("constrained", False))]
    return _overview("AUTONOMOUS POST-SCARCITY MODELING - PHASE 889", "post-scarcity-modeling overview", [f"Scenarios tracked: {len(scenarios)}", f"Abundant scenarios: {len(abundant)}", f"Constrained scenarios: {len(constrained)}"], "Guardrail: post-scarcity models should remain transparent about physical, political, and ethical constraints before advocacy.")


def ai_stewardship_framework() -> str:
    payload = _safe_json(FLOURISHING_DIR / "stewardship_framework.json", {})
    stewards = payload.get("stewards", []) if isinstance(payload, dict) else []
    accountable = [item for item in stewards if isinstance(item, dict) and bool(item.get("accountable", False))]
    overloaded = [item for item in stewards if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("AI STEWARDSHIP FRAMEWORK - PHASE 890", "stewardship-framework overview", [f"Stewards tracked: {len(stewards)}", f"Accountable stewards: {len(accountable)}", f"Overloaded stewards: {len(overloaded)}"], "Guardrail: stewardship frameworks should preserve clear responsibility, reversibility, and human accountability before delegation.")

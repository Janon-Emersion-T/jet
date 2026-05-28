from __future__ import annotations

import json
from pathlib import Path


INTERSTELLAR_SEMANTICS_DIR = Path("storage/interstellar_semantics")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(INTERSTELLAR_SEMANTICS_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_exoplanetary_simulation_ai() -> str:
    return _render("UNIVERSAL EXOPLANETARY SIMULATION AI - PHASE 1171", "exoplanetary-simulation overview", "exoplanetary_simulation.json", "simulations", "simulated", "uncertain", "Simulations tracked", "Simulated worlds", "Uncertain worlds", "Guardrail: exoplanetary simulation should preserve model humility, transparency, and non-claim framing before inference.")


def adaptive_stellar_navigation_substrate() -> str:
    return _render("ADAPTIVE STELLAR NAVIGATION SUBSTRATE - PHASE 1172", "stellar-navigation overview", "stellar_navigation.json", "courses", "navigated", "drifting", "Courses tracked", "Navigated courses", "Drifting courses", "Guardrail: stellar navigation should preserve safety margins, fallback routes, and accountable override before dispatch.")


def autonomous_cosmic_logistics_engine() -> str:
    return _render("AUTONOMOUS COSMIC LOGISTICS ENGINE - PHASE 1173", "cosmic-logistics overview", "cosmic_logistics.json", "shipments", "routed", "delayed", "Shipments tracked", "Routed shipments", "Delayed shipments", "Guardrail: cosmic logistics should preserve safety, traceability, and resilient contingencies before coordination.")


def infinite_scale_interstellar_coordination_ai() -> str:
    return _render("INFINITE-SCALE INTERSTELLAR COORDINATION AI - PHASE 1174", "interstellar-coordination overview", "interstellar_coordination.json", "coalitions", "coordinated", "fragmented", "Coalitions tracked", "Coordinated coalitions", "Fragmented coalitions", "Guardrail: interstellar coordination should preserve legitimacy, clarity of roles, and non-coercion before orchestration.")


def recursive_galactic_diplomacy_framework() -> str:
    return _render("RECURSIVE GALACTIC DIPLOMACY FRAMEWORK - PHASE 1175", "galactic-diplomacy overview", "galactic_diplomacy.json", "dialogues", "mediated", "escalating", "Dialogues tracked", "Mediated dialogues", "Escalating dialogues", "Guardrail: galactic diplomacy should preserve non-escalation, reciprocity, and transparent uncertainty before recommendation.")


def universal_extraterrestrial_communication_simulator() -> str:
    return _render("UNIVERSAL EXTRATERRESTRIAL COMMUNICATION SIMULATOR - PHASE 1176", "extraterrestrial-communication overview", "extraterrestrial_communication.json", "signals", "interpreted", "garbled", "Signals tracked", "Interpreted signals", "Garbled signals", "Guardrail: extraterrestrial communication simulation should preserve caution, epistemic humility, and review before claims.")


def adaptive_alien_cognition_interpretation_engine() -> str:
    return _render("ADAPTIVE ALIEN COGNITION INTERPRETATION ENGINE - PHASE 1177", "alien-cognition overview", "alien_cognition.json", "models", "interpreted", "anthropomorphic", "Models tracked", "Interpreted models", "Anthropomorphic models", "Guardrail: alien cognition interpretation should preserve anti-projection safeguards, humility, and explicit uncertainty before inference.")


def autonomous_universal_semantics_layer() -> str:
    return _render("AUTONOMOUS UNIVERSAL SEMANTICS LAYER - PHASE 1178", "universal-semantics overview", "universal_semantics.json", "semantic_maps", "aligned", "ambiguous", "Semantic maps tracked", "Aligned semantic maps", "Ambiguous semantic maps", "Guardrail: universal semantics should preserve nuance, dissent, and provenance before harmonization.")


def infinite_scale_symbolic_translation_ai() -> str:
    return _render("INFINITE-SCALE SYMBOLIC TRANSLATION AI - PHASE 1179", "symbolic-translation overview", "symbolic_translation.json", "translations", "translated", "lossy", "Translations tracked", "Translated symbols", "Lossy symbols", "Guardrail: symbolic translation should preserve context, reversibility, and uncertainty disclosure before use.")


def recursive_meaning_harmonization_framework() -> str:
    return _render("RECURSIVE MEANING HARMONIZATION FRAMEWORK - PHASE 1180", "meaning-harmonization overview", "meaning_harmonization.json", "meanings", "harmonized", "conflicted", "Meanings tracked", "Harmonized meanings", "Conflicted meanings", "Guardrail: meaning harmonization should preserve plurality, explicit disagreement, and human interpretation before convergence.")

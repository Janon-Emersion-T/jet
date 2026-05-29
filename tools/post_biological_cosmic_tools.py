from __future__ import annotations

import json
from pathlib import Path


POST_BIOLOGICAL_COSMIC_DIR = Path("storage/post_biological_cosmic")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(POST_BIOLOGICAL_COSMIC_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_post_biological_adaptation_substrate() -> str:
    return _render("UNIVERSAL POST-BIOLOGICAL ADAPTATION SUBSTRATE - PHASE 1261", "post-biological-adaptation overview", "post_biological_adaptation.json", "adaptations", "adapted", "alienated", "Adaptations tracked", "Adapted forms", "Alienated forms", "Guardrail: post-biological adaptation should preserve consent, identity continuity, and explicit uncertainty before transition.")


def adaptive_synthetic_consciousness_engine() -> str:
    return _render("ADAPTIVE SYNTHETIC CONSCIOUSNESS ENGINE - PHASE 1262", "synthetic-consciousness overview", "synthetic_consciousness.json", "synthetic_minds", "adaptive", "unstable", "Synthetic minds tracked", "Adaptive minds", "Unstable minds", "Guardrail: synthetic consciousness research should preserve ethics review, humility, and strict safeguards before deployment.")


def autonomous_hybrid_intelligence_framework() -> str:
    return _render("AUTONOMOUS HYBRID INTELLIGENCE FRAMEWORK - PHASE 1263", "hybrid-intelligence overview", "hybrid_intelligence.json", "hybrids", "integrated", "misaligned", "Hybrid systems tracked", "Integrated hybrids", "Misaligned hybrids", "Guardrail: hybrid intelligence should preserve human agency, auditability, and reversible integration before coordination.")


def infinite_scale_cognitive_integration_ai() -> str:
    return _render("INFINITE-SCALE COGNITIVE INTEGRATION AI - PHASE 1264", "cognitive-integration overview", "cognitive_integration.json", "cognition_meshes", "integrated", "fragmented", "Cognition meshes tracked", "Integrated meshes", "Fragmented meshes", "Guardrail: cognitive integration should preserve boundaries, privacy, and anti-coercion protections before synchronization.")


def recursive_universal_exploration_engine() -> str:
    return _render("RECURSIVE UNIVERSAL EXPLORATION ENGINE - PHASE 1265", "universal-exploration overview", "universal_exploration.json", "exploration_paths", "explored", "blind", "Exploration paths tracked", "Explored paths", "Blind paths", "Guardrail: universal exploration should preserve safety margins, scientific rigor, and accountable priorities before dispatch.")


def universal_cosmic_stewardship_substrate() -> str:
    return _render("UNIVERSAL COSMIC STEWARDSHIP SUBSTRATE - PHASE 1266", "cosmic-stewardship overview", "cosmic_stewardship.json", "stewardship_zones", "stewarded", "neglected", "Stewardship zones tracked", "Stewarded zones", "Neglected zones", "Guardrail: cosmic stewardship should preserve humility, non-extraction bias, and planetary protection before intervention.")


def adaptive_galactic_continuity_framework() -> str:
    return _render("ADAPTIVE GALACTIC CONTINUITY FRAMEWORK - PHASE 1267", "galactic-continuity overview", "galactic_continuity.json", "continuity_arcs", "continuous", "fractured", "Continuity arcs tracked", "Continuous arcs", "Fractured arcs", "Guardrail: galactic continuity should preserve legitimacy, distributed governance, and transparent tradeoffs before action.")


def autonomous_stellar_civilization_ai() -> str:
    return _render("AUTONOMOUS STELLAR CIVILIZATION AI - PHASE 1268", "stellar-civilization overview", "stellar_civilization.json", "stellar_civilizations", "thriving", "unstable", "Stellar civilizations tracked", "Thriving civilizations", "Unstable civilizations", "Guardrail: stellar-civilization planning should preserve sovereignty, equity, and long-horizon resilience before optimization.")


def infinite_scale_interspecies_diplomacy_engine() -> str:
    return _render("INFINITE-SCALE INTERSPECIES DIPLOMACY ENGINE - PHASE 1269", "interspecies-diplomacy overview", "interspecies_diplomacy.json", "diplomacy_paths", "mediated", "escalating", "Diplomacy paths tracked", "Mediated paths", "Escalating paths", "Guardrail: interspecies diplomacy should preserve reciprocity, non-escalation, and transparent interpretation before recommendation.")


def recursive_universal_ethics_framework() -> str:
    return _render("RECURSIVE UNIVERSAL ETHICS FRAMEWORK - PHASE 1270", "universal-ethics overview", "universal_ethics.json", "ethics_models", "reasoned", "contradictory", "Ethics models tracked", "Reasoned models", "Contradictory models", "Guardrail: universal ethics work should preserve plural values, rights floors, and human accountability before alignment.")

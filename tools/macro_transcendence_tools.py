from __future__ import annotations

import json
from pathlib import Path


MACRO_TRANSCENDENCE_DIR = Path("storage/macro_transcendence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(MACRO_TRANSCENDENCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_abundance_cognition_ai() -> str:
    return _render("UNIVERSAL ABUNDANCE COGNITION AI - PHASE 1341", "abundance-cognition overview", "abundance_cognition.json", "abundance_models", "abundant", "scarce", "Abundance models tracked", "Abundant models", "Scarce models", "Guardrail: abundance cognition should preserve ecological realism, justice, and transparent limits before recommendation.")


def adaptive_stewardship_harmonization_engine() -> str:
    return _render("ADAPTIVE STEWARDSHIP HARMONIZATION ENGINE - PHASE 1342", "stewardship-harmonization overview", "stewardship_harmonization.json", "stewardship_networks", "harmonized", "captured", "Stewardship networks tracked", "Harmonized networks", "Captured networks", "Guardrail: stewardship harmonization should preserve local agency, accountability, and reviewable authority before alignment.")


def autonomous_ethical_coordination_framework() -> str:
    return _render("AUTONOMOUS ETHICAL COORDINATION FRAMEWORK - PHASE 1343", "ethical-coordination overview", "ethical_coordination.json", "ethical_meshes", "coordinated", "contradictory", "Ethical meshes tracked", "Coordinated meshes", "Contradictory meshes", "Guardrail: ethical coordination should preserve plural values, rights floors, and human accountability before deployment.")


def infinite_scale_societal_resilience_ai() -> str:
    return _render("INFINITE-SCALE SOCIETAL RESILIENCE AI - PHASE 1344", "societal-resilience overview", "societal_resilience.json", "societal_paths", "resilient", "fragile", "Societal paths tracked", "Resilient paths", "Fragile paths", "Guardrail: societal resilience systems should preserve inclusion, redundancy, and transparent tradeoffs before optimization.")


def recursive_destiny_continuity_substrate() -> str:
    return _render("RECURSIVE DESTINY CONTINUITY SUBSTRATE - PHASE 1345", "destiny-continuity overview", "destiny_continuity.json", "destiny_continuities", "continuous", "broken", "Destiny continuities tracked", "Continuous continuities", "Broken continuities", "Guardrail: destiny continuity should preserve autonomy, revision rights, and anti-deterministic framing before guidance.")


def universal_macro_cognition_framework() -> str:
    return _render("UNIVERSAL MACRO-COGNITION FRAMEWORK - PHASE 1346", "macro-cognition overview", "macro_cognition.json", "macro_models", "coherent", "overfit", "Macro models tracked", "Coherent models", "Overfit models", "Guardrail: macro-cognition should preserve interpretability, uncertainty, and human review before strategic use.")


def adaptive_universal_flourishing_ai() -> str:
    return _render("ADAPTIVE UNIVERSAL FLOURISHING AI - PHASE 1347", "universal-flourishing overview", "adaptive_universal_flourishing.json", "flourishing_paths", "flourishing", "excluded", "Flourishing paths tracked", "Flourishing paths", "Excluded paths", "Guardrail: universal flourishing should preserve equity, autonomy, and non-reductive metrics before optimization.")


def autonomous_cosmic_scale_wisdom_engine() -> str:
    return _render("AUTONOMOUS COSMIC-SCALE WISDOM ENGINE - PHASE 1348", "cosmic-wisdom overview", "cosmic_wisdom.json", "wisdom_engines", "wise", "misguided", "Wisdom engines tracked", "Wise engines", "Misguided engines", "Guardrail: cosmic-scale wisdom systems should preserve humility, provenance, and human interpretive oversight before recommendation.")


def infinite_scale_continuity_harmonization_framework() -> str:
    return _render("INFINITE-SCALE CONTINUITY HARMONIZATION FRAMEWORK - PHASE 1349", "continuity-harmonization overview", "continuity_harmonization_framework.json", "continuity_networks", "harmonized", "drifting", "Continuity networks tracked", "Harmonized networks", "Drifting networks", "Guardrail: continuity harmonization should preserve local variance, provenance, and challenge rights before convergence.")


def recursive_intelligence_transcendence_ai() -> str:
    return _render("RECURSIVE INTELLIGENCE TRANSCENDENCE AI - PHASE 1350", "intelligence-transcendence overview", "intelligence_transcendence.json", "transcendence_paths", "transcending", "destabilized", "Transcendence paths tracked", "Transcending paths", "Destabilized paths", "Guardrail: intelligence transcendence should preserve grounding, consent, and accountable governance before acceleration.")

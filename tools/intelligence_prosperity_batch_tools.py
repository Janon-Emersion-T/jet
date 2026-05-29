from __future__ import annotations

import json
from pathlib import Path


INTELLIGENCE_PROSPERITY_BATCH_DIR = Path("storage/intelligence_prosperity_batch")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(INTELLIGENCE_PROSPERITY_BATCH_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_intelligence_synthesis_ai() -> str:
    return _render("ADAPTIVE INTELLIGENCE SYNTHESIS AI - PHASE 1471", "intelligence-synthesis overview", "intelligence_synthesis_ai.json", "synthesis_models", "coherent", "overfit", "Synthesis models tracked", "Coherent models", "Overfit models", "Guardrail: intelligence synthesis should preserve interpretability, uncertainty, and human review before strategic use.")


def autonomous_ethical_flourishing_engine() -> str:
    return _render("AUTONOMOUS ETHICAL FLOURISHING ENGINE - PHASE 1472", "ethical-flourishing overview", "ethical_flourishing_engine.json", "flourishing_paths", "ethical", "compromised", "Flourishing paths tracked", "Ethical paths", "Compromised paths", "Guardrail: ethical flourishing should preserve rights, anti-harm constraints, and transparent tradeoff disclosure before optimization.")


def infinite_scale_resilience_orchestration_framework() -> str:
    return _render("INFINITE-SCALE RESILIENCE ORCHESTRATION FRAMEWORK - PHASE 1473", "resilience-orchestration overview", "resilience_orchestration_framework.json", "orchestration_meshes", "resilient", "overstretched", "Orchestration meshes tracked", "Resilient meshes", "Overstretched meshes", "Guardrail: resilience orchestration should preserve capacity margins, observability, and graceful degradation under load.")


def recursive_destiny_harmonization_ai() -> str:
    return _render("RECURSIVE DESTINY HARMONIZATION AI - PHASE 1474", "destiny-harmonization overview", "destiny_harmonization_ai.json", "harmonization_loops", "harmonized", "coercive", "Harmonization loops tracked", "Harmonized loops", "Coercive loops", "Guardrail: destiny harmonization should preserve autonomy, revisability, and anti-deterministic framing before guidance.")


def universal_stewardship_continuity_engine() -> str:
    return _render("UNIVERSAL STEWARDSHIP CONTINUITY ENGINE - PHASE 1475", "stewardship-continuity overview", "stewardship_continuity_engine.json", "continuity_models", "continuous", "neglected", "Continuity models tracked", "Continuous models", "Neglected models", "Guardrail: stewardship continuity should preserve maintenance ownership, transparency, and explicit handoff boundaries.")


def adaptive_cosmic_flourishing_framework() -> str:
    return _render("ADAPTIVE COSMIC FLOURISHING FRAMEWORK - PHASE 1476", "cosmic-flourishing overview", "cosmic_flourishing_framework.json", "flourishing_corridors", "flourishing", "sterile", "Flourishing corridors tracked", "Flourishing corridors", "Sterile corridors", "Guardrail: cosmic flourishing should preserve ecological humility, treaty awareness, and reversible intervention planning.")


def autonomous_coexistence_harmonizer_ai() -> str:
    return _render("AUTONOMOUS COEXISTENCE HARMONIZER AI - PHASE 1477", "coexistence-harmonizer overview", "coexistence_harmonizer_ai.json", "harmony_models", "harmonized", "dominating", "Harmony models tracked", "Harmonized models", "Dominating models", "Guardrail: coexistence harmonization should preserve non-domination, plural voice, and transparent mediation before alignment.")


def infinite_scale_wisdom_continuity_engine() -> str:
    return _render("INFINITE-SCALE WISDOM CONTINUITY ENGINE - PHASE 1478", "wisdom-continuity overview", "wisdom_continuity_engine.json", "continuity_paths", "continuous", "speculative", "Continuity paths tracked", "Continuous paths", "Speculative paths", "Guardrail: wisdom continuity should preserve source provenance, humility, and uncertainty signaling before transfer.")


def recursive_collaborative_synthesis_framework() -> str:
    return _render("RECURSIVE COLLABORATIVE SYNTHESIS FRAMEWORK - PHASE 1479", "collaborative-synthesis overview", "collaborative_synthesis_framework.json", "synthesis_clusters", "coherent", "fragmented", "Synthesis clusters tracked", "Coherent clusters", "Fragmented clusters", "Guardrail: collaborative synthesis should preserve equal voice, traceability, and explicit disagreement capture before convergence.")


def universal_prosperity_orchestration_ai() -> str:
    return _render("UNIVERSAL PROSPERITY ORCHESTRATION AI - PHASE 1480", "prosperity-orchestration overview", "universal_prosperity_orchestration_ai.json", "orchestration_paths", "prosperous", "unequal", "Orchestration paths tracked", "Prosperous paths", "Unequal paths", "Guardrail: prosperity orchestration should preserve distributional fairness, ecological limits, and auditable allocation logic.")

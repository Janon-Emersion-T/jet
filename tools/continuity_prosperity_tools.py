from __future__ import annotations

import json
from pathlib import Path


CONTINUITY_PROSPERITY_DIR = Path("storage/continuity_prosperity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(CONTINUITY_PROSPERITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_destiny_harmonizer_ai() -> str:
    return _render("ADAPTIVE DESTINY HARMONIZER AI - PHASE 1441", "destiny-harmonizer overview", "adaptive_destiny_harmonizer.json", "destiny_paths", "harmonized", "coercive", "Destiny paths tracked", "Harmonized paths", "Coercive paths", "Guardrail: destiny harmonization should preserve autonomy, revisability, and anti-deterministic framing before guidance.")


def autonomous_universal_continuity_engine() -> str:
    return _render("AUTONOMOUS UNIVERSAL CONTINUITY ENGINE - PHASE 1442", "universal-continuity overview", "autonomous_universal_continuity.json", "continuity_routes", "continuous", "broken", "Continuity routes tracked", "Continuous routes", "Broken routes", "Guardrail: universal continuity should preserve fallback capacity, provenance, and accountable maintenance responsibilities.")


def infinite_scale_wisdom_synthesis_framework() -> str:
    return _render("INFINITE-SCALE WISDOM SYNTHESIS FRAMEWORK - PHASE 1443", "wisdom-synthesis overview", "wisdom_synthesis_framework.json", "wisdom_syntheses", "coherent", "overfit", "Wisdom syntheses tracked", "Coherent syntheses", "Overfit syntheses", "Guardrail: wisdom synthesis should preserve interpretability, evidence traceability, and humility about unknowns.")


def recursive_planetary_flourishing_ai() -> str:
    return _render("RECURSIVE PLANETARY FLOURISHING AI - PHASE 1444", "planetary-flourishing overview", "recursive_planetary_flourishing.json", "flourishing_loops", "flourishing", "degrading", "Flourishing loops tracked", "Flourishing loops", "Degrading loops", "Guardrail: planetary flourishing should preserve ecological thresholds, equity, and transparent long-horizon tradeoffs.")


def universal_collaborative_continuity_engine() -> str:
    return _render("UNIVERSAL COLLABORATIVE CONTINUITY ENGINE - PHASE 1445", "collaborative-continuity overview", "collaborative_continuity_engine.json", "continuity_meshes", "collaborative", "fragmented", "Continuity meshes tracked", "Collaborative meshes", "Fragmented meshes", "Guardrail: collaborative continuity should preserve shared accountability, local agency, and graceful recovery paths.")


def adaptive_stewardship_harmonization_framework() -> str:
    return _render("ADAPTIVE STEWARDSHIP HARMONIZATION FRAMEWORK - PHASE 1446", "stewardship-harmonization overview", "adaptive_stewardship_harmonization_framework.json", "harmonization_meshes", "harmonized", "captured", "Harmonization meshes tracked", "Harmonized meshes", "Captured meshes", "Guardrail: stewardship harmonization should preserve accountability, transparency, and anti-capture checks before alignment.")


def autonomous_prosperity_orchestration_ai() -> str:
    return _render("AUTONOMOUS PROSPERITY ORCHESTRATION AI - PHASE 1447", "prosperity-orchestration overview", "autonomous_prosperity_orchestration.json", "orchestration_paths", "prosperous", "extractive", "Orchestration paths tracked", "Prosperous paths", "Extractive paths", "Guardrail: prosperity orchestration should preserve justice, ecological realism, and auditable allocation logic.")


def infinite_scale_coexistence_synthesis_engine() -> str:
    return _render("INFINITE-SCALE COEXISTENCE SYNTHESIS ENGINE - PHASE 1448", "coexistence-synthesis overview", "infinite_scale_coexistence_synthesis.json", "synthesis_paths", "synthesized", "dominated", "Synthesis paths tracked", "Synthesized paths", "Dominated paths", "Guardrail: coexistence synthesis should preserve plural voices, rights floors, and non-coercive conflict resolution.")


def recursive_resilience_stewardship_framework() -> str:
    return _render("RECURSIVE RESILIENCE STEWARDSHIP FRAMEWORK - PHASE 1449", "resilience-stewardship overview", "recursive_resilience_stewardship.json", "stewardship_frameworks", "resilient", "neglected", "Stewardship frameworks tracked", "Resilient frameworks", "Neglected frameworks", "Guardrail: resilience stewardship should preserve maintenance capacity, explicit ownership, and observable recovery criteria.")


def universal_flourishing_continuity_ai() -> str:
    return _render("UNIVERSAL FLOURISHING CONTINUITY AI - PHASE 1450", "flourishing-continuity overview", "universal_flourishing_continuity_ai.json", "continuity_models", "flourishing", "eroding", "Continuity models tracked", "Flourishing models", "Eroding models", "Guardrail: flourishing continuity should preserve dignity, long-term care, and visible tradeoffs before optimization.")

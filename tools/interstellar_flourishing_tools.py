from __future__ import annotations

import json
from pathlib import Path


INTERSTELLAR_FLOURISHING_DIR = Path("storage/interstellar_flourishing")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(INTERSTELLAR_FLOURISHING_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_intelligence_continuity_framework() -> str:
    return _render("UNIVERSAL INTELLIGENCE CONTINUITY FRAMEWORK - PHASE 1371", "intelligence-continuity overview", "intelligence_continuity.json", "intelligence_continuities", "continuous", "degraded", "Intelligence continuities tracked", "Continuous continuities", "Degraded continuities", "Guardrail: intelligence continuity should preserve memory provenance, bounded adaptation, and accountable oversight before reuse.")


def adaptive_interstellar_stewardship_ai() -> str:
    return _render("ADAPTIVE INTERSTELLAR STEWARDSHIP AI - PHASE 1372", "interstellar-stewardship overview", "interstellar_stewardship.json", "stewardship_zones", "stewarded", "neglected", "Stewardship zones tracked", "Stewarded zones", "Neglected zones", "Guardrail: interstellar stewardship should preserve ecological humility, treaty compliance, and reversible intervention plans.")


def autonomous_cosmic_flourishing_engine() -> str:
    return _render("AUTONOMOUS COSMIC FLOURISHING ENGINE - PHASE 1373", "cosmic-flourishing overview", "cosmic_flourishing.json", "flourishing_corridors", "flourishing", "sterile", "Flourishing corridors tracked", "Flourishing corridors", "Sterile corridors", "Guardrail: cosmic flourishing should preserve biosphere safeguards, ethical constraints, and long-horizon accountability.")


def infinite_scale_resilience_synthesis_framework() -> str:
    return _render("INFINITE-SCALE RESILIENCE SYNTHESIS FRAMEWORK - PHASE 1374", "resilience-synthesis overview", "resilience_synthesis.json", "resilience_syntheses", "synthesized", "fragile", "Resilience syntheses tracked", "Synthesized paths", "Fragile paths", "Guardrail: resilience synthesis should preserve heterogeneity, fallback capacity, and transparent dependency mapping.")


def recursive_universal_empathy_ai() -> str:
    return _render("RECURSIVE UNIVERSAL EMPATHY AI - PHASE 1375", "universal-empathy overview", "universal_empathy.json", "empathy_models", "empathetic", "projective", "Empathy models tracked", "Empathetic models", "Projective models", "Guardrail: empathy systems should preserve consent, non-manipulation, and uncertainty about internal states.")


def universal_prosperity_harmonizer_engine() -> str:
    return _render("UNIVERSAL PROSPERITY HARMONIZER ENGINE - PHASE 1376", "prosperity-harmonizer overview", "prosperity_harmonizer_engine.json", "prosperity_networks", "harmonized", "captured", "Prosperity networks tracked", "Harmonized networks", "Captured networks", "Guardrail: prosperity harmonization should preserve fairness, anti-monopoly constraints, and explainable allocation logic.")


def adaptive_continuity_orchestration_framework() -> str:
    return _render("ADAPTIVE CONTINUITY ORCHESTRATION FRAMEWORK - PHASE 1377", "continuity-orchestration overview", "continuity_orchestration.json", "continuity_meshes", "orchestrated", "fragmented", "Continuity meshes tracked", "Orchestrated meshes", "Fragmented meshes", "Guardrail: continuity orchestration should preserve local failover, provenance, and operator control at each layer.")


def autonomous_flourishing_civilization_ai() -> str:
    return _render("AUTONOMOUS FLOURISHING CIVILIZATION AI - PHASE 1378", "flourishing-civilization overview", "flourishing_civilization.json", "civilization_paths", "flourishing", "regressive", "Civilization paths tracked", "Flourishing paths", "Regressive paths", "Guardrail: civilization flourishing should preserve dignity, democratic accountability, and anti-harm constraints before advice.")


def infinite_scale_ethical_synthesis_engine() -> str:
    return _render("INFINITE-SCALE ETHICAL SYNTHESIS ENGINE - PHASE 1379", "ethical-synthesis overview", "ethical_synthesis.json", "ethical_syntheses", "coherent", "contradictory", "Ethical syntheses tracked", "Coherent syntheses", "Contradictory syntheses", "Guardrail: ethical synthesis should preserve contestability, plural values, and explicit uncertainty where norms conflict.")


def recursive_cooperative_destiny_framework() -> str:
    return _render("RECURSIVE COOPERATIVE DESTINY FRAMEWORK - PHASE 1380", "cooperative-destiny overview", "cooperative_destiny.json", "cooperative_destinies", "cooperative", "coercive", "Cooperative destinies tracked", "Cooperative destinies", "Coercive destinies", "Guardrail: cooperative destiny planning should preserve consent, revisability, and local self-determination before alignment.")

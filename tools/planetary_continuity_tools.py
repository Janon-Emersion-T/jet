from __future__ import annotations

import json
from pathlib import Path


PLANETARY_CONTINUITY_DIR = Path("storage/planetary_continuity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(PLANETARY_CONTINUITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_wisdom_orchestration_framework() -> str:
    return _render("ADAPTIVE WISDOM ORCHESTRATION FRAMEWORK - PHASE 1431", "wisdom-orchestration overview", "adaptive_wisdom_orchestration.json", "wisdom_routes", "orchestrated", "speculative", "Wisdom routes tracked", "Orchestrated routes", "Speculative routes", "Guardrail: wisdom orchestration should preserve evidence traceability, humility, and transparent uncertainty handling.")


def autonomous_planetary_coexistence_ai() -> str:
    return _render("AUTONOMOUS PLANETARY COEXISTENCE AI - PHASE 1432", "planetary-coexistence overview", "planetary_coexistence.json", "coexistence_networks", "cooperative", "hostile", "Coexistence networks tracked", "Cooperative networks", "Hostile networks", "Guardrail: planetary coexistence should preserve rights floors, democratic legitimacy, and non-coercive coordination.")


def infinite_scale_flourishing_stewardship_engine() -> str:
    return _render("INFINITE-SCALE FLOURISHING STEWARDSHIP ENGINE - PHASE 1433", "flourishing-stewardship overview", "flourishing_stewardship.json", "stewardship_paths", "flourishing", "depleting", "Stewardship paths tracked", "Flourishing paths", "Depleting paths", "Guardrail: flourishing stewardship should preserve ecological realism, inclusion, and long-horizon care obligations.")


def recursive_cosmic_continuity_framework() -> str:
    return _render("RECURSIVE COSMIC CONTINUITY FRAMEWORK - PHASE 1434", "cosmic-continuity overview", "recursive_cosmic_continuity.json", "continuity_frameworks", "continuous", "disrupted", "Continuity frameworks tracked", "Continuous frameworks", "Disrupted frameworks", "Guardrail: cosmic continuity should preserve treaty awareness, fallback planning, and transparent resilience assumptions.")


def universal_prosperity_harmonization_ai() -> str:
    return _render("UNIVERSAL PROSPERITY HARMONIZATION AI - PHASE 1435", "prosperity-harmonization overview", "universal_prosperity_harmonization.json", "harmonization_paths", "harmonized", "captured", "Harmonization paths tracked", "Harmonized paths", "Captured paths", "Guardrail: prosperity harmonization should preserve fairness, anti-capture checks, and visible distributional tradeoffs.")


def adaptive_intelligence_flourishing_engine() -> str:
    return _render("ADAPTIVE INTELLIGENCE FLOURISHING ENGINE - PHASE 1436", "intelligence-flourishing overview", "adaptive_intelligence_flourishing.json", "flourishing_models", "flourishing", "misaligned", "Flourishing models tracked", "Flourishing models", "Misaligned models", "Guardrail: intelligence flourishing should preserve safety bounds, grounded evaluation, and accountability for outcomes.")


def autonomous_collaborative_stewardship_framework() -> str:
    return _render("AUTONOMOUS COLLABORATIVE STEWARDSHIP FRAMEWORK - PHASE 1437", "collaborative-stewardship overview", "collaborative_stewardship.json", "stewardship_meshes", "collaborative", "captured", "Stewardship meshes tracked", "Collaborative meshes", "Captured meshes", "Guardrail: collaborative stewardship should preserve shared governance, explicit responsibility, and anti-capture safeguards.")


def infinite_scale_resilience_continuity_ai() -> str:
    return _render("INFINITE-SCALE RESILIENCE CONTINUITY AI - PHASE 1438", "resilience-continuity overview", "infinite_scale_resilience_continuity.json", "continuity_models", "resilient", "brittle", "Continuity models tracked", "Resilient models", "Brittle models", "Guardrail: resilience continuity should preserve redundancy, observability, and graceful failure boundaries.")


def recursive_coexistence_orchestration_engine() -> str:
    return _render("RECURSIVE COEXISTENCE ORCHESTRATION ENGINE - PHASE 1439", "coexistence-orchestration overview", "recursive_coexistence_orchestration.json", "orchestration_meshes", "orchestrated", "polarized", "Orchestration meshes tracked", "Orchestrated meshes", "Polarized meshes", "Guardrail: coexistence orchestration should preserve rights, local voice, and transparent conflict handling.")


def universal_ethical_flourishing_framework() -> str:
    return _render("UNIVERSAL ETHICAL FLOURISHING FRAMEWORK - PHASE 1440", "ethical-flourishing overview", "universal_ethical_flourishing.json", "ethical_frameworks", "flourishing", "compromised", "Ethical frameworks tracked", "Flourishing frameworks", "Compromised frameworks", "Guardrail: ethical flourishing should preserve rights, anti-harm constraints, and visible normative assumptions.")

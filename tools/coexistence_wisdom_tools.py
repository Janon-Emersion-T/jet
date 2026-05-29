from __future__ import annotations

import json
from pathlib import Path


COEXISTENCE_WISDOM_DIR = Path("storage/coexistence_wisdom")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(COEXISTENCE_WISDOM_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_coexistence_continuity_framework() -> str:
    return _render("ADAPTIVE COEXISTENCE CONTINUITY FRAMEWORK - PHASE 1401", "coexistence-continuity overview", "coexistence_continuity.json", "coexistence_continuities", "continuous", "fractured", "Coexistence continuities tracked", "Continuous continuities", "Fractured continuities", "Guardrail: coexistence continuity should preserve local peacebuilding, rights protection, and transparent repair pathways.")


def autonomous_resilience_harmonization_ai() -> str:
    return _render("AUTONOMOUS RESILIENCE HARMONIZATION AI - PHASE 1402", "resilience-harmonization overview", "autonomous_resilience_harmonization.json", "resilience_meshes", "harmonized", "overcoupled", "Resilience meshes tracked", "Harmonized meshes", "Overcoupled meshes", "Guardrail: resilience harmonization should preserve independence between safeguards, observability, and staged rollback.")


def infinite_scale_prosperity_orchestration_engine() -> str:
    return _render("INFINITE-SCALE PROSPERITY ORCHESTRATION ENGINE - PHASE 1403", "prosperity-orchestration overview", "prosperity_orchestration.json", "prosperity_routes", "orchestrated", "extractive", "Prosperity routes tracked", "Orchestrated routes", "Extractive routes", "Guardrail: prosperity orchestration should preserve distributive justice, ecological realism, and auditability of gains.")


def recursive_stewardship_synthesis_framework() -> str:
    return _render("RECURSIVE STEWARDSHIP SYNTHESIS FRAMEWORK - PHASE 1404", "stewardship-synthesis overview", "stewardship_synthesis.json", "stewardship_syntheses", "coherent", "captured", "Stewardship syntheses tracked", "Coherent syntheses", "Captured syntheses", "Guardrail: stewardship synthesis should preserve accountability chains, local autonomy, and anti-capture review.")


def universal_flourishing_harmonizer_ai() -> str:
    return _render("UNIVERSAL FLOURISHING HARMONIZER AI - PHASE 1405", "flourishing-harmonizer overview", "flourishing_harmonizer.json", "flourishing_meshes", "harmonized", "excluded", "Flourishing meshes tracked", "Harmonized meshes", "Excluded meshes", "Guardrail: flourishing harmonization should preserve dignity, diversity, and clear visibility into tradeoffs.")


def adaptive_ethical_continuity_engine() -> str:
    return _render("ADAPTIVE ETHICAL CONTINUITY ENGINE - PHASE 1406", "ethical-continuity overview", "ethical_continuity.json", "ethical_continuities", "continuous", "broken", "Ethical continuities tracked", "Continuous continuities", "Broken continuities", "Guardrail: ethical continuity should preserve accountability, historical context, and rights-preserving red lines.")


def autonomous_collaborative_destiny_framework() -> str:
    return _render("AUTONOMOUS COLLABORATIVE DESTINY FRAMEWORK - PHASE 1407", "collaborative-destiny overview", "collaborative_destiny_framework.json", "destiny_meshes", "collaborative", "dominating", "Destiny meshes tracked", "Collaborative meshes", "Dominating meshes", "Guardrail: collaborative destiny should preserve consent, negotiability, and asymmetry checks before coordination.")


def infinite_scale_wisdom_orchestration_ai() -> str:
    return _render("INFINITE-SCALE WISDOM ORCHESTRATION AI - PHASE 1408", "wisdom-orchestration overview", "wisdom_orchestration.json", "wisdom_orchestrations", "grounded", "speculative", "Wisdom orchestrations tracked", "Grounded orchestrations", "Speculative orchestrations", "Guardrail: wisdom orchestration should preserve source traceability, humility, and uncertainty signaling.")


def recursive_cosmic_flourishing_engine() -> str:
    return _render("RECURSIVE COSMIC FLOURISHING ENGINE - PHASE 1409", "cosmic-flourishing overview", "recursive_cosmic_flourishing.json", "cosmic_paths", "flourishing", "sterile", "Cosmic paths tracked", "Flourishing paths", "Sterile paths", "Guardrail: cosmic flourishing should preserve ecological safeguards, treaty awareness, and slow-to-irreversible deployment.")


def universal_coexistence_synthesis_framework() -> str:
    return _render("UNIVERSAL COEXISTENCE SYNTHESIS FRAMEWORK - PHASE 1410", "coexistence-synthesis overview", "coexistence_synthesis.json", "coexistence_syntheses", "synthesized", "polarized", "Coexistence syntheses tracked", "Synthesized paths", "Polarized paths", "Guardrail: coexistence synthesis should preserve plural norms, non-domination, and transparent mediation logic.")

from __future__ import annotations

import json
from pathlib import Path


RESILIENCE_CONTINUITY_DIR = Path("storage/resilience_continuity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RESILIENCE_CONTINUITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_resilience_harmonization_framework() -> str:
    return _render("UNIVERSAL RESILIENCE HARMONIZATION FRAMEWORK - PHASE 1361", "resilience-harmonization overview", "resilience_harmonization.json", "resilience_networks", "harmonized", "brittle", "Resilience networks tracked", "Harmonized networks", "Brittle networks", "Guardrail: resilience harmonization should preserve redundancy, transparency, and local repair autonomy before rollout.")


def adaptive_prosperity_stewardship_ai() -> str:
    return _render("ADAPTIVE PROSPERITY STEWARDSHIP AI - PHASE 1362", "prosperity-stewardship overview", "prosperity_stewardship.json", "prosperity_paths", "stewarded", "captured", "Prosperity paths tracked", "Stewarded paths", "Captured paths", "Guardrail: prosperity stewardship should preserve fairness, anti-capture controls, and accountable resource governance.")


def autonomous_universal_coordination_engine() -> str:
    return _render("AUTONOMOUS UNIVERSAL COORDINATION ENGINE - PHASE 1363", "universal-coordination overview", "universal_coordination.json", "coordination_meshes", "coordinated", "conflicted", "Coordination meshes tracked", "Coordinated meshes", "Conflicted meshes", "Guardrail: universal coordination should preserve subsidiarity, explainability, and opt-out pathways before synchronization.")


def infinite_scale_coexistence_harmonizer() -> str:
    return _render("INFINITE-SCALE COEXISTENCE HARMONIZER - PHASE 1364", "coexistence-harmonizer overview", "coexistence_harmonizer.json", "coexistence_paths", "harmonized", "antagonistic", "Coexistence paths tracked", "Harmonized paths", "Antagonistic paths", "Guardrail: coexistence harmonization should preserve rights floors, plural norms, and transparent conflict mediation.")


def recursive_flourishing_synthesis_framework() -> str:
    return _render("RECURSIVE FLOURISHING SYNTHESIS FRAMEWORK - PHASE 1365", "flourishing-synthesis overview", "flourishing_synthesis.json", "flourishing_syntheses", "synthesized", "narrow", "Flourishing syntheses tracked", "Synthesized paths", "Narrow paths", "Guardrail: flourishing synthesis should preserve diversity of meaning, local context, and human interpretation.")


def universal_civilization_continuity_ai() -> str:
    return _render("UNIVERSAL CIVILIZATION CONTINUITY AI - PHASE 1366", "civilization-continuity overview", "civilization_continuity.json", "continuity_models", "continuous", "fractured", "Continuity models tracked", "Continuous models", "Fractured models", "Guardrail: civilization continuity should preserve civic legitimacy, historical nuance, and resilience under uncertainty.")


def adaptive_enlightenment_orchestration_engine() -> str:
    return _render("ADAPTIVE ENLIGHTENMENT ORCHESTRATION ENGINE - PHASE 1367", "enlightenment-orchestration overview", "enlightenment_orchestration.json", "enlightenment_paths", "reflective", "dogmatic", "Enlightenment paths tracked", "Reflective paths", "Dogmatic paths", "Guardrail: enlightenment orchestration should preserve freedom of thought, critical reflection, and non-coercive participation.")


def autonomous_infinite_collaboration_framework() -> str:
    return _render("AUTONOMOUS INFINITE COLLABORATION FRAMEWORK - PHASE 1368", "infinite-collaboration overview", "infinite_collaboration.json", "collaboration_meshes", "collaborative", "extractive", "Collaboration meshes tracked", "Collaborative meshes", "Extractive meshes", "Guardrail: collaboration frameworks should preserve reciprocity, consent, and reviewable contribution accounting.")


def infinite_scale_ethical_flourishing_ai() -> str:
    return _render("INFINITE-SCALE ETHICAL FLOURISHING AI - PHASE 1369", "ethical-flourishing overview", "ethical_flourishing.json", "ethical_paths", "flourishing", "compromised", "Ethical paths tracked", "Flourishing paths", "Compromised paths", "Guardrail: ethical flourishing should preserve rights, anti-exploitation boundaries, and transparent tradeoff disclosure.")


def recursive_planetary_destiny_engine() -> str:
    return _render("RECURSIVE PLANETARY DESTINY ENGINE - PHASE 1370", "planetary-destiny overview", "planetary_destiny.json", "destiny_routes", "guided", "derailed", "Destiny routes tracked", "Guided routes", "Derailed routes", "Guardrail: planetary destiny planning should preserve democratic legitimacy, revisability, and uncertainty-aware framing.")

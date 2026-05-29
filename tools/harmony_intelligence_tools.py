from __future__ import annotations

import json
from pathlib import Path


HARMONY_INTELLIGENCE_DIR = Path("storage/harmony_intelligence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(HARMONY_INTELLIGENCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_flourishing_continuity_engine() -> str:
    return _render("UNIVERSAL FLOURISHING CONTINUITY ENGINE - PHASE 1391", "flourishing-continuity overview", "flourishing_continuity.json", "continuity_paths", "flourishing", "eroding", "Continuity paths tracked", "Flourishing paths", "Eroding paths", "Guardrail: flourishing continuity should preserve long-term wellbeing, reversibility, and transparent continuity assumptions.")


def adaptive_civilization_orchestration_framework() -> str:
    return _render("ADAPTIVE CIVILIZATION ORCHESTRATION FRAMEWORK - PHASE 1392", "civilization-orchestration overview", "civilization_orchestration.json", "civilization_meshes", "adaptive", "rigid", "Civilization meshes tracked", "Adaptive meshes", "Rigid meshes", "Guardrail: civilization orchestration should preserve subsidiarity, plural governance, and observable feedback loops.")


def autonomous_ethical_harmony_ai() -> str:
    return _render("AUTONOMOUS ETHICAL HARMONY AI - PHASE 1393", "ethical-harmony overview", "ethical_harmony.json", "ethical_harmonies", "harmonized", "contradictory", "Ethical harmonies tracked", "Harmonized paths", "Contradictory paths", "Guardrail: ethical harmony should preserve disagreement visibility, rights floors, and human accountability before synthesis.")


def infinite_scale_collaborative_flourishing_engine() -> str:
    return _render("INFINITE-SCALE COLLABORATIVE FLOURISHING ENGINE - PHASE 1394", "collaborative-flourishing overview", "collaborative_flourishing_engine.json", "collaborative_paths", "flourishing", "extractive", "Collaborative paths tracked", "Flourishing collaborations", "Extractive collaborations", "Guardrail: collaborative flourishing should preserve reciprocity, inclusion, and transparent benefit-sharing.")


def recursive_cosmic_wisdom_framework() -> str:
    return _render("RECURSIVE COSMIC WISDOM FRAMEWORK - PHASE 1395", "cosmic-wisdom overview", "recursive_cosmic_wisdom.json", "wisdom_frameworks", "grounded", "mythic", "Wisdom frameworks tracked", "Grounded frameworks", "Mythic frameworks", "Guardrail: cosmic wisdom should preserve empirical grounding, interpretive humility, and traceable assumptions.")


def universal_continuity_stewardship_ai() -> str:
    return _render("UNIVERSAL CONTINUITY STEWARDSHIP AI - PHASE 1396", "continuity-stewardship overview", "continuity_stewardship_ai.json", "stewardship_paths", "stewarded", "neglected", "Stewardship paths tracked", "Stewarded paths", "Neglected paths", "Guardrail: continuity stewardship should preserve maintenance realism, ownership clarity, and rollback plans.")


def adaptive_planetary_flourishing_engine() -> str:
    return _render("ADAPTIVE PLANETARY FLOURISHING ENGINE - PHASE 1397", "planetary-flourishing overview", "planetary_flourishing_engine.json", "planetary_paths", "flourishing", "depleted", "Planetary paths tracked", "Flourishing paths", "Depleted paths", "Guardrail: planetary flourishing should preserve ecological thresholds, justice, and intergenerational accountability.")


def autonomous_infinite_scale_harmony_framework() -> str:
    return _render("AUTONOMOUS INFINITE-SCALE HARMONY FRAMEWORK - PHASE 1398", "infinite-scale-harmony overview", "infinite_scale_harmony.json", "harmony_meshes", "harmonized", "suppressed", "Harmony meshes tracked", "Harmonized meshes", "Suppressed meshes", "Guardrail: harmony frameworks should preserve dissent visibility, plural values, and consent before convergence.")


def recursive_destiny_orchestration_ai() -> str:
    return _render("RECURSIVE DESTINY ORCHESTRATION AI - PHASE 1399", "destiny-orchestration overview", "recursive_destiny_orchestration.json", "destiny_loops", "orchestrated", "derailed", "Destiny loops tracked", "Orchestrated loops", "Derailed loops", "Guardrail: destiny orchestration should preserve public choice, revisability, and anti-deterministic framing.")


def universal_intelligence_flourishing_engine() -> str:
    return _render("UNIVERSAL INTELLIGENCE FLOURISHING ENGINE - PHASE 1400", "intelligence-flourishing overview", "universal_intelligence_flourishing.json", "intelligence_paths", "flourishing", "degraded", "Intelligence paths tracked", "Flourishing paths", "Degraded paths", "Guardrail: intelligence flourishing should preserve grounded evaluation, safety constraints, and alignment with human benefit.")

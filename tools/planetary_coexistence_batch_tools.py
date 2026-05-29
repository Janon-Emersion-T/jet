from __future__ import annotations

import json
from pathlib import Path


PLANETARY_COEXISTENCE_BATCH_DIR = Path("storage/planetary_coexistence_batch")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(PLANETARY_COEXISTENCE_BATCH_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_planetary_stewardship_engine() -> str:
    return _render("ADAPTIVE PLANETARY STEWARDSHIP ENGINE - PHASE 1481", "planetary-stewardship overview", "planetary_stewardship.json", "stewardship_paths", "stewarded", "extractive", "Stewardship paths tracked", "Stewarded paths", "Extractive paths", "Guardrail: planetary stewardship should preserve ecological thresholds, democratic legitimacy, and justice-aware intervention design.")


def autonomous_flourishing_continuity_framework() -> str:
    return _render("AUTONOMOUS FLOURISHING CONTINUITY FRAMEWORK - PHASE 1482", "flourishing-continuity overview", "flourishing_continuity_framework.json", "continuity_routes", "flourishing", "declining", "Continuity routes tracked", "Flourishing routes", "Declining routes", "Guardrail: flourishing continuity should preserve long-horizon wellbeing, inclusion, and transparent continuity assumptions.")


def infinite_scale_ethical_harmonizer_ai() -> str:
    return _render("INFINITE-SCALE ETHICAL HARMONIZER AI - PHASE 1483", "ethical-harmonizer overview", "ethical_harmonizer_ai.json", "harmonization_paths", "harmonized", "contradictory", "Harmonization paths tracked", "Harmonized paths", "Contradictory paths", "Guardrail: ethical harmonization should preserve contestability, plural norms, and human accountability before convergence.")


def recursive_coexistence_synthesis_engine() -> str:
    return _render("RECURSIVE COEXISTENCE SYNTHESIS ENGINE - PHASE 1484", "coexistence-synthesis overview", "coexistence_synthesis_engine.json", "synthesis_loops", "synthesized", "polarized", "Synthesis loops tracked", "Synthesized loops", "Polarized loops", "Guardrail: coexistence synthesis should preserve plural voice, rights floors, and transparent conflict mediation before rollout.")


def universal_resilience_orchestration_framework() -> str:
    return _render("UNIVERSAL RESILIENCE ORCHESTRATION FRAMEWORK - PHASE 1485", "resilience-orchestration overview", "universal_resilience_orchestration.json", "orchestration_frameworks", "resilient", "fragile", "Orchestration frameworks tracked", "Resilient frameworks", "Fragile frameworks", "Guardrail: resilience orchestration should preserve redundancy, operator control, and visible dependency mapping before automation.")


def adaptive_destiny_continuity_ai() -> str:
    return _render("ADAPTIVE DESTINY CONTINUITY AI - PHASE 1486", "destiny-continuity overview", "adaptive_destiny_continuity.json", "continuity_models", "continuous", "broken", "Continuity models tracked", "Continuous models", "Broken models", "Guardrail: destiny continuity should preserve revisability, autonomy, and explicit uncertainty about long-term trajectories.")


def autonomous_collaborative_prosperity_engine() -> str:
    return _render("AUTONOMOUS COLLABORATIVE PROSPERITY ENGINE - PHASE 1487", "collaborative-prosperity overview", "collaborative_prosperity.json", "prosperity_meshes", "prosperous", "extractive", "Prosperity meshes tracked", "Prosperous meshes", "Extractive meshes", "Guardrail: collaborative prosperity should preserve reciprocity, anti-capture checks, and fair distribution accounting before optimization.")


def infinite_scale_stewardship_synthesis_framework() -> str:
    return _render("INFINITE-SCALE STEWARDSHIP SYNTHESIS FRAMEWORK - PHASE 1488", "stewardship-synthesis overview", "stewardship_synthesis_framework.json", "synthesis_meshes", "coherent", "captured", "Synthesis meshes tracked", "Coherent meshes", "Captured meshes", "Guardrail: stewardship synthesis should preserve accountability chains, public review, and anti-capture protections before alignment.")


def recursive_flourishing_orchestration_ai() -> str:
    return _render("RECURSIVE FLOURISHING ORCHESTRATION AI - PHASE 1489", "flourishing-orchestration overview", "recursive_flourishing_orchestration.json", "orchestration_loops", "flourishing", "excluded", "Orchestration loops tracked", "Flourishing loops", "Excluded loops", "Guardrail: flourishing orchestration should preserve dignity, inclusion, and visible tradeoffs before optimization.")


def universal_coexistence_harmonizer_engine() -> str:
    return _render("UNIVERSAL COEXISTENCE HARMONIZER ENGINE - PHASE 1490", "coexistence-harmonizer overview", "coexistence_harmonizer_engine.json", "harmony_routes", "harmonized", "dominating", "Harmony routes tracked", "Harmonized routes", "Dominating routes", "Guardrail: coexistence harmonization should preserve non-domination, rights protection, and local mediation authority before deployment.")

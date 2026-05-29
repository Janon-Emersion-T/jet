from __future__ import annotations

import json
from pathlib import Path


STEWARDSHIP_HARMONY_DIR = Path("storage/stewardship_harmony")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(STEWARDSHIP_HARMONY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_continuity_harmonizer_ai() -> str:
    return _render("ADAPTIVE CONTINUITY HARMONIZER AI - PHASE 1411", "continuity-harmonizer overview", "adaptive_continuity_harmonizer.json", "continuity_meshes", "harmonized", "drifting", "Continuity meshes tracked", "Harmonized meshes", "Drifting meshes", "Guardrail: continuity harmonization should preserve provenance, challenge rights, and local variance before convergence.")


def autonomous_planetary_stewardship_engine() -> str:
    return _render("AUTONOMOUS PLANETARY STEWARDSHIP ENGINE - PHASE 1412", "planetary-stewardship overview", "planetary_stewardship_engine.json", "stewardship_routes", "stewarded", "extractive", "Stewardship routes tracked", "Stewarded routes", "Extractive routes", "Guardrail: planetary stewardship should preserve ecological thresholds, justice, and democratic legitimacy.")


def infinite_scale_prosperity_synthesis_framework() -> str:
    return _render("INFINITE-SCALE PROSPERITY SYNTHESIS FRAMEWORK - PHASE 1413", "prosperity-synthesis overview", "prosperity_synthesis_framework.json", "prosperity_syntheses", "synthesized", "unequal", "Prosperity syntheses tracked", "Synthesized paths", "Unequal paths", "Guardrail: prosperity synthesis should preserve equity, anti-capture checks, and explicit assumptions behind gains.")


def recursive_intelligence_coordination_ai() -> str:
    return _render("RECURSIVE INTELLIGENCE COORDINATION AI - PHASE 1414", "intelligence-coordination overview", "intelligence_coordination.json", "coordination_loops", "coordinated", "conflicted", "Coordination loops tracked", "Coordinated loops", "Conflicted loops", "Guardrail: intelligence coordination should preserve bounded autonomy, observability, and accountable supervision.")


def universal_flourishing_orchestration_engine() -> str:
    return _render("UNIVERSAL FLOURISHING ORCHESTRATION ENGINE - PHASE 1415", "flourishing-orchestration overview", "flourishing_orchestration.json", "flourishing_routes", "orchestrated", "excluded", "Flourishing routes tracked", "Orchestrated routes", "Excluded routes", "Guardrail: flourishing orchestration should preserve inclusion, human dignity, and transparent tradeoff handling.")


def adaptive_resilience_harmonizer_framework() -> str:
    return _render("ADAPTIVE RESILIENCE HARMONIZER FRAMEWORK - PHASE 1416", "resilience-harmonizer overview", "resilience_harmonizer_framework.json", "harmonizer_paths", "harmonized", "brittle", "Harmonizer paths tracked", "Harmonized paths", "Brittle paths", "Guardrail: resilience harmonization should preserve redundancy, anti-fragility, and controllable blast radius.")


def autonomous_ethical_synthesis_ai() -> str:
    return _render("AUTONOMOUS ETHICAL SYNTHESIS AI - PHASE 1417", "ethical-synthesis overview", "autonomous_ethical_synthesis.json", "ethical_syntheses", "coherent", "conflicted", "Ethical syntheses tracked", "Coherent syntheses", "Conflicted syntheses", "Guardrail: ethical synthesis should preserve plural reasoning, human override, and visible unresolved conflicts.")


def infinite_scale_destiny_continuity_engine() -> str:
    return _render("INFINITE-SCALE DESTINY CONTINUITY ENGINE - PHASE 1418", "destiny-continuity overview", "destiny_continuity_engine.json", "destiny_continuities", "continuous", "interrupted", "Destiny continuities tracked", "Continuous continuities", "Interrupted continuities", "Guardrail: destiny continuity should preserve revisability, autonomy, and explicit uncertainty about long-term trajectories.")


def recursive_universal_harmony_framework() -> str:
    return _render("RECURSIVE UNIVERSAL HARMONY FRAMEWORK - PHASE 1419", "universal-harmony overview", "recursive_universal_harmony.json", "harmony_frameworks", "harmonized", "suppressed", "Harmony frameworks tracked", "Harmonized frameworks", "Suppressed frameworks", "Guardrail: harmony frameworks should preserve dissent, local sovereignty, and non-coercive alignment.")


def universal_collaborative_flourishing_ai() -> str:
    return _render("UNIVERSAL COLLABORATIVE FLOURISHING AI - PHASE 1420", "collaborative-flourishing overview", "universal_collaborative_flourishing.json", "collaborative_systems", "flourishing", "exploitative", "Collaborative systems tracked", "Flourishing systems", "Exploitative systems", "Guardrail: collaborative flourishing should preserve reciprocity, shared agency, and transparent incentive design.")

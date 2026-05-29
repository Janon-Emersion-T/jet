from __future__ import annotations

import json
from pathlib import Path


INFINITY_ARCHITECTURE_DIR = Path("storage/infinity_architecture")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(INFINITY_ARCHITECTURE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_intelligence_continuity_framework() -> str:
    return _render("ADAPTIVE INTELLIGENCE CONTINUITY FRAMEWORK - PHASE 1491", "intelligence-continuity overview", "intelligence_continuity_framework.json", "continuity_paths", "continuous", "degraded", "Continuity paths tracked", "Continuous paths", "Degraded paths", "Guardrail: intelligence continuity should preserve provenance, bounded adaptation, and operator review before reuse.")


def autonomous_planetary_prosperity_ai() -> str:
    return _render("AUTONOMOUS PLANETARY PROSPERITY AI - PHASE 1492", "planetary-prosperity overview", "planetary_prosperity_ai.json", "prosperity_routes", "prosperous", "unequal", "Prosperity routes tracked", "Prosperous routes", "Unequal routes", "Guardrail: planetary prosperity should preserve justice, ecological realism, and transparent benefit allocation.")


def infinite_scale_ethical_stewardship_engine() -> str:
    return _render("INFINITE-SCALE ETHICAL STEWARDSHIP ENGINE - PHASE 1493", "ethical-stewardship overview", "ethical_stewardship_engine.json", "stewardship_paths", "ethical", "compromised", "Stewardship paths tracked", "Ethical paths", "Compromised paths", "Guardrail: ethical stewardship should preserve rights floors, accountability, and transparent harm accounting before deployment.")


def recursive_resilience_synthesis_framework() -> str:
    return _render("RECURSIVE RESILIENCE SYNTHESIS FRAMEWORK - PHASE 1494", "resilience-synthesis overview", "resilience_synthesis_framework.json", "synthesis_frameworks", "coherent", "fragile", "Synthesis frameworks tracked", "Coherent frameworks", "Fragile frameworks", "Guardrail: resilience synthesis should preserve heterogeneity, redundancy, and failure containment before convergence.")


def universal_flourishing_continuity_ai_phase_1495() -> str:
    return _render("UNIVERSAL FLOURISHING CONTINUITY AI - PHASE 1495", "flourishing-continuity overview", "flourishing_continuity_ai_phase_1495.json", "continuity_models", "flourishing", "eroding", "Continuity models tracked", "Flourishing models", "Eroding models", "Guardrail: flourishing continuity should preserve dignity, long-term care, and visible tradeoffs before optimization.")


def adaptive_collaborative_orchestration_engine() -> str:
    return _render("ADAPTIVE COLLABORATIVE ORCHESTRATION ENGINE - PHASE 1496", "collaborative-orchestration overview", "collaborative_orchestration_engine.json", "orchestration_clusters", "coordinated", "fragmented", "Orchestration clusters tracked", "Coordinated clusters", "Fragmented clusters", "Guardrail: collaborative orchestration should preserve clear accountability, shared agency, and transparent coordination rules.")


def autonomous_coexistence_prosperity_framework() -> str:
    return _render("AUTONOMOUS COEXISTENCE PROSPERITY FRAMEWORK - PHASE 1497", "coexistence-prosperity overview", "coexistence_prosperity_framework.json", "prosperity_meshes", "prosperous", "dominating", "Prosperity meshes tracked", "Prosperous meshes", "Dominating meshes", "Guardrail: coexistence prosperity should preserve non-domination, fair distribution, and plural community voice.")


def infinite_scale_wisdom_harmonizer_ai() -> str:
    return _render("INFINITE-SCALE WISDOM HARMONIZER AI - PHASE 1498", "wisdom-harmonizer overview", "wisdom_harmonizer_ai.json", "wisdom_paths", "harmonized", "speculative", "Wisdom paths tracked", "Harmonized paths", "Speculative paths", "Guardrail: wisdom harmonization should preserve evidence traceability, humility, and explicit unknowns before synthesis.")


def recursive_destiny_synthesis_engine() -> str:
    return _render("RECURSIVE DESTINY SYNTHESIS ENGINE - PHASE 1499", "destiny-synthesis overview", "destiny_synthesis_engine.json", "synthesis_loops", "coherent", "coercive", "Synthesis loops tracked", "Coherent loops", "Coercive loops", "Guardrail: destiny synthesis should preserve autonomy, revisability, and anti-deterministic framing before guidance.")


def jarvis_infinity_architecture_phase_1500() -> str:
    return _render("JARVIS INFINITY ARCHITECTURE - PHASE 1500", "infinity-architecture overview", "jarvis_infinity_architecture.json", "architecture_layers", "stable", "drifting", "Architecture layers tracked", "Stable layers", "Drifting layers", "Guardrail: infinity architecture planning should preserve modularity, rollback boundaries, and operator comprehension before expansion.")

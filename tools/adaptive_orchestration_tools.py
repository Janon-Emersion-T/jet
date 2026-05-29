from __future__ import annotations

import json
from pathlib import Path


ADAPTIVE_ORCHESTRATION_DIR = Path("storage/adaptive_orchestration")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(ADAPTIVE_ORCHESTRATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_adaptive_orchestration_engine() -> str:
    return _render("UNIVERSAL ADAPTIVE ORCHESTRATION ENGINE - PHASE 1351", "adaptive-orchestration overview", "adaptive_orchestration.json", "orchestration_paths", "adaptive", "stalled", "Orchestration paths tracked", "Adaptive paths", "Stalled paths", "Guardrail: adaptive orchestration should preserve local agency, rollback paths, and explicit review before coordination changes.")


def adaptive_infinite_scale_systems_framework() -> str:
    return _render("ADAPTIVE INFINITE-SCALE SYSTEMS FRAMEWORK - PHASE 1352", "infinite-scale-systems overview", "infinite_scale_systems.json", "system_meshes", "adaptive", "rigid", "System meshes tracked", "Adaptive meshes", "Rigid meshes", "Guardrail: infinite-scale systems should preserve modular failure boundaries, observability, and human override before scaling.")


def autonomous_collaborative_transcendence_ai() -> str:
    return _render("AUTONOMOUS COLLABORATIVE TRANSCENDENCE AI - PHASE 1353", "collaborative-transcendence overview", "collaborative_transcendence.json", "transcendence_sessions", "collaborative", "isolated", "Transcendence sessions tracked", "Collaborative sessions", "Isolated sessions", "Guardrail: collaborative transcendence should preserve consent, mutual benefit, and challenge rights before convergence.")


def infinite_scale_continuity_optimization_engine() -> str:
    return _render("INFINITE-SCALE CONTINUITY OPTIMIZATION ENGINE - PHASE 1354", "continuity-optimization overview", "continuity_optimization.json", "continuity_plans", "optimized", "drifting", "Continuity plans tracked", "Optimized plans", "Drifting plans", "Guardrail: continuity optimization should preserve resilience, provenance, and local fallback options before optimization.")


def recursive_civilization_stewardship_framework() -> str:
    return _render("RECURSIVE CIVILIZATION STEWARDSHIP FRAMEWORK - PHASE 1355", "civilization-stewardship overview", "civilization_stewardship.json", "stewardship_loops", "stewarding", "captured", "Stewardship loops tracked", "Stewarding loops", "Captured loops", "Guardrail: stewardship frameworks should preserve public accountability, plural values, and reviewable stewardship boundaries.")


def universal_destiny_harmonizer_ai() -> str:
    return _render("UNIVERSAL DESTINY HARMONIZER AI - PHASE 1356", "destiny-harmonizer overview", "destiny_harmonizer.json", "destiny_models", "harmonized", "coercive", "Destiny models tracked", "Harmonized models", "Coercive models", "Guardrail: destiny harmonization should preserve autonomy, revision rights, and non-deterministic framing before recommendation.")


def adaptive_post_scarcity_orchestration_engine() -> str:
    return _render("ADAPTIVE POST-SCARCITY ORCHESTRATION ENGINE - PHASE 1357", "post-scarcity-orchestration overview", "post_scarcity_orchestration.json", "allocation_paths", "equitable", "extractive", "Allocation paths tracked", "Equitable paths", "Extractive paths", "Guardrail: post-scarcity orchestration should preserve equity, ecological constraints, and transparent allocation logic.")


def autonomous_collective_flourishing_framework() -> str:
    return _render("AUTONOMOUS COLLECTIVE FLOURISHING FRAMEWORK - PHASE 1358", "collective-flourishing overview", "collective_flourishing.json", "flourishing_collectives", "flourishing", "excluded", "Collectives tracked", "Flourishing collectives", "Excluded collectives", "Guardrail: collective flourishing should preserve inclusion, dignity, and non-reductive wellbeing measures.")


def infinite_scale_planetary_wisdom_ai() -> str:
    return _render("INFINITE-SCALE PLANETARY WISDOM AI - PHASE 1359", "planetary-wisdom overview", "planetary_wisdom.json", "wisdom_signals", "wise", "misguided", "Wisdom signals tracked", "Wise signals", "Misguided signals", "Guardrail: planetary wisdom systems should preserve humility, uncertainty, and auditable reasoning before strategic use.")


def recursive_cooperative_continuity_engine() -> str:
    return _render("RECURSIVE COOPERATIVE CONTINUITY ENGINE - PHASE 1360", "cooperative-continuity overview", "cooperative_continuity.json", "cooperative_paths", "continuous", "fragmented", "Cooperative paths tracked", "Continuous paths", "Fragmented paths", "Guardrail: cooperative continuity should preserve reciprocal obligations, local autonomy, and graceful degradation before coordination.")

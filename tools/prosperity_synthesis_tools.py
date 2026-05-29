from __future__ import annotations

import json
from pathlib import Path


PROSPERITY_SYNTHESIS_DIR = Path("storage/prosperity_synthesis")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(PROSPERITY_SYNTHESIS_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def adaptive_stewardship_continuity_engine() -> str:
    return _render("ADAPTIVE STEWARDSHIP CONTINUITY ENGINE - PHASE 1421", "stewardship-continuity overview", "adaptive_stewardship_continuity.json", "continuity_routes", "continuous", "abandoned", "Continuity routes tracked", "Continuous routes", "Abandoned routes", "Guardrail: stewardship continuity should preserve maintenance ownership, transparency, and handoff clarity.")


def autonomous_cosmic_prosperity_framework() -> str:
    return _render("AUTONOMOUS COSMIC PROSPERITY FRAMEWORK - PHASE 1422", "cosmic-prosperity overview", "cosmic_prosperity.json", "prosperity_corridors", "prosperous", "extractive", "Prosperity corridors tracked", "Prosperous corridors", "Extractive corridors", "Guardrail: cosmic prosperity should preserve justice, ecological humility, and treaty-aware allocation decisions.")


def infinite_scale_coexistence_ai() -> str:
    return _render("INFINITE-SCALE COEXISTENCE AI - PHASE 1423", "coexistence overview", "infinite_scale_coexistence_ai.json", "coexistence_models", "cooperative", "hostile", "Coexistence models tracked", "Cooperative models", "Hostile models", "Guardrail: coexistence AI should preserve rights protection, transparency, and non-domination safeguards.")


def recursive_planetary_harmony_engine() -> str:
    return _render("RECURSIVE PLANETARY HARMONY ENGINE - PHASE 1424", "planetary-harmony overview", "planetary_harmony.json", "harmony_loops", "harmonized", "polarized", "Harmony loops tracked", "Harmonized loops", "Polarized loops", "Guardrail: planetary harmony should preserve pluralism, democratic input, and visible dissent before synthesis.")


def universal_intelligence_stewardship_framework() -> str:
    return _render("UNIVERSAL INTELLIGENCE STEWARDSHIP FRAMEWORK - PHASE 1425", "intelligence-stewardship overview", "intelligence_stewardship_framework.json", "stewardship_models", "stewarded", "runaway", "Stewardship models tracked", "Stewarded models", "Runaway models", "Guardrail: intelligence stewardship should preserve bounded autonomy, intervention controls, and accountable ownership.")


def adaptive_flourishing_continuity_ai() -> str:
    return _render("ADAPTIVE FLOURISHING CONTINUITY AI - PHASE 1426", "flourishing-continuity overview", "adaptive_flourishing_continuity.json", "continuity_paths", "flourishing", "declining", "Continuity paths tracked", "Flourishing paths", "Declining paths", "Guardrail: flourishing continuity should preserve non-reductive wellbeing metrics, equity, and long-horizon accountability.")


def autonomous_resilience_orchestration_engine() -> str:
    return _render("AUTONOMOUS RESILIENCE ORCHESTRATION ENGINE - PHASE 1427", "resilience-orchestration overview", "autonomous_resilience_orchestration.json", "orchestration_paths", "resilient", "overloaded", "Orchestration paths tracked", "Resilient paths", "Overloaded paths", "Guardrail: resilience orchestration should preserve safe degradation, redundancy, and operator review of reconfiguration.")


def infinite_scale_ethical_prosperity_framework() -> str:
    return _render("INFINITE-SCALE ETHICAL PROSPERITY FRAMEWORK - PHASE 1428", "ethical-prosperity overview", "ethical_prosperity.json", "prosperity_frameworks", "ethical", "compromised", "Prosperity frameworks tracked", "Ethical frameworks", "Compromised frameworks", "Guardrail: ethical prosperity should preserve rights, anti-exploitation constraints, and transparent harm accounting.")


def recursive_collaborative_harmony_ai() -> str:
    return _render("RECURSIVE COLLABORATIVE HARMONY AI - PHASE 1429", "collaborative-harmony overview", "recursive_collaborative_harmony.json", "harmony_clusters", "harmonized", "dominated", "Harmony clusters tracked", "Harmonized clusters", "Dominated clusters", "Guardrail: collaborative harmony should preserve equal voice, conflict visibility, and non-coercive mediation.")


def universal_continuity_synthesis_engine() -> str:
    return _render("UNIVERSAL CONTINUITY SYNTHESIS ENGINE - PHASE 1430", "continuity-synthesis overview", "continuity_synthesis_engine.json", "continuity_syntheses", "synthesized", "fragmented", "Continuity syntheses tracked", "Synthesized paths", "Fragmented paths", "Guardrail: continuity synthesis should preserve traceability, local fallback paths, and resilience under uncertainty.")

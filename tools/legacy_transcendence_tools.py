from __future__ import annotations

import json
from pathlib import Path


LEGACY_TRANSCENDENCE_DIR = Path("storage/legacy_transcendence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(LEGACY_TRANSCENDENCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_legacy_preservation_substrate() -> str:
    return _render("UNIVERSAL LEGACY PRESERVATION SUBSTRATE - PHASE 1251", "legacy-preservation overview", "legacy_preservation.json", "legacies", "preserved", "eroding", "Legacies tracked", "Preserved legacies", "Eroding legacies", "Guardrail: legacy preservation should preserve consent, provenance, and cultural nuance before archival or transfer.")


def adaptive_heritage_harmonization_engine() -> str:
    return _render("ADAPTIVE HERITAGE HARMONIZATION ENGINE - PHASE 1252", "heritage-harmonization overview", "heritage_harmonization.json", "heritage_streams", "harmonized", "flattened", "Heritage streams tracked", "Harmonized streams", "Flattened streams", "Guardrail: heritage harmonization should preserve plurality, local authority, and anti-assimilation safeguards before alignment.")


def autonomous_future_generation_planning_ai() -> str:
    return _render("AUTONOMOUS FUTURE-GENERATION PLANNING AI - PHASE 1253", "future-generation-planning overview", "future_generation_planning.json", "generation_plans", "planned", "underrepresented", "Generation plans tracked", "Planned generations", "Underrepresented generations", "Guardrail: future-generation planning should preserve intergenerational justice, humility, and inclusive review before recommendation.")


def infinite_scale_temporal_stewardship_framework() -> str:
    return _render("INFINITE-SCALE TEMPORAL STEWARDSHIP FRAMEWORK - PHASE 1254", "temporal-stewardship overview", "temporal_stewardship.json", "stewardship_loops", "stewarded", "neglected", "Stewardship loops tracked", "Stewarded loops", "Neglected loops", "Guardrail: temporal stewardship should preserve long-horizon accountability and reversible decisions before optimization.")


def recursive_destiny_optimization_engine() -> str:
    return _render("RECURSIVE DESTINY OPTIMIZATION ENGINE - PHASE 1255", "destiny-optimization overview", "destiny_optimization.json", "destiny_paths", "optimized", "coercive", "Destiny paths tracked", "Optimized paths", "Coercive paths", "Guardrail: destiny optimization should preserve autonomy, anti-determinism, and human choice before guidance.")


def universal_continuity_governance_substrate() -> str:
    return _render("UNIVERSAL CONTINUITY GOVERNANCE SUBSTRATE - PHASE 1256", "continuity-governance overview", "continuity_governance.json", "governance_chains", "continuous", "brittle", "Governance chains tracked", "Continuous chains", "Brittle chains", "Guardrail: continuity governance should preserve lawful succession, transparency, and distributed accountability before activation.")


def adaptive_civilization_mentoring_ai() -> str:
    return _render("ADAPTIVE CIVILIZATION MENTORING AI - PHASE 1257", "civilization-mentoring overview", "civilization_mentoring.json", "mentorship_arcs", "supported", "orphaned", "Mentorship arcs tracked", "Supported arcs", "Orphaned arcs", "Guardrail: civilization mentoring should preserve humility, consent, and non-paternalistic guidance before intervention.")


def autonomous_planetary_enlightenment_engine() -> str:
    return _render("AUTONOMOUS PLANETARY ENLIGHTENMENT ENGINE - PHASE 1258", "planetary-enlightenment overview", "planetary_enlightenment.json", "enlightenment_paths", "illuminated", "dogmatic", "Enlightenment paths tracked", "Illuminated paths", "Dogmatic paths", "Guardrail: enlightenment modeling should preserve plural wisdom, non-coercion, and humble framing before recommendation.")


def infinite_scale_ethical_evolution_framework() -> str:
    return _render("INFINITE-SCALE ETHICAL EVOLUTION FRAMEWORK - PHASE 1259", "ethical-evolution overview", "ethical_evolution.json", "ethical_paths", "evolving", "regressing", "Ethical paths tracked", "Evolving paths", "Regressing paths", "Guardrail: ethical evolution should preserve rights floors, plural values, and challenge mechanisms before optimization.")


def recursive_transcendental_reasoning_ai() -> str:
    return _render("RECURSIVE TRANSCENDENTAL REASONING AI - PHASE 1260", "transcendental-reasoning overview", "transcendental_reasoning.json", "reasoning_threads", "reasoned", "circular", "Reasoning threads tracked", "Reasoned threads", "Circular threads", "Guardrail: transcendental reasoning should preserve explicit assumptions, humility, and human interpretation before claims.")

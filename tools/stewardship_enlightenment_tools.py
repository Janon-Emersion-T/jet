from __future__ import annotations

import json
from pathlib import Path


STEWARDSHIP_ENLIGHTENMENT_DIR = Path("storage/stewardship_enlightenment")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(STEWARDSHIP_ENLIGHTENMENT_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_stewardship_engine() -> str:
    return _render("UNIVERSAL STEWARDSHIP ENGINE - PHASE 1311", "stewardship overview", "stewardship_engine.json", "stewardship_paths", "stewarded", "neglected", "Stewardship paths tracked", "Stewarded paths", "Neglected paths", "Guardrail: stewardship systems should preserve accountability, humility, and long-horizon care before intervention.")


def adaptive_continuity_preservation_ai() -> str:
    return _render("ADAPTIVE CONTINUITY PRESERVATION AI - PHASE 1312", "continuity-preservation overview", "continuity_preservation.json", "continuity_paths", "preserved", "broken", "Continuity paths tracked", "Preserved paths", "Broken paths", "Guardrail: continuity preservation should preserve lawful process, provenance, and review before action.")


def autonomous_civilization_safeguarding_framework() -> str:
    return _render("AUTONOMOUS CIVILIZATION SAFEGUARDING FRAMEWORK - PHASE 1313", "civilization-safeguarding overview", "civilization_safeguarding.json", "safeguards", "protected", "exposed", "Safeguards tracked", "Protected safeguards", "Exposed safeguards", "Guardrail: civilization safeguarding should preserve rights, redundancy, and non-panicked prioritization before activation.")


def infinite_scale_destiny_orchestration_engine() -> str:
    return _render("INFINITE-SCALE DESTINY ORCHESTRATION ENGINE - PHASE 1314", "destiny-orchestration overview", "destiny_orchestration.json", "destiny_meshes", "orchestrated", "captured", "Destiny meshes tracked", "Orchestrated meshes", "Captured meshes", "Guardrail: destiny orchestration should preserve autonomy, anti-determinism, and human governance before use.")


def recursive_transcendence_harmonizer() -> str:
    return _render("RECURSIVE TRANSCENDENCE HARMONIZER - PHASE 1315", "transcendence-harmonization overview", "transcendence_harmonization.json", "transcendence_paths", "harmonized", "destabilized", "Transcendence paths tracked", "Harmonized paths", "Destabilized paths", "Guardrail: transcendence harmonization should preserve grounding, consent, and psychological safety before recommendation.")


def universal_future_stewardship_ai() -> str:
    return _render("UNIVERSAL FUTURE STEWARDSHIP AI - PHASE 1316", "future-stewardship overview", "future_stewardship.json", "future_paths", "stewarded", "sacrificed", "Future paths tracked", "Stewarded paths", "Sacrificed paths", "Guardrail: future stewardship should preserve intergenerational fairness, uncertainty, and transparent tradeoffs before optimization.")


def adaptive_cosmic_flourishing_substrate() -> str:
    return _render("ADAPTIVE COSMIC FLOURISHING SUBSTRATE - PHASE 1317", "cosmic-flourishing overview", "cosmic_flourishing.json", "flourishing_fields", "flourishing", "deprived", "Flourishing fields tracked", "Flourishing fields", "Deprived fields", "Guardrail: cosmic flourishing should preserve equity, dignity, and contextual humility before ranking.")


def autonomous_universal_enlightenment_framework() -> str:
    return _render("AUTONOMOUS UNIVERSAL ENLIGHTENMENT FRAMEWORK - PHASE 1318", "universal-enlightenment overview", "universal_enlightenment.json", "enlightenment_paths", "illuminated", "dogmatic", "Enlightenment paths tracked", "Illuminated paths", "Dogmatic paths", "Guardrail: enlightenment frameworks should preserve plural wisdom and non-coercive adoption before guidance.")


def infinite_scale_continuity_harmonization_engine() -> str:
    return _render("INFINITE-SCALE CONTINUITY HARMONIZATION ENGINE - PHASE 1319", "continuity-harmonization overview", "continuity_harmonization.json", "continuity_meshes", "harmonized", "misaligned", "Continuity meshes tracked", "Harmonized meshes", "Misaligned meshes", "Guardrail: continuity harmonization should preserve local context, reviewability, and dissent before alignment.")


def recursive_reality_stewardship_ai() -> str:
    return _render("RECURSIVE REALITY STEWARDSHIP AI - PHASE 1320", "reality-stewardship overview", "reality_stewardship.json", "reality_paths", "stewarded", "distorted", "Reality paths tracked", "Stewarded paths", "Distorted paths", "Guardrail: reality stewardship should preserve truthfulness, humility, and accountable interpretation before intervention.")

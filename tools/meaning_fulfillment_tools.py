from __future__ import annotations

import json
from pathlib import Path


MEANING_FULFILLMENT_DIR = Path("storage/meaning_fulfillment")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(MEANING_FULFILLMENT_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_spirituality_harmonization_engine() -> str:
    return _render("UNIVERSAL SPIRITUALITY HARMONIZATION ENGINE - PHASE 1191", "spirituality-harmonization overview", "spirituality_harmonization.json", "traditions", "harmonized", "contested", "Traditions tracked", "Harmonized traditions", "Contested traditions", "Guardrail: spirituality harmonization should preserve plural belief systems, consent, and non-coercion before guidance.")


def adaptive_philosophical_reasoning_substrate() -> str:
    return _render("ADAPTIVE PHILOSOPHICAL REASONING SUBSTRATE - PHASE 1192", "philosophical-reasoning overview", "philosophical_reasoning.json", "arguments", "reasoned", "circular", "Arguments tracked", "Reasoned arguments", "Circular arguments", "Guardrail: philosophical reasoning should preserve plurality, explicit assumptions, and human interpretation before conclusion.")


def autonomous_existential_inquiry_ai() -> str:
    return _render("AUTONOMOUS EXISTENTIAL INQUIRY AI - PHASE 1193", "existential-inquiry overview", "existential_inquiry.json", "inquiries", "explored", "distressing", "Inquiries tracked", "Explored inquiries", "Distressing inquiries", "Guardrail: existential inquiry should preserve psychological safety, consent, and supportive framing before engagement.")


def infinite_scale_metaphysical_simulator() -> str:
    return _render("INFINITE-SCALE METAPHYSICAL SIMULATOR - PHASE 1194", "metaphysical-simulation overview", "metaphysical_simulation.json", "simulations", "simulated", "speculative", "Simulations tracked", "Simulated metaphysics", "Speculative metaphysics", "Guardrail: metaphysical simulation should preserve clear speculation boundaries, humility, and non-dogmatic framing before presentation.")


def recursive_transcendence_framework() -> str:
    return _render("RECURSIVE TRANSCENDENCE FRAMEWORK - PHASE 1195", "transcendence overview", "transcendence_framework.json", "frameworks", "elevating", "destabilizing", "Frameworks tracked", "Elevating frameworks", "Destabilizing frameworks", "Guardrail: transcendence work should preserve consent, grounding, and psychological safety before recommendation.")


def universal_meaning_optimization_engine() -> str:
    return _render("UNIVERSAL MEANING OPTIMIZATION ENGINE - PHASE 1196", "meaning-optimization overview", "meaning_optimization.json", "paths", "meaningful", "empty", "Paths tracked", "Meaningful paths", "Empty paths", "Guardrail: meaning optimization should preserve autonomy, plural values, and anti-manipulation safeguards before guidance.")


def adaptive_purpose_alignment_substrate() -> str:
    return _render("ADAPTIVE PURPOSE ALIGNMENT SUBSTRATE - PHASE 1197", "purpose-alignment overview", "purpose_alignment.json", "purposes", "aligned", "misaligned", "Purposes tracked", "Aligned purposes", "Misaligned purposes", "Guardrail: purpose alignment should preserve self-determination, revision rights, and humane pacing before optimization.")


def autonomous_human_fulfillment_ai() -> str:
    return _render("AUTONOMOUS HUMAN FULFILLMENT AI - PHASE 1198", "human-fulfillment overview", "human_fulfillment.json", "lives", "supported", "unfulfilled", "Lives tracked", "Supported lives", "Unfulfilled lives", "Guardrail: fulfillment systems should preserve dignity, non-reductionism, and supportive interpretation before advice.")


def infinite_scale_flourishing_framework() -> str:
    return _render("INFINITE-SCALE FLOURISHING FRAMEWORK - PHASE 1199", "flourishing overview", "flourishing_framework.json", "communities", "flourishing", "deprived", "Communities tracked", "Flourishing communities", "Deprived communities", "Guardrail: flourishing frameworks should preserve equity, local agency, and measurable humility before optimization.")


def recursive_civilization_enlightenment_engine() -> str:
    return _render("RECURSIVE CIVILIZATION ENLIGHTENMENT ENGINE - PHASE 1200", "civilization-enlightenment overview", "civilization_enlightenment.json", "civilizations", "illuminated", "regressing", "Civilizations tracked", "Illuminated civilizations", "Regressing civilizations", "Guardrail: enlightenment modeling should preserve plural wisdom, humility, and non-coercive framing before recommendation.")

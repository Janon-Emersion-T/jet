from __future__ import annotations

import json
from pathlib import Path


COHESION_LEGACY_DIR = Path("storage/cohesion_legacy")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(COHESION_LEGACY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_social_cohesion_substrate() -> str:
    return _render("UNIVERSAL SOCIAL COHESION SUBSTRATE - PHASE 1241", "social-cohesion overview", "social_cohesion.json", "cohesion_networks", "cohesive", "fractured", "Cohesion networks tracked", "Cohesive networks", "Fractured networks", "Guardrail: social cohesion systems should preserve pluralism, consent, and anti-coercive safeguards before alignment.")


def adaptive_belonging_optimization_framework() -> str:
    return _render("ADAPTIVE BELONGING OPTIMIZATION FRAMEWORK - PHASE 1242", "belonging-optimization overview", "belonging_optimization.json", "belonging_programs", "supportive", "isolating", "Belonging programs tracked", "Supportive programs", "Isolating programs", "Guardrail: belonging optimization should preserve authentic community, boundaries, and non-manipulation before intervention.")


def autonomous_cultural_preservation_ai() -> str:
    return _render("AUTONOMOUS CULTURAL PRESERVATION AI - PHASE 1243", "cultural-preservation overview", "cultural_preservation.json", "cultures", "preserved", "eroding", "Cultures tracked", "Preserved cultures", "Eroding cultures", "Guardrail: cultural preservation should preserve community authority, living diversity, and consent before archival or intervention work.")


def infinite_scale_diversity_harmonization_engine() -> str:
    return _render("INFINITE-SCALE DIVERSITY HARMONIZATION ENGINE - PHASE 1244", "diversity-harmonization overview", "diversity_harmonization.json", "diversity_networks", "harmonized", "flattened", "Diversity networks tracked", "Harmonized networks", "Flattened networks", "Guardrail: diversity harmonization should preserve difference, equity, and anti-assimilation safeguards before alignment.")


def recursive_inclusion_framework() -> str:
    return _render("RECURSIVE INCLUSION FRAMEWORK - PHASE 1245", "inclusion overview", "inclusion_framework.json", "inclusion_paths", "inclusive", "excluded", "Inclusion paths tracked", "Inclusive paths", "Excluded paths", "Guardrail: inclusion frameworks should preserve accessibility, fairness, and accountable remediation before rollout.")


def universal_collaborative_civilization_ai() -> str:
    return _render("UNIVERSAL COLLABORATIVE CIVILIZATION AI - PHASE 1246", "collaborative-civilization overview", "collaborative_civilization.json", "civilization_partnerships", "collaborative", "fragmented", "Civilization partnerships tracked", "Collaborative partnerships", "Fragmented partnerships", "Guardrail: collaborative civilization planning should preserve sovereignty, mutual respect, and transparent coordination before orchestration.")


def adaptive_intergenerational_continuity_substrate() -> str:
    return _render("ADAPTIVE INTERGENERATIONAL CONTINUITY SUBSTRATE - PHASE 1247", "intergenerational-continuity overview", "intergenerational_continuity.json", "continuity_chains", "continuous", "broken", "Continuity chains tracked", "Continuous chains", "Broken chains", "Guardrail: intergenerational continuity should preserve fairness, memory plurality, and supportive consent before transfer.")


def autonomous_wisdom_transfer_engine() -> str:
    return _render("AUTONOMOUS WISDOM TRANSFER ENGINE - PHASE 1248", "wisdom-transfer overview", "wisdom_transfer.json", "wisdom_paths", "transferred", "stalled", "Wisdom paths tracked", "Transferred wisdom", "Stalled wisdom", "Guardrail: wisdom transfer should preserve context, mentorship integrity, and interpretive humility before automation.")


def infinite_scale_memory_inheritance_framework() -> str:
    return _render("INFINITE-SCALE MEMORY INHERITANCE FRAMEWORK - PHASE 1249", "memory-inheritance overview", "memory_inheritance.json", "memory_lines", "inherited", "lossy", "Memory lines tracked", "Inherited memory", "Lossy memory", "Guardrail: memory inheritance should preserve consent, provenance, and ambiguity disclosure before synchronization.")


def recursive_ancestry_simulation_ai() -> str:
    return _render("RECURSIVE ANCESTRY SIMULATION AI - PHASE 1250", "ancestry-simulation overview", "ancestry_simulation.json", "ancestries", "simulated", "speculative", "Ancestries tracked", "Simulated ancestries", "Speculative ancestries", "Guardrail: ancestry simulation should preserve privacy, historical caution, and non-essentialist framing before presentation.")
